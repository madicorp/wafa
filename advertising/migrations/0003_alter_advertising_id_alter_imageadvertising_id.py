# Generated by Django 5.1.2 on 2024-10-26 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertising', '0002_auto_20200315_2257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertising',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='imageadvertising',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
