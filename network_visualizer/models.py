# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Authors(models.Model):
    authorid = models.IntegerField(db_column='AuthorID', primary_key=True) # Field name made lowercase.
    authorname = models.CharField(db_column='AuthorName', max_length=64, blank=True) # Field name made lowercase.
    emailid = models.CharField(db_column='EmailID', max_length=64, blank=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'Authors'

class Citations(models.Model):
    sourcepaperid = models.IntegerField(db_column='sourcePaperId', blank=True, null=True) # Field name made lowercase.
    targetpaperid = models.IntegerField(db_column='targetPaperId', blank=True, null=True) # Field name made lowercase.
    citationid = models.IntegerField(db_column='citationId', primary_key=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'Citations'

class Cocredits(models.Model):
    authorid = models.IntegerField(db_column='AuthorID') # Field name made lowercase.
    coauthorid = models.IntegerField(db_column='CoAuthorID') # Field name made lowercase.
    paperid = models.IntegerField(db_column='PaperID') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'CoCredits'

class Keywordtopaper(models.Model):
    paperid = models.IntegerField(db_column='PaperId', blank=True, null=True) # Field name made lowercase.
    keywordid = models.IntegerField(db_column='KeywordId', blank=True, null=True) # Field name made lowercase.
    id = models.IntegerField(primary_key=True)
    class Meta:
        managed = False
        db_table = 'KeywordToPaper'

class Keywords(models.Model):
    keywordid = models.IntegerField(db_column='KeywordId', primary_key=True) # Field name made lowercase.
    keyword = models.CharField(db_column='Keyword', max_length=50, blank=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'Keywords'

class Papers(models.Model):
    paperid = models.IntegerField(db_column='PaperID', primary_key=True) # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=300, blank=True) # Field name made lowercase.
    doi = models.CharField(db_column='DOI', max_length=20, blank=True) # Field name made lowercase.
    numauthors = models.IntegerField(db_column='NumAuthors') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'Papers'

class Topfives(models.Model):
    parentid = models.IntegerField(db_column='parentId', blank=True, null=True) # Field name made lowercase.
    childid = models.IntegerField(db_column='childId', blank=True, null=True) # Field name made lowercase.
    rank = models.IntegerField(blank=True, null=True)
    id = models.IntegerField(primary_key=True)
    class Meta:
        managed = False
        db_table = 'TopFives'

class Works(models.Model):
    authorid = models.IntegerField(db_column='AuthorId', blank=True, null=True) # Field name made lowercase.
    paperid = models.IntegerField(db_column='PaperId', blank=True, null=True) # Field name made lowercase.
    workid = models.IntegerField(db_column='workId', primary_key=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'Works'

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=80)
    class Meta:
        managed = False
        db_table = 'auth_group'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'auth_permission'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        managed = False
        db_table = 'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'

class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.IntegerField()
    change_message = models.TextField()
    class Meta:
        managed = False
        db_table = 'django_admin_log'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'django_content_type'

class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'django_session'

class SouthMigrationhistory(models.Model):
    id = models.IntegerField(primary_key=True)
    app_name = models.CharField(max_length=255)
    migration = models.CharField(max_length=255)
    applied = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'south_migrationhistory'

