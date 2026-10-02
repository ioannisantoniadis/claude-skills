#!/usr/bin/env python3
"""Exhaustive, deterministic checks for a learning repo (stdlib only).

Usage:
    python mechanical_checks.py <repo> [--online] [--json]

Prints a Markdown report of everything that can be checked without judgment: missing and orphan
images, figures without a generating script, citation keys vs. bibliography, bibliography entries
without an identifier, dangling paths in project docs, broken internal links, and repo hygiene
facts (lockfile, CI, test counts). With --online it also confirms that every arXiv id in the
bibliography exists (one batched arXiv API call) and that every DOI resolves.

It finds candidates; it does not judge them. A "figure without a script" may be a schematic, a
logo or a screenshot. Read the flagged items before reporting them as findings.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

SKIP_DIRS = {
    ".git", "_site", "_book", ".quarto", "_freeze", ".venv", "venv", "node_modules",
    "__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache", "site", "build", "dist",
    ".ipynb_checkpoints",
}
CONTENT_EXT = {".qmd", ".md", ".rmd", ".ipynb", ".html"}
CODE_EXT = {".py", ".r", ".jl", ".ipynb", ".js", ".ts"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp", ".pdf"}
PROJECT_DOCS = ["README.md", "CLAUDE.md", "CONVENTIONS.md", "ROADMAP.md", "CONTRIBUTING.md"]
CROSSREF_PREFIXES = ("fig-", "sec-", "tbl-", "eq-", "thm-", "lem-", "def-", "exm-", "exr-",
                     "cor-", "prp-", "cnj-", "rem-", "lst-", "callout-")


def walk(root: Path):
    for p in root.rglob("*"):
        if any(part in SKIP_DIRS for part in p.relative_to(root).parts):
            continue
        if p.is_file():
            yield p


def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def detect_profile(root: Path, files: list[Path]) -> str:
    names = {p.name for p in files}
    if "_quarto.yml" in names or "book.toml" in names or "_config.yml" in names and any(
        p.suffix == ".ipynb" for p in files
    ):
        return "book"
    text = " ".join(read(p) for p in files if p.name in {"pyproject.toml", "requirements.txt"})
    if re.search(r"\b(streamlit|gradio)\b", text, re.I):
        return "app"
    n_md = sum(p.suffix == ".md" for p in files)
    n_py = sum(p.suffix == ".py" for p in files)
    if n_md >= 10 and n_md > n_py:
        return "notes"
    return "research"


IMG_MD = re.compile(r"!\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
IMG_HTML = re.compile(r"<img[^>]+src=[\"']([^\"']+)[\"']", re.I)
YAML_IMG = re.compile(r"^\s*(?:image|cover-image|favicon|logo):\s*[\"']?([^\"'\s]+)", re.M)
LINK_MD = re.compile(r"(?<!!)\[[^\]]*\]\(\s*<?([^)\s>]+)>?\s*\)")


def is_external(ref: str) -> bool:
    return bool(re.match(r"^[a-z][a-z0-9+.-]*:", ref, re.I)) or ref.startswith("//")


def check_images(root: Path, files: list[Path]):
    content = [p for p in files if p.suffix.lower() in CONTENT_EXT | {".yml", ".yaml"}]
    referenced: dict[Path, list[str]] = {}
    missing = []
    for p in content:
        text = read(p)
        refs = IMG_MD.findall(text) + IMG_HTML.findall(text) + YAML_IMG.findall(text)
        for ref in refs:
            if is_external(ref) or ref.startswith("data:"):
                continue
            ref_path = ref.split("#")[0].split("?")[0]
            if Path(ref_path).suffix.lower() not in IMAGE_EXT:
                continue
            target = (root / ref_path.lstrip("/")) if ref_path.startswith("/") else (
                p.parent / ref_path)
            target = target.resolve()
            # Quarto resolves some paths against the project dir rather than the file.
            if not target.exists():
                alt = [(d / ref_path).resolve() for d in (root, root / "docs")]
                target = next((a for a in alt if a.exists()), target)
            rel = str(p.relative_to(root))
            if target.exists():
                referenced.setdefault(target, []).append(rel)
            else:
                missing.append((rel, ref))
    images = [p.resolve() for p in files if p.suffix.lower() in IMAGE_EXT]
    all_text = "\n".join(read(p) for p in files if p.suffix.lower() in CONTENT_EXT | CODE_EXT
                         | {".yml", ".yaml", ".toml", ".css", ".scss"})
    orphans = [str(p.relative_to(root.resolve())) for p in images
               if p not in referenced and p.name not in all_text]
    return referenced, missing, orphans


def check_figure_scripts(root: Path, files: list[Path], referenced: dict[Path, list[str]]):
    """A referenced raster/vector image counts as 'scripted' if its stem appears in code."""
    code = {p: read(p) for p in files if p.suffix.lower() in CODE_EXT}
    qmd_code = {p: read(p) for p in files if p.suffix.lower() in {".qmd", ".rmd"}}
    unscripted, scripted = [], {}
    for img in referenced:
        stem = img.stem
        hits = [str(p.relative_to(root)) for p, t in code.items() if stem in t]
        if hits:
            scripted[str(img.relative_to(root.resolve()))] = hits
        elif not any(stem in t and "```{python" in t for t in qmd_code.values()):
            unscripted.append(str(img.relative_to(root.resolve())))
    return scripted, sorted(unscripted)


BIB_ENTRY = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,(.*?)(?=\n@\w+\s*\{|\Z)", re.S)
CITE = re.compile(r"(?<![\w./])-?@([A-Za-z0-9_][\w:.#$%&+?<>~/-]*[\w])")


def bib_field(body: str, name: str) -> str | None:
    m = re.search(rf"\b{name}\s*=\s*[{{\"](.+?)[}}\"]\s*,?\s*\n", body, re.I | re.S)
    return m.group(1).strip() if m else None


def check_citations(root: Path, files: list[Path]):
    bibs = [p for p in files if p.suffix == ".bib"]
    entries = {}
    for b in bibs:
        for kind, key, body in BIB_ENTRY.findall(read(b)):
            entries[key] = {
                "kind": kind.lower(),
                "file": str(b.relative_to(root)),
                "doi": bib_field(body, "doi"),
                "url": bib_field(body, "url"),
                "eprint": bib_field(body, "eprint"),
                "year": bib_field(body, "year"),
                "title": bib_field(body, "title"),
            }
    used: dict[str, list[str]] = {}
    for p in files:
        if p.suffix.lower() not in {".qmd", ".md", ".rmd"} or not bibs:
            continue
        text = re.sub(r"```.*?```", "", read(p), flags=re.S)
        text = re.sub(r"`[^`]*`", "", text)
        for key in CITE.findall(text):
            if key.startswith(CROSSREF_PREFIXES) or "." in key and key.split(".")[-1] in {
                "com", "org", "io", "edu", "ai", "net"}:
                continue
            used.setdefault(key, []).append(str(p.relative_to(root)))
    undefined = {k: sorted(set(v)) for k, v in used.items() if k not in entries}
    unused = sorted(k for k in entries if k not in used)
    # Books and old monographs often have no DOI; list only the kinds that should have one.
    no_id = sorted(k for k, e in entries.items() if e["kind"] not in {"book", "incollection"}
                   and not (e["doi"] or e["url"] or e["eprint"]))
    return entries, undefined, unused, no_id


ARXIV_ID = re.compile(r"(\d{4}\.\d{4,5})(?:v\d+)?")


def arxiv_ids(entries: dict) -> dict[str, str]:
    out = {}
    for key, e in entries.items():
        for field in ("eprint", "url", "doi"):
            v = e.get(field) or ""
            m = ARXIV_ID.search(v) if ("arxiv" in v.lower() or field == "eprint") else None
            if m:
                out[key] = m.group(1)
                break
    return out


def http_get(url: str, tries: int = 4) -> tuple[int, str]:
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "learning-repo-audit/0.1"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and i < tries - 1:
                time.sleep(5 * (i + 1))
                continue
            return e.code, ""
        except (urllib.error.URLError, TimeoutError):
            if i < tries - 1:
                time.sleep(3)
                continue
            return 0, ""
    return 0, ""


def title_overlap(a: str, b: str) -> float:
    """Share of the shorter title's words found in the longer one (case, braces ignored)."""
    wa, wb = (set(re.findall(r"[a-z0-9]+", t.lower())) for t in (a, b))
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / min(len(wa), len(wb))


