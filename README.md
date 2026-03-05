# NodePing Status

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

A Home Assistant custom integration that monitors your services via [NodePing](https://nodeping.com) public status reports.

## Features

- **Binary sensor** per check showing up/down connectivity status
- **Uptime sensors** for today's and 30-day uptime percentage
- Supports multiple report entries, each with a custom name

## Installation

### HACS (recommended)

1. Open HACS in Home Assistant
2. Go to **Integrations** → three-dot menu → **Custom repositories**
3. Add this repository URL and select **Integration** as the category
4. Install **NodePing Status**
5. Restart Home Assistant

### Manual

1. Copy `custom_components/nodeping_status` into your `config/custom_components/` directory
2. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services** → **Add Integration**
2. Search for **NodePing Status**
3. Enter a public report ID and a name for the entry
4. Repeat to add additional report IDs

## Disclaimer

This integration was created with the assistance of [Claude Code](https://github.com/anthropics/claude-code) by Anthropic.

## License

This project is licensed under the Apache License 2.0 — see the [LICENSE](LICENSE) file for details.
