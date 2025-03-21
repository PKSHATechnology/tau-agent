# tau-agent

A Python-based agent for MCP (Model Context Protocol) clients.

## Setup

This project uses [uv](https://github.com/astral-sh/uv) for package management.

### Installation

1. Install dependencies:

```bash
# Install for development
make dev-install

# Or install for production
make install
```

2. Create a configuration file:

```bash
cp config.example.json config.json
```

3. Edit the configuration file to add your API keys and MCP server settings.

## Usage

Run the agent:

```bash
python -m tau
```

Or with a custom config file:

```bash
python -m tau -c path/to/config.json
```

## Development

Format and lint the code:

```bash
make format
```

Clean build artifacts:

```bash
make clean
```
