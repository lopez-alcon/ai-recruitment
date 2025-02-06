# Generated by Django 5.1.2 on 2024-10-21 13:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0002_joboffer_application_deadline_joboffer_benefits_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aiquestion',
            name='candidate',
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pendiente'), ('accepted', 'Aceptada'), ('rejected', 'Rechazada')], default='pending', max_length=20)),
                ('application_date', models.DateTimeField(auto_now_add=True)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruitment.candidate')),
                ('job_offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruitment.joboffer')),
            ],
        ),
        migrations.AddField(
            model_name='aiquestion',
            name='job_application',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='recruitment.jobapplication'),
            preserve_default=False,
        ),
    ]
