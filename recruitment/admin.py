from django.contrib import admin
from .models import JobOffer, Candidate, AIQuestion

admin.site.register(JobOffer)
admin.site.register(Candidate)
admin.site.register(AIQuestion)