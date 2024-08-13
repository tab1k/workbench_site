from django import forms


class QuoteForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'}))
    service = forms.ChoiceField(choices=[
        (1, 'Разработка мобильного приложения'),
        (2, 'Разработка сайта'),
        (3, 'Web Design'),
        (4, 'Разработка продукта.'),
    ], widget=forms.Select(attrs={'class': 'has-nice-select'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Сообщение'}))
