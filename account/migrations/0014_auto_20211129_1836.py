# Generated by Django 3.1.1 on 2021-11-29 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_auto_20211129_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='image',
            field=models.ImageField(default='D:\\react_blog\\blog_django\\core\\media\\profilepic\\useravatar.png', upload_to='D:\\react_blog\\blog_django\\core\\media\\profilepic'),
        ),
    ]
