from django.contrib import admin
from core.models import *
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

class CarImageStackedInline(admin.TabularInline):

    model = CarImage
    extra = 1


class CarAdminForm(forms.ModelForm):

    content = forms.CharField(widget=CKEditorUploadingWidget(), label='Контент')

    class Meta:
        model = Car
        fields = '__all__'


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'madel', 'year', 'get_image')
    list_display_links = ('id', 'madel')
    list_filter = ('year', 'type', 'color', 'fuel','gear', 'drive', 'rudder', 'state', 'customs', 'exchange', 'in_stock', 'region', 'city')
    search_fields = ('content',)
    readonly_fields = ('created_at', 'updated_at', 'get_big_image',)
    filter_horizontal = ('look_likes','interiors', 'securities', 'options')
    inlines = [CarImageStackedInline,]
    form = CarAdminForm

    @admin.display(description='Изображение')
    def get_image(self, item):
        if item.images:
            return mark_safe(f'<img src="{item.images.first().image.url}" width="150px">')
        return '-'
    
    @admin.display(description='Изображение')
    def get_big_image(self, item):
        if item.images:
            return mark_safe(f'<img src="{item.images.first().image.url}" width="100%">')
        return '-'
    

admin.site.register(Marka)
admin.site.register(TransmissionCar)
admin.site.register(SteeringCar)
admin.site.register(SuspensionCar)
admin.site.register(BrakeSystemCar)
admin.site.register(Madel)
admin.site.register(Generations)
admin.site.register(CarLookLike)
admin.site.register(CarInterior)
admin.site.register(CarSecurity)
admin.site.register(CarOptipon)
admin.site.register(Color)
admin.site.register(CarImage)
admin.site.register(Country)
admin.site.register(Region)
admin.site.register(City)
