from config import TG_BOT_API_KEY
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from utils import load_massage_for_bot

def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Закінчити", callback_data="start")],
        [InlineKeyboardButton("Хочу ще факт", callback_data="random")],
        [InlineKeyboardButton("Запит до gpt", callback_data="gpt")],
        [InlineKeyboardButton("Діалог з відомою особистістю", callback_data="talk")],
        [InlineKeyboardButton("Квіз", callback_data="quiz")],
        [InlineKeyboardButton("Перекладач", callback_data="translate")]
    ])
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = load_massage_for_bot('main')
    target = update.callback_query.message if update.callback_query else update.message
    await target.reply_text(text, reply_markup=main_keyboard())


async def random_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = load_massage_for_bot('random')
    target = update.callback_query.message if update.callback_query else update.message
    await target.reply_text(text, reply_markup=main_keyboard())


async def gpt_request(update, context):
    target = update.callback_query.message if update.callback_query else update.message
    await target.reply_text("gpt")

async def talk_request(update, context):
    target = update.callback_query.message if update.callback_query else update.message
    await target.reply_text("talk")

async def quiz_request(update, context):
    target = update.callback_query.message if update.callback_query else update.message
    await target.reply_text("quiz")

async def translate_request(update, context):
    target = update.callback_query.message if update.callback_query else update.message
    await target.reply_text("translate")




async  def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "start":
        await start(update,context)
    elif query.data == "random":
        await random_fact(update,context)
    elif query.data == "gpt":
        await gpt_request(update,context)
    elif query.data == "talk":
        await talk_request(update,context)
    elif query.data == "quiz":
        await quiz_request(update,context)
    elif query.data == "translate":
        await translate_request(update,context)



app = ApplicationBuilder().token(TG_BOT_API_KEY).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.run_polling()