import asyncio
from config import OPENAI_API_KEY
from openai import AsyncOpenAI, OpenAIError
from telegram import Update
from telegram.ext import ContextTypes
import random
from pathlib import Path
import sys
import os
sys.path.append(os.path.dirname(__file__))

PATH_TO_RESOURCES = Path(__file__).parent / "resources"
class OpenAiClient:
    def __init__(self):
        self._client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    async def ask(self, user_message: str, system_prompt: str = "You are assistant") -> str:
        try:
            response = await self._client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            return response.choices[0].message.content.strip()

        except OpenAIError as e:
            print(e)
            return "⚠️ Не удалось получить ответ."



client = OpenAiClient()



async def random_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = update.callback_query.message if update.callback_query else update.message

    if random.random() < 0.5:

        with open(PATH_TO_RESOURCES / "random.txt", encoding="UTF-8") as file:
            lines = file.read().splitlines()
            fact = random.choice(lines)
    else:

        fact = await client.ask(
            user_message="Give me one interesting random fact.",
            system_prompt="You are an assistant who responds with short and interesting facts."
        )

    await target.reply_text(fact, reply_markup=main_keyboard())



async def main():
    test_client = OpenAiClient()
    print(await test_client.ask("Who are you?"))


if __name__ == "__main__":
    asyncio.run(main())
