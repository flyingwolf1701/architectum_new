"""YAML blueprint configuration parsing."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import os
import re


@dataclass
class Component:
    """Represents a single blueprint component."""
    file: str
    elements: List[str] = field(default_factory=list)


@dataclass
class BlueprintConfig:
    """Represents a blueprint configuration loaded from YAML."""
    type: str
    name: str
    description: Optional[str] = None
    persistence: str = "temporary"
    detail_level: str = "standard"
    components: List[Component] = field(default_factory=list)


class YAMLValidationError(Exception):
    """Raised when a YAML configuration is invalid."""


def _parse_value(value: str) -> Any:
    value = value.strip()
    if value == "" or value is None:
        return None
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [item.strip() for item in inner.split(",")]
    if (value.startswith("'") and value.endswith("'")) or (
        value.startswith('"') and value.endswith('"')
    ):
        return value[1:-1]
    return value


def _parse_yaml(text: str) -> Dict[str, Any]:
    """Very small YAML subset parser supporting dicts and lists."""
    result: Dict[str, Any] = {}
    stack: List[tuple[int, Any]] = [(0, result)]
    last_key_stack: List[Optional[str]] = [None]

    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.strip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip())
        line = raw_line.lstrip()

        while stack and indent < stack[-1][0]:
            stack.pop()
            last_key_stack.pop()
        parent = stack[-1][1]
        last_key = last_key_stack[-1]

        if line.startswith("- "):
            item_line = line[2:]
            if isinstance(parent, dict):
                if last_key is None:
                    raise YAMLValidationError("List item with no key")
                if not isinstance(parent[last_key], list):
                    parent[last_key] = []
                parent = parent[last_key]
            if isinstance(parent, list):
                if ":" in item_line:
                    key, val = item_line.split(":", 1)
                    d: Dict[str, Any] = {key.strip(): _parse_value(val)}
                    parent.append(d)
                    if val.strip() == "":
                        stack.append((indent + 2, d))
                        last_key_stack.append(key.strip())
                    else:
                        last_key_stack.append(None)
                else:
                    parent.append(_parse_value(item_line))
                    last_key_stack.append(None)
            else:
                raise YAMLValidationError("Invalid list structure")
        else:
            if ":" not in line:
                raise YAMLValidationError(f"Invalid line: {raw_line}")
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            if isinstance(parent, list):
                raise YAMLValidationError("Cannot add key-value pair inside list without dash")
            parent[key] = _parse_value(val)
            last_key_stack[-1] = key
            if val == "":
                stack.append((indent + 2, parent[key]))
                last_key_stack.append(None)
            else:
                last_key_stack.append(None)
    return result


def load_blueprint_config(path: str) -> BlueprintConfig:
    """Load and validate a blueprint YAML definition."""
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    text = open(path, "r", encoding="utf-8").read()
    data = _parse_yaml(text)
    if "type" not in data or "components" not in data:
        raise YAMLValidationError("Blueprint config must contain 'type' and 'components'")

    components = []
    for comp in data.get("components", []):
        if isinstance(comp, dict):
            file = comp.get("file")
            if not file:
                raise YAMLValidationError("Component missing 'file'")
            elements = comp.get("elements", [])
            if not isinstance(elements, list):
                raise YAMLValidationError("'elements' must be a list")
            components.append(Component(file=file, elements=elements))
        else:
            raise YAMLValidationError("Invalid component entry")

    return BlueprintConfig(
        type=data.get("type"),
        name=data.get("name", "blueprint"),
        description=data.get("description"),
        persistence=data.get("persistence", "temporary"),
        detail_level=data.get("detail_level", "standard"),
        components=components,
    )
