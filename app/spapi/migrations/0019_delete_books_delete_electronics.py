# Generated by Django 4.2 on 2024-02-25 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spapi', '0018_delete_homeandkitchen'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Books',
        ),
        migrations.DeleteModel(
            name='Electronics',
        ),
    ]
