# Generated by Django 5.0.2 on 2024-02-28 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_customuser_is_staff_customuser_is_superuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='users/'),
        ),
    ]
