# Environment Variables

This document outlines the environment variables used by Architectum. These variables control various aspects of the application's behavior and can be set in a `.env` file or directly in the environment.

## Core Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `ARCH_LOG_LEVEL` | `INFO` | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`) |
| `ARCH_LOG_FORMAT` | `json` | Log format (`json`, `plain`) |
| `ARCH_WORKSPACE_PATH` | `~/.architectum` | Path to store Architectum workspace data |
| `ARCH_CACHE_SIZE_MB` | `500` | Maximum cache size in megabytes |
| `ARCH_DB_PATH` | `~/.architectum/arch.db` | Path to SQLite database file |

## Parser Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `ARCH_PARSER_TIMEOUT` | `30` | Parser timeout in seconds |
| `ARCH_PARSER_THREADS` | `4` | Number of parser threads for parallel processing |
| `ARCH_MAX_FILE_SIZE_MB` | `10` | Maximum file size to parse in megabytes |
| `ARCH_IGNORE_PATTERNS` | `node_modules,.git,__pycache__,venv` | Comma-separated list of patterns to ignore |

## LSP Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `ARCH_USE_LSP` | `true` | Whether to use Language Server Protocol for enhanced parsing |
| `ARCH_LSP_TIMEOUT` | `10` | LSP request timeout in seconds |
| `ARCH_LSP_PYTHON_CMD` | (system-dependent) | Command to start Python language server |
| `ARCH_LSP_JS_CMD` | (system-dependent) | Command to start JavaScript/TypeScript language server |
| `ARCH_LSP_RETRY_COUNT` | `3` | Number of times to retry LSP connections |

## Blueprint Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `ARCH_DEFAULT_DETAIL_LEVEL` | `standard` | Default detail level for blueprints (`minimal`, `standard`, `detailed`) |
| `ARCH_DEFAULT_FORMAT` | `json` | Default output format (`json`, `xml`) |
| `ARCH_BLUEPRINT_PATH` | `~/.architectum/blueprints` | Path to store persistent blueprints |
| `ARCH_MAX_BLUEPRINT_SIZE_MB` | `50` | Maximum blueprint size in megabytes |
| `ARCH_BLUEPRINT_RETENTION_DAYS` | `90` | Days to retain temporary blueprints |

## Synchronization Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `ARCH_AUTO_SYNC` | `false` | Whether to automatically sync changes |
| `ARCH_SYNC_INTERVAL` | `300` | Interval for auto-sync in seconds (if enabled) |
| `ARCH_MAX_SYNC_FILES` | `1000` | Maximum number of files to sync in one operation |
| `ARCH_SYNC_THREADS` | `4` | Number of threads for parallel synchronization |

## API Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `ARCH_API_HOST` | `127.0.0.1` | Host for API server |
| `ARCH_API_PORT` | `8000` | Port for API server |
| `ARCH_API_WORKERS` | `4` | Number of worker processes for API server |
| `ARCH_API_TIMEOUT` | `60` | API request timeout in seconds |
| `ARCH_API_CORS_ORIGINS` | `*` | Comma-separated list of allowed CORS origins |

## Development Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `ARCH_DEV_MODE` | `false` | Enable development mode with additional logging |
| `ARCH_PROFILE_ENABLED` | `false` | Enable performance profiling |
| `ARCH_TRACE_ENABLED` | `false` | Enable detailed tracing |
| `ARCH_MOCK_LSP` | `false` | Use mock LSP responses for testing |

## Example .env File

```
# Core Configuration
ARCH_LOG_LEVEL=INFO
ARCH_WORKSPACE_PATH=~/.architectum
ARCH_CACHE_SIZE_MB=500

# Parser Configuration
ARCH_PARSER_THREADS=4
ARCH_IGNORE_PATTERNS=node_modules,.git,__pycache__,venv,dist,build

# LSP Configuration
ARCH_USE_LSP=true
ARCH_LSP_TIMEOUT=10

# Blueprint Configuration
ARCH_DEFAULT_DETAIL_LEVEL=standard
ARCH_DEFAULT_FORMAT=json

# Synchronization Configuration
ARCH_AUTO_SYNC=false
ARCH_SYNC_THREADS=4

# API Configuration
ARCH_API_HOST=127.0.0.1
ARCH_API_PORT=8000
```

## Setting Environment Variables

### In Development

For development environments, create a `.env` file in the project root:

```bash
# Create .env file
touch .env

# Edit with your preferred editor
nano .env
```

### In Production

For production environments, set environment variables according to your deployment platform:

#### Linux/macOS

```bash
export ARCH_LOG_LEVEL=INFO
export ARCH_CACHE_SIZE_MB=1000
# Other variables...
```

#### Windows

```cmd
set ARCH_LOG_LEVEL=INFO
set ARCH_CACHE_SIZE_MB=1000
:: Other variables...
```

#### Docker

```dockerfile
ENV ARCH_LOG_LEVEL=INFO
ENV ARCH_CACHE_SIZE_MB=1000
# Other variables...
```

## Loading Environment Variables

Architectum uses `python-dotenv` to load environment variables from a `.env` file. The variables are loaded at application startup.

```python
# Example of how environment variables are loaded in Architectum
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
log_level = os.getenv("ARCH_LOG_LEVEL", "INFO")
cache_size = int(os.getenv("ARCH_CACHE_SIZE_MB", "500"))
```
