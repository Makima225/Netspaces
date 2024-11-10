from django.contrib.auth.models import User
from .models import Article, Like, Comment
from rest_framework import serializers



class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2' ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas")
        return data

    def create(self, validated_data):
        # Supprime password2 car il n'est pas nécessaire pour la création
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()  # Pour afficher le nom de l'auteur
    likes = LikeSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(source='get_likes_count', read_only=True)
    comments_count = serializers.IntegerField(source='get_comments_count', read_only=True)

    class Meta:
        model = Article
        fields = "__all__"
