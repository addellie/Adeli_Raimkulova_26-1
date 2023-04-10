from django.shortcuts import HttpResponse, render, redirect
from posts.models import Product, Comment
from posts.forms import PostCreateForm, CommentCreateForm
from posts.constants import PAGINATION_LIMIT
from django.views.generic import ListView, CreateView, DetailView

# Create your views here.


class MainPageCBV(ListView):
    model = Product
    template_name = 'layouts/index.html'


class ProductsCBV(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'

    def get(self, request, **kwargs):
        products = self.get_queryset().order_by('rate', 'price')
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

        return render(request, self.template_name, context=context)


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


class ProductCreateCBV(ListView, CreateView):
    model = Product
    template_name = 'products/create.html'
    form_class = PostCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'form': kwargs['form'] if kwargs.get('form') else self.form_class
        }

    def get(self, request, **kwargs):
        return render(request, self.template_name, context=self.get_context_data())

    def product(self, request, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            self.model.objects.create(
                description=form.cleaned_data.get('description'),
                name=form.cleaned_data.get('title'),
                rate=form.cleaned_data.get('rate'),
                image=form.cleaned_data.get('image'),
                price=form.cleaned_data.get('price')
            )
            return redirect('/products/')

        return render(request, self.template_name, context=self.get_context_data(form=form))
