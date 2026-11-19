from django.contrib import admin
from .models import (
    Employer,
    JobListing,
    Candidate,
    Resume,
    JobApplication,
    EmployerNotification
)

admin.site.register(Employer)
admin.site.register(JobListing)
admin.site.register(Candidate)
admin.site.register(Resume)
admin.site.register(JobApplication)
admin.site.register(EmployerNotification)