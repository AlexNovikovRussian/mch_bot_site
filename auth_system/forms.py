from django.forms import ModelForm

from auth_system.models import MosUser

class MosRuForm (ModelForm):
    class Meta:
        model = MosUser
        fields = ('mosLogin', 'mosPassword')