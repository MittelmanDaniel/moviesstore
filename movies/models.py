from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')

    def __str__(self):
        return str(self.id) + ' - ' + self.name

    @property
    def average_rating(self):
        # The fix is here: .filter(rating__gt=0)
        # This will only average reviews where a rating has been submitted.
        return self.review_set.filter(rating__gt=0).aggregate(Avg('rating'))['rating__avg']

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    rating = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reported = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name