# games_recommender.py

import os
import pandas as pd
from dotenv import load_dotenv
from langchain.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# Optional: Suppress some warnings
import warnings
warnings.filterwarnings("ignore", message="Created a chunk of size.*")

# Load env variables
load_dotenv()

# Load data (can be cached in Streamlit)
df = pd.read_csv("cleaned_data.csv")  # This should contain game ID, title, description etc.


persist_directory = '/Users/mahamedabdulle/Documents/digital futures/capstone/clean_rec' # Change to where you saved your chroma database
db_games = Chroma(
    persist_directory=persist_directory,
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-large")
)


def retrieve_semantic_recommendations(query: str, top_k: int = 10) -> pd.DataFrame:
    recs = db_games.similarity_search(query, k=100)

    games_list = [
        int(doc.page_content.strip().replace('"', "").split()[0])
        for doc in recs
    ]
    return df[df["ID"].isin(games_list)].head(top_k)
