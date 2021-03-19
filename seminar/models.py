from django.db import models
from datetime import datetime
import logging

class Hall(models.Model):
    """
        Static table for Hall and it's capacity. 
    """
    
    class Meta(object):
        app_label = "seminar"

    hall_name = models.CharField(null=False, max_length=1)
    capacity = models.IntegerField(null=False)
    
    @classmethod
    def get_hall_capacity(cls, hall_id):
        """
            to get Hall capacity. 
        """
        
        return Hall.objects.get(hall_name=hall_id).capacity
    
    @classmethod
    def get_halls_name_list(cls):
        """
            to get list of all Hall names. 
        """
        
        return [hall.hall_name for hall in Hall.objects.all()]
        
class Seminars(models.Model):
    """
        Seminar table to hold all the seminars scheduled so far. 
    """
    
    class Meta(object):
        app_label = "seminar"

    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, db_index=True, related_name='hall')
    date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @classmethod
    def get_booked_halls(cls, date=datetime.now().strftime("%Y-%m-%d"),startTime=datetime.strptime('00:00', '%H:%M'), endTime=datetime.strptime('00:00', '%H:%M') ):
        """
            to get available Hall. 
        """
        booked = Seminars.objects.filter(date=date, start_time__lte=startTime, end_time__gte=endTime)
        return list(set([seminar.hall.hall_name for seminar in booked])) if booked else []
    
    @classmethod
    def book_seminar_hall(cls, hall_name, date, startTime, endTime ):
        """
            to book a seminar hall . 
            NOTE: all the parameters are required in this method.
        """
        date= datetime.strptime(date, '%Y-%m-%d')
        startTime = datetime.strptime(startTime, '%H:%M')
        endTime = datetime.strptime(endTime, '%H:%M')
        hall = Hall.objects.get(hall_name=hall_name)
        if hall:
            seminar = Seminars.objects.filter(hall=hall, date=date, start_time=startTime, end_time=endTime)
            if not seminar:
                try:
                    seminar = Seminars(hall=hall, date=date, start_time=startTime, end_time=endTime)
                    seminar.save()
                except Exception as e:
                    logging.info(e)
                else:
                    return 'Seminar Hall Booked.'
            else:
                return 'already booked'
        else:
            return None
        
    @classmethod
    def seminars_for(cls, startDate, endDate):
        """
            get all the seminars in provided date range. 
            NOTE: all the parameters are required in this method.
        """
        startDate = datetime.strptime(startDate, '%Y-%m-%d')
        endDate = datetime.strptime(endDate, '%Y-%m-%d')
        seminars = Seminars.objects.filter(date__gte=startDate, date__lte=endDate)
        if seminars:
            return [{'hall': seminar.hall.hall_name, 'start_time': seminar.start_time, 'end_time': seminar.end_time, } for seminar in seminars]
        else: 
            return []