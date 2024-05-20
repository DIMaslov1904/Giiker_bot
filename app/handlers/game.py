from aiogram import Router, F, types, Bot

from config_reader import config
from game import TicTacToe
from keyboards import mode_kb, select_side_kb, board_kb, mode_inline_kb
from storage import storage
from utils import get_scoreboard_players, get_text_game_end, edit_prev_message, StorageControl

router = Router()


@router.callback_query(F.data.startswith('select_mode_'))
async def callbacks_mode(callback: types.CallbackQuery):
    select_mode = int(callback.data.split("_")[2])
    game = TicTacToe(mode=select_mode)
    StorageControl.set_game_storage(game, callback)
    await callback.message.edit_text('Выберите сторону', reply_markup=select_side_kb())
    await callback.answer()


@router.callback_query(F.data.startswith('select_side_'))
async def callbacks_mode(callback: types.CallbackQuery, bot: Bot):
    player_symbol = callback.data.split("_")[2]

    key = (callback.message.chat.id, callback.message.message_id)
    game: TicTacToe | None = storage.setdefault(key, 'game')['game']

    if game is None:
        await edit_prev_message(
            text='Перезагрузка игры',
            reply_markup=mode_kb(),
            callback=callback,
            bot=bot
        )
        return
    game.set_player(player_symbol, player_id=callback.from_user.id, name=callback.from_user.first_name)
    players = game.get_players()
    await edit_prev_message(
        text=get_scoreboard_players(players),
        reply_markup=board_kb(game),
        callback=callback,
        bot=bot
    )
    await callback.answer()


@router.callback_query(F.data.startswith('click_board_'))
async def callbacks_mode(callback: types.CallbackQuery, bot: Bot):
    player_step = int(callback.data.split("_")[2])
    game: TicTacToe | None = StorageControl.get_game_storage(callback)

    if game is None:
        if callback.inline_message_id:
            await edit_prev_message(
                text='Игра не найдена. Начните заново',
                reply_markup=mode_inline_kb(),
                bot=bot,
                callback=callback
            )
        else:
            await edit_prev_message(text='Перезагрузка игры', reply_markup=mode_kb(), bot=bot, callback=callback)
        return

    user_id = callback.from_user.id
    current_player = game.get_current_player()
    players = game.get_players()

    if (players[1].id == user_id or players[0].id == user_id) and user_id != current_player.id:
        await callback.answer(text='Ждите своего хода', show_alert=True)
        return

    if players[1].name is None and players[1].is_current:
        game.set_player2(player_id=user_id, name=callback.from_user.first_name)

    result = game.step(player_step)

    if result == -2:
        await callback.answer(text='Ячейка уже занята. Повторите ход', show_alert=True)
        return

    await callback.answer()

    if game.get_winner() != -1:
        text = get_text_game_end(game)
        if callback.inline_message_id:
            await edit_prev_message(text, bot=bot, callback=callback, reply_markup=mode_inline_kb())
        else:
            await edit_prev_message(text, bot=bot, callback=callback)
            await callback.message.answer(
                text='Для начала новой игры выберите режим ниже',
                reply_markup=mode_kb()
            )
        StorageControl.delete_game_storage(callback)
        return

    await edit_prev_message(text=get_scoreboard_players(players), reply_markup=board_kb(game), bot=bot,
                            callback=callback)


@router.inline_query()
async def show_user_images(inline_query: types.InlineQuery):
    results = []
    for sticker in config.stickers:
        results.append(types.InlineQueryResultCachedSticker(
            id=sticker[0],
            sticker_file_id=sticker[1],
            input_message_content=types.InputTextMessageContent(message_text='Запуск...'),
            reply_markup=select_side_kb()
        ))

    await inline_query.answer(results, is_personal=True, cache_time=1)


@router.chosen_inline_result()
async def set_symbol_player_inline_mode(chosen_inline_result: types.ChosenInlineResult):
    bot = chosen_inline_result.bot
    game = TicTacToe(mode=0)
    game.set_player(
        chosen_inline_result.result_id,
        player_id=chosen_inline_result.from_user.id,
        name=chosen_inline_result.from_user.first_name
    )
    StorageControl.set_game_storage(game, chosen_inline_result)
    players = game.get_players()

    await bot.edit_message_text(
        text=get_scoreboard_players(players),
        reply_markup=board_kb(game),
        inline_message_id=chosen_inline_result.inline_message_id
    )
