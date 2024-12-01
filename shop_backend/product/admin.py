from django.contrib import admin
from .models import Product,Color, Size, ProductImage, Category

# Register your models here.
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'style', 'rating', 'price', 'discount', 'discounted_price',
        'get_sizes', 'get_colors', 'stock_quantity', 'get_main_image'
    )
    list_filter = ('style', 'category', 'colors', 'sizes')
    # search_fields = ('name', 'category__name')  # Include 'category__name' to enable autocomplete
    filter_horizontal = ('sizes', 'colors')
    inlines = [ProductImageInline]
    # autocomplete_fields = ('category',)

    def get_main_image(self, obj):
        return obj.main_image.url if obj.main_image else 'No main image exists'
    get_main_image.short_description = 'Main Image'

    def get_sizes(self, obj):
        return ", ".join([size.name for size in obj.sizes.all()]) if obj.sizes.exists() else 'No sizes'
    get_sizes.short_description = 'Sizes'

    def get_colors(self, obj):
        return ", ".join([color.name for color in obj.colors.all()]) if obj.colors.exists() else 'No colors'
    get_colors.short_description = 'Colors'


# Register models
admin.site.register(Product, ProductAdmin)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Category)
