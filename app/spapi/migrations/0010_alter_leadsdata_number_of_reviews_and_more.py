# Generated by Django 4.2 on 2024-02-04 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spapi', '0009_alter_leadsdata_estimated_monthly_sales_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leadsdata',
            name='number_of_reviews',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='NumberOfReviews'),
        ),
        migrations.AlterField(
            model_name='leadsdata',
            name='number_of_sellers_on_listing',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='NumberOfSellersOnListing'),
        ),
    ]
