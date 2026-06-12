import pandas as pd

df = pd.read_csv(
    "datasets/twitter/twitter_clean.csv"
)

def classify(text):

    text = str(text).lower()

    if "refund" in text:
        return "refund"

    elif "order" in text:
        return "order_tracking"

    elif "broken" in text:
        return "complaint"

    elif "recommend" in text:
        return "product_query"

    else:
        return "other"

df["intent"] = df["text"].apply(
    classify
)

df.to_csv(
    "datasets/twitter/intent_data.csv",
    index=False
)

print(df.head())