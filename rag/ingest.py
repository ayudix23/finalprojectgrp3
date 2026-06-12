from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

import pandas as pd

df = pd.read_csv(
    "datasets/processed/amazon_clean.csv"
)

documents = []

for _, row in df.iterrows():

    content = f"""
    Product Id: {row['product_id']}
    Product Name: {row['product_name']} 
    category: {row['category']}
    discount: {row['discounted_price']}
    actual price: {row['actual_price']}
    rating: {row['rating']}
    Description: {row['about_product']}
    User ID: {row['user_id']}
    User Name: {row['user_name']}
    Review Title: {row['review_title']}
    Review Id: {row['review_id']}
    Review: {row['review_content']}
    """

    documents.append(
        Document(page_content=content)
    )

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma.from_documents(
    documents,
    embedding,
    persist_directory="./chroma_db"
)

db.persist()

print("vector db created")