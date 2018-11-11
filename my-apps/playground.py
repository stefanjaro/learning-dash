# for testing out code blocks

import pandas as pd

df = pd.read_csv(r"C:\Users\stefa\Documents\Coding Projects\learning-dash\my-apps\FAO.csv",
                 encoding="ISO-8859-1")

year_col_names = list(df.columns[10:])

filtered_df = df[(df["Area"] == "Afghanistan") &
                 (df["Item"] == "Wheat and products") &
                 (df["Element"] == "Food")]

filtered_df[year_col_names].values.tolist()[0]
year_col_names
