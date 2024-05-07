from django.db import models
from django.core.validators import RegexValidator


class TimeStampAbstractModel(models.Model):
    created_at = models.DateTimeField('дата добавление', auto_now_add=True)
    updated_at = models.DateTimeField('дата изменения', auto_now=True)

    class Meta:
        abstract = True


class Car(TimeStampAbstractModel):

    TYPE_CHOICES = {
        'SEDAN': 'Седан',
        'HATCHBACK': 'Хэтчбек',
        'COUPE': 'Купе',
        'CONVERTIBLE': 'Кабриолет',
        'SUV': 'Внедорожник',
        'TRUCK': 'Грузовик',
        'VAN': 'Фургон',
        'MINIVAN': 'Минивэн',
        'SPORTS_CAR': 'Спортивный автомобиль',
    }

    FUEL_CHOICES = {
        'GASOLINE': 'Бензин',
        'DIESEL': 'Дизель',
        'ELECTRIC': 'Электричество',
        'GAS': 'Газ',
        'GAS_GASOLINE': 'Газ / Бензин',
        'GIBRID': 'Гибрид',
    }

    GEAR_CHOICES = {
        'MANUAL': 'Механика',
        'AUTOMATIC': 'Автомат',
        'CVT': 'Вариатор',
        'ROBOT': 'Робот',
    }

    DRIVE_CHOICES = {
        'FRONT_WHEEL_DRIVE': 'Передний',
        'REAR_WHEEL_DRIVE': 'Задний',
        'ALL_WHEEL_DRIVE': 'Полный',
    }

    STATE_CHOICES = {
        'GOOD': 'Хорошее',
        'PERFECT': 'Идеальное',
        'EMERGENCY': 'Аварийное / Не на ходу',
        'NEW': 'Новое',
    }

    RUDDER_CHOICES = {
        'RIGHT': 'Справа',
        'LEFT': 'Слева',
    }

    EXCHANGE_CHOICES = {
        'LOOK_VARIANT': 'Рассмотрю варианты',
        'MONEY_TO_SURCHARGE': 'C доплатой покупателя',
        'MONEY_TO_SELLER': 'С доплатой продавца',
        'KEY_TO_KEY': 'Ключ на ключ',
        'NO_EXCHANGE': 'Обмен не предлагать',
        'EXCHANGE_TO_IMMOVABLES': 'Обмен на недвижимость',
        'ONLY_EXCHANGE': 'Только обмен',
    }

    IN_STOC_CHOICES = {
        'IN_STOCK': 'В наличии',
        'TO_ORDER': 'На заказ',
        'IN_TRANSIT': 'В пути',
    }

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'

    madel = models.ForeignKey('core.Madel',verbose_name="Модель", related_name="car", on_delete=models.PROTECT)
    generation = models.ForeignKey('core.Generations', verbose_name='Поколение', on_delete=models.CASCADE, related_name='car', blank=True, null=True)
    year = models.PositiveIntegerField(verbose_name="Год выпуска",)
    millage = models.PositiveIntegerField(verbose_name="Пробег")
    type = models.CharField(verbose_name="Кузов", max_length=100, choices=TYPE_CHOICES)
    color = models.ForeignKey('core.Color',verbose_name="Цвет", related_name='cars', on_delete=models.PROTECT)
    engine = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    fuel = models.CharField('Топливо', max_length=30, choices=FUEL_CHOICES)
    gear = models.CharField('Коробка', max_length=30, choices=GEAR_CHOICES)
    drive = models.CharField('Привод', max_length=30, choices=DRIVE_CHOICES)
    rudder = models.CharField('Руль', max_length=30, choices=RUDDER_CHOICES)
    state = models.CharField('Состояние', max_length=30, choices=STATE_CHOICES)
    customs = models.BooleanField(verbose_name="Расстоможен")
    exchange = models.CharField(verbose_name='Обмен', max_length=30, choices=EXCHANGE_CHOICES)
    in_stock = models.CharField(verbose_name='В наличии', max_length=100, choices=IN_STOC_CHOICES)
    region = models.ForeignKey('core.Region', related_name="cars", on_delete=models.PROTECT, verbose_name="Выберите регион")
    city = models.ForeignKey('core.City', related_name="cars", on_delete=models.PROTECT, verbose_name="Выберите город")
    registration = models.ForeignKey('core.Country', related_name='cars', on_delete=models.PROTECT, verbose_name="Выберите где зарегестрирован")
    user = models.ForeignKey('auth.User', verbose_name='Пользователь', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='Комментарий от автора')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена в сомах")
    look_likes = models.ManyToManyField('core.CarLookLike', related_name="cars", verbose_name="Внешний вид")
    interiors = models.ManyToManyField('core.CarInterior', related_name="cars", verbose_name="Салон")
    securities = models.ManyToManyField('core.CarSecurity', related_name="cars", verbose_name="Безопасность")
    options = models.ManyToManyField('core.CarOptipon', related_name="cars", verbose_name="Опции")

    def __str__(self):
        return f'{self.id} {self.madel} - {self.year}'

