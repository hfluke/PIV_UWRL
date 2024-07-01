import pandas as pd
import numpy as np

REPS = 50

POINTS = [
    {'x': -1, 'y': -1},
    {'x': -1, 'y': 0},
    {'x': -1, 'y': 1},
    {'x': 0, 'y': -1},
    {'x': 0, 'y': 1},
    {'x': 1, 'y': -1},
    {'x': 1, 'y': 0},
    {'x': 1, 'y': 1},
]

analyzed = []
with open('anglevar_complete.txt') as f:
    for line in f:
        analyzed.append(pd.to_datetime(line))

df = pd.read_csv('temp2_UWRL_river_velocimetry_dataset.csv')
df.datetime = pd.to_datetime(df.datetime)

dates = []
for date in sorted(df.datetime.unique()):
    date not in analyzed and dates.append(date)

x_vals = sorted(df.x.unique())
y_vals = sorted(df.y.unique())

while dates != []:
    print(f'{len(dates)} more timestamps to process')
    d = []

    for i in range(REPS):
        date = dates.pop(0)
        print(f'{REPS-i:>7}. {date}')

        df_i = df[(df.datetime == date) & ~(df.angle.isna())]

        for index, row in df_i.iterrows():
            x, y = row.x, row.y
            x_i, y_i = x_vals.index(x), y_vals.index(y)

            angles = []

            for POINT in POINTS:
                try:
                    angles.extend(df_i.loc[(df_i.x == x_vals[x_i + POINT['x']]) & (df_i.y == y_vals[y_i + POINT['y']])].angle.values)
                except:
                    continue

            if angles != []:
                angle_diffs = []
                for angle in angles:
                    diff = abs(angle - row.angle) % np.pi
                    angle_diffs.append(diff * diff)
        
                df.at[index, 'angle_var'] = sum(angle_diffs) / len(angle_diffs)
                df.at[index, 'angle_var_support'] = len(angles)

        d.append(date)

    print('saving to csv\n')
    df.to_csv('temp2_UWRL_river_velocimetry_dataset.csv', index=False)

    with open('anglevar_complete.txt', 'a') as f:
        for date in d:
            f.write(f"{date}\n")
