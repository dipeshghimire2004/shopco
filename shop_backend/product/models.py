# Import necessary modules for Django models
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# Get the user model dynamically to maintain flexibility with custom user models
User = get_user_model()

class Category(models.Model):
    name=models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name
    

class Color(models.Model):
    name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.name



# Define a model for storing product images
class ProductImage(models.Model):
    product = models.ForeignKey('Product', related_name='images', on_delete=models.CASCADE)

    image = models.ImageField(upload_to='product_images/')

    is_main_image = models.BooleanField(default=False)

    # Ensure there is only one main image per product
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'is_main_image'],
                name="unique_main_image",
                condition=models.Q(is_main_image=True)
            )
        ]

class Product(models.Model):
    # CATEGORY_CHOICES = [
    #     ('top_selling','top_selling'),
    #     ('new_arrival', 'new_arrival'),
    #     ('you_might_also_like_this','you_might_also_like_this'),
    # ]
    TYPE_CHOICES = [
        ('Tshirt', 'Tshirt'),
        ('Pant', 'Pant'),
        ('Hoodie', 'Hoodie'),
        ('Shirts', 'Shirts'),
        ('Shorts', 'Shorts'),
    ]

    STYLE_CHOICES = [
        ('Casual', 'Casual'),
        ('Formal', 'Formal'),
        ('Party', 'Party'),
        ('Gym', 'Gym'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products') 
    name = models.CharField(max_length=50)  
    type = models.CharField(max_length=30, null=True, choices=TYPE_CHOICES)
    # category = models.CharField(max_length=20, null=True, choices=CATEGORY_CHOICES) 
    category =models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True)
    style = models.CharField(max_length=20, null=True, choices=STYLE_CHOICES)  
    rating = models.DecimalField(max_digits=10, decimal_places=2)  
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    discount = models.DecimalField(max_digits=4, decimal_places=2)  
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)  
    description = models.TextField(max_length=300, blank=True) 
    sizes = models.ManyToManyField(Size)  
    colors = models.ManyToManyField(Color)  # Many-to-many relationship with Color
    main_image = models.ImageField(upload_to='main_images/', blank=True, null=True)  # Optional main image
    stock_quantity = models.PositiveIntegerField()  # Available stock quantity

    # Override save method to calculate discounted price before saving
    def save(self, *args, **kwargs):
        # Ensure the discounted price is calculated
        self.discounted_price = self.price - ((self.price * self.discount) / 100)
        super().save(*args, **kwargs)

    # String representation of the model
    def __str__(self):
        return self.name