class Marka(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'
    
    name = models.CharField(verbose_name="Название марки", max_length=100)
    image = models.ImageField(verbose_name="Изображение", upload_to='car_image/')

    def __str__(self):
        return f'{self.name}'
    
class Madel(models.Model):
    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'
    marka = models.ForeignKey('core.Marka', related_name="madel", on_delete=models.CASCADE, verbose_name="Выберите марку")
    name = models.CharField('Название модели', max_length=100, unique=True)

    def __str__(self):
        return f'{self.id} - {self.marka} - {self.name}'

class Generations(models.Model):
    class Meta:
        verbose_name = 'Поколение'
        verbose_name_plural = 'Поколении'
    madel = models.ForeignKey('core.Madel', related_name="generation", on_delete=models.CASCADE, verbose_name="Выберите модел")
    name = models.CharField('Название поколение', max_length=100, unique=True)

    def __str__(self):
        return f'{self.name}'
    

class CarLookLike(models.Model):
    class Meta:
        verbose_name = 'Внешний вид'
        verbose_name_plural = 'Внешний виды'

    name = models.CharField(verbose_name='Название аттрибута внешнего вида', max_length=100, unique=True)
    def __str__(self):
        return f'{self.name}'


class CarInterior(models.Model):
    class Meta:
        verbose_name = 'Салон'
        verbose_name_plural = 'Салоны'
    name = models.CharField(verbose_name="Название аттрибута салона", max_length=100, unique=True)

    def __str__(self):
        return f'{self.name}'
    

class CarSecurity(models.Model):
    class Meta:
        verbose_name = 'Безопасность'
        verbose_name_plural = 'Безопасности'
    name = models.CharField('Название аттрибута безопасности', max_length=100, unique=True)

    def __str__(self):
        return f'{self.name}'
    

class CarOptipon(models.Model):
    class Meta:
        verbose_name = 'Опция'
        verbose_name_plural = 'Опции'
    name = models.CharField('Название аттрибута опции', max_length=100, unique=True)

    def __str__(self):
        return f'{self.name}'


class Color(models.Model):
    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цветы'
    
    name = models.CharField(verbose_name="Цвет", max_length=50)
    hex_value = models.CharField(verbose_name="HEX", validators=[RegexValidator(
        regex='^[0-9a-fA-F]{6}$',  # Шаблон для шестнадцатеричного значения
        message='Hex value must be exactly 6 hexadecimal characters.',  # Сообщение об ошибке
        code='invalid_hex_value'  # Код ошибки
    )], max_length=100)

    def __str__(self):
        return f'{self.name}'


class CarImage(models.Model):
    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображении'
    car = models.ForeignKey('core.Car', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField('изображение', upload_to='car_images/')

    def __str__(self):
        return f'{self.id} - {self.image} - {self.car}'
    

class Country(models.Model):
    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
    name = models.CharField('Название страны', max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'


class Region(models.Model):
    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'
    name = models.CharField(verbose_name="Название региона", max_length=30, unique=True)
    country = models.ForeignKey('core.Country', related_name="region", on_delete=models.CASCADE, verbose_name="Выберите страну")

    def __str__(self):
        return f'{self.name} - {self.country.name}'


class City(models.Model):
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Городы'
    name = models.CharField(verbose_name="Название города", max_length=50, unique=True)
    region = models.ForeignKey('core.Region', related_name='city', on_delete=models.CASCADE, verbose_name="Выберите область")
    
    def __str__(self):
        return f'{self.name} - {self.region.name}'
    
