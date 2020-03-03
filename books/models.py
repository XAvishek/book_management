from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse

# Create your models here.

def image_path(instance, filename):
    """
    A method to specify the location of the upload
    book image
    """
    return f'book_image/{instance.author.id}/{filename}'

def document_path(instance, filename):
    """
    A method to specify the location of the upload
    book document(pdf)
    """
    return f'documents/{instance.author.id}/{filename}'

class Language(models.Model):
    """
    A Language model related with the Book Model 
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    An Book model to describe the book in the system with a one to
    many relation to the User model and ManyToMany relation
    with the Language model.
    """
    GENRE = (('0','Poetry'),('1','Fiction'),('2','Nonfiction'),('3','Drama'))
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='books')
    image = models.ImageField(upload_to=image_path, validators=[FileExtensionValidator])
    document = models.FileField(upload_to=document_path, validators=[FileExtensionValidator(['pdf'])])
    language = models.ManyToManyField(Language, related_name='book_l')
    count = models.IntegerField(default=0)
    genre = models.CharField(choices=GENRE, max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("detail_book", kwargs={"pk": self.pk})
