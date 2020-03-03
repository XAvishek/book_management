from django import forms
from books.models import Book, Language
from django.forms.widgets import TextInput, FileInput


class CreateBookForm(forms.ModelForm):
    """
    Form for Creating a Book.
    The languages field here is kept in substitution
    for the language field in the model so the user 
    can type the language instead of selecting from a
    drop down
    """
    languages = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = Book
        fields = 'title','description', 'languages', 'genre','image','document',

class UpdateBookForm(forms.ModelForm):
    """
    Form for Updating an existing Book
    """
    class Meta:
        model = Book
        fields = 'title', 'description', 'language', 'genre', 'image', 'document',
