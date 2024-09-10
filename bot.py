from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import re

# Function to replace master.mpd URLs in the file
def process_file(file_content, quality="240"):
    pattern = r"https://d1d34p8vz63oiq\.cloudfront\.net/([a-zA-Z0-9-]+)/master\.mpd"
    updated_content = re.sub(pattern, r'ffmpeg -i "https://jarvis-stream.pages.dev/\1/hls/' + quality + '/main.m3u8" -c copy output.mp4', file_content)
    return updated_content

# Start command handler
def start(update, context):
    update.message.reply_text("Send me a txt file 😘,I'm Txt-file-link-changer😉 and I will update them!😇")

# File processing handler
def handle_file(update, context):
    # Get the file sent by the user
    file = update.message.document.get_file()
    file_content = file.download_as_bytearray().decode('utf-8')

    # Process the file and update URLs
    updated_content = process_file(file_content, "480")  # Use 240 quality as per your requirement

    # Save the updated content to a new file
    with open("updated_file.txt", "w") as f:
        f.write(updated_content)

    # Send the updated file back to the user
    update.message.reply_document(document=open("updated_file.txt", "rb"))
    update.message.reply_text("Here is your updated file!")

# Error handler
def error(update, context):
    print(f"Update {update} caused error {context.error}")

# Main function to setup the bot
def main():
    TOKEN = '6748460867:AAFzQkFcCfg1kqISiV4499pGxIcPtu4qe1w'  # Replace with your bot token

    # Initialize the Updater and Dispatcher
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command handler for /start
    dp.add_handler(CommandHandler("start", start))

    # File handler for processing uploaded text files
    dp.add_handler(MessageHandler(Filters.document.mime_type("text/plain"), handle_file))

    # Error handler
    dp.add_error_handler(error)

    # Start polling for updates from Telegram
    updater.start_polling()

    # Run the bot until stopped
    updater.idle()

if __name__ == '__main__':
    main()
