#!/usr/bin/env python3
"""
Clear X mention queue files to start fresh.

This script is useful when:
- You've hit X API rate limits and accumulated many queued mentions
- The orchestrator keeps trying to process old queued mentions on restart
- You want to start fresh without recreating the entire service

Usage:
    # Clear queue files (keeps processed_mentions.json - recommended)
    python scripts/clear_x_queue.py
    
    # Archive files instead of deleting
    python scripts/clear_x_queue.py --archive
    
    # Also clear processed_mentions.json (not recommended - may reprocess old mentions)
    python scripts/clear_x_queue.py --clear-processed

Alternative (if you have Railway console access):
    In Railway, set environment variable: CLEAR_X_QUEUE_ON_START=true
    This will automatically clear the queue on orchestrator startup.
    Remember to set it back to false after clearing!
"""
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from platforms.x.orchestrator import X_QUEUE_DIR, X_PROCESSED_MENTIONS_FILE
import json

def clear_x_queue(keep_processed=True, archive=False):
    """
    Clear X mention queue files.
    
    Args:
        keep_processed: If True, keep processed_mentions.json (recommended)
        archive: If True, move files to archive directory instead of deleting
    """
    print(f"📁 Queue directory: {X_QUEUE_DIR}")
    
    # Ensure queue directory exists
    X_QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Find all queue files
    queue_files = list(X_QUEUE_DIR.glob("x_mention_*.json"))
    
    if not queue_files:
        print("✅ No queue files found. Queue is already empty.")
        return
    
    print(f"📋 Found {len(queue_files)} queue files")
    
    if archive:
        # Create archive directory
        archive_dir = X_QUEUE_DIR / "archive"
        archive_dir.mkdir(exist_ok=True)
        print(f"📦 Archiving to: {archive_dir}")
        
        for queue_file in queue_files:
            archive_path = archive_dir / queue_file.name
            queue_file.rename(archive_path)
            print(f"   Moved: {queue_file.name} -> archive/")
    else:
        # Delete queue files
        for queue_file in queue_files:
            queue_file.unlink()
            print(f"   Deleted: {queue_file.name}")
    
    print(f"\n✅ Cleared {len(queue_files)} queue files")
    
    # Optionally clear processed mentions (not recommended)
    if not keep_processed and X_PROCESSED_MENTIONS_FILE.exists():
        backup_file = X_PROCESSED_MENTIONS_FILE.parent / "processed_mentions.json.backup"
        X_PROCESSED_MENTIONS_FILE.rename(backup_file)
        print(f"📦 Backed up processed_mentions.json to processed_mentions.json.backup")
        print("⚠️  Note: This means old mentions may be processed again if they're fetched")
    elif keep_processed:
        # Load and show stats
        if X_PROCESSED_MENTIONS_FILE.exists():
            try:
                with open(X_PROCESSED_MENTIONS_FILE, 'r') as f:
                    processed = json.load(f)
                print(f"📊 Kept processed_mentions.json with {len(processed)} processed mention IDs")
            except:
                print("📊 Kept processed_mentions.json")
    
    print("\n✅ Queue cleared! The orchestrator will start fresh on next run.")
    print("   Note: Old mentions are still marked as processed (won't be reprocessed)")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Clear X mention queue files")
    parser.add_argument(
        "--clear-processed",
        action="store_true",
        help="Also clear processed_mentions.json (not recommended - may reprocess old mentions)"
    )
    parser.add_argument(
        "--archive",
        action="store_true",
        help="Move files to archive directory instead of deleting"
    )
    
    args = parser.parse_args()
    
    clear_x_queue(keep_processed=not args.clear_processed, archive=args.archive)

