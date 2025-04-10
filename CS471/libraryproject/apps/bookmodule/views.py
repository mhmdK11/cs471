from django.shortcuts import render
from .models import Book , Address, Student
from django.db.models import Q,Sum, Avg, Max, Min, Count
# Create your views here.
from django.http import HttpResponse

def index(request):
 return render(request, "bookmodule/index.html")

def list_books(request):
 return render(request, 'bookmodule/list_books.html')

def viewbook(request, bookId):
 return render(request, 'bookmodule/one_book.html')

def aboutus(request):
 return render(request, 'bookmodule/aboutus.html')

def links(request):
 return render(request, 'bookmodule/links.html')

def formatting(request):
 return render(request, 'bookmodule/formatting.html')

def listing(request):
 return render(request, 'bookmodule/listing.html') 

def tables(request):
    return render(request, 'bookmodule/tables.html')




def __getBooksList():
 book1 = {'id':12344321, 'title':'Continuous Delivery', 'author':'J.Humble and D. Farley'}
 book2 = {'id':56788765,'title':'Reversing: Secrets of Reverse Engineering', 'author':'E. Eilam'}
 book3 = {'id':43211234, 'title':'The Hundred-Page Machine Learning Book', 'author':'Andriy Burkov'}
 return [book1, book2, book3]

def search(request):
    if request.method == "POST":
        string = request.POST.get('keyword').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')
        # now filter
        books = __getBooksList()
        newBooks = []
        for item in books:
            contained = False
            if isTitle and string in item['title'].lower(): contained = True
            if not contained and isAuthor and string in item['author'].lower():contained = True
            if contained: newBooks.append(item)
        return render(request, 'bookmodule/bookList.html', {'books':newBooks})
    return render(request, 'bookmodule/search.html')



def simple_query(request):
    mybooks=Book.objects.filter(title__icontains='II') # <- multiple objects
    return render(request, 'bookmodule/bookList.html', {'books':mybooks})

def complex_query(request):
    mybooks=books=Book.objects.filter(author__isnull =False).filter(title__icontains='II').filter(edition__gte = 1).exclude(price__lte = 40)[:10]
    if len(mybooks)>=1:
        return render(request, 'bookmodule/bookList.html', {'books':mybooks})
    else:
        return render(request, 'bookmodule/index.html')
    

def task1(request):
   mybook = Book.objects.filter(Q(price__lte=80))
   return render(request,'bookmodule/task1.html',{'books':mybook})

def task2(request):
  mybook = Book.objects.filter(Q(edition__gt=3) & (Q(title__contains='co') | Q(author__contains='co')))
  return render(request,'bookmodule/task2.html',{'books':mybook})

def task3(request):
  mybook = Book.objects.filter(~Q(edition__gt=3) & (~Q(title__contains='co') | ~Q(author__contains='co')))
  return render(request,'bookmodule/task3.html',{'books':mybook})

def task4(request):
  mybook = Book.objects.order_by('title')
  return render(request,'bookmodule/task4.html',{'books':mybook})

def task5(request):
  mybook = Book.objects.aggregate(total_books=Count('id'), total_price=Sum('price',default=0), average_price=Avg('price',default=0), maximum_price=Max('price',default=0),minimumm_price=Min('price',default=0))
  return render(request,'bookmodule/aggr.html',{'books':mybook})

def task7(request):
    student_counts = Address.objects.annotate(num_students= Count('student'))
    return render(request, 'bookmodule/task7.html', {'student_counts': student_counts})