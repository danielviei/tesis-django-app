# Generated by Django 5.0.2 on 2024-02-25 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('name', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('rol', models.CharField(choices=[('user', 'User'), ('admin', 'Admin')], default='user', max_length=100)),
                ('img', models.ImageField(blank=True, null=True, upload_to='users/')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
