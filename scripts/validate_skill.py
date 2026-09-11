#!/usr/bin/env python3
"""Validate the public Claude Delegate package without launching a model."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = ROOT / "SKILL.md"
SCHEMA_PATH = ROOT / "references" / "report-schema.json"
OPENAI_YAML_PATH = ROOT / "agents" / "openai.yaml"

ALLOWED_FRONTMATTER_KEYS = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
}
REQUIRED_CLI_FLAGS = {
    "--allowedTools",
    "--effort",
    "--json-schema",
    "--mcp-config",
    "--model",
    "--no-chrome",
    "--output-format",
    "--permission-mode",
    "--permission-prompts",
    "--restricted",
    "--strict-mcp-config",
    "--tools",
}
SAFE_AUTH_FIELDS = (
    "loggedIn",
    "authMethod",
    "apiProvider",
    "subscriptionType",
)
IGNORED_LINK_DIRECTORIES = {".git", ".venv", "__pycache__"}
SAFE_AUTH_VALUE = re.compile(r"[A-Za-z0-9._-]{1,64}")


class ValidationFailure(RuntimeError):
    """Raised when a package invariant fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationFailure(message)


def load_optional_dependencies(require_deps: bool) -> tuple[Any | None, Any | None]:
    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError:
        yaml = None

    try:
        import jsonschema  # type: ignore[import-not-found]
    except ImportError:
        jsonschema = None

    if require_deps:
        missing = []
        if yaml is None:
            missing.append("PyYAML")
        if jsonschema is None:
            missing.append("jsonschema")
        require(
            not missing,
            "missing development dependencies: " + ", ".join(missing),
        )
    return yaml, jsonschema


def validate_frontmatter(yaml_module: Any | None) -> None:
    content = SKILL_PATH.read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n(.*?)\r?\n---(?:\r?\n|$)", content, re.DOTALL)
    require(match is not None, "SKILL.md has invalid frontmatter delimiters")
    assert match is not None

    if yaml_module is None:
        name_match = re.search(r"(?m)^name:\s*([^\r\n]+)$", match.group(1))
        description_match = re.search(
            r"(?m)^description:\s*([^\r\n]+)$", match.group(1)
        )
        require(name_match is not None, "SKILL.md is missing name")
        require(description_match is not None, "SKILL.md is missing description")
        name = name_match.group(1).strip() if name_match else ""
        description = description_match.group(1).strip() if description_match else ""
    else:
        frontmatter = yaml_module.safe_load(match.group(1))
        require(isinstance(frontmatter, dict), "frontmatter must be a mapping")
        unexpected = set(frontmatter) - ALLOWED_FRONTMATTER_KEYS
        require(not unexpected, f"unexpected frontmatter keys: {sorted(unexpected)}")
        name = frontmatter.get("name", "")
        description = frontmatter.get("description", "")

    require(isinstance(name, str), "skill name must be a string")
    require(
        re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) is not None,
        "skill name must use lowercase hyphen-case",
    )
    require(len(name) <= 64, "skill name exceeds 64 characters")
    require(isinstance(description, str) and bool(description.strip()), "missing description")
    require(len(description) <= 1024, "description exceeds 1024 characters")
    require("<" not in description and ">" not in description, "description has angle brackets")
    require(
        re.search(r"(?m)^\s*\[TODO:[^\r\n]*\]\s*$", content) is None,
        "SKILL.md contains an unfinished TODO placeholder",
    )


def validate_openai_yaml(yaml_module: Any | None) -> None:
    content = OPENAI_YAML_PATH.read_text(encoding="utf-8")
    if yaml_module is None:
        require("interface:" in content, "openai.yaml is missing interface")
        require("$claude-delegate" in content, "default prompt must name the skill")
        return

    document = yaml_module.safe_load(content)
    require(isinstance(document, dict), "openai.yaml must be a mapping")
    interface = document.get("interface")
    require(isinstance(interface, dict), "openai.yaml is missing interface")
    short_description = interface.get("short_description", "")
    require(
        isinstance(short_description, str) and 25 <= len(short_description) <= 64,
        "short_description must contain 25-64 characters",
    )
    default_prompt = interface.get("default_prompt", "")
    require(
        isinstance(default_prompt, str) and "$claude-delegate" in default_prompt,
        "default_prompt must mention $claude-delegate",
    )


def validate_local_links() -> None:
    link_pattern = re.compile(r"\[[^\]]+\]\((?!https?://)([^)#]+)(?:#[^)]+)?\)")
    missing: list[str] = []
    for document in ROOT.rglob("*.md"):
        relative_parts = document.relative_to(ROOT).parts
        if any(part in IGNORED_LINK_DIRECTORIES for part in relative_parts):
            continue
        content = document.read_text(encoding="utf-8")
        for raw_target in link_pattern.findall(content):
            target = (document.parent / raw_target).resolve()
            if not target.exists():
                missing.append(f"{document.relative_to(ROOT)} -> {raw_target}")
    require(not missing, "broken local Markdown links: " + ", ".join(missing))


