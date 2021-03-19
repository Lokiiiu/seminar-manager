import logging
import json

from datetime import datetime, timedelta
from .models import Hall, Seminars

from rest_framework import status
from rest_framework.viewsets import ViewSet
from django.http import JsonResponse

class AvailableHall(ViewSet):
    """
        REST methods for getting Halls list.
    """
    # authentication_classes = ()
    
    # permission_classes = ()
    

    def get(self, request):
        """
            Return available Halls list.
        """
        if not request.data:
            return JsonResponse(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': 'request body missing.'}
            )
        parsed_request_body = request.data
        required_parameters = ( 'date', 'start_time', 'end_time', 'capacity')
        for parameter in required_parameters:
            if (parameter not in parsed_request_body) or (not parsed_request_body.get(parameter)):
                return JsonResponse(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'error': 'missing {} in request body.'.format(parameter)}
                )
        kwargs = {
            'date': parsed_request_body.get('date'),
            'startTime': parsed_request_body.get('start_time'),
            'endTime': parsed_request_body.get('end_time')
        }
        
        halls = Hall.get_halls_name_list()
        booked_halls = Seminars.get_booked_halls(**kwargs)
        available_halls = list()
        if booked_halls:
            halls = list(set(halls) - set(booked_halls))
        
        for hall in halls:
            if Hall.get_hall_capacity(hall) >= parsed_request_body.get('capacity'):
                available_halls.append(hall)
        return JsonResponse(
            status=status.HTTP_200_OK,
            data={'message': available_halls}
        )


class BookHall(ViewSet):
    """
    Provides API endpoints for email reminder sending process.
    """
    # authentication_classes = ()
    
    # permission_classes = ()
    
    def post(self, request):
        """
            Return available Halls list.
        """
        if not request.data:
            return JsonResponse(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': 'request body missing.'}
            )
        
        parsed_request_body = request.data
        required_parameters = ('hall_id', 'date', 'start_time', 'end_time')
        for parameter in required_parameters:
            if (parameter not in parsed_request_body) or (not parsed_request_body.get(parameter)):
                return JsonResponse(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'error': 'missing {} in request body.'.format(parameter)}
                )
        kwargs = {
            'hall_name': parsed_request_body.get('hall_id'),
            'date': parsed_request_body.get('date'),
            'startTime': parsed_request_body.get('start_time'),
            'endTime': parsed_request_body.get('end_time')
        }
        
        resp = Seminars.book_seminar_hall(**kwargs)
        if not resp:
            return JsonResponse(
                status=status.HTTP_403_FORBIDDEN,
                data={'error': 'Unable to book Seminar Hall'}
            )
        
        if resp == 'already booked':
            return JsonResponse(
                status=status.HTTP_409_CONFLICT,
                data={'error': 'Seminar hall already occupied for requested timings.'}
            ) 
              
        return JsonResponse(
            status=status.HTTP_200_OK,
            data={'message': resp }
        )


class SeminarsForDate(ViewSet):
    """
    Provides API endpoints for email reminder sending process.
    """
    # authentication_classes = ()
    
    # permission_classes = ()
    
    def get(self, request):
        """
            Return available Halls list.
        """
        
        if not request.data:
            return JsonResponse(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': 'request body missing.'}
            )
        parsed_request_body = request.data
        required_parameters = ( 'start_date', 'end_date')
        for parameter in required_parameters:
            if (parameter not in parsed_request_body) or (not parsed_request_body.get(parameter)):
                return JsonResponse(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'error': 'missing {} in request body.'.format(parameter)}
                )
        kwargs = {
            'startDate': parsed_request_body.get('start_date'),
            'endDate': parsed_request_body.get('end_date')
        }    
        seminars = Seminars.seminars_for(**kwargs)
        if not seminars:
            return JsonResponse(
                status=status.HTTP_204_NO_CONTENT,
                data={'message': 'No seminar found for requested date range.'}
            )
            
        return JsonResponse(
            status=status.HTTP_200_OK,
            data={'message': seminars}
        )
