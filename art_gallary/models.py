from django.db import models
from django.contrib.auth.models import User
# Create your models here.

art_catagory = (
    ('Abstract Art', 'Abstract Art'),
    ('Landscape Paintings', 'Landscape Paintings'),
    ('Portraits', 'Portraits'),
    ('Sculptures', 'Sculptures'),
    ('Modern Art', 'Modern Art'),
    ('Photography', 'Photography'),
    ('Illustrations', 'Illustrations'),
    ('Others', 'Others')
)



class Artwork(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    artist = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='artworks')
    catagory = models.CharField(choices=art_catagory, max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    art = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

   
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField( max_length=100)

    def __str__(self):
        return self.name


status = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On the Way', 'On the Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
    ('Pending', 'Pending'),
)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_status = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)

class Orderplaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    product = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=status, default='Pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default="")


