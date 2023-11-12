from django import forms


class searchForm(forms.Form):
    city = forms.CharField(max_length=50, required=False)
