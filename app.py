# Import Telegram bot classes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

# Import bot builder and handlers
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Import your config values (token + admin chat ID)
from config import BOT_TOKEN, ADMIN_CHAT_ID

# Import LLM function to generate response (AI reply)
from llm import generate_llm_response

# Import review storage functions
from review import store_review, get_review, clear_review


# This function handles incoming user messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    user_msg = update.message.text        # Get text sent by user
    user_id = update.message.chat_id      # Get user chat ID

    draft = generate_llm_response(user_msg)  # Generate AI response (draft)

    # Store original message + AI draft for admin review
    store_review(user_id, user_msg, draft)

    # Create inline buttons for admin (Approve / Reject)
    keyboard = [[
        InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user_id}"),
        InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user_id}")
    ]]

    # Send message to admin with buttons
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"Message: {user_msg}\n\nDraft: {draft}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    # Notify user that their message is under review
    await update.message.reply_text("Sent for review")


# This function handles button clicks (Approve / Reject)
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    query = update.callback_query   # Get button click data
    await query.answer()            # Acknowledge button click

    # Extract action and user_id from callback_data
    action, user_id = query.data.split("_")
    user_id = int(user_id)

    # Retrieve stored review data
    data = get_review(user_id)

    # If no data found (edge case)
    if not data:
        await query.edit_message_text("No data found")
        return

    # If admin approves
    if action == "approve":
        # Send AI draft to the original user
        await context.bot.send_message(chat_id=user_id, text=data["draft"])

        clear_review(user_id)  # Remove stored data

        await query.edit_message_text("Approved & sent")

    else:
        # If rejected
        clear_review(user_id)

        await query.edit_message_text("Rejected")


# Build the Telegram bot app using token
app = ApplicationBuilder().token(BOT_TOKEN).build()


# Add handler for text messages (ignore commands like /start)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Add handler for button clicks
app.add_handler(CallbackQueryHandler(handle_buttons))


# Print log when bot starts
print("🚀 AgentTelg Running...")


# Start polling (bot listens continuously)
app.run_polling()