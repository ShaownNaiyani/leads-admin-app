# Generated by Django 4.2 on 2024-02-04 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spapi', '0006_alter_leadsdata_number_of_reviews_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leadsdata',
            name='estimated_monthly_sales',
            field=models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='EstimatedMonthlySales'),
        ),
        migrations.AlterField(
            model_name='leadsdata',
            name='estimated_sales_rank',
            field=models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='EstimatedSalesRank'),
        ),
        migrations.AlterField(
            model_name='leadsdata',
            name='number_of_reviews',
            field=models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='NumberOfReviews'),
        ),
        migrations.AlterField(
            model_name='leadsdata',
            name='number_of_sellers_on_listing',
            field=models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='NumberOfSellersOnListing'),
        ),
        migrations.AlterField(
            model_name='leadsdata',
            name='sales_rank_30_days',
            field=models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='SalesRank30Days'),
        ),
        migrations.AlterField(
            model_name='leadsdata',
            name='sales_rank_90_days',
            field=models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='SalesRank90Days'),
        ),
    ]