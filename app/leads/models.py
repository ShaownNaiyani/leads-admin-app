from django.db import models
from simple_history.models import HistoricalRecords
# Create your models here.


class LeadsCatagory(models.Model):
    catagory_type_id = models.IntegerField(unique=True, primary_key=True,
                                           blank=False, null=False, verbose_name="CatagoryTypeId", db_column='catagory_type_id')
    catagory_name = models.CharField(max_length=255, unique=True,
                                     blank=False, null=False, verbose_name="CatagoryName")


class LeadsDataAbstractModelFields(models.Model):
    asin = models.CharField(max_length=255, unique=True, primary_key=True,
                            blank=False, null=False, verbose_name="ASIN", db_column='asin')
    product_name = models.CharField(max_length=255,
                                    blank=True, null=True, verbose_name="product_name")
    amazon_fba_estimated_fees = models.DecimalField(blank=True, null=True,
                                                    max_digits=10, decimal_places=2, verbose_name="AmazonFBAEstimatedFees")
    amazon_price = models.DecimalField(blank=True, null=True,
                                       max_digits=10, decimal_places=2, verbose_name="AmazonPrice")
    sourcing_price = models.DecimalField(blank=True,  null=True,
                                         max_digits=10, decimal_places=2, verbose_name="SourcingPrice")
    estimated_sales_rank = models.PositiveIntegerField(
        default=0, verbose_name="EstimatedSalesRank")
    sales_rank_30_days = models.PositiveIntegerField(
        default=0, verbose_name="SalesRank30Days")
    sales_rank_90_days = models.PositiveIntegerField(
        default=0, verbose_name="SalesRank90Days")
    estimated_monthly_sales = models.PositiveIntegerField(
        default=0, verbose_name="EstimatedMonthlySales")
    product_image_url = models.URLField(
        blank=True,  null=True, verbose_name="ProductImageUrl")
    sourcing_url = models.URLField(
        blank=True,  null=True, verbose_name="SourcingUrl")
    sourcing_price = models.DecimalField(blank=True,  null=True,
                                         max_digits=10, decimal_places=2, verbose_name="SourcingPrice")
    amazon_url = models.URLField(
        blank=True,  null=True, verbose_name="AmazonUrl")
    amazon_on_listing = models.BooleanField(
        default=False,  null=True, verbose_name="AmazonOnListing")
    number_of_sellers_on_listing = models.PositiveIntegerField(
        default=0, verbose_name="NumberOfSellersOnListing")
    number_of_reviews = models.PositiveIntegerField(
        default=0, verbose_name="NumberOfReviews")
    estimated_gross_profit = models.DecimalField(blank=True,
                                                 max_digits=10, decimal_places=2,  null=True, verbose_name="EstimatedGrossProfit")
    estimated_gross_profit_margin = models.DecimalField(blank=True,
                                                        max_digits=10, decimal_places=2,  null=True, verbose_name="EstimatedGrossProfitMargin")
    estimated_net_profit = models.DecimalField(blank=True,
                                               max_digits=10, decimal_places=2,  null=True, verbose_name="EstimatedNetProfit")
    estimated_net_profit_margin = models.DecimalField(blank=True,
                                                      max_digits=10, decimal_places=2,  null=True, verbose_name="EstimatedNetProfitMargin")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.asin


class Electronics(LeadsDataAbstractModelFields):
    history = HistoricalRecords()

    def __str__(self):
        return self.asin


class Books(LeadsDataAbstractModelFields):
    history = HistoricalRecords()

    def __str__(self):
        return self.asin


class HomeAndKitchen(LeadsDataAbstractModelFields):
    history = HistoricalRecords()

    def __str__(self):
        return self.asin


class HealthAndBeauty(LeadsDataAbstractModelFields):
    history = HistoricalRecords()

    def __str__(self):
        return self.asin


class SoftwareAndMobileApps(LeadsDataAbstractModelFields):
    history = HistoricalRecords()

    def __str__(self):
        return self.asin


class ClothingAndAccessories(LeadsDataAbstractModelFields):
    history = HistoricalRecords()

    def __str__(self):
        return self.asin


class ToolsAndHome(LeadsDataAbstractModelFields):
    history = HistoricalRecords()

    def __str__(self):
        return self.asin


class SportsAndOutdoors(LeadsDataAbstractModelFields):
    history = HistoricalRecords()

    def __str__(self):
        return self.asin


class MoviesAndTv(LeadsDataAbstractModelFields):
    history = HistoricalRecords()

    def __str__(self):
        return self.asin


class ToyAndGames(LeadsDataAbstractModelFields):
    history = HistoricalRecords()

    def __str__(self):
        return self.asin


class GroceryAndGourMetFood(LeadsDataAbstractModelFields):
    history = HistoricalRecords()

    def __str__(self):
        return self.asin


class OfficeProducts(LeadsDataAbstractModelFields):
    history = HistoricalRecords()

    def __str__(self):
        return self.asin


class PetSupplies(LeadsDataAbstractModelFields):
    history = HistoricalRecords()

    def __str__(self):
        return self.asin


class AutoMotiveAndIndustrial(LeadsDataAbstractModelFields):
    history = HistoricalRecords()

    def __str__(self):
        return self.asin
