# urls.py
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserRegisterView, ArticleCreateView, ArticleListView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView, LikeCreateView, CommentCreateView, CommentUpdateView, CommentDeleteView

urlpatterns = [
    # Register and login
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    # Articles
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('articles/<int:pk>/update/', ArticleUpdateView.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),

    # Ajouter un like
    path('articles/<int:pk>/like/', LikeCreateView.as_view(), name='like-create'),

    # Ajouter un commentaire
    path('articles/<int:pk>/comment/', CommentCreateView.as_view(), name='comment-create'),

    # Modifier un commentaire 
    path('articles/<int:pk>/comment-update/', CommentUpdateView.as_view(), name='comment-update'),
    
    # Supprimer un commentaire 
    path('articles/<int:pk>/comment-delete/', CommentDeleteView.as_view(), name='comment-delete'),



]
