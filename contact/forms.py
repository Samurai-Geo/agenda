from django import forms
from django.core.exceptions import ValidationError
from . import models


class ContactForm(forms.ModelForm):
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*'
            }
        )
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
            num = int(phone)
        except:
            raise ValidationError(
                'Seu telefone não exite!!!',
                code='invalid'
            )

        return phone
    