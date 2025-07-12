from django.db import models
from django.contrib.auth.models import User

# Contact Model
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    description = models.TextField(max_length=500)
    Phonenumber = models.IntegerField()

    def __str__(self):
        return self.name

# Product Model
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=30)
    category = models.TextField(max_length=30, default='')
    sub_category = models.TextField(max_length=30, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=50, default='')
    image = models.ImageField(upload_to='shop/images')

    def __str__(self):
        return self.product_name


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    order_id       = models.AutoField(primary_key=True)
    full_name      = models.CharField(max_length=200, null=True, blank=True)
    email          = models.EmailField(null=True, blank=True)
    address        = models.TextField(max_length=255)
    phone          = models.CharField(max_length=15)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_proof  = models.ImageField(upload_to='payment_proofs/', null=True, blank=True)
    date_ordered   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.order_id} - {self.full_name or 'No Name'}"



class OrderItem(models.Model):
    order     = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product   = models.ForeignKey('Product', on_delete=models.PROTECT)
    quantity  = models.PositiveIntegerField(default=1)
    price     = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}× {self.product.product_name} (Order {self.order.order_id})"

# # ecommerceapp/models.py
# from django.db import models
# from django.contrib.auth.models import User

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='profile_pics', default='default.jpg')  # ✅ This line is important

#     def __str__(self):
#         return f'{self.user.username} Profile'






