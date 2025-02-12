import pytest

from source.utils import (
    GameSettings,
    GameText,
    ValidationMoveStatus,
    WinnerPos,
    validate_position,
    verify_winner,
    choose_position,
)


@pytest.mark.parametrize(
    "field, row, col, expected_status, expected_msg",
    [
        ([["", "", ""], ["", "", ""], ["", "", ""]], 0, 0,
         ValidationMoveStatus.CORRECT, GameText.CORRECT_CELL),
        ([["X", "", ""], ["", "", ""], ["", "", ""]], 0, 0,
         ValidationMoveStatus.INCORRECT, GameText.WRONG_CROSS_CELL),
        ([["O", "", ""], ["", "", ""], ["", "", ""]], 0, 0,
         ValidationMoveStatus.INCORRECT, GameText.WRONG_ZERO_CELL),
        ([["", "", ""], ["X", "", ""], ["", "", ""]], 1, 0,
         ValidationMoveStatus.INCORRECT, GameText.WRONG_CROSS_CELL),
        ([["", "", ""], ["O", "", ""], ["", "", ""]], 1, 0,
         ValidationMoveStatus.INCORRECT, GameText.WRONG_ZERO_CELL),
        ([["", "", ""], ["", "X", ""], ["", "", ""]], 1, 1,
         ValidationMoveStatus.INCORRECT, GameText.WRONG_CROSS_CELL),
        ([["", "", ""], ["", "O", ""], ["", "", ""]], 1, 1,
         ValidationMoveStatus.INCORRECT, GameText.WRONG_ZERO_CELL),
        ([["", "", ""], ["", "", "X"], ["", "", ""]], 1, 2,
         ValidationMoveStatus.INCORRECT, GameText.WRONG_CROSS_CELL),
        ([["", "", ""], ["", "", "O"], ["", "", ""]], 1, 2,
         ValidationMoveStatus.INCORRECT, GameText.WRONG_ZERO_CELL),
        ([["", "", ""], ["", "", ""], ["X", "", ""]], 2, 0,
         ValidationMoveStatus.INCORRECT, GameText.WRONG_CROSS_CELL),
        ([["", "", ""], ["", "", ""], ["O", "", ""]], 2, 0,
         ValidationMoveStatus.INCORRECT, GameText.WRONG_ZERO_CELL),
        ([["", "", ""], ["", "", ""], ["", "X", ""]], 2, 1,
         ValidationMoveStatus.INCORRECT, GameText.WRONG_CROSS_CELL),
        ([["", "", ""], ["", "", ""], ["", "O", ""]], 2, 1,
         ValidationMoveStatus.INCORRECT, GameText.WRONG_ZERO_CELL),
        ([["", "", ""], ["", "", ""], ["", "", "X"]], 2, 2,
         ValidationMoveStatus.INCORRECT, GameText.WRONG_CROSS_CELL),
        ([["", "", ""], ["", "", ""], ["", "", "O"]], 2, 2,
         ValidationMoveStatus.INCORRECT, GameText.WRONG_ZERO_CELL),
    ],
)
def test_validate_position(field, row, col, expected_status, expected_msg):
    assert validate_position(field, row, col) == (
        expected_status, expected_msg)


@pytest.mark.parametrize(
    "field, expected_game_text, expected_winner_pos",
    [
        # User wins (rows)
        ([["X", "X", "X"], [".", ".", "."], [".", ".", "."]],
         GameText.USER_WON, WinnerPos("row", 0)),
        ([[".", ".", "."], ["X", "X", "X"], [".", ".", "."]],
         GameText.USER_WON, WinnerPos("row", 1)),
        ([[".", ".", "."], [".", ".", "."], ["X", "X", "X"]],
         GameText.USER_WON, WinnerPos("row", 2)),
        # Bot wins (rows)
        ([["O", "O", "O"], [".", ".", "."], [".", ".", "."]],
         GameText.BOT_WON, WinnerPos("row", 0)),
        ([[".", ".", "."], ["O", "O", "O"], [".", ".", "."]],
         GameText.BOT_WON, WinnerPos("row", 1)),
        ([[".", ".", "."], [".", ".", "."], ["O", "O", "O"]],
         GameText.BOT_WON, WinnerPos("row", 2)),
        # User wins (cols)
        ([["X", ".", "."], ["X", ".", "."], ["X", ".", "."]],
         GameText.USER_WON, WinnerPos("col", 0)),
        ([[".", "X", "."], [".", "X", "."], [".", "X", "."]],
         GameText.USER_WON, WinnerPos("col", 1)),
        ([[".", ".", "X"], [".", ".", "X"], [".", ".", "X"]],
         GameText.USER_WON, WinnerPos("col", 2)),
        # Bot wins (cols)
        ([["O", ".", "."], ["O", ".", "."], ["O", ".", "."]],
         GameText.BOT_WON, WinnerPos("col", 0)),
        ([[".", "O", "."], [".", "O", "."], [".", "O", "."]],
         GameText.BOT_WON, WinnerPos("col", 1)),
        ([[".", ".", "O"], [".", ".", "O"], [".", ".", "O"]],
         GameText.BOT_WON, WinnerPos("col", 2)),
        # User wins (diags)
        ([["X", ".", "."], [".", "X", "."], [".", ".", "X"]],
         GameText.USER_WON, WinnerPos("diag", 0)),
        ([[".", ".", "X"], [".", "X", "."], ["X", ".", "."]],
         GameText.USER_WON, WinnerPos("diag", 1)),
        # Bot wins (diags)
        ([[".", ".", "O"], [".", "O", "."], ["O", ".", "."]],
         GameText.BOT_WON, WinnerPos("diag", 1)),
        # Draw
        ([["X", "O", "X"], ["O", "X", "O"], [".", "O", "X"]],
         GameText.USER_WON, WinnerPos("diag", 0)),
        # No winner
        ([["X", ".", "."], [".", "O", "."], [".", ".", "."]],
         GameText.NO_WINNER, WinnerPos(None, None)),
        ([["X", "O", "."], [".", ".", "."], [".", ".", "."]],
         GameText.NO_WINNER, WinnerPos(None, None)),
        ([["X", ".", "O"], ["O", ".", "X"], [".", ".", "."]],
         GameText.NO_WINNER, WinnerPos(None, None)),
        ([["X", "O", "."], ["O", "X", "."], ["O", ".", "."]],
         GameText.NO_WINNER, WinnerPos(None, None)),
        ([["X", ".", "O"], [".", "O", "."], ["O", ".", "X"]],
         GameText.BOT_WON, WinnerPos("diag", 1)),
        ([["X", ".", "."], ["X", ".", "."], [".", "O", "."]],
         GameText.NO_WINNER, WinnerPos(None, None)),
        ([["X", "O", "."], ["O", "X", "."], [".", "O", "."]],
         GameText.NO_WINNER, WinnerPos(None, None)),
        ([["X", ".", "O"], ["O", "X", "."], [".", ".", "X"]],
         GameText.USER_WON, WinnerPos("diag", 0)),
    ],
)
def test_verify_winner(field, expected_game_text, expected_winner_pos):
    game_text, winner_pos = verify_winner(field)
    assert game_text == expected_game_text
    assert winner_pos == expected_winner_pos
    
    