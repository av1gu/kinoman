import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Привет! Напиши название фильма."
    )

def search_movie(title):
    url = f"https://www.tvmaze.com/search/shows?q={title}"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    if not data:
        return None

    return data[0]["show"]

async def movie_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text

    movie = search_movie(query)

    if not movie:
        await update.message.reply_text("❌ Ничего не найдено.")
        return

    title = movie.get("name", "Без названия")

    genres = ", ".join(movie.get("genres", []))
    rating = movie.get("rating", {}).get("average", "N/A")
    premiered = movie.get("premiered", "Неизвестно")

    summary = movie.get("summary", "Нет описания.")
    summary = (
        summary.replace("<p>", "")
        .replace("</p>", "")
        .replace("<b>", "")
        .replace("</b>", "")
    )

    image = None
    if movie.get("image"):
        image = movie["image"].get("original")

    text = (
        f"🎬 <b>{title}</b>\n\n"
        f"⭐ Рейтинг: {rating}\n"
        f"🎭 Жанры: {genres}\n"
        f"📅 Дата выхода: {premiered}\n\n"
        f"📝 {summary}"
    )

    if image:
        await update.message.reply_photo(
            photo=image,
            caption=text,
            parse_mode="HTML"
        )
    else:
        await update.message.reply_text(
            text,
            parse_mode="HTML"
        )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            movie_search
        )
    )

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
