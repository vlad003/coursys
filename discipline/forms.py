from django import forms
from discipline.models import DisciplineCase, DisciplineGroup, DisciplineTemplate
from coredata.models import Member
from django.core.mail import send_mail
import datetime

class DisciplineGroupForm(forms.ModelForm):
    students = forms.MultipleChoiceField(choices=[], required=False)
    
    def __init__(self, offering, *args, **kwargs):
        super(DisciplineGroupForm, self).__init__(*args, **kwargs)
        # force the right course offering into place
        self.offering = offering
        self.fields['offering'].initial = offering.id
    
    def clean_offering(self):
        if self.cleaned_data['offering'] != self.offering:
            raise forms.ValidationError("Wrong course offering.")
        return self.cleaned_data['offering']
    
    class Meta:
        model = DisciplineGroup
        widgets = {
            'offering': forms.HiddenInput(),
        }

class DisciplineCaseForm(forms.ModelForm):
    student = forms.ChoiceField(choices=[])

    def __init__(self, offering, *args, **kwargs):
        super(DisciplineCaseForm, self).__init__(*args, **kwargs)
        # store the course offering for validation
        self.offering = offering
    
    def clean_student(self):
        userid = self.cleaned_data['student']
        members = Member.objects.filter(offering=self.offering, person__userid=userid)
        if members.count() != 1:
            raise forms.ValidationError("Can't find student")

        return members[0]
    
    class Meta:
        model = DisciplineCase
        fields = ("student", "group")


class TemplateForm(forms.ModelForm):
    class Meta:
        model = DisciplineTemplate
        widgets = {
            'text': forms.Textarea(attrs={'cols':'80', 'rows':'20'}),
        }


class CaseNotesForm(forms.ModelForm):
    class Meta:
        model = DisciplineCase
        fields = ("notes",)
        widgets = {
            'notes': forms.Textarea(attrs={'cols':'80', 'rows':'20'}),
        }
class CaseContactedForm(forms.ModelForm):
    def clean(self):
        """
        Send the mail if appropriate.
        """
        contacted = self.cleaned_data['contacted']
        text = self.cleaned_data['contact_email_text']

        if contacted=="MAIL":
            if not text.strip():
                raise forms.ValidationError('Must enter email text: email is sent to student on submitting this form.')
            send_mail( *self.instance.contact_email(message=text) )
            self.cleaned_data['contact_date'] = datetime.date.today()
            self.instance.just_emailed = True
        elif contacted=="OTHR":
            if not self.cleaned_data['contact_date']:
                raise forms.ValidationError('Please enter the date of initial contact about the case.')

        return self.cleaned_data

    class Meta:
        model = DisciplineCase
        fields = ("contacted", "contact_date", "contact_email_text")
        widgets = {
            'contacted': forms.RadioSelect(),
            'contact_email_text': forms.Textarea(attrs={'cols':'80', 'rows':'15'}),
        }
class CaseResponseForm(forms.ModelForm):
    class Meta:
        model = DisciplineCase
        fields = ("response",)
        widgets = {
            'response': forms.RadioSelect(),
        }
class CaseMeetingForm(forms.ModelForm):
    class Meta:
        model = DisciplineCase
        fields = ("meeting_date", "meeting_summary", "meeting_notes")
        widgets = {
            'meeting_summary': forms.Textarea(attrs={'cols':'80', 'rows':'10'}),
            'meeting_notes': forms.Textarea(attrs={'cols':'80', 'rows':'10'}),
        }
class CaseFactsForm(forms.ModelForm):
    class Meta:
        model = DisciplineCase
        fields = ("facts",)
        widgets = {
            'facts': forms.Textarea(attrs={'cols':'80', 'rows':'20'}),
        }
class CaseInstrPenaltyForm(forms.ModelForm):
    class Meta:
        model = DisciplineCase
        fields = ("instr_penalty", "refer_chair", "penalty_reason")
        widgets = {
            'instr_penalty': forms.RadioSelect(),
            'penalty_reason': forms.Textarea(attrs={'cols':'80', 'rows':'10'}),
        }
class CaseLetterReviewForm(forms.ModelForm):
    class Meta:
        model = DisciplineCase
        fields = ("letter_review",)

from grades.models import Activity
from groups.models import GroupMember
from submission.models import StudentSubmission, GroupSubmission
import itertools
class CaseRelatedForm(forms.Form):
    activities = forms.MultipleChoiceField(label="Activities in the course", widget=forms.SelectMultiple(attrs={'size':'8'}), required=False)
    submissions = forms.MultipleChoiceField(label="Submissions by this student (or groups they are in)", widget=forms.SelectMultiple(attrs={'size':'8'}), required=False)
    students = forms.MultipleChoiceField(label="Students from the course (other than students in the case group)", widget=forms.SelectMultiple(attrs={'size':'8'}), required=False)
    
    def set_choices(self, course, case):
        """
        Set choices fields as appropriate to this case.
        """
        # set activity choices
        activity_choices = [(act.id, act.name) for act in Activity.objects.filter(offering=course, deleted=False)]
        self.fields['activities'].choices = activity_choices

        # set submission choices
        gms = GroupMember.objects.filter(student=case.student)
        sub_sets = [StudentSubmission.objects.filter(activity__offering=course, member=case.student)]
        for gm in gms:
            sub_sets.append( GroupSubmission.objects.filter(activity=gm.activity, group=gm.group) )
        subs = itertools.chain(*sub_sets)
        submissions_choices = [(sub.id, "%s @ %s" % (sub.activity.name, sub.created_at.strftime("%Y-%m-%d %H:%M"))) for sub in subs]
        self.fields['submissions'].choices = submissions_choices
        
        # set student choices
        students_choices = [(m.id, m.person.sortname()) for m in Member.objects.filter(offering=course, role="STUD")]
        self.fields['students'].choices = students_choices


STEP_FORM = { # map of field -> form for editing it (all ModelForm for DisciplineCase, except Related)
        'notes': CaseNotesForm,
        'related': CaseRelatedForm,
        'contacted': CaseContactedForm,
        'response': CaseResponseForm,
        'meeting': CaseMeetingForm,
        'facts': CaseFactsForm,
        'instr_penalty': CaseInstrPenaltyForm,
        'letter_review': CaseLetterReviewForm,
        }

