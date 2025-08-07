from  config TG_BOT_API_KEY
from telegram.ext import ApplicationBuilder,CommandHandler,Context
from utils import load_massage_for_bot

async def start(update: Update,context:Context):
    text = load_massage_for_bot('main')
    await update.message.reply_text("shiiiiiiiiiish")


app=ApplicationBuilder().build()
app.token(ApplicationBuilder).token(TG_BOT_API_KEY).build()

app.add_handler(CommandHandler("start", start))
app.run_polling()
