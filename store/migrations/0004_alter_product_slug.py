# Generated by Django 4.0.1 on 2022-02-01 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_category_product_description_product_offer_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]
