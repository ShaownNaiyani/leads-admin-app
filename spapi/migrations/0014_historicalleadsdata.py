# Generated by Django 4.2 on 2024-02-05 16:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('spapi', '0013_alter_leadsdata_asin'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalLeadsData',
            fields=[
                ('asin', models.CharField(db_column='asin', db_index=True, max_length=255, verbose_name='ASIN')),
                ('amazon_fba_estimated_fees', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='AmazonFBAEstimatedFees')),
                ('amazon_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='AmazonPrice')),
                ('estimated_sales_rank', models.PositiveIntegerField(default=0, verbose_name='EstimatedSalesRank')),
                ('sales_rank_30_days', models.PositiveIntegerField(default=0, verbose_name='SalesRank30Days')),
                ('sales_rank_90_days', models.PositiveIntegerField(default=0, verbose_name='SalesRank90Days')),
                ('estimated_monthly_sales', models.PositiveIntegerField(default=0, verbose_name='EstimatedMonthlySales')),
                ('product_image_url', models.URLField(blank=True, null=True, verbose_name='ProductImageUrl')),
                ('sourcing_url', models.URLField(blank=True, null=True, verbose_name='SourcingUrl')),
                ('sourcing_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='SourcingPrice')),
                ('amazon_url', models.URLField(blank=True, null=True, verbose_name='AmazonUrl')),
                ('amazon_on_listing', models.BooleanField(default=False, null=True, verbose_name='AmazonOnListing')),
                ('number_of_sellers_on_listing', models.PositiveIntegerField(default=0, verbose_name='NumberOfSellersOnListing')),
                ('number_of_reviews', models.PositiveIntegerField(default=0, verbose_name='NumberOfReviews')),
                ('estimated_gross_profit', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='EstimatedGrossProfit')),
                ('estimated_gross_profit_margin', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='EstimatedGrossProfitMargin')),
                ('estimated_net_profit', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='EstimatedNetProfit')),
                ('estimated_net_profit_margin', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='EstimatedNetProfitMargin')),
                ('updated', models.DateTimeField(blank=True, editable=False)),
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical leads data',
                'verbose_name_plural': 'historical leads datas',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]