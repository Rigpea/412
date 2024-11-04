from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profiles")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    email = models.EmailField()
    profile_image_url = models.URLField(max_length=500)

    def get_status_messages(self):
        return self.status_messages.all().order_by('-timestamp')
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})
    def get_friends(self):

        #get all friends that is the person appears in eigther col1 or col2 and return

        friends = []
        profile1 = Friend.objects.filter(profile1=self)
        profile2 = Friend.objects.filter(profile2=self)

        for friend in profile1:
            friends.append(friend.profile2) 

        for friend in profile2:
            friends.append(friend.profile1) 
        return friends  
    def add_friend(self, other):
        #Rejection of friends
        if self == other: 
            return
        if other in self.get_friends():
            return 
        # Add the relation
        Friend.objects.create(profile1=self, profile2=other)
    def get_friend_suggestions(self):
       current_friends = self.get_friends()
       return Profile.objects.exclude(id__in=[friend.id for friend in current_friends] + [self.id])

    def get_news_feed(self):
        own_status_message = StatusMessage.objects.filter(profile=self).values_list('id', flat=True)

        friends = self.get_friends()
        friends_status_message = StatusMessage.objects.filter(profile__in = friends).values_list('id', flat=True)

        all_messages = list(own_status_message) + list(friends_status_message)



        feed = StatusMessage.objects.filter(id__in=all_messages).order_by('-timestamp')
        return feed


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

class Friend(models.Model):
    profile1 = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(default=timezone.now)  #anivarsary

    def __str__(self):
        # p1 is friends with p2
        return f"{self.profile1} & {self.profile2}"