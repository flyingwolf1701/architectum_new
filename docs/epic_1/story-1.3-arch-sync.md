# Story 1.3: Implement 'arch sync' Command for Representation Updates

## Status: Draft

## Story

- As a developer
- I want to use the `arch sync` command to synchronize code changes with Architectum's representations
- So that both the Relationship Map and JSON Mirrors remain up to date

## Acceptance Criteria (ACs)

- AC1: The `arch sync` command successfully updates both representations when files change.
- AC2: Only changed files are processed, improving performance for incremental updates.
- AC3: The command supports synchronizing individual files, directories, and multiple files.
- AC4: Status information is displayed showing which files were synchronized.
- AC5: Proper error handling is implemented for synchronization failures.
- AC6: Testing Requirements:
  - Coverage: At least 80% code coverage for the synchronization functionality
  - Framework: Implementation using pytest with file modification simulation
  - Mocking: Mock file changes to test change detection
  - Integration Testing: End-to-end tests for the sync command with various parameters
  - Performance Testing: Verify incremental updates are significantly faster than full scans
  - Error Handling: Test recovery from various error conditions during synchronization
## Tasks / Subtasks

- [ ] Implement change detection mechanism (AC: 2)
  - [ ] Create file hash-based change tracking
  - [ ] Implement comparison logic for detecting file changes
  - [ ] Create database/storage for tracking previous file states
  - [ ] Implement logic to identify which files need synchronization

- [ ] Implement incremental update logic (AC: 1, 2)
  - [ ] Create updater for Relationship Map that processes only changed nodes/relationships
  - [ ] Create updater for JSON Mirrors that processes only changed files
  - [ ] Implement validation to ensure consistency between representations
  - [ ] Create hooks to connect change detection with update logic

- [ ] Implement CLI interface for `arch sync` command (AC: 1, 3, 4)
  - [ ] Create `arch sync` command using Typer framework
  - [ ] Implement option for syncing specific file (`--file` parameter)
  - [ ] Implement option for syncing directory (`--directory` parameter)
  - [ ] Implement option for syncing multiple files (multiple `--file` parameters)
  - [ ] Add option to show sync status without performing updates (`--status` parameter)
  - [ ] Implement progress indicators and status reporting

- [ ] Implement error handling for synchronization (AC: 5)
  - [ ] Create robust error handling for file access issues
  - [ ] Implement graceful failure for individual file synchronization issues
  - [ ] Add detailed error reporting with actionable messages
  - [ ] Ensure partial updates don't corrupt the representations

- [ ] Create comprehensive tests (AC: 6)
  - [ ] Implement unit tests for change detection logic
  - [ ] Implement unit tests for incremental update logic
  - [ ] Create integration tests for the `arch sync` command
  - [ ] Implement mocking for file system changes
  - [ ] Create performance benchmarks for incremental vs. full updates
  - [ ] Test error recovery scenarios
## Dev Technical Guidance

### Change Detection Implementation

The change detection mechanism should use file hashes to identify changes efficiently. Store hashes in a SQLite database or a structured JSON file for persistence across runs. Consider these implementation details:

```python
# Example implementation approach for change detection
import hashlib
import os
import json
from typing import Dict, List, Set, Tuple

class ChangeTracker:
    def __init__(self, tracking_file_path: str = ".arch_sync_tracking.json"):
        self.tracking_file_path = tracking_file_path
        self.file_hashes = self._load_tracking_data()
    
    def _load_tracking_data(self) -> Dict[str, str]:
        if os.path.exists(self.tracking_file_path):
            with open(self.tracking_file_path, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_tracking_data(self) -> None:
        with open(self.tracking_file_path, 'w') as f:
            json.dump(self.file_hashes, f, indent=2)
    
    def compute_file_hash(self, file_path: str) -> str:
        """Compute SHA-256 hash of a file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
```    
    def detect_changes(self, file_paths: List[str]) -> Tuple[Set[str], Set[str], Set[str]]:
        """
        Detects changes in the specified files.
        
        Returns:
            Tuple of (changed_files, new_files, deleted_files)
        """
        changed_files = set()
        new_files = set()
        deleted_files = set()
        
        # Find changed and new files
        for file_path in file_paths:
            if not os.path.exists(file_path):
                if file_path in self.file_hashes:
                    deleted_files.add(file_path)
                continue
                
            current_hash = self.compute_file_hash(file_path)
            
            if file_path not in self.file_hashes:
                new_files.add(file_path)
            elif self.file_hashes[file_path] != current_hash:
                changed_files.add(file_path)
                
            # Update hash
            self.file_hashes[file_path] = current_hash
        
        # Save updated tracking data
        self._save_tracking_data()
        
        return changed_files, new_files, deleted_files
```

### Incremental Update Strategy

For incremental updates, implement the following pattern:

1. Parse only changed files to extract updated nodes and relationships
2. Remove outdated nodes and relationships from the Relationship Map
3. Add new/updated nodes and relationships to the Relationship Map
4. Update JSON Mirrors only for changed files
5. Maintain references to ensure consistency between both representations

Consider using a transaction-like approach where updates are applied atomically to avoid inconsistent states.
### CLI Implementation

Use Typer for the CLI implementation, taking advantage of type hints:

```python
import typer
from typing import List, Optional
from pathlib import Path
from colorama import Fore, Style

app = typer.Typer()

@app.command()
def sync(
    file: List[str] = typer.Option(None, "--file", "-f", help="File to synchronize"),
    directory: Optional[str] = typer.Option(None, "--directory", "-d", help="Directory to synchronize"),
    status: bool = typer.Option(False, help="Show sync status without performing updates")
) -> None:
    """
    Synchronize code changes with Architectum representations.
    
    This command updates both the Relationship Map and JSON Mirrors based on changes
    to code files. It can synchronize specific files, directories, or show status.
    """
    # Implementation details here
```

### Testing Strategy

Focus on robust testing with mocked file systems to avoid external dependencies:

1. Use the `pytest-mock` plugin to mock file system operations
2. Create temporary test files with controlled content for integration tests
3. Simulate file changes by updating content and checking detection
4. Benchmark performance by measuring time taken for incremental vs. full updates
5. Test error conditions by simulating file access failures and corrupted states

## Story Progress Notes

### Agent Model Used: `<Agent Model Name/Version>`

### Completion Notes List
{Not started yet}

### Change Log
- Initial story draft created by POSM

## QA Testing Guide

{This section should be completed when the story implementation is done and tests are passing. Include step-by-step instructions for how a human tester can verify the functionality works as expected. Include example inputs, expected outputs, and any edge cases that should be tested.}