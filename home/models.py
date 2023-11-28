from django.db import models
from django.contrib.auth.models import User 
from django.urls import reverse
#from django.db.models import CharField , TextField




class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='posts')  # You can specify a valid user's ID as the default.
    body = models.TextField()
    slug = models.SlugField()
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created' , )

    def __str__(self):
        return self.slug
    
    def get_absolute_url(self):
        return reverse('home:post_detail' , args=(self.id , self.slug))
    
    def likes_count(self):
        return self.pvotes.count()
    
    def user_can_like(self,user):
        user_like=user.uvotes.filter(post=self)
        if user_like.exists():
            return True
        return False
 

    

class Comment(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='ucomment' )
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name='pcomment' )
    reply = models.ForeignKey('self' , on_delete=models.CASCADE , related_name='rcomment' , blank=True , null=True ) #نزارری گیر میده که باید پر کنی 
    #reply = models.ForeignKey('comment' , on_delete=models.CASCADE , related_name='rcomment' )
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}  -  {self.body[:30]}'


class Vote(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='uvotes' )
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name='pvotes' )

    def __str__(self):
         return f'{self.user}  Liked  {self.post.slug}'

# Create your models here.
