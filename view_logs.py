#!/usr/bin/env python3
"""
Simple log viewer for Artemis conversation logs.
"""
import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Any


def load_logs(log_file: str) -> List[Dict[str, Any]]:
    """Load logs from JSONL file."""
    logs = []
    if not os.path.exists(log_file):
        print(f"Log file not found: {log_file}")
        return logs

    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    logs.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Error parsing log line: {e}")
                    continue
    return logs


def format_timestamp(iso_timestamp: str) -> str:
    """Format ISO timestamp for display."""
    try:
        dt = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return iso_timestamp


def display_conversation(log_entry: Dict[str, Any]):
    """Display a conversation entry nicely."""
    timestamp = format_timestamp(log_entry.get("timestamp", ""))
    conv_id = log_entry.get("conversation_id", "unknown")[:8]  # Short ID

    if log_entry.get("event_type") == "conversation":
        print(f"\n🔹 [{timestamp}] Conversation {conv_id}")
        print(
            f"   Stream: {log_entry.get('stream', False)} | Endpoint: {log_entry.get('endpoint', 'unknown')}"
        )
        print(f"👤 User: {log_entry.get('user_message', '')}")
        print(
            f"🤖 Assistant: {log_entry.get('assistant_response', '')[:200]}{'...' if len(log_entry.get('assistant_response', '')) > 200 else ''}"
        )
        print(
            f"   Lengths: User={log_entry.get('user_message_length', 0)} | Assistant={log_entry.get('response_length', 0)}"
        )

    elif log_entry.get("event_type") == "user_message":
        print(f"\n🔸 [{timestamp}] User Message {conv_id}")
        print(
            f"   Stream: {log_entry.get('stream', False)} | Endpoint: {log_entry.get('endpoint', 'unknown')}"
        )
        print(f"👤 User: {log_entry.get('user_message', '')}")

    elif log_entry.get("event_type") == "assistant_response":
        print(f"\n🔸 [{timestamp}] Assistant Response {conv_id}")
        chunks = log_entry.get("chunks_count", "unknown")
        print(f"   Stream: {log_entry.get('stream', False)} | Chunks: {chunks}")
        print(
            f"🤖 Assistant: {log_entry.get('assistant_response', '')[:200]}{'...' if len(log_entry.get('assistant_response', '')) > 200 else ''}"
        )

    elif log_entry.get("event_type") == "tool_usage":
        print(f"\n🔧 [{timestamp}] Tool Usage {conv_id}")
        print(f"   Tool: {log_entry.get('tool_name', 'unknown')}")
        print(
            f"   Input: {str(log_entry.get('tool_input', ''))[:100]}{'...' if len(str(log_entry.get('tool_input', ''))) > 100 else ''}"
        )
        print(
            f"   Output: {log_entry.get('tool_output', '')[:100]}{'...' if len(log_entry.get('tool_output', '')) > 100 else ''}"
        )

    elif log_entry.get("event_type") == "error":
        print(f"\n❌ [{timestamp}] Error {conv_id}")
        print(f"   Type: {log_entry.get('error_type', 'unknown')}")
        print(f"   Message: {log_entry.get('error_message', '')}")
        print(f"   Context: {log_entry.get('context', '')}")


def main():
    """Main function."""
    if len(sys.argv) > 1:
        log_file = sys.argv[1]
    else:
        # Default to today's log
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = f"logs/conversations_{today}.jsonl"

    print(f"📋 Viewing logs from: {log_file}")
    print("=" * 80)

    logs = load_logs(log_file)
    if not logs:
        print("No logs found.")
        return

    # Sort by timestamp
    logs.sort(key=lambda x: x.get("timestamp", ""))

    # Display logs
    for log_entry in logs:
        display_conversation(log_entry)

    print(f"\n📊 Total entries: {len(logs)}")

    # Summary stats
    event_types = {}
    for log in logs:
        event_type = log.get("event_type", "unknown")
        event_types[event_type] = event_types.get(event_type, 0) + 1

    print("📈 Event types:")
    for event_type, count in event_types.items():
        print(f"   {event_type}: {count}")


if __name__ == "__main__":
    main()
