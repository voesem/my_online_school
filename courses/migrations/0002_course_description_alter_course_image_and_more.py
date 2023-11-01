# Generated by Django 4.2.7 on 2023-11-01 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='описание'),
        ),
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='courses/', verbose_name='превью'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='описание'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='courses/', verbose_name='превью'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='url',
            field=models.URLField(blank=True, null=True, verbose_name='ссылка на видео'),
        ),
    ]
