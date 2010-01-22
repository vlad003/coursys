from django.db import models
from grades.models import NumericActivity, NumericGrade 

class ActivityComponent(models.Model):
    """    
    Markable Component of a numeric activity   
    """
    numeric_activity = models.ForeignKey(NumericActivity, null = False)
    max_mark = models.DecimalField(max_digits=5, decimal_places=2)
    title = models.CharField(max_length=30, help_text='Title of the component.')
    description = models.CharField(max_length = 200, help_text='Description of the component')
    def __unicode__(self):
        return "component %s for %s" % (self.title, self.numeric_activity)
    class Meta:
        unique_together = (('numeric_activity', 'title'),)
    
    
class ActivityMark(models.Model):
    """
    General Marking class for one numeric activity 
    """    
    overall_comment = models.TextField(null = True, max_length=1000, blank=True)
    late_penalty = models.IntegerField(null = True, default = 0, blank = True)
    
    #TODO: add mark adjustment and reason fields  
    def __unicode__(self):
        # get the activity
        activity = self.numeric_grade.typed_activity      
        return "Marking for for activity [%s]" %(activity,)

class StudentActivityMark(ActivityMark):
    """
    Marking of one student on one numeric activity 
    """        
    numeric_grade = models.OneToOneField(NumericGrade, null = False)
    
    def __unicode__(self):
        # get the student and the activity
        student = self.numeric_grade.member.person
        activity = self.numeric_grade.typed_activity      
        return "Marking for [%s] for activity [%s]" %(student, activity)

    def setMark(self, grade):
        self.numeric_grade.value = grade
        self.numeric_grade.flag = FLAGS['GRAD']
        self.numeric_grade.save()    
        
class GroupActivityMark(ActivityMark):
    """
    Marking of one group on one numeric activity
    """
    group = None #TODO:change to ForeignKey(Group.group object, null = False)
    grade = models.DecimalField(max_digits=5, decimal_places=2)
    def __unicode__(self):
        return "Marking for [%s] for activity [%s]" %(self.group,)
    
    def setMark(self, grade, status_flag):
        #set mark for each of the student in the group
        grade = value
 
class ActivityComponentMark(models.Model):
    """
    Marking of one particular component of an activity for one student  
    Stores the mark the student gets for the component
    """
    activity_mark = models.ForeignKey(ActivityMark, null = False)    
    activity_component = models.ForeignKey(ActivityComponent, null = False)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    comment = models.TextField(null = True, max_length=1000, blank=True)
    
    def __unicode__(self):
        # get the student and the activity
        student = self.activity_mark.numeric_grade.member.person  
        return "Marking for [%s]" %(self.activity_component,)
        
    class Meta:
        unique_together = (('activity_mark', 'activity_component'),)
    
    
