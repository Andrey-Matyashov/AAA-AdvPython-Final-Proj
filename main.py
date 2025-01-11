import os
from dotenv import load_dotenv
from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)

from source.bot import start, game
from source.utils import GameSettings
from source.logger import get_logger

logger = get_logger(__name__)


async def post_init(application):
    bot = application.bot
    await bot.set_my_commands(
        BotCommand("start", "Start a new game")
    )


def main():

    load_dotenv()
    TG_TOKEN = os.getenv('TG_TOKEN')

    logger.info("Starting bot...")
    application = Application.builder().token(TG_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            GameSettings.CONTINUE: [
                CallbackQueryHandler(game, pattern='^' + f'{row}{col}' + '$')
                for row in range(3) for col in range(3)
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    logger.info("Bot stopped.")


if __name__ == "__main__":
    main()
