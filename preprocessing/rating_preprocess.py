import pandas as pd

# 평점 결측치 처리
def rating_preprocess(item_df: pd.DataFrame) -> pd.DataFrame:
    avg_rating = item_df[item_df['rating'].notnull()]['rating'].mean()
    item_df['rating'] = item_df['rating'].fillna(avg_rating)
    return item_df
