from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.utils import timezone


class User(AbstractUser):
    roll_no=models.CharField(max_length=10,blank=True,null=True,unique=True)
    reg_no=models.IntegerField(blank=True,null=True,unique=True)
    dep=models.CharField(max_length=50,blank=True,null=True)
    year=models.CharField(max_length=50,blank=True,null=True)
    ph_no=models.IntegerField(null=True,blank=True)
    filed=models.CharField(max_length=50,blank=True,null=True)
    rating=models.IntegerField(blank=True,null=True)
    linkedin=models.CharField(max_length=200,blank=True,null=True)
    github=models.CharField(max_length=200,blank=True,null=True)
    profile_pic = models.ImageField(upload_to='images/')
    hostel=models.CharField(max_length=20,blank=True,null=True)
    people=models.CharField(max_length=50,blank=True,null=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post by {self.user.username} at {self.created_at}'

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def comment_count(self):
        return self.comments.count()


class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.post.id}"
    

class Certificate(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    googledrive_link = models.URLField(max_length=500)
    about_certificate = models.TextField()
    uploaded_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Certificate for {self.student.username} uploaded at {self.uploaded_at}"
    
class Skill(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    skill_name = models.CharField(max_length=100)
    added_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.skill_name} by {self.student.username}"
    
class Timeline(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="timeline_posts")
    content = models.TextField(blank=True, null=True)  # Post text content
    media_link = models.URLField(blank=True, null=True)  # Optional media link (Google Drive URL)
    created_at = models.DateTimeField(default=now)  # Record upload time

    def __str__(self):
        return f"{self.student.username} at {self.created_at}"
    
class Club(models.Model):
    name = models.CharField(max_length=100)  # Club name
    logo = models.ImageField(upload_to="club_logos/", blank=True, null=True)  # Club logo
    head = models.CharField(max_length=100)  # Head of the club
    email = models.EmailField()  # Contact email

    def __str__(self):
        return self.name
    

class Startup(models.Model):
    company_name = models.CharField(max_length=200)  # Company Name
    logo = models.ImageField(upload_to="startup_logos/", blank=True, null=True)  # Logo
    founder_name = models.CharField(max_length=100)  # Founder's name
    founder_profile_pic = models.ImageField(upload_to="founder_profiles/", blank=True, null=True)  # Founder's Profile Picture
    types_of_company = models.CharField(max_length=200)  # Type of company
    email = models.EmailField()  # Contact email
    phone = models.CharField(max_length=15)  # Contact phone number
    role_of_company = models.TextField(blank=True, null=True)  # Role of the company in its industry
    # founder email

    def __str__(self):
        return self.company_name
    

class faculty(models.Model):
    username =models.CharField(max_length=100)
    user_id =models.CharField(max_length=100,unique=True)
    dep = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    ph_no=models.IntegerField(null=True,blank=True)
    profile_pic = models.ImageField(upload_to='images/')
    linkedin=models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):
        return self.user_id
    
# Story
User = get_user_model()
class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
    media = models.FileField(upload_to='story_media/')  # Allow media upload
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set upon creation
    expiry_time = models.DateTimeField(blank=True, null=True)  # Expiry time for the story (set 24 hours later)

    def is_expired(self):
        """Check if the story has expired."""
        return timezone.now() > self.expiry_time

    def save(self, *args, **kwargs):
        """Set expiry_time to 24 hours after creation."""
        if not self.expiry_time and self.created_at:
            # Ensure `created_at` is already populated
            self.expiry_time = self.created_at + timezone.timedelta(hours=24)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s story at {self.created_at}"
    


