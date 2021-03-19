from django.db import models


class Pokemon(models.Model):
    """Pokemon"""
    title = models.CharField(max_length=200, verbose_name='Название')
    en_title = models.CharField(
        max_length=200, blank=True, verbose_name='Название англ.')
    jp_title = models.CharField(
        max_length=200, blank=True, verbose_name='Название яп.')
    image = models.ImageField(
        null=True,
        blank=True,
        verbose_name='Изображение'
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    progenitor = models.ForeignKey(
        'Pokemon',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='evalution',
        verbose_name='От кого произошел?'
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    """Pokemon Entity"""
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name='Покемон',
        related_name='entities'
    )
    appeared_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Появляется'
    )
    disappeared_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Исчезает'
    )
    level = models.IntegerField(null=True, blank=True, verbose_name='Уровень')
    health = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Здоровье'
    )
    strength = models.IntegerField(null=True, blank=True, verbose_name='Сила')
    deffence = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Оборона'
    )
    stamina = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Выносливость'
    )

    def __str__(self):
        return f'{self.pokemon} {self.lat} x {self.lon}'