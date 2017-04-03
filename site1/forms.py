from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    email = forms.EmailField(required=False, label='Your email address')
    message = forms.CharField(widget=forms.Textarea)

    # Any method starts with 'clean', ends with a field
    def clean_message(self):
        msg = self.cleaned_data['message']
        num_words = len(msg.split())
        if num_words < 4:
            raise forms.ValidationError("Less than 4 words")
        return msg
