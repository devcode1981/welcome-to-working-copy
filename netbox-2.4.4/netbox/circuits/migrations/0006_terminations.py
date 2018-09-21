# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-13 16:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def circuits_to_terms(apps, schema_editor):
    Circuit = apps.get_model('circuits', 'Circuit')
    CircuitTermination = apps.get_model('circuits', 'CircuitTermination')
    for c in Circuit.objects.all():
        CircuitTermination(
            circuit=c,
            term_side=b'A',
            site=c.site,
            interface=c.interface,
            port_speed=c.port_speed,
            upstream_speed=c.upstream_speed,
            xconnect_id=c.xconnect_id,
            pp_info=c.pp_info,
        ).save()


def terms_to_circuits(apps, schema_editor):
    CircuitTermination = apps.get_model('circuits', 'CircuitTermination')
    for ct in CircuitTermination.objects.filter(term_side='A'):
        c = ct.circuit
        c.site = ct.site
        c.interface = ct.interface
        c.port_speed = ct.port_speed
        c.upstream_speed = ct.upstream_speed
        c.xconnect_id = ct.xconnect_id
        c.pp_info = ct.pp_info
        c.save()


class Migration(migrations.Migration):

    dependencies = [
        ('dcim', '0022_color_names_to_rgb'),
        ('circuits', '0005_circuit_add_upstream_speed'),
    ]

    operations = [
        migrations.CreateModel(
            name='CircuitTermination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term_side', models.CharField(choices=[(b'A', b'A'), (b'Z', b'Z')], max_length=1,
                                               verbose_name='Termination')),
                ('port_speed', models.PositiveIntegerField(verbose_name=b'Port speed (Kbps)')),
                ('upstream_speed',
                 models.PositiveIntegerField(blank=True, help_text=b'Upstream speed, if different from port speed',
                                             null=True, verbose_name=b'Upstream speed (Kbps)')),
                ('xconnect_id', models.CharField(blank=True, max_length=50, verbose_name=b'Cross-connect ID')),
                ('pp_info', models.CharField(blank=True, max_length=100, verbose_name=b'Patch panel/port(s)')),
                ('circuit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='terminations',
                                              to='circuits.Circuit')),
                ('interface', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                                   related_name='circuit_termination', to='dcim.Interface')),
                ('site',
                 models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='circuit_terminations',
                                   to='dcim.Site')),
            ],
            options={
                'ordering': ['circuit', 'term_side'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='circuittermination',
            unique_together=set([('circuit', 'term_side')]),
        ),
        migrations.RunPython(circuits_to_terms, terms_to_circuits),
        migrations.RemoveField(
            model_name='circuit',
            name='interface',
        ),
        migrations.RemoveField(
            model_name='circuit',
            name='port_speed',
        ),
        migrations.RemoveField(
            model_name='circuit',
            name='pp_info',
        ),
        migrations.RemoveField(
            model_name='circuit',
            name='site',
        ),
        migrations.RemoveField(
            model_name='circuit',
            name='upstream_speed',
        ),
        migrations.RemoveField(
            model_name='circuit',
            name='xconnect_id',
        ),
    ]
