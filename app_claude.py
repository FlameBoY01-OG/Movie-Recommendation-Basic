import streamlit as st
import pickle
import time

# Page configuration
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main container styling */
    .main .block-container {
        padding: 2rem 3rem 10rem 3rem;
        max-width: 1200px;
    }

    /* Background and body styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Animated stars background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, #eee, transparent),
            radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.8), transparent),
            radial-gradient(1px 1px at 90px 40px, #fff, transparent),
            radial-gradient(1px 1px at 130px 80px, rgba(255,255,255,0.6), transparent),
            radial-gradient(2px 2px at 160px 30px, #ddd, transparent);
        background-repeat: repeat;
        background-size: 200px 100px;
        animation: sparkle 3s linear infinite;
        pointer-events: none;
        z-index: -1;
    }

    @keyframes sparkle {
        from { transform: translateY(0px); }
        to { transform: translateY(-100px); }
    }

    /* Title styling */
    .main-title {
        font-size: 3rem !important;
        font-weight: 800 !important;
        background: linear-gradient(45deg, #fff, #f0f8ff, #e6e6fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 1rem !important;
        text-shadow: 0 0 30px rgba(255,255,255,0.3);
        letter-spacing: -2px;
        animation: fadeInDown 1s ease-out;
    }

    .subtitle {
        font-size: 1.2rem;
        color: rgba(255,255,255,0.9);
        text-align: center;
        font-weight: 300;
        max-width: 100%;
        margin: 0 auto 2rem auto;
        line-height: 1.6;
        animation: fadeInDown 1s ease-out 0.2s both;
        padding: 0 1rem;
    }

    /* Card container styling */
    .main-card {
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 3rem;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        animation: fadeInUp 1s ease-out 0.3s both;
    }

    /* Selectbox styling */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.95);
        border: none;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }

    .stSelectbox > div > div:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.2);
        background: white;
    }

    .stSelectbox > div > div > div {
        color: #2d3748 !important;
    }

    .stSelectbox > div > div input {
        color: #2d3748 !important;
    }

    .stSelectbox label {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        color: white !important;
        text-align: center;
        margin-bottom: 1rem !important;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 6px 20px rgba(238, 90, 36, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin-top: 1rem !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 30px rgba(238, 90, 36, 0.6) !important;
    }

    .stButton > button:active {
        transform: translateY(-1px) !important;
    }

    /* Results section styling */
    .results-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        text-align: center;
        margin: 2rem 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        animation: fadeInUp 1s ease-out;
    }

    /* Movie cards styling */
    .movie-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255,255,255,0.2);
        margin: 1rem 0;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.6s ease-out both;
    }

    .movie-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
        background-size: 300% 300%;
        animation: gradientShift 3s ease infinite;
    }

    .movie-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        background: rgba(255,255,255,0.2);
    }

    .movie-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: white;
        line-height: 1.4;
        text-shadow: 0 1px 3px rgba(0,0,0,0.3);
        text-align: center;
    }

    /* Loading animation */
    .loading-container {
        text-align: center;
        padding: 3rem;
        animation: fadeInUp 0.5s ease-out;
    }

    .spinner {
        width: 50px;
        height: 50px;
        border: 4px solid rgba(255,255,255,0.3);
        border-left: 4px solid white;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 1rem auto;
    }

    .loading-text {
        color: white;
        font-size: 1.2rem;
        font-weight: 500;
    }

    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }

    /* Success message styling */
    .success-message {
        background: linear-gradient(45deg, #4ecdc4, #44a08d);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(68, 160, 141, 0.3);
        animation: fadeInUp 0.5s ease-out;
    }

    /* Error message styling */
    .error-message {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(238, 90, 36, 0.3);
        animation: fadeInUp 0.5s ease-out;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem !important;
        }

        .main-card {
            padding: 2rem;
            margin: 1rem;
        }

        .main .block-container {
            padding: 1rem 2rem 5rem 2rem;
        }
    }

    /* Column styling for movie grid */
    .movie-grid {
        display: grid;
        gap: 1rem;
    }

    /* Hide Streamlit column gaps */
    .row-widget.stHorizontal > div {
        padding: 0 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


def recommend(name):
    """Get movie recommendations based on similarity matrix."""
    try:
        movie_index = movies[movies["title"] == name].index[0]
        distance = similarity[movie_index]
        movie_list = sorted(list(enumerate(distance)), reverse=True, key=(lambda x: x[1]))[1:6]
        recommended_movies = []

        for i in movie_list:
            recommended_movies.append(movies.iloc[i[0]]["title"])

        return recommended_movies
    except Exception as e:
        st.error(f"Error getting recommendations: {str(e)}")
        return []


def display_movie_card(movie, delay=0):
    """Display a beautifully styled movie recommendation card."""
    card_html = f"""
    <div class="movie-card" style="animation-delay: {delay}s;">
        <span class="movie-title">{movie}</span>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def show_loading():
    """Display a beautiful loading animation."""
    loading_html = """
    <div class="loading-container">
        <div class="spinner"></div>
        <div class="loading-text">Finding perfect movies for you...</div>
    </div>
    """
    st.markdown(loading_html, unsafe_allow_html=True)


# Initialize session state
if 'recommendations_shown' not in st.session_state:
    st.session_state.recommendations_shown = False
if 'selected_movie' not in st.session_state:
    st.session_state.selected_movie = ""
if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False


# Reset states when movie selection changes
def reset_states():
    st.session_state.recommendations_shown = False
    st.session_state.button_clicked = False


# Load data
@st.cache_data
def load_data():
    """Load movie data and similarity matrix."""
    try:
        movies = pickle.load(open('movies.pkl', 'rb'))
        similarity = pickle.load(open('similarity.pkl', 'rb'))
        return movies, similarity
    except FileNotFoundError:
        st.error(
            "Movie data files not found. Please ensure 'movies.pkl' and 'similarity.pkl' are in the same directory.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()


# Load the data
movies, similarity = load_data()
movies_list = movies["title"].values

# Main card container
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)

    # App header inside the card
    st.markdown('<h1 class="main-title">Movie Recommendation</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Discover your next favorite movie with our intelligent recommendation system. Choose a movie you love, and we\'ll find similar films you\'ll enjoy!</p>',
        unsafe_allow_html=True)

    # Movie selection
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected_movie = st.selectbox(
            "Choose a movie you enjoyed:",
            [""] + list(movies_list),
            key="movie_selector",
            on_change=reset_states
        )

        # Recommendation button
        if st.button("Get Recommendations"):
            if selected_movie:
                st.session_state.selected_movie = selected_movie
                st.session_state.button_clicked = True
                st.session_state.recommendations_shown = True
                st.rerun()
            else:
                st.markdown('<div class="error-message">Please select a movie first!</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Show recommendations
if st.session_state.recommendations_shown and st.session_state.selected_movie and st.session_state.button_clicked:
    st.markdown('<h2 class="results-title">Movies You Might Love</h2>', unsafe_allow_html=True)

    # Show loading animation
    loading_placeholder = st.empty()
    with loading_placeholder.container():
        show_loading()

    # Simulate processing time for better UX
    time.sleep(1.5)
    loading_placeholder.empty()

    # Get recommendations
    recommended_movies = recommend(st.session_state.selected_movie)

    if recommended_movies:
        # Success message
        st.markdown(
            f'<div class="success-message">Based on "{st.session_state.selected_movie}", here are our top recommendations!</div>',
            unsafe_allow_html=True)

        # Display recommendations in a grid
        # Create two columns for better layout
        col1, col2 = st.columns(2)

        for i, movie in enumerate(recommended_movies):
            if i % 2 == 0:
                with col1:
                    display_movie_card(movie, i * 0.1)
            else:
                with col2:
                    display_movie_card(movie, i * 0.1)

        # Add some spacing and a reset button
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Try Another Movie"):
                st.session_state.recommendations_shown = False
                st.session_state.selected_movie = ""
                st.session_state.button_clicked = False
                st.rerun()
    else:
        st.markdown(
            '<div class="error-message">Sorry, we couldn\'t find recommendations for this movie. Please try another one!</div>',
            unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    '<div style="text-align: center; color: rgba(255,255,255,0.7); font-size: 0.9rem; padding: 2rem;">Made with love using Streamlit | Powered by Machine Learning</div>',
    unsafe_allow_html=True
)