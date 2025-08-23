import random
import os
from config import TG_BOT_API_KEY
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, ContextTypes,
    CallbackQueryHandler, MessageHandler,
    CommandHandler, filters
)
from pathlib import Path
from open_ai_client import client

PATH_TO_RESOURCES = Path(__file__).parent / "resources"


# ----------------- Keyboards -----------------
def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Random Fact", callback_data="random")],
        [InlineKeyboardButton("GPT Ask", callback_data="gpt")],
        [InlineKeyboardButton("Talk to Celebrity", callback_data="talk")],
        [InlineKeyboardButton("Quiz", callback_data="quiz")]
    ])


def celebrity_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Einstein", callback_data="talk_einstein")],
        [InlineKeyboardButton("Jobs", callback_data="talk_jobs")],
        [InlineKeyboardButton("Musk", callback_data="talk_musk")],
        [InlineKeyboardButton("Back", callback_data="talk_end")]
    ])


# ----------------- Bot Functions -----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = update.callback_query.message if update.callback_query else update.message
    text = "Hello! I am your AI assistant. Choose an option:"
    await target.reply_text(text, reply_markup=main_keyboard())


async def random_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = update.callback_query.message if update.callback_query else update.message
    if random.random() < 0.5 and (PATH_TO_RESOURCES / "random.txt").exists():
        with open(PATH_TO_RESOURCES / "random.txt", encoding="utf-8") as file:
            lines = [line.strip() for line in file.read().splitlines() if line.strip()]
            fact = random.choice(lines)
    else:
        fact = await client.ask(
            user_message="Give me one interesting random fact.",
            system_prompt="You are an assistant who responds with short and interesting facts."
        )
        fact = fact.splitlines()[0]
    await target.reply_text(fact, reply_markup=main_keyboard())


async def gpt_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = update.callback_query.message if update.callback_query else update.message
    user_question = context.user_data.get("last_message")
    if not user_question:
        await target.reply_text("Send a message first to ask GPT.", reply_markup=main_keyboard())
        return
    await target.reply_text("Generating GPT answer...")
    response = await client.ask(
        user_message=user_question,
        system_prompt="You are an assistant who responds concisely."
    )
    await target.reply_text(response, reply_markup=main_keyboard())


async def talk_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = update.callback_query.message if update.callback_query else update.message
    await target.reply_text("Choose a celebrity to talk to:", reply_markup=celebrity_keyboard())


async def quiz_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = update.callback_query.message if update.callback_query else update.message
    await target.reply_text("Generating a random quiz question...")
    prompt = """Generate one quiz question with four possible answers.
Mark the correct answer with a number from 0 to 3.
Return in the format: question | option0 | option1 | option2 | option3 | correct_number"""
    try:
        response = await client.ask(user_message=prompt, system_prompt="You are a quiz generator")
        parts = response.split("|")
        question = parts[0].strip()
        options = [p.strip() for p in parts[1:5]]
        correct_index = int(parts[5].strip())
        context.user_data["quiz_correct_index"] = correct_index
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(opt, callback_data=f"quiz_{i}")] for i, opt in enumerate(options)]
        )
        await target.reply_text(question, reply_markup=keyboard)
    except Exception as e:
        await target.reply_text(f"❌ Could not generate a question. Try again.\nError: {e}")


# ----------------- Button Handler -----------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "random":
        await random_fact(update, context)
    elif data == "gpt":
        await gpt_request(update, context)
    elif data == "talk":
        await talk_request(update, context)
    elif data.startswith("talk_"):
        persona = data.split("_")[1]
        context.user_data["celebrity"] = persona
        await query.message.reply_text(f"Now you can chat with {persona.title()}!")
    elif data == "quiz":
        await quiz_request(update, context)
    elif data.startswith("quiz_"):
        selected = int(data.split("_")[1])
        correct = context.user_data.get("quiz_correct_index")
        if correct is not None:
            if selected == correct:
                await query.message.reply_text("✅ Correct!", reply_markup=main_keyboard())
            else:
                await query.message.reply_text(f"❌ Wrong! The correct answer was {correct}", reply_markup=main_keyboard())


# ----------------- User Message Handler -----------------
async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    context.user_data["last_message"] = text
    celebrity = context.user_data.get("celebrity")
    if celebrity:
        response = await client.ask(
            user_message=text,
            system_prompt=f"You are talking as {celebrity.title()}. Respond concisely."
        )
    else:
        response = "Press GPT Ask to get an AI response."
    await update.message.reply_text(response, reply_markup=main_keyboard())


# ----------------- Main -----------------
if __name__ == "__main__":
    app = ApplicationBuilder().token(TG_BOT_API_KEY).build()
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))
    app.add_handler(CommandHandler("start", start))

    app.run_polling()

