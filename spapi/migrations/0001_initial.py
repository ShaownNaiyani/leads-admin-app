# Generated by Django 4.2 on 2024-01-26 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LeadsData',
            fields=[
                ('asin', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True, verbose_name='ASIN')),
                ('amazon_fba_estimated_fees', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='AmazonFBAEstimatedFees')),
                ('amazon_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='AmazonPrice')),
                ('estimated_sales_rank', models.PositiveIntegerField(default=0, editable=False, null=True, verbose_name='EstimatedSalesRank')),
                ('sales_rank_30_days', models.PositiveIntegerField(default=0, editable=False, null=True, verbose_name='SalesRank30Days')),
                ('sales_rank_90_days', models.PositiveIntegerField(default=0, editable=False, null=True, verbose_name='SalesRank90Days')),
                ('estimated_monthly_sales', models.PositiveIntegerField(default=0, editable=False, null=True, verbose_name='EstimatedMonthlySales')),
                ('product_image_url', models.URLField(blank=True, null=True, verbose_name='ProductImageUrl')),
                ('sourcing_url', models.URLField(blank=True, null=True, verbose_name='SourcingUrl')),
                ('sourcing_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='SourcingPrice')),
                ('amazon_url', models.URLField(blank=True, null=True, verbose_name='AmazonUrl')),
                ('amazon_on_listing', models.BooleanField(default=False, null=True, verbose_name='AmazonOnListing')),
                ('number_of_sellers_on_listing', models.PositiveIntegerField(default=0, editable=False, null=True, verbose_name='NumberOfSellersOnListing')),
                ('number_of_reviews', models.PositiveIntegerField(default=0, editable=False, null=True, verbose_name='NumberOfReviews')),
                ('estimated_gross_profit', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='EstimatedGrossProfit')),
                ('estimated_gross_profit_margin', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='EstimatedGrossProfitMargin')),
                ('estimated_net_profit', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='EstimatedNetProfit')),
                ('estimated_net_profit_margin', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='EstimatedNetProfitMargin')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]