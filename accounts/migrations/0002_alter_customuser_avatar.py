# Generated by Django 4.0.5 on 2022-07-06 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(default='default.png', null=True, upload_to='profile/'),
        ),
    ]