Telegram OpenAI Bot
==================

Description:
------------
This is a Telegram bot integrated with OpenAI's GPT model. The bot can:
- Send random facts
- Answer GPT queries
- Simulate conversations with famous personalities
- Conduct quizzes
- Translate messages
- Display images and interactive keyboards

Setup:
------
1. Clone the repository.
2. Install dependencies:
   pip install -r requirements.txt
3. Add your API keys in the config.py file:
   - TG_BOT_API_KEY: Your Telegram bot API token
   - OPENAI_API_KEY: Your OpenAI API key

Project Structure:
------------------
/src
  bot.py               - Main bot logic
  utils.py             - Utility functions (load messages, random facts)
  open_ai_client.py    - Handles OpenAI requests
  keyboards.py         - Inline keyboards for bot
/resources
  main.txt             - Text for the start message
  random.txt           - Random facts for the bot
/img
  main.png             - Start image for the bot

Usage:
------
Run the bot:
   python src/bot.py

Commands:
---------
/start - Start the bot and show main menu

Notes:
------
- Ensure you have the correct folder structure.
- Update 'resources' with your custom messages.
- Make sure to handle the OpenAI API key securely.

Author:
-------
Your Name
