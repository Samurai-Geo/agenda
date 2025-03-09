from django import forms
from django.core.exceptions import ValidationError
from . import models


class ContactForm(forms.ModelForm):
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
        'first_name',
        'last_name',
        'phone',
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
        # cleaned_data = self.cleaned_data

        self.add_error(
            'first_name',
            ValidationError(
                'Mensagem de erro 1',
                code='invalid'
            )
        )

        self.add_error(
            None,
            ValidationError(
                'Mensagem de erro 2',
                code='invalid'
            )
        )

        return super().clean()