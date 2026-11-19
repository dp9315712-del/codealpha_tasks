from rest_framework import serializers
from .models import (
    Employer,
    JobListing,
    Candidate,
    Resume,
    JobApplication,
    EmployerNotification
)


class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = '__all__'


class JobListingSerializer(serializers.ModelSerializer):
    employer_name = serializers.CharField(
        source='employer.company_name',
        read_only=True
    )

    class Meta:
        model = JobListing
        fields = '__all__'


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'

    def validate_resume_file(self, value):
        if not value.name.lower().endswith('.pdf'):
            raise serializers.ValidationError(
                "Only PDF resume files are allowed."
            )

        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError(
                "Resume file size must not exceed 5 MB."
            )

        return value


class JobApplicationSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(
        source='candidate.full_name',
        read_only=True
    )

    job_title = serializers.CharField(
        source='job.title',
        read_only=True
    )

    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ('status', 'applied_at')

    def validate(self, data):
        candidate = data.get('candidate')
        job = data.get('job')
        resume = data.get('resume')

        if not job.is_active:
            raise serializers.ValidationError(
                "This job is not currently active."
            )

        if resume and resume.candidate != candidate:
            raise serializers.ValidationError(
                "Resume must belong to the selected candidate."
            )

        if JobApplication.objects.filter(
            candidate=candidate,
            job=job
        ).exists():
            raise serializers.ValidationError(
                "You have already applied for this job."
            )

        return data

    def create(self, validated_data):
        application = JobApplication.objects.create(
            **validated_data
        )

        EmployerNotification.objects.create(
            employer=application.job.employer,
            application=application,
            message=(
                f"{application.candidate.full_name} "
                f"applied for {application.job.title}"
            )
        )

        return application


class EmployerNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerNotification
        fields = '__all__'


class JobApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['status']
