import numpy as np
import math
import pandas as pd

def calculate_angle(x, y):
    
    a = np.array([90,283])
    b = np.array([x,y])
    c = np.array([90,227])

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)

    return np.degrees(angle)


def calculate_distance_goal(x, y):
    return math.hypot(x - 90, y - 255)


def calculate_distance(p1, p2):
    #print(p1, p2)
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def process_dataframe(df):
    # Ignore shots outside of the rink coordinates
    df = df[(df['ShotX'] > 0) & (df['ShotY'] > 0)]

    # Group shots to the left side of the rink
    df.loc[df['ShotX'] > 511, 'ShotY'] = df["ShotY"] - 2 * (df["ShotY"] - 256)
    df.loc[df['ShotX'] > 511, 'ShotX'] = df["ShotX"] - 2 * (df["ShotX"] - 511)

    # Calculate the angle of the shot
    df['Angle_Deg'] = df.apply(lambda x: calculate_angle(x['ShotX'], x['ShotY']), axis=1)

    # Calculate the distance to the goal
    df['Distance'] = df.apply(lambda x: calculate_distance([x['ShotX'],x['ShotY']], [90, 255]), axis=1)

    # Calculate the time from last shot. If no previous shot => value = 0
    df['TimeFromPreviousShot'] = df.GameTime - df.GameTime.shift(1, fill_value=df.GameTime[0])
    df.loc[df['TimeFromPreviousShot'] < 0, "TimeFromPreviousShot"] = 0
    
    
    # Ignore blocked shots
    df = df[df['EventType'] != 3]

    # EventType = 1 => goal, EventType = 0 => no goal (Saved/Shot off target)
    df.loc[df['EventType'] == 2, 'EventType'] = 0

    # Ignore shots in penalties or at empty net

    df = df[(df['Goaltype'] != "RL") & (df['Goaltype'] != "TM") & (df['Goaltype'] != "YV") & (df['Goaltype'] != "YV2")]

    return df


def separate_games(df):
    names = list(df.columns)
    current_game = int(df.iloc[0]["GAME_ID"])
    temp_df = pd.DataFrame(columns=names)

    dfs = []
    for index, row in df.iterrows():
        if current_game == int(row["GAME_ID"]):
            temp_df.loc[len(temp_df.index)] = row
        else:
            dfs.append(temp_df)
            temp_df = temp_df[0:0]
            current_game = int(row["GAME_ID"])
            temp_df.loc[len(temp_df.index)] = row
    return dfs

