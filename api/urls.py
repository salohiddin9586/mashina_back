from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('cars', CarViewSet)
router.register('nopagin', ViewSetPagin, basename="nopagin")
router.register('marks', MarkViewSet, basename="marks")
router.register('models', CarModelViewSet, basename="madels")
router.register('colors', ColorViewSet, basename="colors")
router.register('generations', GenerationsViewSet, basename="generations")
router.register('countries', CountryViewSet, basename="countries")
router.register('regions', RegionViewSet, basename="regions")
router.register('cyties', CityViewSet, basename="cyties")
router.register('look_likes', LooksLikesViewSet, basename="look_likes")
router.register('interiors', InteriorsViewSet, basename="interiors")
router.register('securities', SecuritiesViewSet, basename="securities")
router.register('options', OptionsViewSet, basename="options")
router.register('tokens', TokenViewSet, basename="tokens")
router.register('images', CarImageViewSet, basename="images")
urlpatterns = [
    path('user/<int:id>', UserViewSet.as_view()),

    path('auth/login/', LoginApiView.as_view()),
    path('auth/register/', RegisterApiView.as_view()),
    
    path('redactor_profile/<int:id>/', RedactorProfileApiView.as_view()),

    path('', include(router.urls)),
]