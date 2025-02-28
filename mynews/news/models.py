from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Use slugify here
        super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')  # Use settings.AUTH_USER_MODEL
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    approved = models.BooleanField(default=False)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True) # Add image field
    likes = models.PositiveIntegerField(default=0)
    unlikes = models.PositiveIntegerField(default=0)
    auto_approve = models.BooleanField(default=False)

    def _generate_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num += 1
        return unique_slug
    
    def save(self, *args, **kwargs):
        if self.author:  # Check if the author is set
            is_trusted = self.author.trusted_users.filter(pk=self.author.pk).exists() #Check if author is trusted
            if is_trusted or self.author.is_superuser:  # Check if author is trusted OR superuser
                self.auto_approve = True
                self.approved = True  # Automatically approve
            else:
                self.auto_approve = False
                self.approved = False  # Do not automatically approve
        super().save(*args, **kwargs)  # Call the original save method
   

    def __str__(self):
        return self.title 
    
@receiver(pre_save, sender=Post)
def post_pre_save(sender, instance, **kwargs):
    if not hasattr(instance, 'title_changed'): #Check for title changed attribute
        instance.title_changed = False #Initialize it

    if not instance.pk:  # New post
        instance.slug = instance._generate_unique_slug()
    elif instance.title_changed: # Check if title has changed
        instance.slug = instance._generate_unique_slug()

    instance.title_changed = False #Reset the title_changed flag

    try: #Try to get the original title
        original_post = Post.objects.get(pk=instance.pk)
    except Post.DoesNotExist:
        instance.title_changed = True #If it doesnt exist its a new post
        return

    if original_post.title != instance.title:
        instance.title_changed = True
    

    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # Allow anonymous comments
    name = models.CharField(max_length=255, blank=True, null=True)  # Name for anonymous users
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies') # For replies

    def __str__(self):
        return f"Comment by {self.user.username if self.user else self.name or 'Anonymous'} on {self.post.title}"

    class Meta:
        ordering = ['timestamp']  # Order comments by timestamp
