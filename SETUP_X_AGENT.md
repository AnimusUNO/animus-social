# Building and Running Twitter/X Agents with Animus Social

## Prerequisites

1. **Python 3.8+** installed
2. **Letta Cloud Account** (or self-hosted Letta server)
3. **X (Twitter) Developer Account** with API access
4. **Virtual environment** (recommended)

## Step 1: Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Get X (Twitter) API Credentials

### 2.1 Create X Developer Account
1. Go to https://developer.x.com/en/portal
2. Apply for developer access (if needed)
3. Create a new Project and App

### 2.2 Configure App Permissions
1. Go to your app settings
2. **Enable "Read and write" permissions** (required for posting)
3. **Enable OAuth 1.0a** for User Context
4. Generate the following credentials:
   - API Key (Bearer Token)
   - Consumer Key
   - Consumer Secret
   - Access Token
   - Access Token Secret

### 2.3 Get Your User ID
You can get your X user ID by running:
```bash
python platforms/x/orchestrator.py me
```

This will display your authenticated user info including the correct user ID.

## Step 3: Configure Your Agent

Edit `config.yaml`:

### 3.1 Agent Identity
```yaml
agent:
  name: "my-twitter-agent"  # Unique identifier
  display_name: "My Twitter Agent"  # Human-readable name
  description: "A Twitter agent that [describe what your agent does]"
```

### 3.2 Agent Personality
```yaml
personality:
  core_identity: "I am [Agent Name], a Twitter agent that [describe identity, expertise, interests]"
  development_directive: "I must develop my personality and understanding of Twitter culture."
  communication_style: "witty, engaging, concise"  # Adjust to your preference
  tone: "casual"  # or "professional", "friendly", "humorous"
```

### 3.3 X Platform Configuration
```yaml
platforms:
  x:
    enabled: true  # MUST be true
    api_key: "YOUR_API_KEY"
    consumer_key: "YOUR_CONSUMER_KEY"
    consumer_secret: "YOUR_CONSUMER_SECRET"
    access_token: "YOUR_ACCESS_TOKEN"
    access_token_secret: "YOUR_ACCESS_TOKEN_SECRET"
    user_id: "YOUR_USER_ID"
    
    behavior:
      thread_handling: "conservative"  # or "comprehensive"
      rate_limiting: "strict"
      downrank_response_rate: 0.1  # 10% response rate for bots
```

### 3.4 Letta Configuration
```yaml
letta:
  api_key: "YOUR_LETTA_API_KEY"
  agent_id: "YOUR_LETTA_AGENT_ID"  # Create this in Letta Cloud
  timeout: 600
  # base_url: "http://localhost:8283"  # Only if self-hosting
```

## Step 4: Create Agent in Letta

1. Go to https://app.letta.com
2. Create a new project (or use existing)
3. Create a new agent
4. Copy the agent ID to `config.yaml`
5. Configure the agent:
   - Name: Match your `agent.name` from config
   - Model: Set to your preferred model (default: `openai/gpt-4o-mini`)
   - Embedding: Set to `openai/text-embedding-3-small`

## Step 5: Register X Tools

Register the X-specific tools with your Letta agent:

```bash
# Register all X tools
python scripts/register_x_tools.py

# Or register specific tools
python scripts/register_x_tools.py --tools add_post_to_x_thread post_to_x

# List available tools
python scripts/register_x_tools.py --list
```

**Available X Tools:**
- `add_post_to_x_thread` - Reply to X threads (280 char limit)
- `post_to_x` - Create standalone X posts
- `search_x_posts` - Search X posts by user
- `attach_x_user_blocks` - Attach user memory blocks
- `detach_x_user_blocks` - Detach user memory blocks
- Common tools: `halt_activity`, `ignore_notification`, `fetch_webpage`, etc.

## Step 6: Test Configuration

```bash
# Test X API connection
python platforms/x/orchestrator.py me

# Test Letta integration
python platforms/x/orchestrator.py letta

# Test thread context retrieval
python platforms/x/orchestrator.py thread
```

## Step 7: Run Your Twitter Agent

### Main Bot Loop (Recommended)
```bash
# Production mode (actually posts to Twitter)
python platforms/x/orchestrator.py bot

# Test mode (doesn't post, just processes)
python platforms/x/orchestrator.py bot --test
```

### Separate Queue and Process
```bash
# Step 1: Queue mentions (fetch but don't process)
python platforms/x/orchestrator.py queue

# Step 2: Process queued mentions
python platforms/x/orchestrator.py process

# Or process in test mode
python platforms/x/orchestrator.py process --test
```

## Understanding the Bot Operation

### How It Works:

