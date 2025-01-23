

from aiogram import Bot, Dispatcher, types
import asyncio

bot_api="7701233425:AAEYRT6i28mAhoDoyQQMbYE4iIRWJnuI_io"

# bot = Bot(token=bot_api)
# dp = Dispatcher()

async def main(token, an_message, list_ids):
    # loop = asyncio.get_event_loop()
    bot = Bot(token)
    try:
        # for list_id in list_ids:
        await bot.send_message(list_ids[0], an_message)
    except Exception as e:
        await bot.send_message(-1002311333309, "EXCEPTION")
    await bot.close()

def send_messages(token, an_message, list_ids):
    asyncio.run(main(token, an_message, list_ids))

send_messages(bot_api, "send_messages", [-1002311333309, -1002311333309])