# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NonStudent'
        db.create_table('advisornotes_nonstudent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('pref_first_name', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('high_school', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('college', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('start_year', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coredata.Unit'], null=True, blank=True)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from=None, unique_with=())),
            ('config', self.gf('jsonfield.fields.JSONField')(default={})),
        ))
        db.send_create_signal('advisornotes', ['NonStudent'])

        # Adding model 'AdvisorNote'
        db.create_table('advisornotes_advisornote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(related_name='student', null=True, to=orm['coredata.Person'])),
            ('nonstudent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['advisornotes.NonStudent'], null=True)),
            ('advisor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='advisor', to=orm['coredata.Person'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('file_attachment', self.gf('django.db.models.fields.files.FileField')(max_length=500, null=True, blank=True)),
            ('file_mediatype', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coredata.Unit'])),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('emailed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('advisornotes', ['AdvisorNote'])

        # Adding model 'Artifact'
        db.create_table('advisornotes_artifact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from=None, unique_with=())),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coredata.Unit'])),
            ('config', self.gf('jsonfield.fields.JSONField')(default={})),
        ))
        db.send_create_signal('advisornotes', ['Artifact'])

        # Adding unique constraint on 'Artifact', fields ['name', 'unit']
        db.create_unique('advisornotes_artifact', ['name', 'unit_id'])

        # Adding model 'ArtifactNote'
        db.create_table('advisornotes_artifactnote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coredata.Course'], null=True, blank=True)),
            ('course_offering', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coredata.CourseOffering'], null=True, blank=True)),
            ('artifact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['advisornotes.Artifact'], null=True, blank=True)),
            ('important', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('advisor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coredata.Person'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('best_before', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('file_attachment', self.gf('django.db.models.fields.files.FileField')(max_length=500, null=True, blank=True)),
            ('file_mediatype', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coredata.Unit'])),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal('advisornotes', ['ArtifactNote'])


    def backwards(self, orm):
        # Removing unique constraint on 'Artifact', fields ['name', 'unit']
        db.delete_unique('advisornotes_artifact', ['name', 'unit_id'])

        # Deleting model 'NonStudent'
        db.delete_table('advisornotes_nonstudent')

        # Deleting model 'AdvisorNote'
        db.delete_table('advisornotes_advisornote')

        # Deleting model 'Artifact'
        db.delete_table('advisornotes_artifact')

        # Deleting model 'ArtifactNote'
        db.delete_table('advisornotes_artifactnote')


    models = {
        'advisornotes.advisornote': {
            'Meta': {'ordering': "['student', 'created_at']", 'object_name': 'AdvisorNote'},
            'advisor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'advisor'", 'to': "orm['coredata.Person']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'emailed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'file_attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'file_mediatype': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nonstudent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['advisornotes.NonStudent']", 'null': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'student'", 'null': 'True', 'to': "orm['coredata.Person']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coredata.Unit']"})
        },
        'advisornotes.artifact': {
            'Meta': {'ordering': "['name']", 'unique_together': "[('name', 'unit')]", 'object_name': 'Artifact'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'config': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coredata.Unit']"})
        },
        'advisornotes.artifactnote': {
            'Meta': {'ordering': "['created_at']", 'object_name': 'ArtifactNote'},
            'advisor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coredata.Person']"}),
            'artifact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['advisornotes.Artifact']", 'null': 'True', 'blank': 'True'}),
            'best_before': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coredata.Course']", 'null': 'True', 'blank': 'True'}),
            'course_offering': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coredata.CourseOffering']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file_attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'file_mediatype': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'important': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coredata.Unit']"})
        },
        'advisornotes.nonstudent': {
            'Meta': {'object_name': 'NonStudent'},
            'college': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'config': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'high_school': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'pref_first_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()'}),
            'start_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coredata.Unit']", 'null': 'True', 'blank': 'True'})
        },
        'coredata.course': {
            'Meta': {'ordering': "('subject', 'number')", 'unique_together': "(('subject', 'number'),)", 'object_name': 'Course'},
            'config': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '4', 'db_index': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '4', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'coredata.courseoffering': {
            'Meta': {'ordering': "['-semester', 'subject', 'number', 'section']", 'unique_together': "(('semester', 'subject', 'number', 'section'), ('semester', 'crse_id', 'section'), ('semester', 'class_nbr'))", 'object_name': 'CourseOffering'},
            'campus': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'class_nbr': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'component': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_index': 'True'}),
            'config': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coredata.Course']"}),
            'crse_id': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'enrl_cap': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'enrl_tot': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'flags': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'graded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instr_mode': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '2', 'db_index': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'member'", 'symmetrical': 'False', 'through': "orm['coredata.Member']", 'to': "orm['coredata.Person']"}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '4', 'db_index': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coredata.Unit']", 'null': 'True'}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '4', 'db_index': 'True'}),
            'semester': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coredata.Semester']"}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '4', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True'}),
            'units': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'wait_tot': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'coredata.member': {
            'Meta': {'ordering': "['offering', 'person']", 'object_name': 'Member'},
            'added_reason': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'career': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'config': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'credits': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'labtut_section': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'offering': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coredata.CourseOffering']"}),
            'official_grade': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'person'", 'to': "orm['coredata.Person']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        },
        'coredata.person': {
            'Meta': {'ordering': "['last_name', 'first_name', 'userid']", 'object_name': 'Person'},
            'config': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'emplid': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'pref_first_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'userid': ('django.db.models.fields.CharField', [], {'max_length': '8', 'unique': 'True', 'null': 'True', 'db_index': 'True'})
        },
        'coredata.semester': {
            'Meta': {'ordering': "['name']", 'object_name': 'Semester'},
            'end': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4', 'db_index': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {})
        },
        'coredata.unit': {
            'Meta': {'ordering': "['label']", 'object_name': 'Unit'},
            'acad_org': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'config': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coredata.Unit']", 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()'})
        }
    }

    complete_apps = ['advisornotes']