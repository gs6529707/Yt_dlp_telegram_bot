import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi! Send me a YouTube video link, and I'll download it for you.")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text

    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("Please send a valid YouTube link.")
        return

    await update.message.reply_text("Downloading the video. Please wait...")

    # Define the download options
    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save videos to the downloads folder
        'format': 'bestvideo+bestaudio/best',     # Best quality
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        # Send the video to the user
        with open(file_path, 'rb') as video:
            await update.message.reply_video(video)

        # Clean up the downloaded file
        os.remove(file_path)

    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

def main():
    # Replace 'YOUR_BOT_TOKEN' with the token you got from BotFather
    TOKEN = "7706041024:AAEblL50100Fiw1aOYq74Tr5wqiUpJYL1yQ"

    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Register the command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    # Ensure the downloads directory exists
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    main()
