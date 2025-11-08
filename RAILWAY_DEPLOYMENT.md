# Railway Deployment Guide for Animus Social

This guide explains how to deploy Animus Social on Railway using environment variables instead of committing `config.yaml` to git.

## Overview

Since `config.yaml` contains sensitive credentials and is gitignored, we use a **startup script** (`scripts/generate_config.py`) that generates `config.yaml` from Railway environment variables when the application starts.

## Deployment Steps

### 1. Connect Your Repository to Railway

1. Go to [Railway](https://railway.app)
2. Create a new project
3. Connect your GitHub repository
4. Railway will automatically detect it's a Python project

### 2. Configure Environment Variables

In Railway dashboard, go to your project → **Variables** tab and add all required environment variables:

#### Required Variables (Minimum)

```bash
# Letta Configuration
LETTA_API_KEY=sk-let-...
LETTA_AGENT_ID=agent-...
LETTA_BASE_URL=https://your-letta-server.up.railway.app  # Optional, for self-hosted

# X (Twitter) Configuration
X_ENABLED=true
X_API_KEY=your_x_api_key
X_USER_ID=your_user_id
X_CONSUMER_KEY=your_consumer_key
X_CONSUMER_SECRET=your_consumer_secret
X_ACCESS_TOKEN=your_access_token
X_ACCESS_TOKEN_SECRET=your_access_token_secret
X_POLLING_INTERVAL_SEC=60  # Optional: Polling interval in seconds (default: 60)

# Agent Configuration
AGENT_NAME=bianca
AGENT_DISPLAY_NAME=Bianca
AGENT_MODEL=openai/gpt-4o-mini
AGENT_EMBEDDING=openai/text-embedding-3-small
```

#### Optional Variables

```bash
# Agent Personality (can be long strings)
AGENT_CORE_IDENTITY=I am Bianca, an expert on everything Animus...
AGENT_DEVELOPMENT_DIRECTIVE=I must develop my understanding...
AGENT_COMMUNICATION_STYLE=witty, engaging, informative, conversational
AGENT_TONE=friendly, knowledgeable, curious
AGENT_STOP_COMMAND=#biancastop

# Memory Blocks (can be long strings)
MEMORY_ZEITGEIST=I'm learning about the current state of Twitter...
MEMORY_PERSONA=I am Bianca, an expert on everything Animus...
MEMORY_HUMANS=I'm starting to build relationships with Twitter users...
MEMORY_ANIMUS_KNOWLEDGE=I am deeply knowledgeable about Animus...

# Logging
LOG_LEVEL=INFO
```

### 3. Configure Start Command

Railway will automatically use the `Procfile` or `railway.json`. The start command is:

```bash
python scripts/generate_config.py && python platforms/x/orchestrator.py bot
```

This will:
1. Generate `config.yaml` from environment variables
2. Start the X orchestrator bot

### 4. Set Python Version (Optional)

In Railway, you can set the Python version in the **Variables** tab:

```bash
PYTHON_VERSION=3.11
```

Or add a `runtime.txt` file to your repo:

```
python-3.11
```

### 5. Deploy

Railway will automatically:
1. Install dependencies from `requirements.txt`
2. Run `scripts/generate_config.py` to create `config.yaml`
3. Start the bot with `python platforms/x/orchestrator.py bot`

## Environment Variables Reference

### Letta Configuration

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `LETTA_API_KEY` | Yes | Your Letta API key | `sk-let-...` |
| `LETTA_AGENT_ID` | Yes | Your Letta agent ID | `agent-...` |
| `LETTA_BASE_URL` | No | Self-hosted Letta server URL | `https://...` |
| `LETTA_TIMEOUT` | No | API timeout in seconds | `600` |

### X (Twitter) Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `X_ENABLED` | Yes | Set to `true` to enable X platform |
| `X_API_KEY` | Yes | X API Bearer Token |
| `X_USER_ID` | Yes | Your X user ID |
| `X_CONSUMER_KEY` | Yes | OAuth consumer key |
| `X_CONSUMER_SECRET` | Yes | OAuth consumer secret |
| `X_ACCESS_TOKEN` | Yes | OAuth access token |
| `X_ACCESS_TOKEN_SECRET` | Yes | OAuth access token secret |
| `X_POLLING_INTERVAL_SEC` | No | Polling interval in seconds (default: 60) |
| `X_START_FRESH` | No | Set to `true` to ignore all old mentions and only process new ones created after service starts. Uses the most recent mention before startup as a cutoff marker (that mention is NOT processed). **Perfect for new deployments or after API key changes.** |
| `X_SKIP_RECENT_MENTIONS` | No | Number of most recent mentions to skip (default: 0). Useful after rate limit issues to skip old mentions. **Set back to 0 after use.** |
| `CLEAR_X_QUEUE_ON_START` | No | Set to `true` to clear queued mentions on startup (useful after rate limit issues). **Remember to set back to `false` or delete after use.** |

### Agent Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `AGENT_NAME` | No | `bianca` | Agent name (used in memory blocks) |
| `AGENT_DISPLAY_NAME` | No | `Bianca` | Human-readable name |
| `AGENT_DESCRIPTION` | No | Default | Agent description |
| `AGENT_MODEL` | No | `openai/gpt-4o-mini` | LLM model to use |
| `AGENT_EMBEDDING` | No | `openai/text-embedding-3-small` | Embedding model |
| `AGENT_MAX_STEPS` | No | `100` | Maximum agent steps |
| `AGENT_STOP_COMMAND` | No | `#biancastop` | Stop command |
| `AGENT_CORE_IDENTITY` | No | Empty | Agent's core identity prompt |
| `AGENT_DEVELOPMENT_DIRECTIVE` | No | Empty | Agent's development directive |
| `AGENT_COMMUNICATION_STYLE` | No | Default | Communication style |
| `AGENT_TONE` | No | Default | Communication tone |

### Memory Blocks

Memory blocks can be set as environment variables. They support multi-line strings in Railway:

| Variable | Description |
|----------|-------------|
| `MEMORY_ZEITGEIST` | Zeitgeist memory block content |
| `MEMORY_PERSONA` | Persona memory block content |
| `MEMORY_HUMANS` | Humans memory block content |
| `MEMORY_ANIMUS_KNOWLEDGE` | Animus knowledge memory block content |

## Using Railway Secrets

For long values (like system prompts or memory blocks), Railway supports **secrets** which are better for multi-line content:

1. Go to **Variables** → **Raw Editor**
2. Paste your multi-line content
3. Railway will automatically handle it

Or use Railway's **Secrets** feature for sensitive values.

## Testing Locally

You can test the config generation locally:

```bash
# Set environment variables
export LETTA_API_KEY="sk-let-..."
export LETTA_AGENT_ID="agent-..."
export X_ENABLED="true"
export X_API_KEY="..."
# ... etc

# Generate config
python scripts/generate_config.py

# Run the bot
python platforms/x/orchestrator.py bot
```

## Troubleshooting

### Config file not found
- Make sure `scripts/generate_config.py` runs before the bot starts
- Check Railway logs to see if config generation succeeded

### Missing environment variables
- Check Railway logs for warnings about missing variables
- Ensure all required variables are set in Railway dashboard

### Bot not starting
- Check Railway logs for errors
- Verify `PYTHONPATH` is set if needed: `PYTHONPATH=.`
- Ensure all dependencies are in `requirements.txt`

### X API Rate Limit Issues - Starting Fresh

If you've hit X API rate limits, changed API keys, or want to ignore all old mentions:

**The Problem**: After rate limit issues or API key changes, when the orchestrator restarts, it fetches ALL mentions since the last checkpoint and tries to process them all, hitting rate limits again.

**Solution 1: Start Fresh** (Best for New Deployments/Key Changes):

1. Go to **Variables** tab
2. Add: `X_START_FRESH` = `true`
3. Save/Deploy
4. Check logs - you should see: `🆕 Fresh start initialized`
5. **The orchestrator will only process mentions created AFTER the service starts**
6. **You can leave this as `true` permanently** - it only initializes once on first run

**How it works:**
- On startup, fetches the most recent mention that exists (the last mention before startup)
- Uses that mention ID as a cutoff marker (this mention is NOT processed)
- Only processes mentions created AFTER that cutoff ID
- All past mentions (including the cutoff one) are ignored
- Prevents API limit issues from processing backlog

This is perfect when:
- You've created a new service/deployment
- You've changed API keys
- You want to ignore all historical mentions
- You want to prevent API limit issues from old mentions

**Solution 2: Skip Recent Mentions** (For Existing Deployments):

1. Go to **Variables** tab
2. Add: `X_SKIP_RECENT_MENTIONS` = `20` (or however many mentions you want to skip)
3. Save/Deploy
4. Check logs - you should see: `⏭️ Skipping X most recent mentions`
5. **Important**: After the orchestrator runs once, set it back to `0` or delete the variable

This will:
- Skip the most recent N mentions when fetching
- Update `last_seen_id` to include skipped mentions (so they won't be fetched again)
- Only process new mentions going forward

**Alternative: Clear Queue** (if you also have queued files):

1. Set: `CLEAR_X_QUEUE_ON_START` = `true`
2. Save/Deploy
3. Set back to `false` after clearing

See `docs/TROUBLESHOOTING.md` for more details.

## Production Tips

1. **Use Railway Secrets**: For sensitive values, use Railway's secrets feature
2. **Monitor Logs**: Keep an eye on Railway logs for any issues
3. **Set Up Alerts**: Configure Railway alerts for deployment failures
4. **Backup Config**: Keep a backup of your environment variables somewhere safe
5. **Health Checks**: Consider adding a health check endpoint if needed

## Alternative: Use config.yaml Template

If you prefer to commit a template and fill it in Railway:

1. Create `config.yaml.template` (commit this)
2. In Railway, use a startup script to copy and fill it
3. Or use Railway's **File System** to upload `config.yaml` directly

However, using environment variables is more secure and follows Railway best practices.
