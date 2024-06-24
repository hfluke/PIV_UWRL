import pandas as pd
import numpy as np

REPS = 100

POINTS = [
    {'x': -0.13, 'y': -0.13},
    {'x': -0.13, 'y': 0},
    {'x': -0.13, 'y': 0.13},
    {'x': 0, 'y': -0.13},
    {'x': 0, 'y': 0.13},
    {'x': 0.13, 'y': -0.13},
    {'x': 0.13, 'y': 0},
    {'x': 0.13, 'y': 0.13},
]

analyzed = []
with open('anglevar_complete.txt') as f:
    for line in f:
        analyzed.append(pd.to_datetime(line))

df = pd.read_csv('temp_UWRL_river_velocimetry_dataset.csv')
df.datetime = pd.to_datetime(df.datetime)

dates = []
for date in sorted(df.datetime.unique()):
    date not in analyzed and dates.append(date)

while dates != []:
    print(f'{len(dates)} more timestamps to process')
    d = []

    for i in range(REPS):
        date = dates.pop(0)
        print(f'{REPS-i:>3}. {date}')

        df_curr = df[(df.datetime == date) & ~(df.angle.isna())]

        for index, row in df_curr.iterrows():
            xr, yr = round(row.x, 3), round(row.y, 3)
            angles = []

            for POINT in POINTS:
                angles.extend(df_curr.loc[(df_curr.x == xr + POINT['x'])&(df_curr.y == yr + POINT['y'])].angle.values)
            
            if angles != []:
                angle_diffs = []
                for angle in angles:
                    diff = abs(angle - row.angle) % np.pi
                    angle_diffs.append(diff * diff)
        
                df.at[index, 'angle_var'] = sum(angle_diffs) / len(angle_diffs)
        d.append(date)

    print('saving to csv\n')
    df.to_csv('temp_UWRL_river_velocimetry_dataset.csv', index=False)

    with open('anglevar_complete.txt', 'a') as f:
        for date in d:
            f.write(f"{date}\n")