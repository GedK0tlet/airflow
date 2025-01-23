from aiogram import Bot
import asyncio

async def main(token, an_message, list_ids):

    bot = Bot(token)
    try:
        for id in list_ids:
            await bot.send_message(id, an_message)
    except Exception as e:
        await bot.send_message(-1002311333309, f"{e} \n\n EXEPTION")
    await bot.close()

def send_messages(token, list_ids, **kwargs):
    ti = kwargs["ti"]
    an_message = ti.xcom_pull(task_ids='task_fetch_data', key='text_anekdot')

    asyncio.run(main(token, an_message, list_ids))
