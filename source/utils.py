import random
from typing import Union
from dataclasses import dataclass
from source.logger import get_logger

logger = get_logger(__name__)


@dataclass
class GameSettings:
    FREE_SPACE = "."
    CROSS = "X"
    ZERO = "O"
    CONTINUE = 0
    FINISH = 1
    CROSS_SP = "❎"
    ZERO_SP = "🟢"

    DEFAULT_STATE = [
        ["." for _ in range(3)]
        for _ in range(3)
    ]


@dataclass
class GameText:

    DEFAULT_TEXT = f'Your turn! Please, put {GameSettings.CROSS} to the free place'
    FINAL_TEXT = "The game is over, press /start to play again"

    CORRECT_CELL = "Correct cell."
    WRONG_ZERO_CELL = "Incorrect cell, it already has a zero on it."
    WRONG_CROSS_CELL = "Incorrect cell, it already has a cross on it."

    USER_WON = "You've won! Great job!"
    BOT_WON = "The bot has won, try again."
    DRAW = "It's a draw, it wasn't enough, try again."
    NO_WINNER = "There is no winner yet."


@dataclass
class ValidationMoveStatus:
    CORRECT = 0
    INCORRECT = 1


@dataclass
class WinnerPos:
    type: str
    number: int


def validate_position(field: list[list[str]], row: int, col: int) -> Union[ValidationMoveStatus, GameText]:
    """
    Validate the move on the given position.

    Parameters
    ----------
    field : list[list[str]]
        The current state of the game board.
    row : int
        The row of the move.
    col : int
        The column of the move.

    Returns
    -------
    Union[ValidationMoveStatus, GameText]
        A tuple of (ValidationMoveStatus, GameText) where the first element
        indicates whether the move is correct or not, and the second element
        is a message to be displayed to the user.
    """
    if field[row][col] == GameSettings.ZERO:
        return ValidationMoveStatus.INCORRECT, GameText.WRONG_ZERO_CELL
    elif field[row][col] == GameSettings.CROSS:
        return ValidationMoveStatus.INCORRECT, GameText.WRONG_CROSS_CELL
    return ValidationMoveStatus.CORRECT, GameText.CORRECT_CELL


def verify_winner(field: list[list[str]]) -> Union[GameText, WinnerPos]:
    """
    Verify the winner of the current game state.

    Parameters
    ----------
    field : list[list[str]]
        The current state of the game board.

    Returns
    -------
    result : Union[GameText, WinnerPos]
        A tuple containing the message to display at the end of the game
        and a WinnerPos object describing the winning position if the game is over.
        If the game is not over, return GameText.NO_WINNER and WinnerPos(None, None).
    """
    for i, row in enumerate(field):
        if row[0] == row[1] == row[2] and row[0] != GameSettings.FREE_SPACE:
            if row[0] == GameSettings.CROSS:
                logger.debug(f"User won on row {i}")
                return GameText.USER_WON, WinnerPos("row", i)
            logger.debug(f"Bot won on row {i}")
            return GameText.BOT_WON, WinnerPos("row", i)

    for col in range(3):
        if field[0][col] == field[1][col] == field[2][col] and field[0][col] != GameSettings.FREE_SPACE:
            if field[0][col] == GameSettings.CROSS:
                logger.debug(f"User won on col {col}")
                return GameText.USER_WON, WinnerPos("col", col)
            logger.debug(f"Bot won on col {col}")
            return GameText.BOT_WON, WinnerPos("col", col)

    if field[0][0] == field[1][1] == field[2][2] and field[0][0] != GameSettings.FREE_SPACE:
        if field[0][0] == GameSettings.CROSS:
            logger.debug("User won on diag 0")
            return GameText.USER_WON, WinnerPos("diag", 0)
        logger.debug("Bot won on diag 0")
        return GameText.BOT_WON, ("diag", 0)

    if field[0][2] == field[1][1] == field[2][0] and field[0][2] != GameSettings.FREE_SPACE:
        if field[0][2] == GameSettings.CROSS:
            logger.debug("User won on diag 1")
            return GameText.USER_WON, WinnerPos("diag", 1)
        logger.debug("Bot won on diag 1")
        return GameText.BOT_WON, WinnerPos("diag", 1)

    is_draw = True
    for row in field:
        for cell in row:
            is_draw = False
            break
        if not is_draw:
            break
    if is_draw:
        logger.debug("Draw")
        return GameText.DRAW, WinnerPos(None, None)

    logger.debug("No winner yet")
    return GameText.NO_WINNER, WinnerPos(None, None)


def choose_position(field: list[list[str]]) -> int | tuple:
    """
    Choose a free position on the field.

    Iterate over the field and find all free positions.
    If there are no free positions, return -1.
    Otherwise, return a random free position as a tuple of (row, col).

    Returns:
        int | tuple: -1 if no free positions left, otherwise a tuple of (row, col)
    """
    free_positions = []
    for row in range(3):
        for col in range(3):
            if field[row][col] == GameSettings.FREE_SPACE:
                free_positions.append((row, col))

    if len(free_positions) == 0:
        logger.info("No free positions left")
        return -1

    row, col = random.choice(free_positions)
    logger.info(f"Chosen position: {row}, {col}")
    return row, col