def report_fixtures() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    valid = {
        "status": "complete",
        "summary": "Completed and verified.",
        "instruction_files": [],
        "changed_files": ["result.txt"],
        "checks": [
            {
                "command": "verify result.txt",
                "required": True,
                "status": "passed",
                "exit_code": 0,
                "outcome": "Expected content observed.",
            }
        ],
        "permission_denials": [],
        "unexpected_changes": [],
        "unfinished_work": [],
    }
    missing_exit = json.loads(json.dumps(valid))
    del missing_exit["checks"][0]["exit_code"]
    complete_with_unfinished = json.loads(json.dumps(valid))
    complete_with_unfinished["unfinished_work"] = ["Still pending."]
    failed_with_zero = json.loads(json.dumps(valid))
    failed_with_zero["checks"][0].update(status="failed", exit_code=0)
    empty_summary = json.loads(json.dumps(valid))
    empty_summary["summary"] = ""
    complete_with_required_denial = json.loads(json.dumps(valid))
    complete_with_required_denial["checks"][0] = {
        "command": "verify result.txt",
        "required": True,
        "status": "denied",
        "outcome": "Permission was denied.",
    }
    return valid, [
        missing_exit,
        complete_with_unfinished,
        failed_with_zero,
        empty_summary,
        complete_with_required_denial,
    ]


def validate_schema(jsonschema_module: Any | None) -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    require(
        schema.get("$schema") == "http://json-schema.org/draft-07/schema#",
        "report schema must declare draft 7",
    )
    require(schema.get("additionalProperties") is False, "top-level extras must be denied")
    for keyword in ("oneOf", "allOf", "anyOf"):
        require(
            keyword not in schema,
            f"top-level {keyword} is incompatible with Claude structured output",
        )

    def check_array_keyword_types(node: Any, location: str = "#") -> None:
        if isinstance(node, dict):
            array_keywords = {"contains", "maxItems", "minItems", "uniqueItems"}
            if array_keywords.intersection(node):
                require(
                    node.get("type") == "array",
                    f"array keyword without explicit array type at {location}",
                )
            for key, value in node.items():
                check_array_keyword_types(value, f"{location}/{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                check_array_keyword_types(value, f"{location}/{index}")

    check_array_keyword_types(schema)
    if jsonschema_module is None:
        return

    validator_type = jsonschema_module.Draft7Validator
    validator_type.check_schema(schema)
    validator = validator_type(schema)
    valid, invalid = report_fixtures()
    require(not list(validator.iter_errors(valid)), "positive report fixture was rejected")
    for index, fixture in enumerate(invalid, start=1):
        require(
            bool(list(validator.iter_errors(fixture))),
            f"negative report fixture {index} was accepted",
        )


def run_command(arguments: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        arguments,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )


def validate_cli() -> None:
    executable = shutil.which("claude")
    require(executable is not None, "claude is not available on PATH")
    assert executable is not None

    version_result = run_command([executable, "--version"])
    require(version_result.returncode == 0, "claude --version failed")
    version_output = version_result.stdout + "\n" + version_result.stderr
    version_match = re.search(r"(\d+)\.(\d+)\.(\d+)", version_output)
    require(version_match is not None, "could not parse Claude Code version")
    version = tuple(int(part) for part in version_match.groups()) if version_match else (0, 0, 0)
    require(version >= (2, 1, 259), "Claude Code 2.1.259 or later is required")

    help_result = run_command([executable, "--help"])
    require(help_result.returncode == 0, "claude --help failed")
    missing_flags = sorted(flag for flag in REQUIRED_CLI_FLAGS if flag not in help_result.stdout)
    require(not missing_flags, "Claude help is missing flags: " + ", ".join(missing_flags))

    max_turns_result = run_command([executable, "--max-turns", "1", "--help"])
    require(max_turns_result.returncode == 0, "Claude CLI rejected --max-turns")

    auth_result = run_command([executable, "auth", "status", "--json"])
    require(auth_result.returncode == 0, "claude auth status failed")
    try:
        auth = json.loads(auth_result.stdout)
    except json.JSONDecodeError as error:
        raise ValidationFailure("claude auth status returned invalid JSON") from error
    require(isinstance(auth, dict), "claude auth status did not return an object")
    assert isinstance(auth, dict)
    logged_in = auth.get("loggedIn")
    require(isinstance(logged_in, bool), "Claude login state is not a boolean")
    projected: dict[str, bool | str | None] = {"loggedIn": logged_in}
    for field in SAFE_AUTH_FIELDS[1:]:
        value = auth.get(field)
        require(
            value is None
            or (isinstance(value, str) and SAFE_AUTH_VALUE.fullmatch(value) is not None),
            f"Claude {field} value could not be safely normalized",
        )
        projected[field] = value
    require(projected["loggedIn"] is True, "Claude Code is not logged in")
    print("auth=" + json.dumps(projected, separators=(",", ":")))
    print(f"claude_version={'.'.join(str(part) for part in version)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--require-deps",
        action="store_true",
        help="fail unless PyYAML and jsonschema are installed",
    )
    parser.add_argument(
        "--check-cli",
        action="store_true",
        help="check local CLI flags and redacted auth without a model request",
    )
    arguments = parser.parse_args()

    try:
        yaml_module, jsonschema_module = load_optional_dependencies(arguments.require_deps)
        validate_frontmatter(yaml_module)
        validate_openai_yaml(yaml_module)
        validate_local_links()
        validate_schema(jsonschema_module)
        if arguments.check_cli:
            validate_cli()
    except (OSError, subprocess.SubprocessError, ValidationFailure, ValueError) as error:
        print(f"validation failed: {error}", file=sys.stderr)
        return 1

    skipped = []
    if yaml_module is None:
        skipped.append("full YAML parsing")
    if jsonschema_module is None:
        skipped.append("draft-7 metaschema and fixtures")
    if skipped:
        print("core validation passed; skipped: " + ", ".join(skipped))
    else:
        print("full package validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
