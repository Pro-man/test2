from django.shortcuts import render, redirect
from models import Book, Author, Review
from ..login_registration.models import User
from django.contrib import messages

# Create your views here.
def index(request):
    context = {
        'name': User.objects.get(id=request.session['id']).first_name,
        'reviews': Review.objects.all().order_by('created_at').reverse(),
        'books': Book.objects.all()
    }
    return render(request, 'book_reviews/index.html', context)

def logout(request):
    request.session.pop('id')
    return redirect('login_registration:index')

def add_form(request):
    return render(request, 'book_reviews/add.html', {'authors': Author.objects.all()})

def create_review(request):
    errors = []
    if len(request.POST['title']) < 1:
        errors.append("Title cannot be blank.")
    if request.POST['author_list'] == '':
        if request.POST['add_author'] == '':
            errors.append("Author cannot be blank.")
        else:
            author_name = request.POST['add_author']
    else:
        author_name = request.POST['author_list']
    if len(request.POST['review']) < 1:
        errors.append("Review cannot be blank.")
    for err in errors:
        messages.add_message(request, messages.ERROR, err)
    if errors:
        return redirect('books:add_form')
    if not Author.objects.filter(name=author_name):
        Author.objects.create(name=author_name)
    try:
        request.session['book_id'] = Book.objects.get(title=request.POST['title'], author=Author.objects.get(name=author_name)).id
    except:
        request.session['book_id'] = Book.objects.create(title=request.POST['title'], author=Author.objects.get(name=author_name)).id # create Book, if none
    Review.objects.create(rating=request.POST['rating'], review_text=request.POST['review'], book=Book.objects.get(id=request.session['book_id']), reviewer=User.objects.get(id=request.session['id'])) # create Review, if none
    print request.session['book_id'], "<<<-------- request.session['book_id']"
    return redirect('books:book_details', book_id=request.session['book_id'])

def add_review(request, book_id):
    Review.objects.create(rating=request.POST['rating'], review_text=request.POST['review'], book=Book.objects.get(id=book_id), reviewer=User.objects.get(id=request.session['id']))
    request.session['book_id'] = book_id
    return redirect('books:book_details', book_id=request.session['book_id'])

def book_details(request, book_id):
    context = {
        'book': Book.objects.get(id=book_id),
        'reviews': Review.objects.filter(book=book_id)
    }
    return render(request, 'book_reviews/book_details.html', context)

def user_details(request, user_id):
    context = {
        'user': User.objects.filter(id=user_id)[0],
        'reviewed_books': Book.objects.filter(reviews__reviewer=user_id),
        'num_reviews': Review.objects.filter(reviewer=user_id).count()
    }
    return render(request, 'book_reviews/user_details.html', context)

def delete_review(request, book_id, review_id):
    if request.method == 'POST':
        Review.objects.filter(id=review_id).delete()
    return redirect('books:book_details', book_id=book_id)
