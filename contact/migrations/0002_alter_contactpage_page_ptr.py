# Generated by Django 4.1.5 on 2023-01-21 23:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0078_referenceindex'),
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactpage',
            name='page_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page'),
        ),
    ]
