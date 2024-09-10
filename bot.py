from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler
from telegram.ext.filters import TEXT, Document
import re

# Function to replace master.mpd URLs in the file
def process_file(file_content, quality="240"):
    pattern = r"https://d1d34p8vz63oiq\.cloudfront\.net/([a-zA-Z0-9-]+)/master\.mpd"
    updated_content = re.sub(pattern, r'ffmpeg -i "https://jarvis-stream.pages.dev/\1/hls/' + quality + '/main.m3u8" -c copy output.mp4', file_content)
    return updated_content

# Start command handler
async def start(update: Update, context):
    await update.message.reply_text("Send me a txt file 😘,I'm Txt-file-link-changer😉 and I will update them!😇")

# File processing handler
async def handle_file(update: Update, context):
    file = await update.message.document.get_file()
    file_content = await file.download_as_bytearray()

    # Process the file and update URLs
    updated_content = process_file(file_content.decode('utf-8'), "240")

    # Save the updated content to a new file
    with open("updated_file.txt", "w") as f:
        f.write(updated_content)

    # Send the updated file back to the user
    await update.message.reply_document(document=open("updated_file.txt", "rb"))
    await update.message.reply_text("Here is your updated file!")

# Main function to setup the bot
async def main():
    TOKEN = '6748460867:AAFzQkFcCfg1kqISiV4499pGxIcPtu4qe1w'

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(Document.MIME_TYPE("text/plain"), handle_file))

    await application.start()
    await application.idle()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())