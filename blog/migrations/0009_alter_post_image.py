# Generated by Django 3.2.5 on 2021-09-13 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ManyToManyField(default='media/default.jpg', related_name='products', to='blog.Image'),
        ),
    ]