# Generated by Django 4.2.2 on 2023-07-08 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('altar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainingsession',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
