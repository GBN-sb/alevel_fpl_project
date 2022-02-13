import pandas as pd

x = 12
num1 = []
num2 = []
result = []
for i in range(x):
    if i != 0:
        num1.append(i)
        num2.append(x-i)
        result.append(i * (x-i))

data = []
data.append(num1)
data.append(num2)
data.append(result)

df = pd.DataFrame(data).transpose()
df.columns = ['no.1', 'no.2', 'result']
print(df.sort_values(by=['result'], ascending=False))
