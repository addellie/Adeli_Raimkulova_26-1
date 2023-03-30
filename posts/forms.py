from django import forms


class PostCreateForm(forms.Form):
    image = forms.ImageField(required=False)
    title = forms.CharField(max_length=255, min_length=6)
    description = forms.CharField(widget=forms.Textarea())
    rate = forms.FloatField(required=False)
    price = forms.DecimalField(max_digits=10, decimal_places=2)


class CommentCreateForm(forms.Form):
    text = forms.CharField(max_length=255, min_length=3)
