# Generated by Django 2.0 on 2017-12-16 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20171216_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tag',
            field=models.CharField(blank=True, choices=[('Python3.6.3', 'Python3.6.3'), ('Django1.11', 'Django1.11'), ('Django', 'Django'), ('Nodejs', 'Nodejs'), ('jQuery', 'jQuery'), ('CSS', 'CSS'), ('Font-end', 'Font-end'), ('Back-end', 'Back-end'), ('Bootstrap', 'Bootstrap')], max_length=20, null=True),
        ),
    ]
