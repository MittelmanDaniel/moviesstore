from django.db import models
from django.contrib.auth.models import User


class Petition(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} - {self.title}"

    @property
    def yes_count(self) -> int:
        from .models import Vote  # type: ignore
        return Vote.objects.filter(petition=self, value=True).count()

    @property
    def no_count(self) -> int:
        from .models import Vote  # type: ignore
        return Vote.objects.filter(petition=self, value=False).count()


class Vote(models.Model):
    id = models.AutoField(primary_key=True)
    petition = models.ForeignKey(Petition, related_name='votes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.BooleanField()  # True = yes, False = no
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('petition', 'user')

    def __str__(self):
        return f"{self.petition.id} - {self.user.username} - {'yes' if self.value else 'no'}"
