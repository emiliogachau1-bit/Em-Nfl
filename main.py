import os
import random
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

def get_games():
    url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    data = requests.get(url).json()

    games = []
    for event in data.get("events", []):
        teams = event["competitions"][0]["competitors"]
        home = teams[0]["team"]["displayName"]
        away = teams[1]["team"]["displayName"]
        games.append((home, away))
    return games

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    games = get_games()

    if not games:
        await update.message.reply_text("No NFL games today.")
        return

    home, away = random.choice(games)

    winner = random.choice([home, away])
    confidence = round(random.uniform(55, 75), 2)

    await update.message.reply_text(
        f"🏈 NFL Prediction\n\n{home} vs {away}\n\nWinner: {winner}\nConfidence: {confidence}%"
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("predict", predict))

print("Bot running...")
app.run_polling()
