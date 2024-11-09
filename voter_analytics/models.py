from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
import csv
from datetime import datetime


# Create your models here.

class Voter(models.Model):
    voter_id = models.CharField(max_length=20, primary_key=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=50)
    precinct_number = models.CharField(max_length=10)  # Changed to CharField
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Precinct {self.precinct_number}"
    
def load_data():
    '''Load data and put it in the Results model'''

    Voter.objects.all().delete()
    #file locaiton
    filename = '/Users/rigs/Desktop/cs412/newton_voters.csv'
    #open file
    table = open(filename)

    headers = table.readline()

    # read a single line 

    for row in table: 
        fields = row.strip().split(',')
        fields = row.split(',')
        #create the voter
        voter = Voter(
                voter_id=fields[0],  
                last_name=fields[1],
                first_name=fields[2],
                street_number=fields[3],
                street_name=fields[4],
                apartment_number=fields[5] if fields[5] else None,
                zip_code=fields[6],
                date_of_birth=fields[7],
                date_of_registration=fields[8],
                party_affiliation=fields[9],
                precinct_number=fields[10],  # Removed int() conversion here
                v20state=True if fields[11].strip().upper() == 'TRUE' else False,
                v21town=True if fields[12].strip().upper() == 'TRUE' else False,
                v21primary=True if fields[13].strip().upper() == 'TRUE' else False,
                v22general=True if fields[14].strip().upper() == 'TRUE' else False,
                v23town=True if fields[15].strip().upper() == 'TRUE' else False,
                voter_score=int(fields[16])
            )

        
        print(f'Created result: {voter}')
        voter.save()
    print('Done.')
