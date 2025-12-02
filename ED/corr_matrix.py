import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

data = pd.read_csv("heart.csv")

categorical_cols = ["Sex", "ChestPainType", "RestingECG", "ExerciseAngina", "ST_Slope"]
data_encoded = pd.get_dummies(data, columns=categorical_cols, drop_first=True)

print(data)
corr_matrix = data_encoded.corr()
print("\nMacierz korelacji:")
print(corr_matrix)

plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", center=0)
plt.title("Macierz korelacji ze zmiennymi zakodowanymi")
plt.savefig("br_duke.png")
plt.show()
