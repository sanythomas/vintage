# Generated by Django 4.1.2 on 2022-12-29 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_colorvariant_color_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='color_variant',
            field=models.ManyToManyField(blank=True, to='store.colorvariant'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='size_variant',
            field=models.ManyToManyField(blank=True, to='store.sizevariant'),
        ),
        migrations.AlterField(
            model_name='products',
            name='color_variant',
            field=models.ManyToManyField(blank=True, to='store.colorvariant'),
        ),
        migrations.AlterField(
            model_name='products',
            name='size_variant',
            field=models.ManyToManyField(blank=True, to='store.sizevariant'),
        ),
    ]
