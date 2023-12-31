# Generated by Django 4.2.5 on 2023-09-10 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AWSReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=10)),
                ('status_extended', models.TextField()),
                ('check_metadata', models.JSONField()),
                ('resource_details', models.TextField()),
                ('resource_tags', models.JSONField()),
                ('resource_id', models.CharField(max_length=100)),
                ('resource_arn', models.CharField(max_length=255)),
                ('region', models.CharField(max_length=50)),
            ],
        ),
    ]
