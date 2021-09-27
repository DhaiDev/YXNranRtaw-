from django import forms
from django_quill.forms import QuillFormField

from apps.forum.models import Comment


# QuillWrapper
# Wrapper
class Form(forms.Form):
    content = QuillFormField()

    # def save(self):
    #     return Comment.objects.create(content=self.cleaned_data["content"])
