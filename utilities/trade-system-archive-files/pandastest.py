import pandas as pd

df = pd.DataFrame()

df["test"] = [[1,2,3],[1,2,3],[1,2,3],[1,2,3],[1,2,3]]

print(df)
print()
print(df["test"][0][0])