from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import BookForm
from .models import Book


def index(request):
    return render(request, 'popupapp/home.html')


def book_list(request):
    books = Book.objects.all()
    return render(request, 'popupapp/book_list.html', {'books': books})


def save_book_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            book = form.save()
            data['form_is_valid'] = True
            data['book_id'] = book.id
            books = Book.objects.all()
            data['html_book_list'] = render_to_string('popupapp/partial_book_list.html', {
                'books': books
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
    else:
        form = BookForm()
    return save_book_form(request, form, 'popupapp/partial_book_create.html')


def book_update(request, pk):
    book_details = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book_details)
    else:
        form = BookForm(instance=book_details)
    return save_book_form(request, form, 'popupapp/partial_book_update.html')


def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    data = dict()
    if request.method == 'POST':
        book.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        books = Book.objects.all()
        data['html_book_list'] = render_to_string('popupapp/partial_book_list.html', {
            'books': books
        })
    else:
        context = {'book': book}
        data['html_form'] = render_to_string('popupapp/partial_book_delete.html', context, request=request, )
    return JsonResponse(data)
