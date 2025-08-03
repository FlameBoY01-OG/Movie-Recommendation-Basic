# Movie Recommendation System

A content-based movie recommender that suggests similar movies based on genres, keywords, cast, and director. Built using the TMDB Movie Metadata dataset and deployed with a Streamlit UI.

---

## 🔧 Features
- Content-based filtering using metadata (genres, keywords, cast, director)  
- Text vectorization with `CountVectorizer` and cosine similarity  
- Precomputed pickle files (`movie.pkl`, `similarity.pkl`) for fast startup  
- Interactive web UI built with Streamlit  

---

## 📁 Project Structure
```text
movie-recommender/
├── data/                     # Folder for raw CSV files
│   ├── tmdb_5000_movies.csv
│   └── tmdb_5000_credits.csv
├── movie_recomm.ipynb        # Jupyter notebook to build the model & pickles
├── app.py                    # Streamlit UI script
├── movie.pkl                 # Pickled DataFrame with processed movie data
├── similarity.pkl            # Pickled cosine similarity matrix
├── requirements.txt          # Python dependencies
└── README.md                 # This file
---
**Download the TMDB data files**  
   - Go to the Kaggle dataset: https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata  
   - Download **tmdb_5000_movies.csv** and **tmdb_5000_credits.csv**  
   - Place both files into the `data/` folder
