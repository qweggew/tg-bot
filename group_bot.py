import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import re

TOKEN = '7582607812:AAEXb99qup6c25EoVi77fignM5X1PAprRrU'

# Список запрещенных слов
BAD_WORDS = ['мат1', 'мат2', 'мат3']

# Функция для проверки мата
def contains_bad_words(text):
    text = text.lower()
    for word in BAD_WORDS:
        if re.search(r'\b' + word + r'\b', text):
            return True
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("")

# Обработчик сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message.chat.type in ['group', 'supergroup'] and message.text:
        if contains_bad_words(message.text):
            try:
                await context.bot.delete_message(chat_id=message.chat_id, message_id=message.message_id)
            except telegram.error.BadRequest:
                await context.bot.send_message(chat_id=message.chat_id,)

def main():
    # Создаем приложение вместо Updater
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start",start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    print("Бот запущен!")
    application.run_polling()

if __name__ == '__main__':
    main()