from django import forms
from LinkedApp.models import User, Status
from django.utils.safestring import mark_safe
from LinkedApp.models import jobSeeker, student, employed
from django.core.validators import EmailValidator


class UserCreationForm(forms.ModelForm):
    error_messages = {
        'duplicate_email': 'The email address, you have entered , is already registered. Already on LinkedIn? <a href="/sign-in/">Sign In</a>',
    }
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password")

    def clean_email(self):
        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(mark_safe(self.error_messages['duplicate_email']))

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserCreationForm2(forms.Form):
    country = forms.ChoiceField(choices=User.county_choices, widget=forms.Select())
    postal_code = forms.IntegerField(required=False)
    user_type = forms.ChoiceField(choices=User.user_type_choices, widget=forms.RadioSelect(), initial=User.user_type_choices[0][0])
    job_title = forms.CharField(max_length=1000, required=False)
    most_recent_job_title = forms.CharField(max_length=1000, required=False)
    self_employed = forms.BooleanField(label="self_employed", widget=forms.CheckboxInput, required=False)
    self_employed_2 = forms.BooleanField(label="self_employed_2", widget=forms.CheckboxInput, required=False)
    company = forms.CharField(max_length=2000, required=False)
    Industry = forms.ChoiceField(choices=jobSeeker.Industry_choices, widget=forms.Select(), required=False)
    Company = forms.CharField(max_length=1000, required=False)
    Industry2 = forms.ChoiceField(choices=jobSeeker.Industry_choices, widget=forms.Select(), required=False)
    time_period_from_industry = forms.ChoiceField(choices=jobSeeker.time_period_choices1, widget=forms.Select(), required=False)
    time_period_to_industry = forms.ChoiceField(choices=jobSeeker.time_period_choices2, widget=forms.Select(), required=False)
    institution = forms.CharField(max_length=2000, required=False)
    time_period_to_student = forms.ChoiceField(choices=jobSeeker.time_period_choices3, widget=forms.Select(), required=False)
    time_period_from_student = forms.ChoiceField(choices=jobSeeker.time_period_choices1, widget=forms.Select(), required=False)

    def clean_time_period_to_industry(self):
        user_type = self.cleaned_data['user_type']
        if user_type == "Job Seeker":
            time_period_to_industry = self.cleaned_data['time_period_to_industry']
            if time_period_to_industry == "":
                raise forms.ValidationError("This is required field")
            else:
                return time_period_to_industry

    def clean_time_period_from_industry(self):
        user_type = self.cleaned_data['user_type']
        if user_type == "Job Seeker":
            time_period_from_industry = self.cleaned_data['time_period_from_industry']
            if time_period_from_industry == "":
                raise forms.ValidationError("This is required field")
            else:
                return time_period_from_industry

    def clean_time_period_from_student(self):
        user_type = self.cleaned_data['user_type']
        if user_type == "Student":
            time_period_from_student = self.cleaned_data['time_period_from_student']
            if time_period_from_student == "":
                raise forms.ValidationError("This is required field")
            else:
                return time_period_from_student

    def clean_institution(self):
        user_type = self.cleaned_data['user_type']
        if user_type == "Student":
            institution = self.cleaned_data['institution']
            if institution == "":
                raise forms.ValidationError("This is required field")
            else:
                return institution

    def clean_time_period_to_student(self):
        user_type = self.cleaned_data['user_type']
        if user_type == "Student":
            time_period_to_student = self.cleaned_data['time_period_to_student']
            if time_period_to_student == "":
                raise forms.ValidationError("This is required field")
            else:
                return time_period_to_student

    def clean_job_title(self):
        user_type = self.cleaned_data['user_type']
        if user_type == "Employed":
            job_title = self.cleaned_data['job_title']
            if job_title == "":
                raise forms.ValidationError("This is required field")
            else:
                return job_title

    def clean_Industry(self):
        user_type = self.cleaned_data['user_type']
        if user_type == "Employed":
            self_employed = self.cleaned_data['self_employed']
            industry = self.cleaned_data['Industry']
            if self_employed is True and industry == "":
                raise forms.ValidationError("This is required field")
            else:
                return industry

    def clean_Industry2(self):
        user_type = self.cleaned_data['user_type']
        if user_type == "Job Seeker":
            self_employed = self.cleaned_data['self_employed_2']
            industry = self.cleaned_data['Industry2']
            if self_employed is True and industry == "":
                raise forms.ValidationError("This is required field")
            else:
                return industry

    def clean_Company(self):
        user_type = self.cleaned_data['user_type']
        if user_type == "Employed":
            self_employed = self.cleaned_data['self_employed']
            company = self.cleaned_data['Company']
            if self_employed is False and company == "":
                    raise forms.ValidationError("This is required field")
            else:
                    return company

    def clean_company(self):
        user_type = self.cleaned_data['user_type']
        if user_type == "Job Seeker":
            self_employed = self.cleaned_data['self_employed_2']
            company = self.cleaned_data['company']
            if self_employed is False and company == "":
                    raise forms.ValidationError("This is required field")
            else:
                    return company


    def clean_most_recent_job_title(self):
        user_type = self.cleaned_data['user_type']
        if user_type == "Job Seeker":
            most_recent_job_title = self.cleaned_data['most_recent_job_title']
            if most_recent_job_title == "":
                raise forms.ValidationError("This is required field")
            else:
                return most_recent_job_title

    def save(self, User):
        User.country = self.cleaned_data['country']
        User.postal_code = self.cleaned_data['postal_code']
        User.user_type = self.cleaned_data['user_type']
        User.save()

        if User.user_type == "Employed":
            employ = employed()
            employ.user_id = User
            employ.Job_title = self.cleaned_data['job_title']
            employ.self_employed = self.cleaned_data['self_employed']
            if employ.self_employed == 0:
                employ.Company = self.cleaned_data['Company']
            else:
                employ.Industry = self.cleaned_data['Industry']
            employ.save()
        elif User.user_type == "Job Seeker":
            jobseeker_instance = jobSeeker()
            jobseeker_instance.most_recent_job_title = self.cleaned_data['most_recent_job_title']
            jobseeker_instance.self_employed = self.cleaned_data['self_employed']
            if jobseeker_instance.self_employed == 0:
                jobseeker_instance.MostRecentCompany = self.cleaned_data['company']
            else:
                jobseeker_instance.Industry = self.cleaned_data['Industry2']

            jobseeker_instance.TimePeriod_from = self.cleaned_data['time_period_from_industry']
            jobseeker_instance.TimePeriod_to = self.cleaned_data['time_period_to_industry']
            jobseeker_instance.user_id = User
            jobseeker_instance.save()
        elif User.user_type == "Student":
            student_instance = student()
            student_instance.user_id = User
            student_instance.School_University = self.cleaned_data['institution']
            student_instance.DateAttended_from = self.cleaned_data['time_period_from_student']
            student_instance.DateAttended_to = self.cleaned_data['time_period_to_student']
            student_instance.save()


class LoginForm(forms.Form):
    username = forms.EmailField(max_length=150, validators=[EmailValidator])
    password = forms.CharField(min_length=6, widget=forms.PasswordInput())


class ProfilePic(forms.Form):
    pic = forms.ImageField(required=False)


class AdvanceSearchForm(forms.Form):
    keyword = forms.CharField(max_length=10000)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    title = forms.CharField(max_length=400)
    company = forms.CharField(max_length=500)
    school = forms.CharField(max_length=500)
    country = forms.ChoiceField(choices=User.county_choices, widget=forms.Select())















