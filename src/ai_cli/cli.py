import os
import click
from datetime import datetime
from .chat import ChatManager

def create_new_conversation(model, name=None):
    """Create a new conversation."""
    try:
        chat = ChatManager(model=model)
        
        # Use provided name or generate timestamp
        conv_name = name or datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Initial system message
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant in a CLI interface."}
        ]
        
        # Save initial conversation
        chat.save_conversation(conv_name, messages)
        click.echo(f"New conversation created: {conv_name}")
        # Immediately start the conversation
        continue_conversation(conv_name)
        return conv_name
    
    except ValueError as e:
        click.echo(str(e), err=True)
        return None
    
def show_last_conversation_history(messages, n=10):
    """
    Show the last n messages from the conversation history.
    
    :param messages: List of message dictionaries
    :param n: Number of last messages to display
    :return: None (prints the last messages)
    """
    if not messages:
        click.echo("No conversation history found.")
        return
    
    # Filter out system messages and get the last n messages
    conversation_messages = [msg for msg in messages if msg['role'] != 'system']
    last_messages = conversation_messages[-n:]
    
    click.echo("\n--- Last Conversation History ---")
    for msg in last_messages:
        role = "You" if msg['role'] == 'user' else "AI"
        click.echo(f"{role}: {msg['content']}")
    click.echo("--- End of History ---\n")

def list_conversations():
    """List all saved conversations."""
    chat = ChatManager()
    conversations = chat.list_conversations()
    
    if not conversations:
        click.echo("No conversations found.")
    else:
        click.echo("Saved Conversations:")
        for conv in conversations:
            click.echo(conv)

def continue_conversation(name):
    """Continue a conversation."""
    try:
        chat = ChatManager()
        
        # Load conversation
        messages = chat.load_conversation(name)
        
        if not messages:
            return
        
        # Show last conversation history
        show_last_conversation_history(messages)
        
        click.echo(f"Continuing conversation: {name}")
        click.echo("Type your message. Press Ctrl+D or Ctrl+C to end.")
        
        # Interactive chat loop
        try:
            while True:
                # Get user input
                try:
                    user_input = click.prompt("You: ", prompt_suffix="", default="", show_default=False)
                except (EOFError, KeyboardInterrupt):
                    break
                
                # Add user message
                messages.append({"role": "user", "content": user_input})
                
                # Generate AI response
                ai_response = chat.generate_response(messages)
                
                # Print AI response
                click.echo(f"AI: {ai_response}")
                
                # Add AI response to conversation
                messages.append({"role": "assistant", "content": ai_response})
        
        except KeyboardInterrupt:
            click.echo("\nConversation interrupted.")
        
        finally:
            # Always save the conversation when exiting
            chat.save_conversation(name, messages)
            click.echo(f"Conversation saved: {name}")
    
    except ValueError as e:
        click.echo(str(e), err=True)

def delete_conversation(name):
    """Delete a saved conversation."""
    chat = ChatManager()
    path = chat.get_conversation_path(name)
    
    try:
        os.remove(path)
        click.echo(f"Conversation deleted: {name}")
    except FileNotFoundError:
        click.echo(f"Conversation not found: {name}")
