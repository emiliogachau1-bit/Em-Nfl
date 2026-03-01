import requests
import joblib
import numpy as np
import random
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Auto-create model if missing
if not os.path.exists("model.pkl"):
    import train_model

model = joblib.load("model.pkl")

def get_today_games():
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
    games = get_today_games()

    if not games:
        await update.message.reply_text("No NFL games found today.")
        return

    home, away = random.choice(games)

    elo_diff = np.random.randint(-200, 200)
    features = np.array([[elo_diff, 1]])

    prob = model.predict_proba(features)[0][1]
    winner = home if prob > 0.5 else away

    message = f"""
🏈 AI NFL Prediction

Match:
{home} vs {away}

Predicted Winner:
🔥 {winner}

Win Probability:
{round(prob * 100, 2)}%
"""

    await update.message.reply_text(message)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("predict", predict))

print("Bot running...")
app.run_polling()
