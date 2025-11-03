#!/usr/bin/env python3
"""
Generate config.yaml from environment variables for Railway deployment.
This script reads all configuration from Railway environment variables and
creates a config.yaml file that the application can use.
"""
import os
import yaml
from pathlib import Path

def generate_config_from_env():
    """Generate config.yaml from environment variables."""
    
    # Start with template config structure
    config = {
        "agent": {
            "name": os.getenv("AGENT_NAME", "bianca"),
            "display_name": os.getenv("AGENT_DISPLAY_NAME", "Bianca"),
            "description": os.getenv("AGENT_DESCRIPTION", "An AI agent built with Animus Social framework."),
            "personality": {
                "core_identity": os.getenv("AGENT_CORE_IDENTITY", ""),
                "development_directive": os.getenv("AGENT_DEVELOPMENT_DIRECTIVE", ""),
                "communication_style": os.getenv("AGENT_COMMUNICATION_STYLE", "witty, engaging, informative, conversational"),
                "tone": os.getenv("AGENT_TONE", "friendly, knowledgeable, curious")
            },
            "capabilities": {
                "model": os.getenv("AGENT_MODEL", "openai/gpt-4o-mini"),
                "embedding": os.getenv("AGENT_EMBEDDING", "openai/text-embedding-3-small"),
                "max_steps": int(os.getenv("AGENT_MAX_STEPS", "100"))
            },
            "commands": {
                "stop_command": os.getenv("AGENT_STOP_COMMAND", "#biancastop"),
                "synthesis_frequency": os.getenv("AGENT_SYNTHESIS_FREQUENCY", "daily"),
                "journal_enabled": os.getenv("AGENT_JOURNAL_ENABLED", "true").lower() == "true"
            },
            "memory_blocks": {}
        },
        "letta": {
            "api_key": os.getenv("LETTA_API_KEY", ""),
            "timeout": int(os.getenv("LETTA_TIMEOUT", "600")),
            "agent_id": os.getenv("LETTA_AGENT_ID", ""),
            "base_url": os.getenv("LETTA_BASE_URL", None)
        },
        "platforms": {
            "bluesky": {
                "enabled": os.getenv("BLUESKY_ENABLED", "false").lower() == "true",
                "username": os.getenv("BLUESKY_USERNAME", ""),
                "password": os.getenv("BLUESKY_PASSWORD", ""),
                "pds_uri": os.getenv("BLUESKY_PDS_URI", "https://bsky.social")
            },
            "x": {
                "enabled": os.getenv("X_ENABLED", "true").lower() == "true",
                "api_key": os.getenv("X_API_KEY", ""),
                "user_id": os.getenv("X_USER_ID", ""),
                "consumer_key": os.getenv("X_CONSUMER_KEY", ""),
                "consumer_secret": os.getenv("X_CONSUMER_SECRET", ""),
                "access_token": os.getenv("X_ACCESS_TOKEN", ""),
                "access_token_secret": os.getenv("X_ACCESS_TOKEN_SECRET", "")
            },
            "discord": {
                "enabled": os.getenv("DISCORD_ENABLED", "false").lower() == "true",
                "bot_token": os.getenv("DISCORD_BOT_TOKEN", "")
            }
        },
        "logging": {
            "level": os.getenv("LOG_LEVEL", "INFO"),
            "logger_names": {
                "main": os.getenv("LOG_MAIN_LOGGER", "{agent_name}_bot"),
                "prompts": os.getenv("LOG_PROMPTS_LOGGER", "{agent_name}_bot_prompts"),
                "platform": os.getenv("LOG_PLATFORM_LOGGER", "{agent_name}_platform")
            },
            "loggers": {
                "{agent_name}_bot": os.getenv("LOG_BOT_LEVEL", "INFO"),
                "{agent_name}_bot_prompts": os.getenv("LOG_PROMPTS_LEVEL", "WARNING"),
                "httpx": "CRITICAL"
            }
        }
    }
    
    # Add memory blocks if provided
    memory_blocks = {
        "zeitgeist": {
            "label": "zeitgeist",
            "value": os.getenv("MEMORY_ZEITGEIST", ""),
            "description": "A block to store your understanding of the current social environment."
        },
        "persona": {
            "label": "{agent_name}-persona",
            "value": os.getenv("MEMORY_PERSONA", ""),
            "description": "The personality of {agent_name}."
        },
        "humans": {
            "label": "{agent_name}-humans",
            "value": os.getenv("MEMORY_HUMANS", ""),
            "description": "A block to store your understanding of users you talk to or observe on social networks."
        }
    }
    
    # Only add memory blocks if values are provided
    if memory_blocks["zeitgeist"]["value"]:
        config["agent"]["memory_blocks"]["zeitgeist"] = memory_blocks["zeitgeist"]
    if memory_blocks["persona"]["value"]:
        config["agent"]["memory_blocks"]["persona"] = memory_blocks["persona"]
    if memory_blocks["humans"]["value"]:
        config["agent"]["memory_blocks"]["humans"] = memory_blocks["humans"]
    
    # Add animus_knowledge block if provided
    animus_knowledge = os.getenv("MEMORY_ANIMUS_KNOWLEDGE", "")
    if animus_knowledge:
        config["agent"]["memory_blocks"]["animus_knowledge"] = {
            "label": "{agent_name}-animus-knowledge",
            "value": animus_knowledge,
            "description": "My comprehensive knowledge of the Animus framework, ecosystem, and philosophy."
        }
    
    # Write config.yaml
    config_path = Path("config.yaml")
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    print(f"✅ Generated config.yaml from environment variables")
    print(f"   Agent: {config['agent']['name']}")
    print(f"   X Enabled: {config['platforms']['x']['enabled']}")
    print(f"   Letta Base URL: {config['letta'].get('base_url', 'Not set (using cloud)')}")
    
    # Validate required fields
    required_fields = []
    if not config["letta"]["api_key"]:
        required_fields.append("LETTA_API_KEY")
    if not config["letta"]["agent_id"]:
        required_fields.append("LETTA_AGENT_ID")
    if config["platforms"]["x"]["enabled"]:
        if not config["platforms"]["x"]["api_key"]:
            required_fields.append("X_API_KEY")
        if not config["platforms"]["x"]["consumer_key"]:
            required_fields.append("X_CONSUMER_KEY")
        if not config["platforms"]["x"]["consumer_secret"]:
            required_fields.append("X_CONSUMER_SECRET")
        if not config["platforms"]["x"]["access_token"]:
            required_fields.append("X_ACCESS_TOKEN")
        if not config["platforms"]["x"]["access_token_secret"]:
            required_fields.append("X_ACCESS_TOKEN_SECRET")
    
    if required_fields:
        print(f"\n⚠️  Warning: Missing required environment variables:")
        for field in required_fields:
            print(f"   - {field}")
        print("\n   The application may not work correctly without these.")
    else:
        print("\n✅ All required configuration fields are set")
    
    return config_path

if __name__ == "__main__":
    generate_config_from_env()
