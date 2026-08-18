[project]
name = "{{repo-name}}"
version = "0.1.0"
description = "{{one-line description: interview prep and drills for <company/topic> <round>.}}"
requires-python = ">=3.10"
dependencies = []

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]

[dependency-groups]
dev = [
    "pytest>=9.0.3",
]
