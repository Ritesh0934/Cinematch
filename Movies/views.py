from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Movie, Review
from .forms import ReviewForm
from .api_helper import get_popular_movies, get_movie_details, search_movies
from datetime import datetime

# 🎬 Home Page — shows popular movies
def home(request):
    try:
        movies = get_popular_movies()
    except Exception as e:
        print("TMDB API error:", e)
        movies = []
    return render(request, "Movies/home.html", {"movies": movies})


# 🔍 Search Movies Page
def search(request):
    query = request.GET.get("q")
    movies = []
    if query:
        try:
            movies = search_movies(query)
        except Exception as e:
            print("Search error:", e)
    context = {
        "query": query,
        "movies": movies
    }
    return render(request, "Movies/search.html", context)


# 🎞 Movie Detail Page (with similar movies + reviews)
def movie_detail(request, movie_id):
    # 1️⃣ Get movie details from TMDB
    movie_data = get_movie_details(movie_id)

    # 2️⃣ Safely handle release_date (fix for ValidationError)
    release_date_str = movie_data.get("release_date")
    if release_date_str:
        try:
            release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date()
        except ValueError:
            release_date = None
    else:
        release_date = None

    # 3️⃣ Save movie info locally (to link reviews)
    movie, created = Movie.objects.get_or_create(
        tmdb_id=movie_id,
        defaults={
            "title": movie_data.get("title", "Unknown"),
            "poster_url": f"https://image.tmdb.org/t/p/w500{movie_data['poster_path']}" if movie_data.get("poster_path") else "",
            "overview": movie_data.get("overview", ""),
            "release_date": release_date,  # ✅ properly handled
            "tmdb_rating": movie_data.get("vote_average", 0),
        }
    )

    # 4️⃣ Fetch all reviews for this movie
    reviews = movie.reviews.all().order_by("-created_at")

    # 5️⃣ Handle new review submission
    if request.method == "POST":
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                # Prevent duplicate review by same user
                existing_review = Review.objects.filter(user=request.user, movie=movie).first()
                if existing_review:
                    messages.warning(request, "You’ve already reviewed this movie.")
                else:
                    review = form.save(commit=False)
                    review.user = request.user
                    review.movie = movie
                    review.save()
                    messages.success(request, "Your review has been added!")
                return redirect("movie_detail", movie_id=movie_id)
            else:
                messages.error(request, "Invalid form input. Please try again.")
        else:
            messages.warning(request, "Please log in to post a review.")
            return redirect("login")
    else:
        form = ReviewForm()

    # 6️⃣ Get similar movie recommendations (optional)
    similar = movie_data.get("similar", {}).get("results", [])[:6]

    # 7️⃣ Render detail page
    context = {
        "movie": movie_data,       # Data from TMDB
        "movie_obj": movie,        # Local DB object
        "reviews": reviews,
        "form": form,
        "similar": similar,
    }
    return render(request, "Movies/movie_detail.html", context)


# ❤ Optional: List of user’s own reviews
@login_required(login_url="/Auth/login/")
def my_reviews(request):
    user_reviews = Review.objects.filter(user=request.user).select_related("movie").order_by("-created_at")
    return render(request, "Movies/my_reviews.html", {"reviews": user_reviews})