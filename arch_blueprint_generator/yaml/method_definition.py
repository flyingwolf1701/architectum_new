"""YAML handling for method-based blueprints."""

from dataclasses import dataclass, field
from typing import Dict, List

from arch_blueprint_generator.yaml.blueprint_config import (
    BlueprintConfig,
    Component,
    YAMLValidationError,
    load_blueprint_config,
)


@dataclass
class MethodBlueprintConfig:
    """Structured configuration for a method-based blueprint."""

    name: str
    detail_level: str
    components: Dict[str, List[str]] = field(default_factory=dict)


def load_method_blueprint_config(path: str) -> MethodBlueprintConfig:
    """Load a method blueprint YAML definition."""

    config: BlueprintConfig = load_blueprint_config(path)
    if config.type != "method":
        raise YAMLValidationError("Blueprint type must be 'method'")

    components: Dict[str, List[str]] = {
        comp.file: comp.elements for comp in config.components
    }

    return MethodBlueprintConfig(
        name=config.name,
        detail_level=config.detail_level,
        components=components,
    )

