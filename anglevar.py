import pandas as pd
import numpy as np

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

df = pd.read_csv('temp_UWRL_river_velocimetry_dataset.csv')
df.datetime = pd.to_datetime(df.datetime)
df['angle'] = np.arctan2(df['v_y'], df['v_x'])
# df['angle_var'] = [np.nan for _ in range(len(df))]

analyzed = []
with open('anglevar_complete.txt') as f:
    for line in f:
        analyzed.append(pd.to_datetime(line))

dates = []
for date in sorted(df.datetime.unique()):
    date not in analyzed and dates.append(date)

while dates != []:
    print(f'{len(dates)} more timestamps to process')
    d = []

    for _ in range(12):
        date = dates.pop(0)
        print(date)

        df_curr = df[(df.datetime == date) & ~(df.angle.isna())]

        for index, row in df_curr.iterrows():
            xr, yr = round(row.x, 3), round(row.y, 3)
            angles = []

            for point in POINTS:
                angles.extend(df_curr.loc[(df_curr.x == xr + point['x'])&(df_curr.y == yr + point['y'])].angle.values)
            
            if angles != []:
                angle_diffs = []
                for angle in angles:
                    diff = abs(angle - row.angle) % np.pi
                    angle_diffs.append(diff * diff)
        
                df.at[index, 'angle_var'] = sum(angle_diffs) / len(angle_diffs)
        d.append(date)

    print('saving to csv\n')
    df.to_csv('temp_UWRL_river_velocimetry_dataset.csv')

    with open('anglevar_complete.txt', 'a') as f:
        for date in d:
            f.write(f"{date}\n")