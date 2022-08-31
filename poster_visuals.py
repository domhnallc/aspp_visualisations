import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("/home/domhnall/visualisations/ref_digital_software_08_14_21.csv")
df = df.set_index('Type')

# digital submissions
df_digital = df.iloc[0]
df_digital.plot(kind='bar', width=.8, color='black')
plt.show()

# software submissions
df_software = df.iloc[1]
df_software.plot(kind='bar',  width=.8, color=(0.2, 0.4, 0.6, 0.6))
plt.show()

df_digital = df.iloc[0]
fig, ax = plt.subplots()
bars = ax.barh()