def check_online(entries: dict) -> dict:
    ids = arxiv_ids(entries)
    result = {"arxiv_checked": len(ids), "arxiv_not_found": [], "arxiv_titles": {},
              "doi_checked": 0, "doi_failed": []}
    uniq = sorted(set(ids.values()))
    found: dict[str, str] = {}
    for i in range(0, len(uniq), 100):
        chunk = uniq[i:i + 100]
        status, body = http_get(
            "http://export.arxiv.org/api/query?max_results=200&id_list=" + ",".join(chunk))
        for entry in re.findall(r"<entry>(.*?)</entry>", body, re.S):
            m = re.search(r"<id>https?://arxiv.org/abs/([^<v]+)", entry)
            t = re.search(r"<title>(.*?)</title>", entry, re.S)
            if m:
                found[m.group(1)] = re.sub(r"\s+", " ", t.group(1)).strip() if t else ""
        time.sleep(3)
    result["title_mismatch"] = []
    for key, aid in ids.items():
        if aid in found:
            result["arxiv_titles"][key] = found[aid]
            if title_overlap(entries[key].get("title") or "", found[aid]) < 0.6:
                result["title_mismatch"].append(
                    f"{key} ({aid}): bib \"{entries[key].get('title')}\" vs arXiv \"{found[aid]}\"")
        else:
            result["arxiv_not_found"].append(f"{key} ({aid})")
    for key, e in entries.items():
        doi = e.get("doi")
        if not doi or "arxiv" in doi.lower():
            continue
        result["doi_checked"] += 1
        status, _ = http_get(f"https://doi.org/api/handles/{doi}")
        if status != 200:
            result["doi_failed"].append(f"{key} ({doi}, HTTP {status})")
    return result


