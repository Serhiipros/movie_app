import requests



headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiZDM1MzRlYzM1NTFhYmU0NDJlZTQ0YTgzY2IyNWE1YyIsIm5iZiI6MTczNzk5NzI4Ny42MzIsInN1YiI6IjY3OTdiYmU3MGEzMGQ2ZDA1OTI0MjBlMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.J5KJ4D29Oy3GM45qZjI6uP8KVzdzfMZ522A9shEDkDI"
}

def get_popular_movies(page=1):
    global headers
    url = f"https://api.themoviedb.org/3/movie/popular?language=en-US&page={page}"
    response = requests.get(url, headers=headers)

    if response.status_code==200:
        data=response.json()
        return data.get("results", [])
    else:
        print("Failed get popular:", response.status_code)
              
        return []
    




def get_toprated_movies():
    global headers
    url = "https://api.themoviedb.org/3/movie/top_rated?language=en-US&page=1"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])
    else:
        print("Failed get top rated: ", response.status_code)
        return []






def get_upcoming_movies():
    global headers
    url = "https://api.themoviedb.org/3/movie/upcoming?language=en-US&page=1"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])
    else:
        print("Failed get upcoming rated: ", response.status_code)
        return []







def get_movies_details(movie_id):
    global headers
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed get upcoming rated: ", response.status_code)
        return []

def get_images_detail(movie_id):
    global headers
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/images?include_image_language=en"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed get images: ", response.status_code)
        return {}

def get_movie_videos(movie_id):
    global headers
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?language=en-US"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])
    else:
        print("Failed get videos: ", response.status_code)
        return []


def get_recomendations_films(movie_id):
    global headers
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?language=en-US&page=1"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])
    else:
        print("Failed get recomendations: ", response.status_code)
        return []



def search_movies_db(query, page=1):
    global headers
    url = f"https://api.themoviedb.org/3/search/movie?query={query}&include_adult=true&language=en-US&page={page}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])
    else:
        print("Failed search movies: ", response.status_code)
        return []




