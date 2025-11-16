import requests

API_KEY = "Enter Your TMDB API KEY"
BASE_URL = "https://api.themoviedb.org/3"

def get_popular_movies(page=1, language="en-US"):
    url = f"{BASE_URL}/movie/popular"
    params = {
        "api_key": API_KEY,
        "language": language,
        "page": page
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Error fetching popular movies:", response.status_code, response.text)
        return []
    return response.json().get("results", [])

def get_movie_details(movie_id, language="en-US"):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": API_KEY,
        "language": language,
        "append_to_response": "similar"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Error fetching movie details:", response.status_code, response.text)
        return {}
    return response.json()

def search_movies(query, page=1, language="en-US"):
    url = f"{BASE_URL}/search/movie"
    params = {
        "api_key": API_KEY,
        "query": query,
        "page": page,
        "language": language
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Error searching movies:", response.status_code, response.text)
        return []
    return response.json().get("results", [])
