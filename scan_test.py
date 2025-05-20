"""
Simple test script to run a path scan.
"""

from arch_blueprint_generator.scanner.path_scanner import PathScanner
from arch_blueprint_generator.models.detail_level import DetailLevel

# Create and run scanner with minimal detail level
scanner = PathScanner(".")
relationship_map, json_mirrors = scanner.scan(max_depth=1, detail_level=DetailLevel.MINIMAL)

print(f"Nodes: {relationship_map.node_count()}")
print(f"Relationships: {relationship_map.relationship_count()}")
