from rest_framework import status
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from django.core.paginator import Paginator
from rest_framework.response import Response
from api.filters import CarFilter
from .serializers import *
from core.models import *


@api_view(['GET', 'POST'])
def list_and_create_car(request):
    if request.method == 'POST':
        serializer = CreateCarSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        car = serializer.save()
        detail_serializer = DetailCarSerializer(
            instance=car, context={'request': request})
        return Response(detail_serializer.data, status.HTTP_201_CREATED)

    cars = Car.objects.all()

    ordering = request.GET.get('ordering', '')
    order_fields = ['created_at', 'price']

    if ordering.replace('-', '') in order_fields:
        cars = cars.order_by(ordering)

    search = request.GET.get('search')
    if search:
        cars = cars.filter(
            Q(madel__name__icontains=search) | Q(madel__marka__name__icontains=search) | Q(content__icontains=search))

    filterset = CarFilter(queryset=cars, data=request.GET)
    cars = filterset.qs

    qs_count = cars.count()

    pagin = Paginator(cars, int(request.GET.get('page_size') or 6))
    page = int(request.GET.get('page') or 1)

    if 1 > page or page > pagin.num_pages:
        return Response({'detail': f'Номер страницы не должно превыщать {pagin.num_pages}.'}, status.HTTP_400_BAD_REQUEST)

    cars = pagin.get_page(page)
    serializer = ListCarSerializer(cars, many=True, context={'request': request})
    
    return Response({
        'count': qs_count,
        'page_count': pagin.num_pages,
        'results': serializer.data
    })


