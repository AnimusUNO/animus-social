# Animus Architecture Overview

## System Architecture

Animus is built as a modular ecosystem of specialized repositories, each handling specific cognitive functions. The Animus ecosystem follows a brain-inspired modular design where each repository represents a specific cognitive function, working together through the Letta kernel to create a complete multi-agent system.

## Component Categories

### Core System Components
These are core components that flesh out the core systems required to run Animus agents.

- **[installer](https://github.com/AnimusUNO/installer)** - Bootstrap installation and system setup
- **[smcp](https://github.com/AnimusUNO/smcp)** - Sanctum Model Context Protocol server for advanced agent tools

### Research Repositories
These exist to help you build advanced functions, and the individual repos describe how these algorithms and methodologies fit into the larger framework.

- **[thalamus](https://github.com/AnimusUNO/thalamus)** - Sensory routing and filtering system
- **[cochlea](https://github.com/AnimusUNO/cochlea)** - Audio processing and voice interaction

### Integration Components
Utility repos we've created to demonstrate modalities or help you in your Animus journey.

- **[animus-tui](https://github.com/AnimusUNO/animus-tui)** - Terminal user interface for agent interaction
- **[animus-discord](https://github.com/AnimusUNO/animus-discord)** - Discord integration and webhook processing
- **[animus-web-chat](https://github.com/AnimusUNO/animus-web-chat)** - Flask-based web client for Animus

---

**Source**: [about-animus.md](https://github.com/AnimusUNO)

