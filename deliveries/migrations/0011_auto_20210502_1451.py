# Generated by Django 3.2 on 2021-05-02 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deliveries', '0010_auto_20210502_0305'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='box',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='delivery',
            name='city',
            field=models.CharField(default='Detroit', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='delivery',
            name='delivery_notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='delivery',
            name='driver_notes',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='delivery',
            name='member_id',
            field=models.CharField(default='00000000', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='delivery',
            name='phone',
            field=models.CharField(default='734-277-5603', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='delivery',
            name='status_change_time',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='delivery',
            name='street_address',
            field=models.CharField(default='319 Josephine St', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='delivery',
            name='text_opt_int',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='delivery',
            name='zip_code',
            field=models.CharField(default='48202', max_length=12),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='route',
            name='driver',
            field=models.CharField(default='Unassigned', max_length=255),
        ),
    ]
