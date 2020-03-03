from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView)

from books.forms import CreateBookForm, UpdateBookForm
from books.models import Book, Language
from books.tasks import book_created_task, book_updated_task

# Create your views here.


class HomeView(TemplateView):
    """
    View for the HomePage of the website
    """
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = Book.objects.all()
        context["latest_books"] = books.order_by("-created_at")[:9]
        return context


class CreateBookView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    View for creating a Book
    """
    login_url = "/login/"
    form_class = CreateBookForm
    template_name = "books/create_book.html"
    success_url = reverse_lazy('home')
    success_message = "%(title)s was created successfully"

    def form_valid(self, form):
        """
        Saving the values in the database if the form
        is valid
        """
        book = form.save(commit=False)
        book.author = self.request.user
        languages = form.cleaned_data['languages']
        book.save()
        language_list = [Language.objects.get_or_create(
            name=lang)[0] for lang in languages.lower().split()]
        print(language_list)
        for lang in language_list:
            a = book.language.add(lang)
        book.language.set = a
        book.save()
        book_created_task.delay(book.pk)
        return super(CreateBookView, self).form_valid(form)

    def form_invalid(self, form):
        """
        Reload the form with the invalid fields empited
        and the valid fields with their previous value
        """
        return super(CreateBookView, self).form_invalid(form)


class DetailBook(DetailView):
    """
    View to view a single book
    """
    model = Book
    template_name = 'books/detail_book.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        book = Book.objects.all()
        context = super().get_context_data(**kwargs)
        self.object.count = self.object.count + 1
        self.object.save()
        return context


# class BookUpdateView(SuccessMessageMixin, UpdateView):
#     """
#     View for updating an existing Book
#     """
#     model = Book
#     template_name = "books/update_book.html"
#     fields = ("title", "description", "image", "document", "language")
#     success_url = reverse_lazy("home")
#     success_message = "%(title)s was updated successfully"

@login_required
def post_update(request, pk):
    update = get_object_or_404(Book, pk=pk)
    form = UpdateBookForm(request.POST or None,
                        request.FILES or None, instance=update)
    if request.method == 'POST':
        book = form.save(commit=False)
        book.save()
        messages.success(request, "The Book was updated successfully")
        book_updated_task.delay(book.pk)
    context = {
        'form': form,
    }

    return render(request, 'books/update_book.html', context)

class BookDeleteView(SuccessMessageMixin, DeleteView):
    """
    View for deleting an existing Book
    """
    model = Book
    success_url = reverse_lazy("home")
    success_message = "%(title)s was deleted successfully"

    def delete(self, request, *args, **kwargs):
        """
        We overwrite this method so that we can see the success
        message after the object is deleted
        """
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(BookDeleteView, self).delete(request, *args, **kwargs)


class BookGenreView(ListView):
    """
    View for displaying a list of a specific genre.
    """
    model = Book
    ordering = ['pk']
    context_object_name = 'genre_list'
    template_name = 'books/genre_book.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genre"] = self.kwargs.get('genre')
        return context

    def get_queryset(self):
        genre = self.kwargs.get('genre')
        genre_key = [item[0] for item in Book.GENRE if item[1] == genre][0]        
        return Book.objects.filter(genre__iexact=genre_key)
