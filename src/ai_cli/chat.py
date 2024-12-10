import os
import json
from datetime import datetime
from typing import List, Dict

from openai import OpenAI
import tiktoken
from rich.console import Console

class ChatManager:
    """Manages AI conversations with persistent storage."""
    
    def __init__(self, api_key=None, model="gpt-3.5-turbo"):
        """
        Initialize ChatManager with OpenAI client and conversation management.
        
        :param api_key: OpenAI API key
        :param model: OpenAI model to use
        """
        # Determine API key
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("No OpenAI API key found. Set OPENAI_API_KEY environment variable.")
        
        # Initialize clients and configuration
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.console = Console()
        self.tokenizer = tiktoken.encoding_for_model(model)
        
        # Conversation storage
        self.conversations_dir = os.path.expanduser("~/.ai_cli/conversations")
        os.makedirs(self.conversations_dir, exist_ok=True)
    
    def get_conversation_path(self, name: str) -> str:
        """Get full path for a conversation file."""
        return os.path.join(self.conversations_dir, f"{name}.json")
    
    def list_conversations(self) -> List[str]:
        """List all saved conversations."""
        return [
            os.path.splitext(f)[0] 
            for f in os.listdir(self.conversations_dir) 
            if f.endswith('.json')
        ]
    
    def save_conversation(self, name: str, messages: List[Dict]) -> None:
        """Save conversation to a JSON file."""
        path = self.get_conversation_path(name)
        with open(path, 'w') as f:
            json.dump(messages, f, indent=2)
        self.console.print(f"Conversation saved: [bold green]{name}[/]")
    
    def load_conversation(self, name: str) -> List[Dict]:
        """Load conversation from a JSON file."""
        path = self.get_conversation_path(name)
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.console.print(f"[bold red]Conversation not found: {name}[/]")
            return []
    
    def truncate_context(self, messages: List[Dict], max_tokens: int = 3000) -> List[Dict]:
        """Truncate conversation history to stay within token limits."""
        while self._get_token_count(messages) > max_tokens:
            if len(messages) > 1:
                messages.pop(1)  # Remove oldest message, keep system message
            else:
                break
        return messages
    
    def _get_token_count(self, messages: List[Dict]) -> int:
        """Calculate token count for messages."""
        return len(self.tokenizer.encode(json.dumps(messages)))
    
    def generate_response(self, messages: List[Dict]) -> str:
        """Generate AI response using OpenAI API."""
        try:
            # Truncate messages
            truncated_messages = self.truncate_context(messages.copy())
            
            # Generate response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=truncated_messages,
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error generating response: {str(e)}"
