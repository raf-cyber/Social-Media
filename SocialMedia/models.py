from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    reciever = models.ForeignKey(User, related_name='recieved_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name='friend1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friend2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

# Post for home page
    
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='blog_posts')
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    is_short = models.BooleanField(default=False) 

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.content[:20]
    

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="Anonymous")
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}: {self.body[:20]}'
    


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="bookmarked_by")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'post')  # Ensure that a post is bookmarked only once by the same user

    def __str__(self):
        return f"{self.user.username} bookmarked {self.post.title}"

    def get_absolute_url(self):
        return reverse('bookmarks')

# Profile Picture
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='images/default.png', blank=True, null=True)
    pronouns = models.CharField(max_length=50, blank=True)  # Add this line
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.sender} -> {self.receiver}"
    
class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name='friend1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friend2', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user1.username} is friends with {self.user2.username}"
    
    
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver}'


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cards")  # To associate cards with users
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='card_images/', null=True, blank=True)  # Store images in the 'card_images/' directory
    description = models.TextField()

    def __str__(self):
        return self.title