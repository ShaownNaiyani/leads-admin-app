# Generated by Django 4.2.10 on 2024-03-22 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0008_alter_historicalautomotiveandindustrial_table_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LeadsCatagory',
            new_name='LeadsCategory',
        ),
        migrations.RenameField(
            model_name='leadscategory',
            old_name='catagory_name',
            new_name='category_name',
        ),
        migrations.RenameField(
            model_name='leadscategory',
            old_name='catagory_type_id',
            new_name='category_type_id',
        ),
    ]
