# Generated by Django 4.2.10 on 2024-04-19 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0016_alter_automotiveandindustrial_amazon_fba_estimated_fees_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='automotiveandindustrial',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AddField(
            model_name='books',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AddField(
            model_name='clothingandaccessories',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AddField(
            model_name='electronics',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AddField(
            model_name='groceryandgourmetfood',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AddField(
            model_name='healthandbeauty',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AddField(
            model_name='historicalautomotiveandindustrial',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AddField(
            model_name='historicalbooks',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AddField(
            model_name='historicalclothingandaccessories',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AddField(
            model_name='historicalelectronics',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AddField(
            model_name='historicalgroceryandgourmetfood',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AddField(
            model_name='historicalhealthandbeauty',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AddField(
            model_name='historicalhomeandkitchen',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AddField(
            model_name='historicalmoviesandtv',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AddField(
            model_name='historicalofficeproducts',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AddField(
            model_name='historicalpetsupplies',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AddField(
            model_name='historicalsoftwareandmobileapps',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AddField(
            model_name='historicalsportsandoutdoors',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AddField(
            model_name='historicaltoolsandhome',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AddField(
            model_name='historicaltoyandgames',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AddField(
            model_name='homeandkitchen',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AddField(
            model_name='moviesandtv',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AddField(
            model_name='officeproducts',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AddField(
            model_name='petsupplies',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AddField(
            model_name='softwareandmobileapps',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AddField(
            model_name='sportsandoutdoors',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AddField(
            model_name='toolsandhome',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AddField(
            model_name='toyandgames',
            name='category_id',
            field=models.PositiveIntegerField(default=0, verbose_name='CategoryId'),
        ),
        migrations.AlterField(
            model_name='automotiveandindustrial',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
        migrations.AlterField(
            model_name='books',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
        migrations.AlterField(
            model_name='clothingandaccessories',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
        migrations.AlterField(
            model_name='electronics',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
        migrations.AlterField(
            model_name='groceryandgourmetfood',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
        migrations.AlterField(
            model_name='healthandbeauty',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
        migrations.AlterField(
            model_name='historicalautomotiveandindustrial',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
        migrations.AlterField(
            model_name='historicalbooks',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
        migrations.AlterField(
            model_name='historicalclothingandaccessories',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
        migrations.AlterField(
            model_name='historicalelectronics',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
        migrations.AlterField(
            model_name='historicalgroceryandgourmetfood',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
        migrations.AlterField(
            model_name='historicalhealthandbeauty',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
        migrations.AlterField(
            model_name='historicalhomeandkitchen',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
        migrations.AlterField(
            model_name='historicalmoviesandtv',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
        migrations.AlterField(
            model_name='historicalofficeproducts',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
        migrations.AlterField(
            model_name='historicalpetsupplies',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
        migrations.AlterField(
            model_name='historicalsoftwareandmobileapps',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
        migrations.AlterField(
            model_name='historicalsportsandoutdoors',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
        migrations.AlterField(
            model_name='historicaltoolsandhome',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
        migrations.AlterField(
            model_name='historicaltoyandgames',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
        migrations.AlterField(
            model_name='homeandkitchen',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
        migrations.AlterField(
            model_name='moviesandtv',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
        migrations.AlterField(
            model_name='officeproducts',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
        migrations.AlterField(
            model_name='petsupplies',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
        migrations.AlterField(
            model_name='softwareandmobileapps',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
        migrations.AlterField(
            model_name='sportsandoutdoors',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
        migrations.AlterField(
            model_name='toolsandhome',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
        migrations.AlterField(
            model_name='toyandgames',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ProductName'),
        ),
    ]
