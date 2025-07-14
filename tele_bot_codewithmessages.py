
# Import necessary modules
from typing import Final  # For type hints
from telegram import Update  # For handling Telegram updates (messages, commands, etc.)
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes  # Telegram bot framework
from response_engine import handle_response  # Custom function to generate responses

import os  # For accessing environment variables
from dotenv import load_dotenv  # For loading variables from .env file

# Load environment variables from .env file (like your bot token and username)
load_dotenv()

# Get the bot token and username from environment variables
TOKEN: Final = os.getenv("TOKEN")
BOT_USERNAME: Final = os.getenv("BOT_USERNAME")


# This function handles the /start command
# It sends a welcome message when a user starts the bot
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am your bot. How can I assist you today?')

# This function handles the /help command
# It sends a list of available commands to the user
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Here are the commands you can use:\n'
                                     '/start - Start the bot\n'
                                     '/help - Get help information\n'
                                     '/about - Learn more about this bot')

# This function handles the /about command
# It tells the user what the bot is for
async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This bot is designed to assist you with various tasks. '
                                     'Feel free to ask me anything!')

# This function handles all text messages sent to the bot
# It checks if the message is in a group and if the bot is mentioned, or if it's a private chat
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type  # 'private' or 'group'
    text: str = update.message.text  # The actual message text

    # Print who sent the message and what it was (for debugging)
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # If the message is in a group
    if message_type == 'group':
        # Only respond if the bot is mentioned in the message
        if BOT_USERNAME in text:
            # Remove the bot's username from the message
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            # Generate a response using the custom response engine
            response: str = handle_response(new_text)
        else:
            # If the bot is not mentioned, do nothing
            return
    else:
        # If it's a private chat, always respond
        response: str = handle_response(text)
    
    # Print the bot's response (for debugging)
    print('bot:', response)
    # Send the response back to the user
    await update.message.reply_text(response)

# This function handles errors that occur in the bot
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update "{update}" caused error "{context.error}"')


# This is the main entry point for the bot
if __name__ == '__main__':
    print('Starting bot...')  # Print a message to show the bot is starting
    app = Application.builder().token(TOKEN).build()  # Create the bot application with your token

    # Add command handlers so the bot knows what to do when a user sends /start, /help, or /about
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('about', about_command))

    # Add a message handler for all text messages (not commands)
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Add an error handler to catch and print errors
    app.add_error_handler(error)

    # Start polling Telegram for new messages (the bot will keep running)
    print('Polling...')
    app.run_polling(poll_interval=3)