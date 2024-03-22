from django.db import models
from simple_history.models import HistoricalRecords
# Create your models here.


class LeadsCategory(models.Model):
    class Meta:
        db_table = 'leads_category'

    category_type_id = models.IntegerField(unique=True, primary_key=True,
                                           blank=False, null=False, verbose_name="CatagoryTypeId", db_column='category_id')
    category_name = models.CharField(max_length=255, unique=True,
                                     blank=False, null=False, verbose_name="CatagoryName")


class LeadsDataAbstractModelFields(models.Model):
    asin = models.CharField(max_length=255, unique=True, primary_key=True,
                            blank=False, null=False, verbose_name="ASIN", db_column='asin')
    product_name = models.CharField(max_length=255,
                                    blank=True, null=True, verbose_name="product_name")
    amazon_fba_estimated_fees = models.DecimalField(blank=True, null=True,
                                                    max_digits=10, decimal_places=6, verbose_name="AmazonFBAEstimatedFees")
    amazon_price = models.DecimalField(blank=True, null=True,
                                       max_digits=10, decimal_places=6, verbose_name="AmazonPrice")
    sourcing_price = models.DecimalField(blank=True,  null=True,
                                         max_digits=10, decimal_places=6, verbose_name="SourcingPrice")
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
                                         max_digits=10, decimal_places=6, verbose_name="SourcingPrice")
    amazon_url = models.URLField(
        blank=True,  null=True, verbose_name="AmazonUrl")
    amazon_on_listing = models.BooleanField(
        default=False,  null=True, verbose_name="AmazonOnListing")
    number_of_sellers_on_listing = models.PositiveIntegerField(
        default=0, verbose_name="NumberOfSellersOnListing")
    number_of_reviews = models.PositiveIntegerField(
        default=0, verbose_name="NumberOfReviews")
    estimated_gross_profit = models.DecimalField(blank=True,
                                                 max_digits=10, decimal_places=6,  null=True, verbose_name="EstimatedGrossProfit")
    estimated_gross_profit_margin = models.DecimalField(blank=True,
                                                        max_digits=10, decimal_places=6,  null=True, verbose_name="EstimatedGrossProfitMargin")
    estimated_net_profit = models.DecimalField(blank=True,
                                               max_digits=10, decimal_places=6,  null=True, verbose_name="EstimatedNetProfit")
    estimated_net_profit_margin = models.DecimalField(blank=True,
                                                      max_digits=10, decimal_places=6,  null=True, verbose_name="EstimatedNetProfitMargin")
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
    class Meta:
        db_table = 'leads_home_and_kitchen'
    history = HistoricalRecords(table_name='history_leads_home_and_kitchen')

    def __str__(self):
        return self.asin


class HealthAndBeauty(LeadsDataAbstractModelFields):
    class Meta:
        db_table = 'leads_health_and_beauty'
    history = HistoricalRecords(table_name='history_leads_health_and_beauty')

    def __str__(self):
        return self.asin


class SoftwareAndMobileApps(LeadsDataAbstractModelFields):
    class Meta:
        db_table = 'leads_software_and_mobile_apps'
    history = HistoricalRecords(
        table_name='history_leads_software_and_mobile_apps')

    def __str__(self):
        return self.asin


class ClothingAndAccessories(LeadsDataAbstractModelFields):
    class Meta:
        db_table = 'leads_clothing_and_accessories'
    history = HistoricalRecords(
        table_name='history_leads_clothing_and_accessories')

    def __str__(self):
        return self.asin


class ToolsAndHome(LeadsDataAbstractModelFields):
    class Meta:
        db_table = 'leads_tools_and_home'
    history = HistoricalRecords(table_name='history_leads_tools_and_home')

    def __str__(self):
        return self.asin


class SportsAndOutdoors(LeadsDataAbstractModelFields):
    class Meta:
        db_table = 'leads_sports_and_outdoors'
    history = HistoricalRecords(table_name='history_leads_sports_and_outdoors')

    def __str__(self):
        return self.asin


class MoviesAndTv(LeadsDataAbstractModelFields):
    class Meta:
        db_table = 'leads_movies_and_tv'
    history = HistoricalRecords(table_name='history_leads_movies_and_tv')

    def __str__(self):
        return self.asin


class ToyAndGames(LeadsDataAbstractModelFields):
    class Meta:
        db_table = 'leads_toy_and_games'
    history = HistoricalRecords(table_name='history_leads_toy_and_games')

    def __str__(self):
        return self.asin


class GroceryAndGourMetFood(LeadsDataAbstractModelFields):
    class Meta:
        db_table = 'leads_grocery_and_gourmet_food'
    history = HistoricalRecords(
        table_name='history_leads_grocery_and_gourmet_food')

    def __str__(self):
        return self.asin


class OfficeProducts(LeadsDataAbstractModelFields):
    class Meta:
        db_table = 'leads_office_product'
    history = HistoricalRecords(table_name='history_leads_office_product')

    def __str__(self):
        return self.asin


class PetSupplies(LeadsDataAbstractModelFields):
    class Meta:
        db_table = 'leads_pets_supplies'
    history = HistoricalRecords(table_name='history_leads_pets_supplies')

    def __str__(self):
        return self.asin


class AutoMotiveAndIndustrial(LeadsDataAbstractModelFields):
    class Meta:
        db_table = 'leads_automotive_and_industrial'

    history = HistoricalRecords(
        table_name='history_leads_automotive_and_industrial')

    def __str__(self):
        return self.asin
