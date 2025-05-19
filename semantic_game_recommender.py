# streamlit_app.py

import streamlit as st
import openai
from games_recommender import retrieve_semantic_recommendations
import pandas as pd
from dotenv import load_dotenv
import ast

st.set_page_config(page_title="Semantic Game Recommender", layout="wide")
st.title("Game Recommender")
st.markdown("Welcome to my game recommender! This is for anyone looking for a new game to play! Just enter in a concept or a description of the game you want to play, add in some filters if you want, and play away!")

load_dotenv()

# Load and prepare tag data
clean_data = pd.read_csv('cleaned_data.csv')
clean_data["Tags"] = clean_data["Tags"].apply(ast.literal_eval)  # Safer than eval
df_exploded = clean_data.explode('Tags')
unique_tags = sorted(df_exploded["Tags"].dropna().unique())

# Get number of years
years = pd.to_datetime(clean_data["Release Date"], errors="coerce").dt.year
unique_years = sorted(years.dropna().unique())

# Get unique reviews
unique_reviews = clean_data['Review'].dropna().unique()


# UI inputs
st.title("Game & Concept Search")

with st.container():
    st.subheader("Search Criteria")
    
    query = st.text_input("Describe a game or concept you like")

    # Use columns to align inputs neatly
    col1, col2 = st.columns(2)
    with col1:
        number_of_results = st.number_input(
            "Number of results", value=10, min_value=1
        )
    with col2:
        exclude_nsfw = st.checkbox("Exclude NSFW content", value=True)

with st.container():
    st.subheader("Filters")

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_tags = st.multiselect("Tags", options=unique_tags)
    with col2:
        selected_year = st.multiselect("Year", options=unique_years)
    with col3:
        selected_review = st.multiselect("Reviews", options=unique_reviews)

# NSFW tags definition remains internal (not shown to user)
nsfw_tags = {"NSFW", "Adult", "Mature", "Sexual Content", "Nudity"}  # Update as needed


# Handle recommendation request
if query:
    with st.spinner("Finding games you might like..."):
        try:
            results = retrieve_semantic_recommendations(query, number_of_results * 100)
            
            # Ensure Tags column is treated as a list
            results["Tags"] = results["Tags"].apply(ast.literal_eval)

            # Filter by selected tags (if any)
            if selected_tags:
                results = results[results['Tags'].apply(lambda tags: all(tag in tags for tag in selected_tags))]

            # Filter by selected year(s)
            if selected_year:
                results = results[
                pd.to_datetime(results['Release Date'], errors='coerce').dt.year.isin(selected_year)
                ]

            if selected_review:
                results = results[results['Review'].isin(selected_review)]


            # Filter out NSFW content if selected
            if exclude_nsfw:
                results = results[results['Tags'].apply(lambda tags: not any(tag in nsfw_tags for tag in tags))]

            

            # Only return the top n filtered results
            results = results.head(number_of_results)

            # Display results
            st.subheader("🧠 Recommended Games")
            for _, row in results.iterrows():
            # Create a two-column layout: image | info
                col1, col2 = st.columns([1, 3])  # Adjust ratio as needed

                with col1:
                    st.image(row['Images'], use_column_width=True)

                with col2:
                    # Game title with link
                    st.markdown(f"### [{row['Name']}]({row['Links']})")

                    # Short description (truncate if too long)
                    description = row['Description']
                    if len(description) > 300:
                        description = description[:300] + "..."

                    st.markdown(description)

                    # Tags and release date
                    tags_str = ", ".join(row['Tags'])
                    st.markdown(f"**Tags:** {tags_str}")
                    st.markdown(f"**Release Date:** {row['Release Date']}")

            st.markdown("---")  # Divider


        except Exception as e:
            st.error(f"Error: {e}")
