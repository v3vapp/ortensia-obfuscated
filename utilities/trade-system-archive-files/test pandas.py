import pandas as pd

df = pd.DataFrame({'legs': [23, 44, 85, 50],
                   'wings': [58, 10, 62, 20],
                   'sample': [16, 26, 41, 83]},
                  index=['falcon', 'dog', 'spider', 'fish'])
        
print(df)

print()

last1_index_legs = df.iloc[-1]["legs"]
last2_index_legs = df.iloc[-2]["legs"]

print("last_index_legs")
print(last1_index_legs)
print(last2_index_legs)


path = "https://atelierkobato.com/wp-content/uploads/person.xlsx"
data = pd.read_excel(path, header=1)
print(data)