from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import database as db
import gemini_service as gemini
import web_search
from config import TELEGRAM_TOKEN
from analytics_service import get_analytics_data
from PIL import Image
import io
from telegram.request import HTTPXRequest

# Set bot with increased timeout
request = HTTPXRequest(connect_timeout=30, read_timeout=60)
bot = Bot(token=TELEGRAM_TOKEN, request=request)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command and asks users for their phone number."""
    user_data = {
        'chat_id': update.effective_chat.id,
        'first_name': update.effective_user.first_name,
        'username': update.effective_user.username
    }
    await db.save_user(user_data)

    # Request phone number
    button = KeyboardButton("📞 Share Contact", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[button]], resize_keyboard=True)

    await update.message.reply_text(
        "👋 Welcome! Please share your contact number to complete registration.",
        reply_markup=reply_markup
    )

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles user contact sharing."""
    phone = update.message.contact.phone_number
    await db.save_user({
        'chat_id': update.effective_chat.id,
        'phone': phone
    })
    await update.message.reply_text("✅ Registration complete! You can now start chatting.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles user text messages and sends responses from Gemini AI."""
    user_input = update.message.text
    chat_id = update.effective_chat.id

    try:
        response = await gemini.get_chat_response(user_input)
        await db.save_chat_history(chat_id, user_input, response)
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text("⚠️ Error processing your request. Please try again later.")
        print(f"Error in handle_message: {e}")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles image/document uploads and performs AI-based analysis."""
    try:
        if update.message.photo:
            file = await update.message.photo[-1].get_file()
        elif update.message.document:
            file = await update.message.document.get_file()
        else:
            await update.message.reply_text("⚠️ Unsupported file type. Please upload an image or document.")
            return

        file_data = await file.download_as_bytearray()

        image_prompt = """
        Analyze this image carefully. Describe only what is clearly visible. Avoid guessing details.
        Focus on:
        - Objects
        - Text (if any)
        - Colors and patterns
        - Any obvious context
        Do NOT assume hidden meanings or relationships.
        """

        # Convert image to standard format
        image = Image.open(io.BytesIO(file_data)).convert("RGB")
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')  # Convert to JPEG
        processed_file_data = img_byte_arr.getvalue()

        # Analyze image
        analysis = await gemini.analyze_image(processed_file_data, prompt=image_prompt)

        # Save metadata
        await db.save_file_metadata(update.effective_chat.id, {
            'file_name': file.file_id,
            'description': analysis
        })

        # Confidence-based response
        confidence = analysis.get('confidence', 1.0)  # Default confidence 1.0 if not provided
        if confidence < 0.7:
            await update.message.reply_text("🔍 Sorry, I'm not confident in my analysis. Try another image.")
        else:
            await update.message.reply_text(f"🖼️ **Image Analysis:** {analysis['description']}")

    except Exception as e:
        await update.message.reply_text("⚠️ Error processing the image. Please try again.")
        print(f"Error in handle_file: {e}")

async def web_search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /websearch command and asks for a query."""
    await update.message.reply_text("🔎 Please enter your search query:")
    context.user_data['expecting_search'] = True

async def handle_search_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles user-provided search queries and fetches web results."""
    try:
        if context.user_data.get('expecting_search'):
            query = update.message.text
            search_results = await web_search.search_web(query)

            response = f"📝 **Summary:** {search_results['summary']}\n\n🔗 **Top results:**\n"
            for result in search_results['results']:
                response += f"\n• [{result['title']}]({result['link']})"

            await update.message.reply_text(response, parse_mode="Markdown")
            context.user_data['expecting_search'] = False
        else:
            await handle_message(update, context)
    except Exception as e:
        await update.message.reply_text("⚠️ Error fetching search results. Please try again.")
        print(f"Error in handle_search_query: {e}")

async def dashboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /dashboard command to display bot analytics."""
    admin_username = "YOUR_ADMIN_USERNAME"  # Replace with actual admin username
    if update.effective_user.username == admin_username:
        try:
            analytics_data = await get_analytics_data()
            dashboard_url = "http://localhost:5173"  # Replace with actual dashboard URL

            await update.message.reply_text(
                f"📊 **Analytics Dashboard:** [View Here]({dashboard_url})\n\n"
                f"📌 **Stats:**\n"
                f"👥 Total Users: {analytics_data['total_users']}\n"
                f"💬 Total Messages: {analytics_data['total_messages']}",
                parse_mode="Markdown"
            )
        except Exception as e:
            await update.message.reply_text("⚠️ Error fetching analytics data.")
            print(f"Error in dashboard_command: {e}")
    else:
        await update.message.reply_text("⛔ Sorry, this command is for administrators only.")

def main():
    """Initializes and starts the Telegram bot."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("dashboard", dashboard_command))
    application.add_handler(CommandHandler("websearch", web_search_command))

    # Message Handlers
    application.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    application.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, handle_file))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search_query))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
