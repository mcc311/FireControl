# Generated by Django 3.2.5 on 2022-04-19 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vessel', '0003_missile_belongs_to'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vessil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100, null=True, unique=True)),
                ('value', models.FloatField(default=0.5)),
                ('belongs_to', models.CharField(choices=[('e', 'Enemy'), ('a', 'Ally'), ('b', 'Both')], default='b', max_length=1)),
                ('default_fires', models.ManyToManyField(to='Vessel.Missile')),
            ],
        ),
    ]
