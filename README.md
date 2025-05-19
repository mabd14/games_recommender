# Semantic Games Recommender

This is a project I undertook as my Capstone Project at Digitial Futures. It incorporates  Natural Language Processing (NLP), by using OpenAI's embedding model.   
Embeddings are representations of text as high-dimensional vectors that preserve the relationships between words or sentences based on their meaning, enabling more meaningful comparisons than simple keyword matching.  
Essentially, a semantic recommender finds games by comparing the meaning of game descriptions using these text embeddings.

To use this, first you need to download all the required modules from `requirements.txt`

```
pip install -r requirements.txt
```

Then, I also have a webscrapper attached, to get the top 10,000 popular games currently on Steam. You just need to run the cell blocks on **Jupyter Notebook**., `steamscrapper.ipynb`.  This will give you your dataset. Or if you want, you can use the `tagged_description.txt` as your dataset. 

**WARNING**  
If you do decide to use your own dataset, after collecting the data from Steam, ensure that you created an extra column, name it `*tagged_description*, and attach a unique ID and then the games description. The way the recommender works is that it will recommend based on the games descriptoion, and by attaching a unique ID to every games description, you can use that to call the dataset, and get all the information of the game from the unique ID.  

After getting the dataset, you will need to get an OpenAI API key, and insert it into a file called `.env`. This will hide it, and to call it, just use the code below
```
load_dotenv()
```
This can be found in the file, `vector_search.ipynb`.  Follow the **Juypter Notebook**, and when you get to creating your Chroma Database, ensure you change it to a local path, as this is where you similarities will be stored. 

After this, you can the run the `semantic_game_recommender.py`, by running:
```
 streamlit run semantic_game_recommender.py
```
This is a streamlit-built app. 

Thanks for reaching this far, and have fun using my code! If you see any ways I can improve my code, don't hesitate to reach out! I'm always looking for new things to learn!
