"""
Bot for playing tic tac toe game with multiple CallbackQueryHandlers
"""
from copy import deepcopy
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

from source.utils import (
    GameSettings,
    GameText,
    ValidationMoveStatus,
    WinnerPos,
    validate_position,
    verify_winner,
    choose_position,
)
from source.logger import get_logger


logger = get_logger(__name__)


def get_default_state():
    """Helper function to get default state"""
    return deepcopy(GameSettings.DEFAULT_STATE)


def generate_keyboard(state: list[list[str]]):
    """Generate tic tac toe keyboard 3x3 (telegram buttons)"""

    return [
        [
            InlineKeyboardButton(state[r][c], callback_data=f"{r}{c}")
            for c in range(3)
        ]
        for r in range(3)
    ]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Start a new game.

    This function is called when the user starts a conversation with the bot.
    It generates a new tic tac toe board and sends it to the user as a message.
    The message contains a reply markup that allows the user to move on the board.
    The function then returns the next state of the conversation.

    Args:
        update (Update): The incoming update.
        context (ContextTypes.DEFAULT_TYPE): The context of the conversation.

    Returns:
        int: The next state of the conversation.
    """
    context.user_data['keyboard_state'] = get_default_state()
    keyboard = generate_keyboard(context.user_data['keyboard_state'])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(GameText.DEFAULT_TEXT,
                                    reply_markup=reply_markup)
    return GameSettings.CONTINUE


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    """
    Handle the user's move and bot's move in the tic tac toe game.

    Validate the user's move and update the game state accordingly.
    If the move is invalid, send a message to the user and return to the
    current state.

    If the move is valid, update the game state and send the new keyboard
    to the user. Then, choose a position for the bot's move and update
    the game state accordingly. If the bot has won, send a message to
    the user and end the game.

    If the game is a draw, send a message to the user and end the game.

    Parameters
    ----------
    update : Update
        The incoming update.
    context : ContextTypes.DEFAULT_TYPE
        The context of the conversation.

    Returns
    -------
    int
        The state of the conversation.
    """
    row, col = map(int, update.callback_query.data)

    validation_status, validation_msg = validate_position(
        context.user_data['keyboard_state'], row, col)

    if validation_status == ValidationMoveStatus.INCORRECT:
        keyboard = generate_keyboard(context.user_data['keyboard_state'])
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.callback_query.edit_message_text(
            validation_msg, reply_markup=reply_markup
        )

        return GameSettings.CONTINUE

    context.user_data['keyboard_state'][row][col] = GameSettings.CROSS
    keyboard = generate_keyboard(context.user_data['keyboard_state'])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_reply_markup(reply_markup)

    winner_msg, winner_location = verify_winner(
        context.user_data['keyboard_state'])
    if winner_msg != GameText.NO_WINNER:
        await update.callback_query.edit_message_text(
            winner_msg, reply_markup=reply_markup
        )
        return await end_game(update, context, winner_msg, winner_location)

    pos = choose_position(context.user_data['keyboard_state'])

    if pos == -1:
        await update.callback_query.edit_message_text(
            GameText.DRAW, reply_markup=reply_markup
        )
        return await end_game(update, context, winner_msg)

    row, col = pos
    context.user_data['keyboard_state'][row][col] = GameSettings.ZERO
    keyboard = generate_keyboard(context.user_data['keyboard_state'])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_reply_markup(reply_markup)

    winner_msg, winner_location = verify_winner(
        context.user_data['keyboard_state'])
    if winner_msg != GameText.NO_WINNER:
        await update.callback_query.edit_message_text(
            winner_msg, reply_markup=reply_markup
        )
        return await end_game(update, context, winner_msg, winner_location)

    return GameSettings.CONTINUE


async def end_game(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        winner_msg=GameText.NO_WINNER,
        winner_location: WinnerPos = None) -> int:

    """
    Function to end the game.

    Parameters
    ----------
    update : Update
        The incoming update.
    context : ContextTypes.DEFAULT_TYPE
        The context of the conversation.
    winner_msg : str
        The message to display to the user (default is GameText.NO_WINNER).
    winner_location : WinnerPos
        The winner location (default is None).

    Returns
    -------
    int
        The state of the conversation.
    """
    if winner_location is not None and winner_msg != GameText.DRAW:
        special_symb = GameSettings.CROSS_SP if winner_msg == GameText.USER_WON else GameSettings.ZERO_SP
        if winner_location.type == "diag":
            if winner_location.number == 0:
                for i in range(3):
                    context.user_data['keyboard_state'][i][i] = special_symb
            else:
                for i in range(3):
                    context.user_data['keyboard_state'][i][2 -
                                                           i] = special_symb
        else:
            if winner_location.type == "row":
                for i in range(3):
                    context.user_data['keyboard_state'][winner_location.number][i] = special_symb
            else:
                for i in range(3):
                    context.user_data['keyboard_state'][i][winner_location.number] = special_symb

        keyboard = generate_keyboard(context.user_data['keyboard_state'])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.edit_message_reply_markup(reply_markup)

    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text=GameText.FINAL_TEXT)

    return ConversationHandler.END
