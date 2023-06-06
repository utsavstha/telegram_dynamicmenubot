import logging
import requests
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ForceReply, ReplyKeyboardMarkup

from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

BASE_URL = 'http://127.0.0.1:8000/api'
FILE_BASE_URL = '../information_api/static'
TOKEN = "6141215482:AAHXl1LNtFuuKbY0fml-vX3Uyk3cqfq5VoE"

def get_data(url):
    url = f"{BASE_URL}{url}"
    response = requests.request(
        "GET", url)

    return response.json()

def post_data(url, id):
    url = f"{BASE_URL}{url}"
    params = {
        "telegram_id": id
    }
    response = requests.request(
        "POST", url, json=params)

    return response

def handleImage(url):
    f = open(url,'wb')
    f.write(requests.get(url).content)
    f.close()

async def handleResponse(query, response):
    if response['image']:
        image =  FILE_BASE_URL + response['image']
        file = open(image, 'rb')
        await query.message.reply_photo(file)
    message = response['name'] + '\n'
    buttons = []
    for button in response["Menu"]:
        if button["source_url"]:
            buttons.append([InlineKeyboardButton(
                    button["button_name"], url=button["source_url"])])
        else:
            buttons.append([InlineKeyboardButton(
                    button["button_name"], callback_data=button["source_id"])])
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.reply_text(text=message, reply_markup=reply_markup)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    # print(user)
    post_data("/user/", user.id)
    query = update.callback_query
    response = get_data("/menu")
    await handleResponse(response=response, query=update)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    user = update.effective_user
    response = get_data(f"/menu/{query.data}")
    await handleResponse(response=response, query=query)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()