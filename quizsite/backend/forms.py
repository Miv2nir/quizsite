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
    #image=forms.ImageField(required=False)
class CoursePageForm(forms.Form):
    A_TYPE = (
        ('N',None),
        ('T','Text'),
        ('S','Singular Choice'),
        ('M','Multiple Choice'),
        ('F','File Upload'),
    )
    answer_type=forms.ChoiceField(choices=A_TYPE,widget=forms.Select(attrs={'class':'form-field','id':'answer_type','onChange':'displayWarning()'}))
    title=forms.CharField(label='Page Title',widget=forms.TextInput(attrs={'placeholder':'Course Name','class':'form-field'}))
    text=forms.CharField(label='Text',required=False,widget=forms.Textarea(attrs={'placeholder':'Page Text here','class':'form-field description big','id':'textfield'}))
    question=forms.CharField(label='Text',required=False,widget=forms.Textarea(attrs={'placeholder':'Question here','class':'form-field description'}))
    choices=forms.CharField(label='Answer Choices',required=False,widget=forms.Textarea(attrs={'id':'json_input','style':'display: none;'}))

'''
class AnswerTypeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
'''