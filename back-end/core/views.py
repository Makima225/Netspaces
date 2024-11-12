# views.py
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .serializers import UserRegisterSerializer, ArticleSerializer, LikeSerializer, CommentSerializer
from django.contrib.auth.models import User
from .models import Article, Like, Comment

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()  # Facultatif ici, mais c'est utile si vous avez besoin de la liste d'objets
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]  # Permet à n'importe qui d'accéder à cette vue

    def perform_create(self, serializer):
        # Vous pouvez éventuellement personnaliser la création de l'utilisateur ici
        serializer.save()

class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Retourne l'utilisateur actuellement connecté
        return self.request.user


class ArticleCreateView(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]


class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]


class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]


class ArticleUpdateView(generics.UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Ensure that users can only update their own articles.
        """
        return self.queryset.filter(author=self.request.user)
    

class ArticleDeleteView(generics.DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Ensure that users can only update their own articles.
        """
        return self.queryset.filter(author=self.request.user)


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


class CommentUpdateView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        # Vérifier que l'utilisateur est le propriétaire du commentaire
        comment = self.get_object()
        if comment.user != self.request.user:
            raise PermissionDenied("Vous n'avez pas la permission de modifier ce commentaire.")
        serializer.save()



class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]    

    def perform_destroy(self, instance):
        # Vérifier que l'utilisateur est le propriétaire du commentaire
        if instance.user != self.request.user:
            raise PermissionDenied("Vous n'avez pas la permission de supprimer ce commentaire.")
        instance.delete()


class LikeCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        article = Article.objects.get(pk=pk)
        user = request.user

        # Vérifier si l'utilisateur a déjà liké l'article
        like, created = Like.objects.get_or_create(article=article, user=user)

        if not created:
            # Si l'utilisateur a déjà liké l'article, on annule le like
            like.delete()
            return Response({"message": "Like retiré."}, status=status.HTTP_200_OK)

        return Response({"message": "Article liké."}, status=status.HTTP_201_CREATED)

