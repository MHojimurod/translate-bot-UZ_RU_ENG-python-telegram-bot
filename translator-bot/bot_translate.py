from googletrans import Translator

tr = Translator()
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, Updater, ConversationHandler, CommandHandler, MessageHandler, Filters, \
    CallbackQueryHandler
import globals
from database import Database
from datetime import datetime

database = Database("member.db")


def start_command(update, context):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    if not user:
        database.create_user(user_id, username, datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    button = [
        [KeyboardButton(globals.language[1]), KeyboardButton(globals.language[2])],
        [KeyboardButton(globals.language[3]), KeyboardButton(globals.language[4])],
        [KeyboardButton(globals.language[5]), KeyboardButton(globals.language[6])]
    ]
    update.message.reply_html(
        "<b>Quydagilardan birini tanlang\n\nВыберите один из следующих\n\nChoose one of the following</b>\n\n🔽🔽🔽🔽🔽🔽",
        reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True))


def user_command(update, context):
    users = database.count_user()
    count = 0
    for user in users:
        count += 1
    update.message.reply_html(
        text=f"<b>Foydalanuvchilar soni</b> {count}\n\n<b>Количество пользователей</b> {count}\n\n<b>Quantity of users</b> {count}")

def help_command(update,context):
    update.message.reply_text(text=f"{globals.helpp[1]}\n\n{globals.helpp[2]}\n\n{globals.helpp[3]}")

def message_handler(update, context):
    state = context.user_data.get('state', 0)
    msg = update.message.text
    if msg == globals.language[1] or msg == globals.language[3]:
        update.message.reply_html("matn kiriting:")
        if msg == globals.language[1]:
            context.user_data['state'] = 1
        else:
            context.user_data['state'] = 3

    elif msg == globals.language[2] or msg == globals.language[5]:
        update.message.reply_html("введите текст:")
        if msg == globals.language[2]:
            context.user_data['state'] = 2
        else:
            context.user_data['state'] = 5

    elif msg == globals.language[4] or msg == globals.language[6]:
        update.message.reply_html("enter the text:")
        if msg == globals.language[4]:
            context.user_data['state'] = 4
        else:
            context.user_data['state'] = 6
    elif state == 1:
        result = tr.translate(msg, src='uz', dest='ru')
        update.message.reply_text(f"{result.text}")
    elif state == 2:
        result = tr.translate(msg, src='ru', dest='uz')
        update.message.reply_text(f"{result.text}")
    elif state == 3:
        result = tr.translate(msg, src='uz', dest='en')
        update.message.reply_text(f"{result.text}")
    elif state == 4:
        result = tr.translate(msg, src='en', dest='uz')
        update.message.reply_text(f"{result.text}")
    elif state == 5:
        result = tr.translate(msg, src='ru', dest='en')
        update.message.reply_text(f"{result.text}")
    elif state == 6:
        result = tr.translate(msg, src='en', dest='ru')
        update.message.reply_text(f"{result.text}")
    else:
        start_command(update,context)

def main():
    updater = Updater("YOUR_TOKEN")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("users", user_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()


