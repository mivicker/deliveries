# Generated by Django 3.2 on 2021-05-02 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deliveries', '0009_auto_20210430_0250'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='delivery',
            options={'ordering': ['stop_num'], 'verbose_name_plural': 'Deliveries'},
        ),
        migrations.AlterField(
            model_name='delivery',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='route',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='token',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]