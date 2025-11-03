#!/usr/bin/env python3
"""Get the system prompt from config.yaml for manual copy to Letta."""
from core.config import get_config

config = get_config()
personality = config.get('agent.personality', {})

system_prompt = f"""{personality.get('core_identity', '')}

{personality.get('development_directive', '')}

Communication style: {personality.get('communication_style', '')}
Tone: {personality.get('tone', '')}"""

print("\n" + "="*70)
print("BIANCA'S SYSTEM PROMPT - Copy this to Letta Agent Instructions:")
print("="*70)
print(system_prompt)
print("="*70 + "\n")

# Also save to file
with open('BIANCA_SYSTEM_PROMPT.txt', 'w', encoding='utf-8') as f:
    f.write(system_prompt)
print("✓ Saved to BIANCA_SYSTEM_PROMPT.txt\n")

