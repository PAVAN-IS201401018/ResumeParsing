from django import forms

class DocumentForm(forms.Form):
    title = forms.CharField(max_length=50)
    doc = forms.FileField()

class PostingForm(forms.Form):
	title = forms.CharField(widget=forms.TextInput)
        text = forms.CharField(widget=forms.Textarea)
