from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import JobListing, Resume, JobApplication
from .serializers import JobListingSerializer, ResumeSerializer, JobApplicationSerializer, JobApplicationStatusSerializer


# GET: View all jobs and search jobs
# POST: Create a new job
@api_view(['GET', 'POST'])
def job_list(request):

    if request.method == 'GET':

        jobs = JobListing.objects.filter(
            is_active=True
        )

        # Search by job title
        title = request.GET.get('title')
        if title:
            jobs = jobs.filter(title__icontains=title)

        # Search by location
        location = request.GET.get('location')
        if location:
            jobs = jobs.filter(location__icontains=location)

        # Filter by job type
        job_type = request.GET.get('job_type')
        if job_type:
            jobs = jobs.filter(job_type__iexact=job_type)

        # Search by required skills
        skills = request.GET.get('skills')
        if skills:
            jobs = jobs.filter(skills_required__icontains=skills)

        jobs = jobs.order_by('-created_at')

        serializer = JobListingSerializer(
            jobs,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    serializer = JobListingSerializer(data=request.data)

    if serializer.is_valid():
        job = serializer.save()

        return Response(
            JobListingSerializer(job).data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

# POST: Upload candidate resume
@api_view(['POST'])
def resume_upload(request):

    serializer = ResumeSerializer(data=request.data)

    if serializer.is_valid():
        resume = serializer.save()

        return Response(
            ResumeSerializer(resume).data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


# POST: Candidate applies for a job
@api_view(['POST'])
def apply_for_job(request):
    serializer = JobApplicationSerializer(data=request.data)

    if serializer.is_valid():
        application = serializer.save()

        return Response(
            JobApplicationSerializer(application).data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


# GET: Track candidate job applications
@api_view(['GET'])
def my_applications(request):
    candidate_id = request.query_params.get('candidate')

    if not candidate_id:
        return Response(
            {"error": "Candidate ID is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    applications = JobApplication.objects.filter(
        candidate_id=candidate_id
    ).order_by('-applied_at')

    serializer = JobApplicationSerializer(
        applications,
        many=True
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


# PATCH: Update job application status
@api_view(['PATCH'])
def update_application_status(request, pk):
    try:
        application = JobApplication.objects.get(pk=pk)
    except JobApplication.DoesNotExist:
        return Response(
            {"error": "Application not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = JobApplicationStatusSerializer(
        application,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
