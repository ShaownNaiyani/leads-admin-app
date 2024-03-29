# Generated by Django 4.2 on 2024-02-04 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spapi', '0008_alter_leadsdata_estimated_monthly_sales_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leadsdata',
            name='estimated_monthly_sales',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='EstimatedMonthlySales'),
        ),
        migrations.AlterField(
            model_name='leadsdata',
            name='estimated_sales_rank',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='EstimatedSalesRank'),
        ),
        migrations.AlterField(
            model_name='leadsdata',
            name='sales_rank_30_days',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='SalesRank30Days'),
        ),
        migrations.AlterField(
            model_name='leadsdata',
            name='sales_rank_90_days',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='SalesRank90Days'),
        ),
    ]
