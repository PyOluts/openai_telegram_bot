from telegram import InlineKeyboardButton, InlineKeyboardMarkup


main_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("Random Fact", callback_data="random")],
    [InlineKeyboardButton("GPT Ask", callback_data="gpt")],
    [InlineKeyboardButton("Talk to Celebrity", callback_data="talk")],
    [InlineKeyboardButton("Quiz", callback_data="quiz")],
    [InlineKeyboardButton("Translate", callback_data="translate")],
])


celebrity_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("Einstein", callback_data="talk_einstein")],
    [InlineKeyboardButton("Jobs", callback_data="talk_jobs")],
    [InlineKeyboardButton("Musk", callback_data="talk_musk")],
    [InlineKeyboardButton("Back", callback_data="talk_end")],
])


quiz_topics_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("Science", callback_data="quiz_topic_science")],
    [InlineKeyboardButton("History", callback_data="quiz_topic_history")],
    [InlineKeyboardButton("Movies", callback_data="quiz_topic_movies")],
    [InlineKeyboardButton("Medicine", callback_data="quiz_topic_medicine")],
])