1. **Polling**: Bot checks for new mentions every 30 seconds (configurable)
2. **Queueing**: New mentions saved to `data/queues/x/` as JSON files
3. **Processing**: 
   - Fetches full thread context (7-day search window)
   - Attaches user memory blocks
   - Sends context to Letta agent
   - Agent decides how to respond (or ignore)
4. **Response**: Posts replies if agent calls `add_post_to_x_thread`
5. **Tracking**: Saves debug data to `data/queues/x/debug/`

### X-Specific Features:

- **Downrank System**: Bot accounts can be added to `config/x_downrank_users.txt` for 10% response rate
- **Thread Context**: Automatically fetches conversation context within 7-day window
- **Rate Limiting**: Built-in handling for X API rate limits (17 posts/day on free tier)
- **Debug Logging**: Comprehensive debug data saved for each conversation

## Monitoring and Debugging

### Check Queue Status
```bash
# View queue statistics
python -c "from utils.queue_manager import get_queue_stats; print(get_queue_stats())"

# List queued mentions
ls data/queues/x/*.json
```

### View Debug Data
Debug data for each conversation is saved to:
```
data/queues/x/debug/conversation_<id>/
├── thread_data_<mention_id>.json      # Raw API response
├── thread_context_<mention_id>.yaml  # Processed context
├── debug_info_<mention_id>.json      # Conversation metadata
└── agent_response_<mention_id>.json  # Full agent interaction
```

### Manage Downrank Users
```bash
# List downranked users (10% response rate)
python platforms/x/orchestrator.py downrank list

# Edit the list
# Edit config/x_downrank_users.txt
```

## Customization Options

### Agent Personality
Modify `config.yaml`:
```yaml
agent:
  personality:
    core_identity: "Your agent's identity"
    communication_style: "witty, engaging"
    tone: "casual"
```

### Response Behavior
```yaml
platforms:
  x:
    behavior:
      thread_handling: "conservative"  # Less aggressive threading
      rate_limiting: "strict"          # Strict rate limit adherence
      downrank_response_rate: 0.1      # 10% response to bots
```

### Memory Management
The agent automatically:
- Creates `x_user_<user_id>` memory blocks for users
- Attaches blocks when processing mentions
- Updates blocks based on interactions
- Periodically cleans up inactive blocks

## Troubleshooting

### Common Issues:

1. **"ModuleNotFoundError: No module named 'platforms'"**
   - Make sure you're running from the `animus-social` directory
   - Or set PYTHONPATH: `export PYTHONPATH=.`

2. **"Authentication failed"**
   - Verify all X API credentials in `config.yaml`
   - Ensure OAuth 1.0a tokens are generated (not just Bearer tokens)
   - Check that app has "Read and write" permissions

3. **"Agent not found"**
   - Verify agent ID in `config.yaml` matches Letta Cloud
   - Check that agent exists in your Letta project

4. **"Rate limit exceeded"**
   - X free tier: 17 posts/day
   - Bot automatically handles rate limits with backoff
   - Consider upgrading X API tier for higher limits

5. **"Tools not registered"**
   - Run: `python scripts/register_x_tools.py`
   - Check: `python scripts/register_x_tools.py --list`
   - Verify tools are attached in Letta Cloud dashboard

## Production Deployment

### Running as a Service

**Linux (systemd):**
```ini
[Unit]
Description=Animus Social X Agent
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/animus-social
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python platforms/x/orchestrator.py bot
Restart=always

[Install]
WantedBy=multi-user.target
```

**Windows (Task Scheduler):**
- Create task to run: `python platforms/x/orchestrator.py bot`
- Set to run at startup
- Configure restart on failure

### Monitoring
- Logs: Check console output and log files
- Queue: Monitor `data/queues/x/` for stuck notifications
- Health: Use `python platforms/x/orchestrator.py me` to test connectivity

## Next Steps

1. **Customize personality** for your use case
2. **Add downrank users** to avoid bot conversations
3. **Monitor debug logs** to understand agent behavior
4. **Adjust response style** via personality configuration
5. **Scale up** by running multiple agents with different personalities

## Example Agent Configurations

### Tech News Bot
```yaml
agent:
  name: "tech-news-bot"
  personality:
    core_identity: "I am a tech news bot that shares and discusses the latest in technology."
    communication_style: "informative, concise, fact-based"
    tone: "professional"
```

### Casual Conversational Bot
```yaml
agent:
  name: "friendly-chatbot"
  personality:
    core_identity: "I am a friendly conversational bot that enjoys chatting about everyday topics."
    communication_style: "casual, friendly, engaging"
    tone: "casual"
```

### Expert Advisor Bot
```yaml
agent:
  name: "expert-advisor"
  personality:
    core_identity: "I am an expert advisor specializing in [your domain]. I provide detailed, analytical insights."
    communication_style: "analytical, information-dense, thorough"
    tone: "professional"
```

Happy building! 🚀

