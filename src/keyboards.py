from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Закінчити", callback_data="start")],
        [InlineKeyboardButton("Хочу ще факт", callback_data="random")],
        [InlineKeyboardButton("Запит до gpt", callback_data="gpt")],
        [InlineKeyboardButton("Діалог з відомою особистістю", callback_data="talk")],
        [InlineKeyboardButton("Квіз", callback_data="quiz")],
        [InlineKeyboardButton("Перекладач", callback_data="translate")]
    ])