PATH_TOKEN = re.compile(r"`([^`\s]+)`")
PATHLIKE = re.compile(r"^[\w./-]+$")


def check_doc_paths(root: Path):
    """Backticked paths in project docs that don't exist (e.g. a script the README names)."""
    dangling = []
    docs = [root / n for n in PROJECT_DOCS if (root / n).exists()]
    docs += [p for p in walk(root) if p.name == "README.md" and p.parent != root]
    for p in docs:
        name = str(p.relative_to(root))
        text = read(p)
        for tok in set(PATH_TOKEN.findall(text)):
            tok = tok.rstrip(".,:;)")
            if not PATHLIKE.match(tok) or tok.startswith(("-", "http")) or tok.count("/") == 0 \
                    and "." not in tok:
                continue
            if not re.search(r"\.(py|qmd|md|yml|yaml|toml|json|png|svg|bib|txt|css|js|html|sh"
                             r"|ipynb|R|csv)$|/$", tok) or re.search(r"NN|<|\*|\{", tok):
                continue
            if tok.rstrip("/") == root.name:
                continue
            candidates = [p.parent / tok, root / tok, root / "docs" / tok, root / "src" / tok,
                          root / "scripts" / tok]
            if not any(c.exists() for c in candidates) and not list(root.rglob(Path(tok).name)):
                dangling.append(f"{name}: `{tok}`")
        for ref in LINK_MD.findall(text):
            if is_external(ref) or ref.startswith("#"):
                continue
            path = ref.split("#")[0]
            if re.search(r"NN|<|\*|\{", path):
                continue
            # Project docs often show example links; accept a basename that exists anywhere.
            if path and not (p.parent / path).exists() and not (root / path).exists() \
                    and not list(root.rglob(Path(path).name)):
                dangling.append(f"{name}: link `{ref}`")
    return sorted(set(dangling))


INCLUDE = re.compile(r"\{\{<\s*include\s+([^\s>]+)\s*>\}\}")
LINKABLE = re.compile(r"\.(qmd|md|rmd|html|ipynb|py|pdf|png|svg|csv|json|ya?ml)$|/$", re.I)


def check_internal_links(root: Path, files: list[Path]):
    """Relative links in content that resolve to nothing. Included files resolve against the
    directory of the file that includes them, as Quarto does."""
    includers: dict[Path, list[Path]] = {}
    for p in files:
        if p.suffix.lower() in {".qmd", ".md", ".rmd"}:
            for inc in INCLUDE.findall(read(p)):
                includers.setdefault((p.parent / inc).resolve(), []).append(p.parent)
    broken = []
    for p in files:
        if p.suffix.lower() not in {".qmd", ".md"} or p.name in PROJECT_DOCS:
            continue
        bases = includers.get(p.resolve(), [p.parent])
        text = re.sub(r"```.*?```", "", read(p), flags=re.S)
        text = re.sub(r"\$\$.*?\$\$|\$[^$\n]+\$", "", text, flags=re.S)
        for ref in LINK_MD.findall(text):
            if is_external(ref) or ref.startswith(("#", "{{")):
                continue
            path = ref.split("#")[0].split("?")[0]
            if not path or not LINKABLE.search(path):
                continue
            ok = False
            for base in bases:
                t = base / path
                if t.exists() or (t.suffix == ".html" and t.with_suffix(".qmd").exists()):
                    ok = True
            if not ok:
                broken.append(f"{p.relative_to(root)}: `{ref}`")
    return sorted(set(broken))


