from django.db import models
from django.utils import timezone
from django.urls import reverse


# Create your models here.

class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    email = models.EmailField()
    profile_image_url = models.URLField(max_length=500)

    def get_status_messages(self):
        return self.status_messages.all().order_by('-timestamp')
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class StatusMessage(models.Model):
    timestamp = models.DateTimeField(default=timezone.now) #auto stores the time when the message is created 
    message = models.TextField()  #just an ordinary text field
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='status_messages') 

    def get_images(self):
        return self.images.all()
    def __str__(self):
        return f"Status by {self.profile.first_name}: {self.message[:30]}..."
    


    




class Image(models.Model):
    image_file = models.ImageField(upload_to='images/')
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE, related_name="images")
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Image for {self.status_message} at {self.timestamp}"

# class Friends(models.Model):
#     profiles = 