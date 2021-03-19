
from django.conf.urls import url, include

from .views import AvailableHall, BookHall, SeminarsForDate


LIST_AVAILABLE_HALL = AvailableHall.as_view({
    'get': 'get'
})
BOOK_HALL = BookHall.as_view({
    'post': 'post'
})
SEMINARS = SeminarsForDate.as_view({
    'get': 'get'
})

urlpatterns = [
    url(r'^halls$', LIST_AVAILABLE_HALL, name='get_available_seminar_halls'), #body: date start_time end_time capasity
    url(r'^book_hall$', BOOK_HALL, name='book_seminar_halls'), #body: date tart_time end_time hall_id
    url(r'^seminars$', SEMINARS, name='get_all_seminars_for_date'), #body: start_date, end_date
]
