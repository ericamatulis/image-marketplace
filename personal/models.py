from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

# Models

class Profile(models.Model):
    amount_sold = models.DecimalField(max_digits=999, decimal_places=2, default=0)
    amount_spent = models.DecimalField(max_digits=999, decimal_places=2, default=0)
    credit_left = models.DecimalField(max_digits=999, decimal_places=2, default=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    
class Category(models.Model):
    category_name = models.CharField(max_length=200, unique=True)
    category_description = models.TextField(default="")
    
    def __str__(self):
        return self.category_name
    
    
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True);
    product_description = models.TextField(default="")
    product_quantity = models.IntegerField(default=1, validators=[MaxValueValidator(100), MinValueValidator(0)])
    product_price = models.DecimalField(max_digits=999, decimal_places=2, validators=[MaxValueValidator(1000), MinValueValidator(0.01)])
    product_image = models.ImageField(upload_to='images')
    seller = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    number_sold = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    amount_sold = models.DecimalField(default=0, max_digits=999, decimal_places=2, validators=[MaxValueValidator(1000), MinValueValidator(0)])
    categories = models.ManyToManyField(Category, related_name='products', blank=True)
    is_active = models.BooleanField(default=True)
    discount = models.DecimalField(default=0, max_digits=999, decimal_places=2, validators=[MaxValueValidator(1000), MinValueValidator(0)])
    
    class Meta:
        ordering = ['-is_active', '-product_quantity']
    
    def __str__(self):
        return self.product_name
        
    
class Order(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=999, decimal_places=2, validators=[MaxValueValidator(1000), MinValueValidator(0.01)])
    total = models.DecimalField(max_digits=999, decimal_places=2)
    date = models.DateField(default=timezone.now)
    seller = models.CharField(max_length=200)
    
    def __str__(self):
        return self.product.product_name + " - " + self.customer.username
    

class ChangeLog(models.Model):
    previous_product = models.TextField(null=True)
    new_product = models.TextField(null=True)
    type_of_change = models.CharField(max_length=200, choices=(
        (1,"Delete"),
        (2,"Update"),
        (3,"Add")))
    changed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return self.type_of_change
    
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
 


