# Generated by Django 3.0.6 on 2020-05-30 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20200530_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='store/images/'),
        ),
    ]