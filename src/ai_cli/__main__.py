# src/ai_cli/__main__.py
import click
from .cli import (
    create_new_conversation, 
    list_conversations, 
    continue_conversation, 
    delete_conversation
)

@click.group()
def main():
    """Warroom: Your terminal-based AI assistant."""
    pass

@main.command()
@click.option('--model', default='gpt-3.5-turbo', help='OpenAI model to use')
@click.option('--name', help='Conversation name (default: timestamp)')
def new(model, name):
    """Start a new conversation."""
    create_new_conversation(model, name)

@main.command()
def list():
    """List all saved conversations."""
    list_conversations()

@main.command()
@click.argument('name')
def chat(name):
    """Continue a conversation."""
    continue_conversation(name)

@main.command()
@click.argument('name')
def delete(name):
    """Delete a saved conversation."""
    delete_conversation(name)

if __name__ == "__main__":
    main()