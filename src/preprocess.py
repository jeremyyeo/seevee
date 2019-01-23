import pandas as pd

data = pd.read_csv("data/spam.csv", encoding="latin-1").sample(frac=1).drop_duplicates()
data = data[["v1", "v2"]].rename(columns={"v1": "label", "v2": "text"})

data["label"] = "__label__" + data["label"].astype(str)

data.iloc[0 : int(len(data) * 0.8)].to_csv(
    "data/train.csv", sep="\t", index=False, header=False
)
data.iloc[int(len(data) * 0.8) : int(len(data) * 0.9)].to_csv(
    "data/test.csv", sep="\t", index=False, header=False
)
data.iloc[int(len(data) * 0.9) :].to_csv(
    "data/dev.csv", sep="\t", index=False, header=False
)
