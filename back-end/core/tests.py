from django.test import TestCase
from django.contrib.auth.models import User
from .models import Article, Like, Comment

class ArticleModelTest(TestCase):

    def setUp(self):
        # Crée un utilisateur
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Crée un article
        self.article = Article.objects.create(
            title='Test Article',
            content='This is the content of the article.',
            description='This is a test description.',
            author=self.user
        )

    def test_article_creation(self):
        # Teste la création de l'article
        self.assertEqual(self.article.title, 'Test Article')
        self.assertEqual(self.article.author, self.user)
        self.assertIsNotNone(self.article.created_at)

    def test_str_method(self):
        # Vérifie la méthode __str__ de l'article
        self.assertEqual(str(self.article), 'Test Article')

    def test_get_likes_count(self):
        # Ajoute des likes et vérifie le compte de likes
        Like.objects.create(user=self.user, article=self.article)
        self.assertEqual(self.article.get_likes_count(), 1)

    def test_get_comments_count(self):
        # Ajoute des commentaires et vérifie le compte de commentaires
        Comment.objects.create(user=self.user, article=self.article, content="Nice article!")
        self.assertEqual(self.article.get_comments_count(), 1)


class LikeModelTest(TestCase):

    def setUp(self):
        # Crée un utilisateur et un article
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.article = Article.objects.create(
            title='Test Article',
            content='This is the content of the article.',
            author=self.user
        )

    def test_like_creation(self):
        # Crée un like et vérifie sa création
        like = Like.objects.create(user=self.user, article=self.article)
        self.assertEqual(str(like), 'testuser likes Test Article')

    def test_unique_like(self):
        # Vérifie qu'un utilisateur ne peut pas liker deux fois le même article
        Like.objects.create(user=self.user, article=self.article)
        with self.assertRaises(Exception):
            Like.objects.create(user=self.user, article=self.article)


class CommentModelTest(TestCase):

    def setUp(self):
        # Crée un utilisateur et un article
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.article = Article.objects.create(
            title='Test Article',
            content='This is the content of the article.',
            author=self.user
        )

    def test_comment_creation(self):
        # Crée un commentaire et vérifie sa création
        comment = Comment.objects.create(user=self.user, article=self.article, content="Great article!")
        self.assertEqual(str(comment), 'Comment by testuser on Test Article')

