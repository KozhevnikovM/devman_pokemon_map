# Generated by Django 3.1.7 on 2021-03-16 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0006_pokemonentity_pockemon'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemonentity',
            name='appear_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
