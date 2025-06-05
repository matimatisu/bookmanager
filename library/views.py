from django.shortcuts import render, redirect, get_object_or_404
from .models import Book #モデルをインポート
from .forms import BookForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from django.db.models.functions import TruncMonth
from django.db.models import Count

@never_cache
@login_required
def book_list(request):
    books = Book.objects.filter(user=request.user).order_by("-id")
    query = request.GET.get("q","")
    filter_status = request.GET.get("filter", "all")
    
    books = Book.objects.all()
    
    if query:
        books = books.filter(title__icontains=query)
    if filter_status == "read":
        books = books.filter(is_read=True)
    elif filter_status == "unread":
        books = books.filter(is_read=False)

    return render(request, "library/book_list.html", {
        "books": books,
        "query": query,
        "filter_status": filter_status,
    })

@login_required
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            form.save()
            return redirect("book_list") #登録後に一覧ページへリダイレクト
    else:
        form = BookForm()
    return render(request, 'library/add_book.html', {'form': form})


@login_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    book.delete()
    return redirect("book_list")

@login_required
def edit_book(request, pk):
    book = get_object_or_404(Book, pk = pk, user=request.user)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm(instance=book)
    return render(request,"library/edit_book.html",{"form": form, "book": book})

@login_required
def toggle_read(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.is_read = not book.is_read
    book.save()
    return redirect("book_list")

@login_required
@require_http_methods(["GET","POST"])
def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        book.delete()
        return redirect("book_list")
    return render(request, "library/delete_book_confirm.html", {"book": book})

@login_required
def stats_view(request):
    total_books = Book.objects.count()
    read_books = Book.objects.filter(is_read=True).count()
    unread_books = Book.objects.filter(is_read=False).count()

    #月別読書数（読了日のある本を月ごとにカウント）
    monthly_data = (
        Book.objects.filter(is_read=True, read_date__isnull=False)
        .annotate(month=TruncMonth("read_date"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    #グラフようにデータを整形
    months = [entry["month"].strftime("%Y-%m") for entry in monthly_data]
    counts = [entry["count"] for entry in monthly_data]

    return render(request, "library/stats.html", {
        "total_books": total_books,
        "read_books": read_books,
        "unread_books": unread_books,
        "months": months,
        "counts": counts,
    })
# Create your views here.
