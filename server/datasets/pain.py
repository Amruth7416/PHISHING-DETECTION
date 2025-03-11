import pandas as pd

dataset_path = "datasets/dataset_email.csv" 


# Load CSV while ensuring only two columns are used
df = pd.read_csv(dataset_path, usecols=[0, 1], names=["email", "label"], header=None)

# Save the cleaned dataset
df.to_csv("cleaned_dataset.csv", index=False)
print("Dataset cleaned and saved as cleaned_dataset.csv")
