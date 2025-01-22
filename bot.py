import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi! Send me a YouTube video link, and I'll download the audio for you.")

async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text

    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("Please send a valid YouTube link.")
        return

    message = await update.message.reply_text("Starting the download...")

    # Function to handle progress updates
    def progress_hook(d):
        if d['status'] == 'downloading':
            percentage = d.get('progress_percent', 0)
            text = f"Downloading: {percentage:.2f}%"
            context.bot.loop.create_task(message.edit_text(text))
        elif d['status'] == 'finished':
            context.bot.loop.create_task(message.edit_text("Download complete! Sending the audio..."))

    # Define the download options for audio-only
    ydl_opts = {
        'outtmpl': '/tmp/%(title)s.%(ext)s',  # Save audio to a temporary directory
        'format': 'bestaudio/best',           # Download the best available audio
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',     # Extract audio using FFmpeg
            'preferredcodec': 'mp3',         # Convert to MP3 format
            'preferredquality': '192',       # Set audio quality (192kbps)
        }],
        'progress_hooks': [progress_hook],    # Hook for progress updates
        'ffmpeg_location': './ffmpeg',       # Path to the local ffmpeg binary
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info).replace('.webm', '.mp3')  # Ensure correct extension

        # Send the audio to the user
        with open(file_path, 'rb') as audio:
            await update.message.reply_audio(audio)

        # Clean up the downloaded file
        os.remove(file_path)

    except Exception as e:
        await message.edit_text(f"An error occurred: {str(e)}")

def main():
    # Get the bot token from environment variables
    TOKEN = os.getenv("BOT_TOKEN")

    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Register the command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_audio))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
