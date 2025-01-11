from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from .models import Author, Quote

def quote_list(request):
    quotes = Quote.objects.all()
    return render(request, 'main/quote_list.html', {'quotes': quotes})

def author_detail(request, pk):
    author = Author.objects.get(pk=pk)
    return render(request, 'main/author_detail.html', {'author': author})

def add_author(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Author.objects.create(name=name)
        return redirect('quote_list')
    return render(request, 'main/add_author.html')

def add_quote(request):
    if request.method == "POST":
        text = request.POST.get('text')
        author_id = request.POST.get('author')

        # Перевірка: чи обраний автор
        if not author_id:
            authors = Author.objects.all()
            return render(request, 'main/add_quote.html', {
                'authors': authors,
                'error': 'Please select an author.'
            })

        # Отримуємо автора або повертаємо 404
        author = get_object_or_404(Author, pk=author_id)

        # Створюємо цитату
        Quote.objects.create(
            text=text,
            author=author,
            created_by=request.user,
        )
        return redirect('quote_list')

    authors = Author.objects.all()
    return render(request, 'main/add_quote.html', {'authors': authors})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quote_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def author_detail(request, pk):
    # Находим автора или возвращаем 404, если он не существует
    author = get_object_or_404(Author, pk=pk)
    # Находим все цитаты данного автора
    quotes = Quote.objects.filter(author=author)
    return render(request, 'main/author_detail.html', {
        'author': author,
        'quotes': quotes
    })
