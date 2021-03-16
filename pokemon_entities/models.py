from django.db import models

# your models here
class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    pockemon = models.ForeignKey(Pokemon, on_delete=models.SET_NULL, null=True)
    appeared_at = models.DateTimeField(blank=True, null=True)
    disappeared_at = models.DateTimeField(blank=True, null=True)
    level = models.IntegerField(null=True, blank=True)
    health = models.IntegerField(null=True, blank=True)
    strength = models.IntegerField(null=True, blank=True)
    deffence = models.IntegerField(null=True, blank=True)
    stamina = models.IntegerField(null=True, blank=True)