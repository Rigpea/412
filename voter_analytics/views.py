from datetime import datetime
from django.views.generic import ListView, DetailView
from .models import Voter
from .forms import VoterFilterForm
import plotly.express as px
import plotly.graph_objs as go
from django.db.models import Count



class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    form_class = VoterFilterForm
    context_object_name = 'voters'
    paginate_by = 100  # Show 100 records per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Generate the list of years from 1900 to the current year
        current_year = datetime.now().year
        context['years'] = range(1900, current_year + 1)
        
        # Provide range for voter_score from 0 to 5
        context['voter_scores'] = range(6)

        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        form = VoterFilterForm(self.request.GET)

        if form.is_valid():
            # Retrieve filter values from form data

            #Use of GPT was done to do the quring: 

            party_affiliation = form.cleaned_data.get('party_affiliation')
            min_dob = form.cleaned_data.get('min_dob')
            max_dob = form.cleaned_data.get('max_dob')
            voter_score = form.cleaned_data.get('voter_score')
            
            # Apply filters if specified 
            if party_affiliation:
                queryset = queryset.filter(party_affiliation=party_affiliation)
            if min_dob:
                queryset = queryset.filter(date_of_birth__gte=f"{min_dob}-01-01")
            if max_dob:
                queryset = queryset.filter(date_of_birth__lte=f"{max_dob}-12-31")
            if voter_score:
                queryset = queryset.filter(voter_score=voter_score)

            # Boolean filters for elections
            if form.cleaned_data['v20state']:
                queryset = queryset.filter(v20state=True)
            if form.cleaned_data['v21town']:
                queryset = queryset.filter(v21town=True)
            if form.cleaned_data['v21primary']:
                queryset = queryset.filter(v21primary=True)
            if form.cleaned_data['v22general']:
                queryset = queryset.filter(v22general=True)
            if form.cleaned_data['v23town']:
                queryset = queryset.filter(v23town=True)

        return queryset
            


class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'



class GraphListView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        queryset = super().get_queryset()
        form = VoterFilterForm(self.request.GET)

        if form.is_valid():
            party_affiliation = form.cleaned_data.get('party_affiliation')
            min_dob = form.cleaned_data.get('min_dob')
            max_dob = form.cleaned_data.get('max_dob')
            voter_score = form.cleaned_data.get('voter_score')

            if party_affiliation:
                queryset = queryset.filter(party_affiliation=party_affiliation)
            if min_dob:
                queryset = queryset.filter(date_of_birth__gte=f"{min_dob}-01-01")
            if max_dob:
                queryset = queryset.filter(date_of_birth__lte=f"{max_dob}-12-31")
            if voter_score:
                queryset = queryset.filter(voter_score=voter_score)

            for field in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
                if form.cleaned_data.get(field):
                    queryset = queryset.filter(**{field: True})

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
     
        context['form'] = VoterFilterForm(self.request.GET)

        # G1
        by = [v.date_of_birth.year for v in self.get_queryset()]
        birth_year_dist = px.histogram(x=by, title="YOB distribution of voters")
        birth_year_dist.update_layout(xaxis_title="Year of Birth", yaxis_title="Count of Voters")
        context['birth_year_chart'] = birth_year_dist.to_html(full_html=False)

        # G2
        party_counts = self.get_queryset().values('party_affiliation').annotate(count=Count('party_affiliation'))
        party_labels = [item['party_affiliation'] for item in party_counts]
        party_values = [item['count'] for item in party_counts]
        party_fig = go.Figure(data=[go.Pie(labels=party_labels, values=party_values)])
        party_fig.update_layout(title="Party Affiliation Distribytion")
        context['party_chart'] = party_fig.to_html(full_html=False)

        # G3
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        election_counts = [self.get_queryset().filter(**{election: True}).count() for election in elections]
        election_bar = px.bar(x=elections, y=election_counts, title="Voter Participiation")
        election_bar.update_layout(xaxis_title="Election", yaxis_title="Voter Count")
        context['election_chart'] = election_bar.to_html(full_html=False)

        return context