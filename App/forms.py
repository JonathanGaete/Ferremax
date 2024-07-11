from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth import get_user_model
from App.models import *
from Productos.models import *
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit



class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None  # Eliminar el texto de ayuda por defecto

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'autofocus': True, 'autocomplete': 'current-password', 'class': 'form-control'}))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))

class CustomerProfileForm(forms.ModelForm):
    direccion = forms.CharField(max_length=100)
    telefono = forms.CharField(max_length=20)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'telefono', 'direccion']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'readonly': True}),  # Email readonly
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomerProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = False  # Hacer que el campo de email no sea obligatorio
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Confirmar'))


class ChangeUserTypeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

class DestacadosForm(forms.ModelForm):
    class Meta:
        model = Destacados
        fields = '__all__'


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añade widgets personalizados si es necesario
        self.fields['nombre'].widget = forms.TextInput(attrs={'class': 'form-control'})  # Ejemplo de widget personalizado


class DestacadosForm(forms.ModelForm):
    class Meta:
        model = Destacados
        fields = ['nombre', 'producto']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar un queryset dinámico para el campo 'producto'
        self.fields['producto'].queryset = Producto.objects.all()  # Opcional: Filtra los productos según tu lógica necesaria