from django import forms
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class NewsSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label='Заголовок',
        widget=forms.TextInput(attrs={'placeholder': 'Введите часть заголовка'})
    )
    author = forms.CharField(
        max_length=100,
        required=False,
        label='Автор',
        widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'})
    )
    created_after = forms.DateField(
        required=False,
        label='Дата публикации',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

class PostForm(forms.ModelForm):
    class Meta:
        model = Post  # ← ЭТА СТРОКА ОБЯЗАТЕЛЬНА!
        fields = ['title', 'content', 'categories']
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
        }



class CommonSignupForm(SignupForm):
    def save(self,request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user