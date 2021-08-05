from django.urls import path
from .views import MovieView, MovieRetrieveDestroyView, CriticReviewView, CommentReviewView

urlpatterns = [
    path("movies/", MovieView.as_view()),
    path("movies/<int:movie_id>/", MovieRetrieveDestroyView.as_view()),
    path("movies/<int:movie_id>/review/", CriticReviewView.as_view()),
    path("movies/<int:movie_id>/comments/", CommentReviewView.as_view())
]