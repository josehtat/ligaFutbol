# Generated by Django 4.2 on 2025-02-13 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('futbol', '0002_alter_event_jugador_alter_event_partit'),
    ]

    operations = [
        migrations.AddField(
            model_name='equip',
            name='ciutat',
            field=models.CharField(default='ninguna parte', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='equip',
            name='estadi',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
