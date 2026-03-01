import pandas as pd
import numpy as np
import joblib
from xgboost import XGBClassifier

np.random.seed(42)

data = []

for i in range(2000):
    elo_diff = np.random.randint(-300, 300)
    home_adv = 1
    result = 1 if elo_diff > 0 else 0
    data.append([elo_diff, home_adv, result])

df = pd.DataFrame(data, columns=["elo_diff", "home_adv", "result"])

X = df[["elo_diff", "home_adv"]]
y = df["result"]

model = XGBClassifier(
    n_estimators=400,
    max_depth=5,
    learning_rate=0.05,
    eval_metric="logloss"
)

model.fit(X, y)

joblib.dump(model, "model.pkl")
print("Model trained and saved.")
