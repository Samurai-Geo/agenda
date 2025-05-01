from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from . import models


class ContactForm(forms.ModelForm):
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*'
            }
        ),
        required=False
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({
            'class':'class-a class-b',
            'placeholder': 'Escreva aqui seu primeiro nome e nome complementar caso o tenha.',
        },
        help_text='Texto de ajuda',
        )

    class Meta:
        model = models.Contact
        fields = (
        'first_name', 'last_name',
        'phone', 'email',
        'description', 'category',
        'picture',
         )
        # widgets = {
        #     # 'first_name': forms.PasswordInput()
        #     'first_name': forms.TextInput(
        #         attrs={
        #             'class': 'class-a class-b',
        #             'placeholder': 'Escreva seu primeiro nome e nome complementar caso o tenha'
        #         }
        #     )
        # }

    def clean(self):
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        var_nome = str(first_name).upper().strip()
        var_sobrenome = str(last_name).upper().strip()
        if var_nome == var_sobrenome:
            self.add_error(
                'last_name',
                ValidationError(
                    'Sobrenome não pode ser igual ao nome',
                    code='invalid'
                )
            )

        return super().clean()
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        var = first_name
        var = str(var).upper()
        if var == 'ABC':
            raise ValidationError(
                'Não digite ABC neste campo!',
                code='invalid'
            )

        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        var = last_name
        var = str(var).upper()
        if var == 'ABC':
            raise ValidationError(
                'Seu sobrenome não é esse!!!',
                code='invalid'
            )

        return last_name
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
    
        try:
            phone = str(phone)
            if str.isdigit(phone):
                phone = int(phone)
                
        except:
            raise ValidationError(
                'Seu telefone não exite!!!',
                code='invalid'
            )

        return phone
    
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=3,
        # error_messages={
        #     'required': 'Nova mensagem de erro'
        # }
    )
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username', 'password1', 'password2'
        )
   
class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.',
        error_messages={
            'min_length': 'Please, add more than 2 letters.'
        }
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.'
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label="Password 2",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Use the same password as before.',
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username',
        )

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        password = cleaned_data.get('password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('Senhas não coincidem')
                )

        return super().clean()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError('Já existe este e-mail', code='invalid')
                )

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)
                )

        return password1