from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

from keyboards import mode_kb, mode_inline_kb
from storage import set_function_deleting

router = Router()


@router.message(Command('start'))
async def start(message: Message):
    await message.answer(
        text="Привет! Для начала игры выберите режим ниже",
        reply_markup=mode_kb()
    )


@router.message(Command('help'))
async def faq(message: Message):
    await message.answer(
        text="""
<b>Управление</b>
Взаимодействуйте с ботом только по полученной клавиатуре.

<b>Как играть</b>
Во время игры вы будете получать клавиатуру с кнопками, соответствующими клеткам на поле. Нажмите на пустую кнопку, чтобы сделать ход. Когда на поле будет 3 одинаковые фигуры, самая ране поставленная изменит свой вид. Это значит, что после текущего хода она исчезнет и откроет новое места для оппонента. Если игра не завершается в течение 5 минут, она удаляется, а сообщение заменяется ⌛️

<b>Мультиплеер</b>
Для начала игры выберите режим <b>Игра с другом 👥</b>, или введите имя бота (<code>@Giiker_bot</code>) в чате, в котором хотите начать игру и выберите фигуру из появившихся выше.

<b>О боте</b>
Мы не храним переписку, поэтому если у вас есть вопросы или пожелания, пишите мне @DIMaslov1904
        """,
        parse_mode='HTML',
        reply_markup=mode_kb()
    )


@set_function_deleting
async def conclude_game(key: str, bot: Bot):
    text = '⏳'
    if isinstance(key, tuple):
        await bot.edit_message_text(chat_id=key[0], message_id=key[1], text=text, reply_markup=mode_kb(True))
    else:
        await bot.edit_message_text(inline_message_id=key, text=text, reply_markup=mode_inline_kb())
