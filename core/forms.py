from django import forms
from .models import Usuario


class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"})
    )

    class Meta:
        model   = Usuario
        exclude = ("rol_id",)        # NO pedimos rol_id
