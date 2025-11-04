from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MarketItem(models.Model):
    PROVINCE_CHOICES = [
        ('Punjab', 'Punjab'),
        ('Sindh', 'Sindh'),
        ('KPK', 'KPK'),
        ('Balochistan', 'Balochistan'),
    ]

    name = models.CharField(max_length=100)
    price = models.FloatField()
    date = models.DateField(auto_now_add=True)
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES)
    category = models.CharField(max_length=50, choices=[
        ('Fruit', 'Fruit'),
        ('Vegetable', 'Vegetable'),
    ])

    def __str__(self):
        return f"{self.name} ({self.category}) - {self.province}"
    

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.post.title}"