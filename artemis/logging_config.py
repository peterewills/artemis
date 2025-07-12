import json
import logging
import os
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    
    def format(self, record):
        """Format log record as JSON."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage()
        }
        
        # Add any extra fields from the record
        if hasattr(record, 'conversation_data'):
            log_entry.update(record.conversation_data)
            
        return json.dumps(log_entry, ensure_ascii=False)


class ConversationLogger:
    """Structured JSON logger for conversations and tool usage."""
    
    def __init__(self, log_dir: str = "logs"):
        """Initialize conversation logger."""
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        # Set up conversation log file (daily rotation)
        today = datetime.now().strftime("%Y-%m-%d")
        self.conversation_log_file = os.path.join(log_dir, f"conversations_{today}.jsonl")
        
        # Set up conversation logger
        self.conversation_logger = logging.getLogger("conversation")
        self.conversation_logger.setLevel(logging.INFO)
        
        # Remove existing handlers to avoid duplicates
        for handler in self.conversation_logger.handlers[:]:
            self.conversation_logger.removeHandler(handler)
        
        # Create file handler with JSON formatter
        handler = logging.FileHandler(self.conversation_log_file, encoding='utf-8')
        handler.setFormatter(JSONFormatter())
        self.conversation_logger.addHandler(handler)
        
        # Don't propagate to root logger
        self.conversation_logger.propagate = False
    
    def log_conversation(self, user_message: str, assistant_response: str, 
                        metadata: Dict[str, Any] = None):
        """Log a complete conversation turn."""
        conversation_id = str(uuid.uuid4())
        metadata = metadata or {}
        
        log_data = {
            "event_type": "conversation",
            "conversation_id": conversation_id,
            "user_message": user_message,
            "assistant_response": assistant_response,
            "response_length": len(assistant_response),
            "user_message_length": len(user_message),
            **metadata
        }
        
        # Create a log record with the conversation data
        record = self.conversation_logger.makeRecord(
            self.conversation_logger.name,
            logging.INFO,
            __file__,
            0,
            "Conversation logged",
            (),
            None
        )
        record.conversation_data = log_data
        self.conversation_logger.handle(record)
        
        return conversation_id
    
    def log_user_message(self, message: str, metadata: Dict[str, Any] = None):
        """Log just a user message (for streaming scenarios)."""
        conversation_id = str(uuid.uuid4())
        metadata = metadata or {}
        
        log_data = {
            "event_type": "user_message",
            "conversation_id": conversation_id,
            "user_message": message,
            "user_message_length": len(message),
            **metadata
        }
        
        record = self.conversation_logger.makeRecord(
            self.conversation_logger.name,
            logging.INFO,
            __file__,
            0,
            "User message logged",
            (),
            None
        )
        record.conversation_data = log_data
        self.conversation_logger.handle(record)
        
        return conversation_id
    
    def log_assistant_response(self, response: str, conversation_id: str = None, 
                             metadata: Dict[str, Any] = None):
        """Log just an assistant response (for streaming scenarios)."""
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
        metadata = metadata or {}
        
        log_data = {
            "event_type": "assistant_response",
            "conversation_id": conversation_id,
            "assistant_response": response,
            "response_length": len(response),
            **metadata
        }
        
        record = self.conversation_logger.makeRecord(
            self.conversation_logger.name,
            logging.INFO,
            __file__,
            0,
            "Assistant response logged",
            (),
            None
        )
        record.conversation_data = log_data
        self.conversation_logger.handle(record)
    
    def log_tool_usage(self, tool_name: str, tool_input: Dict[str, Any], 
                      tool_output: Any, conversation_id: str = None,
                      metadata: Dict[str, Any] = None):
        """Log tool usage for future extensibility."""
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
        metadata = metadata or {}
        
        log_data = {
            "event_type": "tool_usage",
            "conversation_id": conversation_id,
            "tool_name": tool_name,
            "tool_input": tool_input,
            "tool_output": str(tool_output)[:1000],  # Truncate long outputs
            "tool_output_length": len(str(tool_output)),
            **metadata
        }
        
        record = self.conversation_logger.makeRecord(
            self.conversation_logger.name,
            logging.INFO,
            __file__,
            0,
            "Tool usage logged",
            (),
            None
        )
        record.conversation_data = log_data
        self.conversation_logger.handle(record)
    
    def log_error(self, error: Exception, context: str = "", 
                 conversation_id: str = None, metadata: Dict[str, Any] = None):
        """Log errors with context."""
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
        metadata = metadata or {}
        
        log_data = {
            "event_type": "error",
            "conversation_id": conversation_id,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context,
            **metadata
        }
        
        record = self.conversation_logger.makeRecord(
            self.conversation_logger.name,
            logging.ERROR,
            __file__,
            0,
            "Error logged",
            (),
            None
        )
        record.conversation_data = log_data
        self.conversation_logger.handle(record)


# Global instance
conversation_logger = ConversationLogger()