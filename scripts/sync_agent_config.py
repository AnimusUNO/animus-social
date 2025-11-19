#!/usr/bin/env python3
"""
Sync agent configuration from config.yaml to Letta agent.
This updates:
- Agent description
- System prompt (instructions) from core_identity and development_directive
- Memory blocks (persona, zeitgeist, humans, custom blocks)
"""
import logging
from pathlib import Path
from letta_client import Letta
from core.config import get_config, get_letta_config, get_memory_blocks_config
from utils.utils import upsert_block
from rich.console import Console
from rich.table import Table

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
console = Console()

def sync_agent_config():
    """Sync agent configuration from config.yaml to Letta."""
    try:
        # Load configuration
        config = get_config()
        letta_config = get_letta_config()
        
        # Initialize Letta client
        client_params = {
            'token': letta_config['api_key'],
            'timeout': letta_config['timeout']
        }
        if letta_config.get('base_url'):
            client_params['base_url'] = letta_config['base_url']
        client = Letta(**client_params)
        
        agent_id = letta_config['agent_id']
        
        # Get agent
        try:
            agent = client.agents.retrieve(agent_id=agent_id)
            console.print(f"[green]✓[/green] Found agent: {agent.name} ({agent_id})")
        except Exception as e:
            console.print(f"[red]✗[/red] Failed to retrieve agent: {e}")
            return
        
        # Get agent config from config.yaml
        agent_name = config.get_agent_name()
        agent_display_name = config.get('agent.display_name', agent_name)
        agent_description = config.get('agent.description', '')
        
        # Build system prompt from personality
        personality = config.get('agent.personality', {})
        core_identity = personality.get('core_identity', '')
        development_directive = personality.get('development_directive', '')
        communication_style = personality.get('communication_style', '')
        tone = personality.get('tone', '')
        
        system_prompt = f"""{core_identity}

{development_directive}

Communication style: {communication_style}
Tone: {tone}"""
        
        # Update agent description
        console.print("\n[bold]Updating agent settings...[/bold]")
        try:
            client.agents.modify(
                agent_id=agent_id,
                description=agent_description
            )
            console.print(f"[green]✓[/green] Updated agent description")
            console.print(f"[yellow]⚠[/yellow] System prompt (instructions) cannot be updated via API")
            console.print(f"  Please update manually in Letta dashboard with this content:")
            console.print(f"  [dim]{system_prompt[:200]}...[/dim]")
        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] Could not update agent description: {e}")
            console.print("  (You may need to update this manually in Letta dashboard)")
        
        # Get and sync memory blocks
        console.print("\n[bold]Syncing memory blocks...[/bold]")
        memory_blocks_config = get_memory_blocks_config(config._config)
        
        table = Table(title="Memory Blocks Sync")
        table.add_column("Block", style="cyan")
        table.add_column("Label", style="dim")
        table.add_column("Status", style="green")
        
        # Get current blocks
        current_blocks = client.agents.blocks.list(agent_id=agent_id)
        current_block_labels = {block.label: block for block in current_blocks}
        
        # Sync each memory block
        for block_name, block_config in memory_blocks_config.items():
            label = block_config.get('label', f"{agent_name}-{block_name}")
            value = block_config.get('value', '')
            description = block_config.get('description', '')
            
            try:
                # Check if block exists
                existing_block = None
                if label in current_block_labels:
                    existing_block = current_block_labels[label]
                
                # Create or update block
                if existing_block:
                    # Update existing block
                    client.blocks.modify(
                        block_id=str(existing_block.id),
                        value=value
                    )
                    status = "Updated"
                else:
                    # Create new block
                    block = client.blocks.create(
                        label=label,
                        value=value,
                        limit=5000
                    )
                    
                    # Attach to agent if not already attached
                    if label not in current_block_labels:
                        client.agents.blocks.attach(
                            agent_id=agent_id,
                            block_id=str(block.id)
                        )
                    status = "Created & Attached"
                
                table.add_row(block_name, label, status)
                
            except Exception as e:
                table.add_row(block_name, label, f"[red]Error: {str(e)[:50]}[/red]")
                logger.error(f"Error syncing block {block_name}: {e}")
        
        console.print(table)
        console.print("\n[green]✓[/green] Configuration sync complete!")
        
    except Exception as e:
        console.print(f"[red]✗[/red] Fatal error: {e}")
        logger.error(f"Fatal error syncing config: {e}")
        raise

if __name__ == "__main__":
    sync_agent_config()

