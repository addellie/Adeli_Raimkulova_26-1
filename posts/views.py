from django.shortcuts import HttpResponse, render, redirect
from datetime import date
from posts.models import Product, Comment
from posts.forms import PostCreateForm, CommentCreateForm


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
        products = Product.objects.all()

        context = {
            'products': products
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
