import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from util import process_dataframe
from util import separate_games
from sklearn.metrics import log_loss
import xgboost as xgb
from sklearn.metrics import roc_auc_score


def main():
    model2 = xgb.XGBClassifier()
    model2.load_model("model_xgboost.json")

    df = pd.read_csv('fliiga2022-2023.csv', header=0, sep='|', on_bad_lines='skip')
    df_list = separate_games(df)

    x_test = process_dataframe(df)
    y_test = x_test["EventType"].copy()
    x_test = x_test.drop(["Unnamed: 0", "UniqueID", "GameTime", "GoalX", "GoalY", "Period", "LogTime", "LTeamID", "RTeamID",
                   "ShootingTeamID", "ShootingPlayerID", "SPJersey", "BlockingPlayerID", "Plus", "Minus", "Ass1Jersey",
                   "Ass2Jersey", "Goaltype", "GAME_ID", "EventType"], axis=1).copy()
    x_test["TimeFromPreviousShot"] = x_test["TimeFromPreviousShot"].astype(str).astype('int64')
    y_pred = model2.predict_proba(x_test.values)

    print("Log loss:", log_loss(y_test, y_pred))
    print(roc_auc_score(y_test, y_pred[:, 1]))

    y_test_list = []
    y_pred_list = []
    game_ids = []
    for i in df_list:
        x_test = process_dataframe(i)
        y_test = x_test["EventType"].copy()
        game_ids.append(x_test.iloc[0]["GAME_ID"])
        x_test = x_test.drop(["Unnamed: 0", "UniqueID", "GameTime", "GoalX", "GoalY", "Period", "LogTime", "LTeamID", "RTeamID",
                   "ShootingTeamID", "ShootingPlayerID", "SPJersey", "BlockingPlayerID", "Plus", "Minus", "Ass1Jersey",
                   "Ass2Jersey", "Goaltype", "GAME_ID", "EventType"], axis=1).copy()
        x_test["TimeFromPreviousShot"] = x_test["TimeFromPreviousShot"].astype(str).astype('int64')
        y_pred = model2.predict_proba(x_test.values)
        y_test = y_test[(y_test == 1)]
        y_test_list.append(y_test.sum())
        y_pred_list.append(y_pred[:, 1].sum())

    plt.plot(np.arange(len(y_test_list)), y_test_list, c="g", marker="s", label="Goals")
    plt.plot(np.arange(len(y_test_list)), y_pred_list, c="r", marker="o", label="xG")
    plt.legend(loc='upper left')
    plt.title('FLiiga 2022-23 Games')
    plt.xlabel('Game')
    plt.ylabel('The amount of goals')

    plt.show()


if __name__ == "__main__":
    main()
