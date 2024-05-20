from aiogram import Bot
from aiogram.types import CallbackQuery


async def edit_prev_message(*args, callback: CallbackQuery, bot: Bot, **kwargs):
    if callback.inline_message_id:
        await bot.edit_message_text(*args, inline_message_id=callback.inline_message_id, **kwargs)
    else:
        await callback.message.edit_text(*args, **kwargs)
