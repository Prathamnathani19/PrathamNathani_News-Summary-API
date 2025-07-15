from django.urls import path
from .views import RegisterView, LatestNewsView, SearchNewsView, SaveArticleView, SavedArticlesView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),

    path('news/latest/', LatestNewsView.as_view()),
    path('news/search/', SearchNewsView.as_view()),
    path('news/save/', SaveArticleView.as_view()),
    path('news/saved/', SavedArticlesView.as_view()),
]
