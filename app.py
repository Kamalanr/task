from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from config import BOT_TOKEN, ADMIN_CHAT_ID
from llm import generate_llm_response
from review import store_review, get_review, clear_review

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    user_id = update.message.chat_id

    draft = generate_llm_response(user_msg)
    store_review(user_id, user_msg, draft)

    keyboard = [[
        InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user_id}"),
        InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user_id}")
    ]]

    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"Message: {user_msg}\n\nDraft: {draft}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    await update.message.reply_text("Sent for review")

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, user_id = query.data.split("_")
    user_id = int(user_id)

    data = get_review(user_id)

    if not data:
        await query.edit_message_text("No data found")
        return

    if action == "approve":
        await context.bot.send_message(chat_id=user_id, text=data["draft"])
        clear_review(user_id)
        await query.edit_message_text("Approved & sent")
    else:
        clear_review(user_id)
        await query.edit_message_text("Rejected")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(CallbackQueryHandler(handle_buttons))

print("🚀 AgentTelg Running...")
app.run_polling()