# Generated by Django 4.2 on 2024-01-24 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "library",
            "0003_author_bio_author_birth_date_book_quantity_available_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="published_date",
            field=models.DateField(null=True),
        ),
    ]