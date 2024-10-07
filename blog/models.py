#Define data modles (objects) for use in this blog application
#If you add or delete migrate the model otherwise no need
from django.db import models

# Create your models here.
class Article(models.Model):
    '''Encapulates the data for a blog an Article by some Author'''

    #data attributes:
    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    text =  models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        '''Return a string representation of this Article'''
        return f"{self.title} by {self.author}"