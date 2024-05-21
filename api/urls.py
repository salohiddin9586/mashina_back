from django.urls import path
from .views import *

urlpatterns = [
    path('models/', list_and_create_madel),
    path('models/<int:id>/', detail_madel),

    path('marks/', list_and_create_marks),
    path('marks/<int:id>/', detail_update_delete_mark),

    path('cars/', list_and_create_car),
    path('cars/<int:id>/', detail_car),

    path('cars-images/', create_car_image),
    path('cars-images/<int:id>/', detail_car_image),

    path('colors/', list_and_create_color),
    path('colors/<int:id>/', detail_color),

    path('generations/', list_and_create_generations),
    path('generations/<int:id>/', detail_generations),

    path('countries/', list_and_create_country),
    path('countries/<int:id>/', detail_country),

    path('regions/', list_and_create_region),
    path('regions/<int:id>/', detail_region),

    path('cyties/', list_and_create_city),
    path('cyties/<int:id>/', detail_city),

    path('look_likes/', list_look_likes),
    path('look_likes/<int:id>/', detail_look_likes),

    path('interiors/', list_interiors),
    path('interiors/<int:id>/', detail_interiors),

    path('secutities/', list_securities),
    path('secutities/<int:id>/', detail_securities),

    path('options/', list_options),
    path('options/<int:id>/', detail_options),
]