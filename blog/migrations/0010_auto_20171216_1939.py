# Generated by Django 2.0 on 2017-12-16 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_post_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tag',
            field=models.CharField(blank=True, choices=[('Django', 'Django'), ('Nodejs', 'Nodejs'), ('jQuery', 'jQuery'), ('CSS', 'CSS'), ('Font-end', 'Font-end'), ('Back-end', 'Back-end'), ('Bootstrap', 'Bootstrap')], max_length=20, null=True),
        ),
    ]
