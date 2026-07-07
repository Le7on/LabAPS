[project]
name = "lab-aps"
version = "{{VERSION}}"
description = "Laboratory Advanced Planning & Scheduling Platform"
requires-python = ">=3.11"

[tool.ruff]
line-length = 100
target-version = "py311"
extend-exclude = [
    ".venv",
    "frontend",
    "resources",
    "deployment",
]

[tool.ruff.lint]
select = ["E", "W", "F", "I", "UP", "B", "SIM", "C4"]
ignore = [
    "E501",
]

[tool.ruff.lint.isort]
known-first-party = ["backend"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.black]
line-length = 100
target-version = ["py311"]

[tool.isort]
profile = "black"
line_length = 100
known_first_party = ["backend"]

[tool.mypy]
python_version = "3.11"
ignore_missing_imports = true
exclude = ["frontend", ".venv"]

[tool.pytest.ini_options]
testpaths = ["backend", "tests"]
python_files = ["test_*.py"]
