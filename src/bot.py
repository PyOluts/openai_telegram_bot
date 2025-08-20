import random
import os
from config import TG_BOT_API_KEY
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from utils import load_massage_for_bot
from pathlib import Path
PATH_TO_RESOURCES = Path(__file__).parent / "resources"
from open_ai_client import client
from keyboards import main_keyboard

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = load_massage_for_bot('main')
    target = update.callback_query.message if update.callback_query else update.message

    # Путь к картинке
    photo_path = os.path.join(os.path.dirname(__file__), "img", "main.png")

    # Отправка картинки с подписью и клавиатурой
    with open(photo_path, "rb") as photo:
        await target.reply_photo(
            photo=photo,
            caption=text,
            reply_markup=main_keyboard()
        )

async def random_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = update.callback_query.message if update.callback_query else update.message

    if random.random() < 0.5:
        # факт из файла
        with open(PATH_TO_RESOURCES / "random.txt", encoding="utf-8") as file:
            lines = [line.strip() for line in file.read().splitlines() if line.strip()]
            fact = random.choice(lines)
    else:
        # факт от OpenAI
        fact = await client.ask(
            user_message="Give me one interesting random fact.",
            system_prompt="You are an assistant who responds with short and interesting facts."
        )
        # оставляем только первую строку, если OpenAI вернул несколько
        fact = fact.splitlines()[0]

    await target.reply_text(fact, reply_markup=main_keyboard())

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


if __name__ == "__main__":
    app = ApplicationBuilder().token(TG_BOT_API_KEY).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()