import pandas as pd

df = pd.read_csv("data/manual_data.csv",encoding="cp949")
#중복 제거 (source 기준)
df = df.drop_duplicates(subset=["source"]).reset_index(drop=True)
#결측치 제거
df = df.dropna(subset=["source", "target"])
#양쪽 공백 제거
df["source"] = df["source"].str.strip()
df["target"] = df["target"].str.strip()
#정제된 데이터 저장
df.to_csv("data/clean_data.csv", index=False)



#train, test data로 나눔 
from sklearn.model_selection import train_test_split

df = pd.read_csv("data/clean_data.csv",encoding="utf-8-sig")

train_df, valid_df = train_test_split(
    df,
    test_size=0.2,
    random_state=42,      # 재현성 확보
    shuffle=True
)
# 파일 저장
train_df.to_csv("data/train.csv", index=False)
valid_df.to_csv("data/valid.csv", index=False)