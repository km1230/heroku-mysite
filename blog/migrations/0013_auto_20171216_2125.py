# Generated by Django 2.0 on 2017-12-16 10:25

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20171216_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tag',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Python3.6', 'Python3.6'), ('Django2.0', 'Django2.0'), ('Nodejs', 'Nodejs'), ('jQuery', 'jQuery'), ('CSS', 'CSS'), ('Font-end', 'Font-end'), ('Back-end', 'Back-end'), ('Bootstrap', 'Bootstrap')], max_length=65, null=True),
        ),
    ]
