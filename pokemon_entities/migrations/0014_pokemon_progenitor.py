# Generated by Django 3.1.7 on 2021-03-17 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0013_auto_20210317_0715'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='progenitor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pokemon_entities.pokemon'),
        ),
    ]