@api_view(['GET', 'DELETE', 'PATCH'])
def detail_car(request, id):
    car = get_object_or_404(Car, id=id)

    if request.method == 'DELETE':
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == 'PATCH':
        serializer = CarSerializer(
            instance=car, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        detail_serializer = DetailCarSerializer(
            instance=car, context={'request': request})
        return Response(detail_serializer.data)

    serializer = DetailCarSerializer(
        instance=car, context={'request': request})
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def list_and_create_marks(request):
    if request.method == 'POST':
        serializer = MarkSerializer(None, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    marks = Marka.objects.all()
    serializer = MarkSerializer(marks, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
def detail_update_delete_mark(request, id):
    mark = get_object_or_404(Marka, id=id)
    if request.method == 'PATCH' or request.method == 'PUT':
        partial = request.method == 'PATCH'
        serializer = MarkSerializer(
            instance=mark, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        mark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = MarkSerializer(instance=mark)
    return Response(serializer.data)


@api_view(['POST',])
def create_car_image(request):
    serializer = CarImageSerializer(
        data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE'])
def detail_car_image(request, id):
    car_image = get_object_or_404(CarImage, id=id)
    if request.method == 'DELETE':
        car_image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = CarImageSerializer(
        instance=car_image, context={'request': request})
    return Response(serializer.data)


@api_view(['POST', 'GET'])
def list_and_create_madel(request):
    if request.method == 'POST':
        serializer = MadelSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        madel = serializer.save()
        detail_serializer = DetailMadelSerializer(
            instance=madel, context={'request': request})
        return Response(detail_serializer.data, status.HTTP_201_CREATED)
    madels = Madel.objects.all()
    serializer = MadelSerializer(
        madels, context={'context': request}, many=True)
    return Response(serializer.data)


@api_view(['GET', 'DELETE', 'PATCH'])
def detail_madel(request, id):
    madel = get_object_or_404(Madel, id=id)
    if request.method == 'DELETE':
        madel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method == 'PATCH':
        serializer = MadelSerializer(
            instance=madel, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        detail_serializer = DetailMadelSerializer(
            instance=madel, context={'request': request})
        return Response(detail_serializer.data)
    detail_serializer = DetailMadelSerializer(
        instance=madel, context={'request': request})
    return Response(detail_serializer.data)


@api_view(['POST', 'GET'])
def list_and_create_generations(request):
    if request.method == 'POST':
        serializer = GenerationsSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    generations = Generations.objects.all()
    serializer = GenerationsSerializer(
        instance=generations, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET', 'DELETE', 'PATCH'])
def detail_generations(request, id):
    generations = get_object_or_404(Generations, id=id)
    if request.method == 'DELETE':
        generations.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method == 'PATCH':
        serializer = GenerationsSerializer(
            instance=generations, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    serializer = GenerationsSerializer(instance=generations, context={'request': request})
    return Response(serializer.data)


@api_view(['POST', 'GET'])
def list_and_create_color(request):
    if request.method == 'POST':
        serializer = ColorSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    colors = Color.objects.all()
    serializer = ColorSerializer(
        instance=colors, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET', 'DELETE', 'PATCH'])
def detail_color(request, id):
    color = get_object_or_404(Color, id=id)
    if request.method == 'DELETE':
        color.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method == 'PATCH':
        serializer = ColorSerializer(
            instance=color, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    serializer = ColorSerializer(instance=color, context={'request': request})
    return Response(serializer.data)


@api_view(['POST', 'GET'])
def list_and_create_country(request):
    if request.method == 'POST':
        serializer = CountrySerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    countries = Country.objects.all()
    serializer = CountrySerializer(
        instance=countries, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET', 'DELETE', 'PATCH'])
def detail_country(request, id):
    country = get_object_or_404(Country, id=id)
    if request.method == 'DELETE':
        country.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method == 'PATCH':
        serializer = CountrySerializer(
            instance=country, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    serializer = CountrySerializer(
        instance=country, context={'request': request})
    return Response(serializer.data)


@api_view(['POST', 'GET'])
def list_and_create_region(request):
    if request.method == 'POST':
        serializer = RegionSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        region = serializer.save()
        detail_serializer = DetailRegionSerializer(
            instance=region, context={'request': request})
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)
    regions = Region.objects.all()
    serializer = RegionSerializer(
        instance=regions, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET', 'DELETE', 'PATCH'])
def detail_region(request, id):
    region = get_object_or_404(Region, id=id)
    if request.method == 'DELETE':
        region.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method == 'PATCH':
        serializer = RegionSerializer(
            instance=region, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        region = serializer.save()
        detail_serializer = DetailRegionSerializer(
            instance=region, context={'request': request})
        return Response(detail_serializer.data)
    serializer = RegionSerializer(
        instance=region, context={'request': request})
    return Response(serializer.data)


@api_view(['POST', 'GET'])
def list_and_create_city(request):
    if request.method == 'POST':
        serializer = CitySerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        city = serializer.save()
        detail_serializer = DetailCitySerializer(
            instance=city, context={'request': request})
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)
    cities = City.objects.all()
    serializer = CitySerializer(
        instance=cities, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET', 'DELETE', 'PATCH'])
def detail_city(request, id):
    city = get_object_or_404(City, id=id)
    if request.method == 'DELETE':
        city.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method == 'PATCH':
        serializer = CitySerializer(
            instance=city, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        city = serializer.save()
        detail_serializer = DetailCitySerializer(
            instance=city, context={'request': request})
        return Response(detail_serializer.data)
    serializer = CitySerializer(instance=city, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def list_look_likes(request):
    look_likes = CarLookLike.objects.all()
    serializer = LooksLikesCarSerializer(
        instance=look_likes, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def detail_look_likes(request, id):
    look_likes = get_object_or_404(CarLookLike, id=id)
    serializer = LooksLikesCarSerializer(
        instance=look_likes, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def list_interiors(request):
    interiors = CarInterior.objects.all()
    serializer = InteriorsCarSerializer(
        instance=interiors, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def detail_interiors(request, id):
    interiors = get_object_or_404(CarInterior, id=id)
    serializer = InteriorsCarSerializer(
        instance=interiors, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def list_options(request):
    options = CarOptipon.objects.all()
    serializer = OptionsCarSerializer(
        instance=options, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def detail_options(request, id):
    options = get_object_or_404(CarOptipon, id=id)
    serializer = OptionsCarSerializer(
        instance=options, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def list_securities(request):
    securities = CarSecurity.objects.all()
    serializer = SecutitiesCarSerializer(
        instance=securities, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def detail_securities(request, id):
    securities = get_object_or_404(CarSecurity, id=id)
    serializer = SecutitiesCarSerializer(
        instance=securities, context={'request': request})
    return Response(serializer.data)
