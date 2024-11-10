from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)  # Contenu de l'article
    description = models.TextField(blank=True, null=True)  # Description de l'article
    image = models.ImageField(upload_to='articles/', blank=True, null=True)  # Image de l'article (optionnel)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.title

    def get_likes_count(self):
        return self.likes.count()

    def get_comments_count(self):
        return self.comments.count()
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')  # Un utilisateur ne peut liker qu'une seule fois un article

    def __str__(self):
        return f'{self.user.username} likes {self.article.title}'



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.article.title}'

