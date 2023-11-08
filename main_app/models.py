from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


TOPIC_CHOICES = [
  ('Advice, Digital, Social Media', 'Advice, Digital, Social Media'),
  ('Advice, Lifestyle', 'Advice, Lifestyle'),
  ('Arts and Culture', 'Arts and Culture'),
  ('Beauty and Skincare', 'Beauty and Skincare'),
  ('Books', 'Books'),
  ('Education and Learning', 'Education and Learning'),
  ('Fashion', 'Fashion'),
  ('Fitness and Exercise', 'Fitness and Exercise'),
  ('Food', 'Food'),
  ('Interior Design', 'Interior Design'),
  ('Mindfulness', 'Mindfulness'),
  ('Movies', 'Movies'),
  ('Music', 'Music'),
  ('Nutrition', 'Nutrition'),
  ('Psycholody, Advice', 'Psychology, Advice'),
  ('Photography', 'Photography'),
  ('Recipes', 'Recipes'),
  ('Stories', 'Stories'),
  ('Travel', 'Travel'),
  ('Hobbies', 'Hobbies'),
]

class Article(models.Model):
  title = models.CharField(max_length=150)
  content_main = models.TextField()  
  content_section_1 = models.TextField(null=True, blank=True)  
  content_section_2 = models.TextField(null=True, blank=True) 
  likes = models.IntegerField(default=0)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  topic = models.CharField(
    max_length=50,
    choices=TOPIC_CHOICES,
    default=TOPIC_CHOICES[1][1]
  )
  created_at = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('article-detail', kwargs={'article_id': self.id})
  
class Photo(models.Model):
  url = models.CharField(max_length=250)
  article = models.ForeignKey(Article, related_name='photos', on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for article_id: {self.article_id} @{self.url}"