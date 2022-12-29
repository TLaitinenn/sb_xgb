import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from util import process_dataframe
import xgboost as xgb



def main():
    model = xgb.XGBClassifier()
    model.load_model("model_xgboost.json")

    df_game = pd.read_csv('3468.csv', header=0,sep='|', on_bad_lines='skip')

    df_game = process_dataframe(df_game)
    y_test_gametime = df_game[["EventType", "GameTime"]].copy()
    gametimes = df_game["GameTime"].copy().to_numpy()
    
    x_test = df_game.drop(["Unnamed: 0", "UniqueID", "GameTime", "GoalX", "GoalY", "Period", "LogTime", "LTeamID", "RTeamID",
                   "ShootingTeamID", "ShootingPlayerID", "SPJersey", "BlockingPlayerID", "Plus", "Minus", "Ass1Jersey",
                   "Ass2Jersey", "Goaltype", "GAME_ID", "EventType"], axis=1).copy()
    x_test["TimeFromPreviousShot"] = x_test["TimeFromPreviousShot"].astype(str).astype('int64')

    y_pred = model.predict_proba(x_test.values)
    y_test_gametime = y_test_gametime[(y_test_gametime["EventType"] == 1)]
    df_game["xG"] = y_pred[:,1].cumsum()
    cumu_values = y_pred[:,1].cumsum()



    goaltimes = y_test_gametime["GameTime"].to_numpy()
    goalvalues = y_test_gametime["EventType"].cumsum()
    goaltimes= np.append([0], goaltimes)
    goalvalues= np.append([0], goalvalues)
    goalvalues = np.append(goalvalues, goalvalues[-1])
    goaltimes = np.append(goaltimes, gametimes[-1])


    intermission_x = np.full((1, 20), 20)
    intermission_y = np.linspace(0, len(y_test_gametime), 20)


    plt.scatter(intermission_x, intermission_y, c='black', marker='|', label='Intermission')
    plt.scatter(intermission_x*2, intermission_y, c='black', marker='|')
    plt.scatter(intermission_x*3, intermission_y, c='black', marker='|')

    plt.plot(gametimes/60, cumu_values, c="g", marker="s", label="xG",drawstyle="steps-post")
    plt.plot(goaltimes/60, goalvalues, c="r", marker="o", label="Goals",drawstyle="steps-post")

    plt.legend(loc='upper left')
    plt.title('Game 3468')
    plt.xlabel('GameTime (minutes)')

    plt.ylabel('Cumulative xG/Goals')
    plt.show()


if __name__ == "__main__":
    main()
