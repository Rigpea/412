from django import forms
from datetime import datetime

class VoterFilterForm(forms.Form):
    PARTY_CHOICES = [
        ('', 'Any'),
        ('Democrat', 'Democrat'),
        ('Republican', 'Republican'),
        # Add other affiliations as needed
    ]
    VOTER_SCORE_CHOICES = [(str(i), i) for i in range(6)]  # Voter scores from 0 to 5

    party_affiliation = forms.ChoiceField(choices=PARTY_CHOICES, required=False)
    min_dob = forms.ChoiceField(choices=[('', 'Any')] + [(str(year), year) for year in range(1900, datetime.now().year + 1)], required=False)
    max_dob = forms.ChoiceField(choices=[('', 'Any')] + [(str(year), year) for year in range(1900, datetime.now().year + 1)], required=False)
    voter_score = forms.ChoiceField(choices=[('', 'Any')] + VOTER_SCORE_CHOICES, required=False)
    v20state = forms.BooleanField(required=False, label="2020 State Election")
    v21town = forms.BooleanField(required=False, label="2021 Town Election")
    v21primary = forms.BooleanField(required=False, label="2021 Primary")
    v22general = forms.BooleanField(required=False, label="2022 General Election")
    v23town = forms.BooleanField(required=False, label="2023 Town Election")