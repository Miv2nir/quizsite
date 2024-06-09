from django import forms

class RegisterForm(forms.Form): #reused from the last year's project
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Email','class': 'login-input-box'}))
    login = forms.CharField(label='Login', widget=forms.TextInput(attrs={'placeholder': 'Login','class': 'login-input-box'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'login-input-box'}))
    password_verify = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password','class': 'login-input-box'})) #, 'class': 'square_login' - cut out as no css work is done at this point

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

class AuthForm(forms.Form):
    # login = forms.CharField(label='Login', max_length=100)
    login = forms.CharField(label='Login', widget=forms.TextInput(attrs={'placeholder': 'Login', 'class': 'login-input-box'}))

    # password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'login-input-box'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

class SearchForm(forms.Form):
    search = forms.CharField(label='Search',required=False, widget=forms.TextInput(attrs={'placeholder': 'Type the course name here', 'class': 'search-box'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

class CourseForm(forms.Form):
    ACCESS_LEVEL = (
        ('A','Public'),
        ('B','Unlisted'),
        ('C','Private'),
    )
    name=forms.CharField(label='Name',widget=forms.TextInput(attrs={'placeholder':'Course Name','class':'form-field'}))
    description=forms.CharField(label='Description',required=False,widget=forms.Textarea(attrs={'placeholder':'Description','class':'form-field description'}))
    access=forms.ChoiceField(choices=ACCESS_LEVEL,widget=forms.Select(attrs={'class':'form-field'}))
    quiz=forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'checkbox-editor'}))
    #image=forms.ImageField(required=False)
class CoursePageForm(forms.Form):
    A_TYPE = (
        ('N',None),
        ('T','Text'),
        ('S','Singular Choice'),
        ('M','Multiple Choice'),
        ('F','File Upload'),
    )
    answer_type=forms.ChoiceField(choices=A_TYPE,widget=forms.Select(attrs={'class':'form-field','id':'answer_type','onChange':'displayWarning();'}))
    title=forms.CharField(label='Page Title',widget=forms.TextInput(attrs={'placeholder':'Course Name','class':'form-field stretch'}))
    text=forms.CharField(label='Text',required=False,widget=forms.Textarea(attrs={'placeholder':'Page Text here','class':'form-field description big','id':'textfield'}))
    question=forms.CharField(label='Text',required=False,widget=forms.Textarea(attrs={'placeholder':'Question here','class':'form-field description'}))
    choices=forms.CharField(label='Answer Choices',required=False,widget=forms.Textarea(attrs={'id':'json_input','style':'display:none;'}))
    correct_choices=forms.CharField(label='Correct Choices',required=False,widget=forms.Textarea(attrs={'id':'json_check','style':'display:none;'}))
    timer=forms.IntegerField(label='Timer',required=False,widget=forms.NumberInput(attrs={'class':'form-field'}))
    grade=forms.IntegerField(label='Correct Answer Grade',required=False,widget=forms.NumberInput(attrs={'class':'form-field'}))
    penalty=forms.IntegerField(label='Penalty',required=False,widget=forms.NumberInput(attrs={'class':'form-field'}))
'''
class AnswerTypeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
'''

class UserResponseText(forms.Form):
    user_response=forms.CharField(label='Type your answer below:',widget=forms.Textarea(attrs={'placeholder':'Type your answer here','class':'form-field description big'}))

class UserResponseSingular(forms.Form):
    #pass choices as an argument to response from the respective view
    user_response=forms.ChoiceField(label='Select your answer from the following options:',widget=forms.RadioSelect())

class UserResponseMultiple(forms.Form):
    user_response=forms.MultipleChoiceField(label='Select all correct answers below:',widget=forms.CheckboxSelectMultiple(),required=False)

class UserGroupsForm(forms.Form):
    name=forms.CharField(label='Name',widget=forms.TextInput(attrs={'placeholder':'Course Name','class':'form-field'}))

class UserGet(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Student Username','class':'form-field'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
class CourseGet(forms.Form):
    course=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Course Name','class':'form-field'}))
    #deadline=forms.DateTimeField(widget=forms.DateTimeInput(),required=False)
    
class UserDetailsForm(forms.Form):
    username=forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder':'Username','class':'form-field'}))
    pfp=forms.ImageField(required=False,widget=forms.FileInput(attrs={'style':'margin-top: 0.5rem; margin-bottom: 0.5rem;'}))