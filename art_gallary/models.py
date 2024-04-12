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
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='artworks')
    catagory = models.CharField(choices=art_catagory, max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    art = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total(self):
        return self.quantity * self.art.price