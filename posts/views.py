from django.shortcuts import HttpResponse, render, redirect
from datetime import date
from posts.models import Product, Comment
from posts.forms import PostCreateForm, CommentCreateForm
from posts.constants import PAGINATION_LIMIT

# Create your views here.


def hello_view(request):
    if request.method == 'GET':
        return HttpResponse("Hello! Its my project")


def now_date_view(request):
    if request.method == 'GET':
        return HttpResponse(date.today())


def goodbye_view(request):
    if request.method == 'GET':
        return HttpResponse('Goodbye user!')


def main_view(request):
    if request.method == 'GET':
        return render(request, 'layouts/index.html')


def products_view(request):
    if request.method == 'GET':
        products = Product.objects.all().order_by('rate', 'price')
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        """starts_with, ends_with, icontains"""

        """and | or == |"""

        if search:
            products = products.filter(name__icontains=search) | products.filter(description__icontains=search)

        max_page = products.__len__() / PAGINATION_LIMIT
        max_page = round(max_page) + 1 if round(max_page) < max_page else round(max_page)

        """posts splice"""
        products = products[PAGINATION_LIMIT * (page-1):PAGINATION_LIMIT * page]


        context = {
            'products': products,
            'users': request.user,
            'page': range(1, max_page+1)
        }

        return render(request, 'products/products.html', context=context)


def product_detail_view(request, id):
    if request.method == 'GET':
        product = Product.objects.get(id=id)

        context = {
            'product': product,
            'comments': product.comment_set.all(),
            'form': CommentCreateForm
        }

        return render(request, 'products/detail.html', context=context)

    if request.method == 'POST':
        product = Product.objects.get(id=id)
        form = CommentCreateForm(data=request.POST)

        if form.is_valid():
            Comment.objects.create(
                text=form.cleaned_data.get('text'),
                product_id=id
            )

        context = {
            'product': product,
            'comments': product.comment_set.all(),
            'form': form
        }

        return render(request, 'products/detail.html', context=context)


def product_create_view(request):
    if request.method == 'GET':
        context = {
            'form': PostCreateForm
        }
        return render(request, 'products/create.html', context=context)

    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)

        if form.is_valid():
            Product.objects.create(
                description=form.cleaned_data.get('description'),
                name=form.cleaned_data.get('title'),
                rate=form.cleaned_data.get('rate'),
                image=form.cleaned_data.get('image'),
                price=form.cleaned_data.get('price')
            )
            return redirect('/products/')

        return render(request, 'products/create.html', context={
            'form': form
        })
