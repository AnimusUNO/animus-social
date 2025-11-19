# Installation Guide

Animus uses a bootstrap installer for easy setup. The installer automates the installation and configuration of the complete Animus multi-agent system.

## Prerequisites

- **Operating System**: Ubuntu, WSL, or Raspbian
- **Root Access**: sudo privileges required
- **Internet Connection**: Required for package installation and Docker pulls
- **Domain**: A domain name pointing to your server (for SSL certificates)

## Installation Steps

### 1. Clone the installer repository:
```bash
git clone https://github.com/AnimusUNO/installer.git
cd installer
```

### 2. Customize the bootstrap script:
```bash
nano kernel-installer/animus_bootstrap.sh
```

**Required Customizations:**
```bash
DOMAIN="your-domain.com"                    # Your actual domain
EMAIL="your-email@domain.com"               # Your email for SSL
LETTAPASS="your-secure-password"            # Secure password for Letta
OPENAI_API_KEY="your-openai-key"            # Your OpenAI API key
ANTHROPIC_API_KEY="your-anthropic-key"      # Your Anthropic API key
```

### 3. Run the installation:
```bash
sudo bash kernel-installer/animus_bootstrap.sh
```

### 4. Verify installation:
```bash
# Check if Letta container is running
docker ps | grep letta

# Check Nginx status
sudo systemctl status nginx

# Check SSL certificate
sudo certbot certificates
```

## Post-Installation Access

After installation, you can access:
- **Letta Web Interface**: `https://your-domain.com`
- **Letta Admin**: `https://app.letta.com/`
- **TUI Interface**: Terminal-based user interface ([animus-tui](https://github.com/AnimusUNO/animus-tui))

## Quick Start Workflow

### 1. Create an agent using the ADE:
- Access the Letta Web Interface at `https://your-domain.com`
- Use the Agent Development Environment to create and configure your first agent
- Set up the agent's personality, memory, and capabilities

### 2. Access your agent:
- **Web Interface**: Continue using the ADE at `https://your-domain.com`
- **CLI/TUI**: Use the [animus-tui](https://github.com/AnimusUNO/animus-tui) interface for terminal-based interaction
- **API**: Access programmatically via the Letta API endpoints

### 3. Agent Management:
- Configure agent settings through the ADE
- Monitor agent performance and memory usage
- Scale and deploy multiple agents as needed

## Adding Components

### Core Installation
Start with the installer. Get the foundational Animus framework up and running by following the installation guide in our [installer repository](https://github.com/AnimusUNO/installer).

### Advanced Functionality
Adding advanced functionality to your installation? Install the **SMCP** (Sanctum Model Context Protocol) to enable your agents to use advanced tools and integrations. Learn more at the [SMCP repository](https://github.com/AnimusUNO/smcp).

### Voice Integration
Experimenting with voice for the first time? Start with the **Cochlea** repository for audio processing and voice interaction capabilities. Explore voice features at the [Cochlea repository](https://github.com/AnimusUNO/cochlea).

### Advanced Sensory Input
Doing advanced sensory input? Experiment with the **Thalamus** repository for sophisticated sensory processing, routing, and context management. Dive into sensory systems at the [Thalamus repository](https://github.com/AnimusUNO/thalamus).

## Troubleshooting

### Common Issues

**1. SSL Certificate Issues**
```bash
# Check certificate status
sudo certbot certificates

# Renew certificates manually
sudo certbot renew --dry-run
```

**2. Docker Container Not Starting**
```bash
# Check container logs
docker logs letta-container

# Restart container
docker restart letta-container
```

**3. Nginx Configuration Issues**
```bash
# Test configuration
sudo nginx -t

# Reload configuration
sudo systemctl reload nginx
```

---

**Source**: [about-animus.md](https://github.com/AnimusUNO), [installer repository](https://github.com/AnimusUNO/installer)

