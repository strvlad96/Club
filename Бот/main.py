import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Этапы диалога
NAME, SURNAME, CLASS = range(3)

# Файл для хранения данных
DATA_FILE = "users.json"

def save_user_data(user_data):
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(user_data)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Регистрация"]]
    await update.message.reply_text(
        "Привет! Нажми кнопку для начала регистрации:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите ваше имя:")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Введите вашу фамилию:")
    return SURNAME

async def get_surname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["surname"] = update.message.text
    await update.message.reply_text("Введите ваш класс обучения:")
    return CLASS

async def get_class(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["class"] = update.message.text

    # Сохраняем данные
    save_user_data({
        "id": update.effective_user.id,
        "name": context.user_data["name"],
        "surname": context.user_data["surname"],
        "class": context.user_data["class"]
    })

    await update.message.reply_text("✅ Регистрация завершена! Спасибо.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Регистрация отменена.")
    return ConversationHandler.END


def main():
    # 🔑 Вставь сюда токен от BotFather
    TOKEN = "8285843005:AAFnmzEa0XK3v-tmsLGJYx6RaErs-XA3eY8"

    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Регистрация$"), register)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            SURNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_surname)],
            CLASS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_class)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()