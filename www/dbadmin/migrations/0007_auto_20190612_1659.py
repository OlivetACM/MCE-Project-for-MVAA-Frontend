# Generated by Django 2.2.2 on 2019-06-12 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbadmin', '0006_institution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='InstitutionID',
            field=models.IntegerField(choices=[(1, 'Olivet'), (2, 'KCC'), (3, 'Military')]),
        ),
    ]
