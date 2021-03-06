# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Activity'
        db.create_table('grades_activity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, db_index=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=50, populate_from=None)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('due_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('percent', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('group', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('config', self.gf('jsonfield.fields.JSONField')(default={})),
            ('offering', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coredata.CourseOffering'])),
        ))
        db.send_create_signal('grades', ['Activity'])

        # Adding unique constraint on 'Activity', fields ['offering', 'slug']
        db.create_unique('grades_activity', ['offering_id', 'slug'])

        # Adding model 'NumericActivity'
        db.create_table('grades_numericactivity', (
            ('activity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['grades.Activity'], unique=True, primary_key=True)),
            ('max_grade', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
        ))
        db.send_create_signal('grades', ['NumericActivity'])

        # Adding model 'LetterActivity'
        db.create_table('grades_letteractivity', (
            ('activity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['grades.Activity'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('grades', ['LetterActivity'])

        # Adding model 'CalNumericActivity'
        db.create_table('grades_calnumericactivity', (
            ('numericactivity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['grades.NumericActivity'], unique=True, primary_key=True)),
            ('formula', self.gf('django.db.models.fields.TextField')(default='[[activitytotal]]')),
        ))
        db.send_create_signal('grades', ['CalNumericActivity'])

        # Adding model 'CalLetterActivity'
        db.create_table('grades_calletteractivity', (
            ('letteractivity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['grades.LetterActivity'], unique=True, primary_key=True)),
            ('numeric_activity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='numeric_source', to=orm['grades.NumericActivity'])),
            ('exam_activity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='exam_activity', null=True, to=orm['grades.Activity'])),
            ('letter_cutoffs', self.gf('django.db.models.fields.CharField')(default='[95, 90, 85, 80, 75, 70, 65, 60, 55, 50]', max_length=500)),
        ))
        db.send_create_signal('grades', ['CalLetterActivity'])

        # Adding model 'NumericGrade'
        db.create_table('grades_numericgrade', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['grades.NumericActivity'])),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coredata.Member'])),
            ('value', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2)),
            ('flag', self.gf('django.db.models.fields.CharField')(default='NOGR', max_length=4)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('grades', ['NumericGrade'])

        # Adding unique constraint on 'NumericGrade', fields ['activity', 'member']
        db.create_unique('grades_numericgrade', ['activity_id', 'member_id'])

        # Adding model 'LetterGrade'
        db.create_table('grades_lettergrade', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['grades.LetterActivity'])),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coredata.Member'])),
            ('letter_grade', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('flag', self.gf('django.db.models.fields.CharField')(default='NOGR', max_length=4)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('grades', ['LetterGrade'])

        # Adding unique constraint on 'LetterGrade', fields ['activity', 'member']
        db.create_unique('grades_lettergrade', ['activity_id', 'member_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'LetterGrade', fields ['activity', 'member']
        db.delete_unique('grades_lettergrade', ['activity_id', 'member_id'])

        # Removing unique constraint on 'NumericGrade', fields ['activity', 'member']
        db.delete_unique('grades_numericgrade', ['activity_id', 'member_id'])

        # Removing unique constraint on 'Activity', fields ['offering', 'slug']
        db.delete_unique('grades_activity', ['offering_id', 'slug'])

        # Deleting model 'Activity'
        db.delete_table('grades_activity')

        # Deleting model 'NumericActivity'
        db.delete_table('grades_numericactivity')

        # Deleting model 'LetterActivity'
        db.delete_table('grades_letteractivity')

        # Deleting model 'CalNumericActivity'
        db.delete_table('grades_calnumericactivity')

        # Deleting model 'CalLetterActivity'
        db.delete_table('grades_calletteractivity')

        # Deleting model 'NumericGrade'
        db.delete_table('grades_numericgrade')

        # Deleting model 'LetterGrade'
        db.delete_table('grades_lettergrade')


    models = {
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
        },
        'grades.activity': {
            'Meta': {'ordering': "['deleted', 'position']", 'unique_together': "(('offering', 'slug'),)", 'object_name': 'Activity'},
            'config': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'due_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'group': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True'}),
            'offering': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coredata.CourseOffering']"}),
            'percent': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        },
        'grades.calletteractivity': {
            'Meta': {'ordering': "['deleted', 'position']", 'object_name': 'CalLetterActivity', '_ormbases': ['grades.LetterActivity']},
            'exam_activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'exam_activity'", 'null': 'True', 'to': "orm['grades.Activity']"}),
            'letter_cutoffs': ('django.db.models.fields.CharField', [], {'default': "'[95, 90, 85, 80, 75, 70, 65, 60, 55, 50]'", 'max_length': '500'}),
            'letteractivity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['grades.LetterActivity']", 'unique': 'True', 'primary_key': 'True'}),
            'numeric_activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'numeric_source'", 'to': "orm['grades.NumericActivity']"})
        },
        'grades.calnumericactivity': {
            'Meta': {'ordering': "['deleted', 'position']", 'object_name': 'CalNumericActivity', '_ormbases': ['grades.NumericActivity']},
            'formula': ('django.db.models.fields.TextField', [], {'default': "'[[activitytotal]]'"}),
            'numericactivity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['grades.NumericActivity']", 'unique': 'True', 'primary_key': 'True'})
        },
        'grades.letteractivity': {
            'Meta': {'ordering': "['deleted', 'position']", 'object_name': 'LetterActivity', '_ormbases': ['grades.Activity']},
            'activity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['grades.Activity']", 'unique': 'True', 'primary_key': 'True'})
        },
        'grades.lettergrade': {
            'Meta': {'unique_together': "(('activity', 'member'),)", 'object_name': 'LetterGrade'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grades.LetterActivity']"}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'flag': ('django.db.models.fields.CharField', [], {'default': "'NOGR'", 'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letter_grade': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coredata.Member']"})
        },
        'grades.numericactivity': {
            'Meta': {'ordering': "['deleted', 'position']", 'object_name': 'NumericActivity', '_ormbases': ['grades.Activity']},
            'activity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['grades.Activity']", 'unique': 'True', 'primary_key': 'True'}),
            'max_grade': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'})
        },
        'grades.numericgrade': {
            'Meta': {'unique_together': "(('activity', 'member'),)", 'object_name': 'NumericGrade'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grades.NumericActivity']"}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'flag': ('django.db.models.fields.CharField', [], {'default': "'NOGR'", 'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coredata.Member']"}),
            'value': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'})
        },
        'groups.group': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name', 'courseoffering'), ('slug', 'courseoffering'), ('svn_slug', 'courseoffering'))", 'object_name': 'Group'},
            'courseoffering': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coredata.CourseOffering']"}),
            'groupForSemester': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coredata.Member']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None'}),
            'svn_slug': ('autoslug.fields.AutoSlugField', [], {'max_length': '17', 'unique_with': '()', 'null': 'True', 'populate_from': 'None'})
        },
        'marking.activitymark': {
            'Meta': {'ordering': "['created_at']", 'object_name': 'ActivityMark'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grades.NumericActivity']", 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'file_attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'file_mediatype': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'late_penalty': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'mark': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'mark_adjustment': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'mark_adjustment_reason': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'overall_comment': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['grades']