from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Event, Registration
from .serializers import EventSerializer, RegistrationSerializer


@api_view(['GET'])
def event_list(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def event_detail(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response(
            {"error": "Event not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = EventSerializer(event)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_event(request, pk):
    with transaction.atomic():
        try:
            event = Event.objects.select_for_update().get(pk=pk)
        except Event.DoesNotExist:
            return Response(
                {"error": "Event not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if Registration.objects.filter(event=event, user=request.user).exists():
            return Response(
                {"error": "You are already registered for this event"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if event.available_seats <= 0:
            return Response(
                {"error": "No seats available"},
                status=status.HTTP_400_BAD_REQUEST
            )

        registration = Registration.objects.create(
            event=event,
            user=request.user
        )

        event.available_seats -= 1
        event.save(update_fields=['available_seats'])

    serializer = RegistrationSerializer(registration)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_registrations(request):
    registrations = Registration.objects.filter(
        user=request.user
    ).select_related('event')

    serializer = RegistrationSerializer(
        registrations,
        many=True
    )

    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cancel_registration(request, pk):
    with transaction.atomic():
        try:
            registration = Registration.objects.select_related(
                'event'
            ).get(
                pk=pk,
                user=request.user
            )
        except Registration.DoesNotExist:
            return Response(
                {"error": "Registration not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        event = Event.objects.select_for_update().get(
            pk=registration.event_id
        )

        registration.delete()

        event.available_seats += 1
        event.save(update_fields=['available_seats'])

    return Response(
        {"message": "Registration cancelled successfully"},
        status=status.HTTP_200_OK
    )

