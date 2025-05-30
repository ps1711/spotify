
# Spotify Song Recommender System  

## Overview  
This project is a song recommender system that uses Natural Language Processing (NLP) techniques and cosine similarity to recommend songs based on lyrics. It processes the Spotify Million Song Dataset, cleans and preprocesses the text, and applies TF-IDF vectorization to identify similar songs. The recommendation functionality is exposed through a Streamlit application for easy use. It has a sidebar with Gemini Chatbot integration and a preview of song playing through Spotify Web Playback SDK.

---

## Features  
- Preprocessing of song lyrics with tokenization and stemming.  
- TF-IDF vectorization for feature extraction.  
- Cosine similarity-based song recommendations.  
- Interactive user interface via Streamlit for easy song recommendation.
- Gemini API chatbot to resolve user queries
- Spotify WebPlayback SDK to play songs
- Retrieves covers from Spotify

---

## Prerequisites  

### Dependencies  
Install the required Python libraries:  
```bash  
pip install -r requirements.txt  
```  

If you don't have a `requirements.txt`, the dependencies can be manually installed:  
```bash  
pip install pandas scikit-learn nltk streamlit pickle-mixin  
```  

### Environment Variables  
Create a `.env` file in the project directory and add the following keys (if applicable):  
```plaintext  
SPOTIFY_CLIENT_ID=your_spotify_client_id  
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret  
GEMINI_API_KEY=your_gemini_api_key  
```  

### Dataset  
Download the dataset from [Spotify Million Song Dataset](https://www.kaggle.com/datasets/notshrirang/spotify-million-song-dataset).  
Place the dataset file (`spotify_millsongdata.csv`) in the project directory.  

---

## How to Use  

### Step 1: Clone the Repository  
```bash  
git clone https://github.com/NikhilKumarSingh4002/spotify-recommender.git  
cd spotify-recommender  
```  

### Step 2: Run Model Training (Jupyter Notebook)  
Open the `model_training.ipynb` Jupyter notebook in your preferred environment (such as Jupyter Lab or Google Colab) and run all cells. This will preprocess the dataset, apply NLP techniques, and generate the similarity matrix used by the recommender system.  
The notebook will generate the necessary pickle files:  
- `similarity` (stores the cosine similarity matrix)  
- `df` (stores the processed dataset)

### Step 3: Run the Streamlit App  
Launch the Streamlit application to use the recommender system in a user-friendly interface:  
```bash  
streamlit run app.py  
```  

---

## File Structure  
```
📂 spotify-recommender  
├── spotify_millsongdata.csv  # Dataset (to be downloaded separately)  
├── model_training.ipynb      # Jupyter notebook for training the model  
├── app.py                    # Streamlit app for user interface  
├── similarity                # Pickle file storing the similarity matrix  
├── df                        # Pickle file storing processed dataset  
├── .env                      # Environment variables (optional)  
```  

---

## Future Enhancements  
- Add real-time integration with Spotify's API for live recommendations.  
- Include additional song metadata (e.g., genre, artist) to improve recommendation quality.  
- Support for multi-language lyrics.  

---

## License  
This project is licensed under the MIT License.  

---

## Acknowledgements  
- [Kaggle - Spotify Million Song Dataset](https://www.kaggle.com/datasets/notshrirang/spotify-million-song-dataset)  
- Python libraries: Pandas, NLTK, Scikit-learn, Streamlit  