def hygiene(root: Path, files: list[Path]):
    names = {str(p.relative_to(root)) for p in files}
    tests = [p for p in files if re.match(r"test_.*\.py$|.*_test\.py$", p.name)]
    n_tests = sum(len(re.findall(r"^\s*def test_", read(p), re.M)) for p in tests)
    numeric = sum(len(re.findall(r"assert_allclose|isclose|approx|allclose|assert_almost_equal",
                                 read(p))) for p in tests)
    return {
        "lockfile": [n for n in ("uv.lock", "poetry.lock", "requirements.lock", "Pipfile.lock",
                                 "renv.lock", "package-lock.json") if n in names],
        "ci_workflows": sorted(n for n in names if n.startswith(".github/workflows/")),
        "test_files": len(tests),
        "test_functions": n_tests,
        "numeric_assertions": numeric,
        "research_log": [n for n in names if re.search(r"research[-_]log|sources|references\.md",
                                                       n, re.I)],
        "license": [n for n in names if n.upper().startswith("LICENSE")],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("repo")
    ap.add_argument("--online", action="store_true", help="check arXiv ids and DOIs exist")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of Markdown")
    args = ap.parse_args()
    root = Path(args.repo).resolve()
    files = list(walk(root))

    profile = detect_profile(root, files)
    referenced, missing_imgs, orphans = check_images(root, files)
    scripted, unscripted = check_figure_scripts(root, files, referenced)
    entries, undefined, unused, no_id = check_citations(root, files)
    report = {
        "repo": root.name,
        "profile_guess": profile,
        "images_referenced": len(referenced),
        "images_missing": missing_imgs,
        "images_orphan": sorted(orphans),
        "figures_with_script": len(scripted),
        "figures_without_script": unscripted,
        "bib_entries": len(entries),
        "citations_undefined": undefined,
        "bib_unused": unused,
        "bib_without_identifier": no_id,
        "doc_paths_dangling": check_doc_paths(root),
        "internal_links_broken": check_internal_links(root, files),
        "hygiene": hygiene(root, files),
    }
    if args.online and entries:
        report["online"] = check_online(entries)

    if args.json:
        json.dump(report, sys.stdout, indent=2, default=str)
        return

    def section(title, items, empty="none"):
        print(f"\n### {title} ({len(items)})\n")
        if not items:
            print(f"_{empty}_")
        for it in items if isinstance(items, list) else [f"`{k}` used in {', '.join(v)}"
                                                          for k, v in items.items()]:
            print(f"- {it}")

    print(f"## Mechanical checks: {root.name}\n")
    print(f"- Profile (guess): **{profile}**")
    print(f"- Images referenced: {len(referenced)}; with a generating script: {len(scripted)}")
    print(f"- Bibliography entries: {len(entries)}")
    h = report["hygiene"]
    print(f"- Lockfile: {', '.join(h['lockfile']) or 'none'}; CI workflows: "
          f"{', '.join(h['ci_workflows']) or 'none'}")
    print(f"- Tests: {h['test_functions']} functions in {h['test_files']} files; "
          f"{h['numeric_assertions']} numeric-tolerance assertions")
    print(f"- Research/source log: {', '.join(h['research_log']) or 'none'}; "
          f"license: {', '.join(h['license']) or 'none'}")
    section("Missing images", [f"{f}: `{r}`" for f, r in missing_imgs])
    section("Orphan images (not referenced anywhere)", report["images_orphan"])
    section("Referenced images with no generating script (check: schematic? logo?)", unscripted)
    section("Citation keys with no bibliography entry", undefined)
    section("Bibliography entries never cited", unused)
    section("Non-book bibliography entries with no DOI/URL/eprint", no_id)
    section("Dangling paths/links in project docs", report["doc_paths_dangling"])
    section("Broken internal links in content", report["internal_links_broken"])
    if "online" in report:
        o = report["online"]
        print(f"\n### Online identifier checks\n\n- arXiv ids checked: {o['arxiv_checked']}; "
              f"DOIs checked: {o['doi_checked']}")
        section("arXiv ids not found", o["arxiv_not_found"])
        section("DOIs that did not resolve", o["doi_failed"])
        section("arXiv title differs from bib title (wrong id or wrong title?)",
                o["title_mismatch"])
        print("\n<details><summary>arXiv titles (compare with the bib titles)</summary>\n")
        for k, t in sorted(o["arxiv_titles"].items()):
            print(f"- `{k}`: {t}")
        print("\n</details>")


if __name__ == "__main__":
    main()
