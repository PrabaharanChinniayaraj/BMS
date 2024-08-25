# Generated by Django 5.0.2 on 2024-06-13 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Billingapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='buying_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='transaction_sale',
            name='transaction_id',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
