from telegram import Update
from telegram.ext import ContextTypes
from open_ai_client import client
from utils import load_messages_for_bot

from keyboards import main_keyboard, celebrity_keyboard, quiz_topics_keyboard

# --- Start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = update.message if update.message else update.callback_query.message
    text = load_messages_for_bot("main")
    await target.reply_text(text, reply_markup=main_keyboard())

# --- Random fact ---
async def random_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = update.message if update.message else update.callback_query.message
    fact = await client.ask("Give me a short interesting random fact.")
    await target.reply_text(fact, reply_markup=main_keyboard())

# --- GPT question ---
async def gpt_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = update.message if update.message else update.callback_query.message
    await target.reply_text("Send me a question, I will answer it.")

async def gpt_end(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    target = update.message if update.message else update.callback_query.message
    await target.reply_text(text, reply_markup=main_keyboard())

# --- Celebrity talk ---
async def talk_start(update, context):
    target = update.message if update.message else update.callback_query.message
    await target.reply_text("Choose a celebrity to talk with:", reply_markup=celebrity_keyboard())

async def talk_set_persona(update, context, persona: str):
    context.user_data["persona"] = persona
    target = update.message if update.message else update.callback_query.message
    await target.reply_text(f"You are now talking to {persona.title()}. Send your message:")

async def talk_end(update, context, text: str):
    context.user_data.pop("persona", None)
    target = update.message if update.message else update.callback_query.message
    await target.reply_text(text, reply_markup=main_keyboard())

# --- Quiz ---
async def quiz_start(update, context):
    target = update.message if update.message else update.callback_query.message
    await target.reply_text("Choose a quiz topic:", reply_markup=quiz_topics_keyboard())

async def quiz_set_topic(update, context, topic: str):
    context.user_data["quiz_topic"] = topic
    target = update.message if update.message else update.callback_query.message
    await target.reply_text(f"Topic set to {topic}. Generating first question...")

async def quiz_next_question(update, context):
    # TODO: implement random question generation
    target = update.message if update.message else update.callback_query.message
    await target.reply_text("Next question (placeholder)")

async def quiz_end(update, context, text: str):
    context.user_data.pop("quiz_topic", None)
    target = update.message if update.message else update.callback_query.message
    await target.reply_text(text, reply_markup=main_keyboard())

# --- Translate ---
async def translate_start(update, context):
    target = update.message if update.message else update.callback_query.message
    context.user_data["translate_mode"] = True
    await target.reply_text("Translate mode activated. Send text to translate.")

# --- Handle user text ---
async def handle_text(update, context):
    target = update.message
    text = update.message.text
    if context.user_data.get("translate_mode"):
        response = await client.ask(f"Translate to English: {text}")
        await target.reply_text(response, reply_markup=main_keyboard())
    elif persona := context.user_data.get("persona"):
        response = await client.ask(f"{persona.title()} conversation: {text}")
        await target.reply_text(response, reply_markup=main_keyboard())
    else:
        context.user_data["last_message"] = text
        await target.reply_text("Press GPT button for an answer.", reply_markup=main_keyboard())
