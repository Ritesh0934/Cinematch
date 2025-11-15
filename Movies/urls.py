from django.urls import path
from.import views

urlpatterns = [
    path('',views.home,name = 'home'),
    path('search/',views.search,name = 'search'),
    path('movie/<int:movie_id>',views.movie_detail, name='movie_detail'),
    path('my-reviews/',views.my_reviews,name="my_reviews"),
]