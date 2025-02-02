"""
Различные модули представления.

Разные View интернет магазина: по товарам, заказам и тд.
"""
import logging
from csv import DictWriter
from dataclasses import field
from timeit import default_timer
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import Group, User
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.core.cache import cache

from shopapp.models import Product, Order, ProductImage
from shopapp.forms import ProductForm, CreateOrder, GroupForm
from django.views import View
from rest_framework.viewsets import ModelViewSet
from .serializers import ProductSerializer, OrderSerializer
from .common import save_csv_products
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse

from os import listdir
from os.path import isfile, join
import os


log = logging.getLogger(__name__)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['user', 'products']
    filterset_fields = ['user', 'products', 'promocode', 'delivery_address', 'created_at',]
    ordering_fields = [
        'user',
        'products',
        'created_at',
        ]


@extend_schema(description="Product view CRUD")
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product
    Полный CRUD для сущнотей товара
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,#не регистрозависимый
        DjangoFilterBackend,#полное совпадение ищет
        OrderingFilter, #sort
    ]
    search_fields = ['name', 'description']
    filterset_fields = [
        'name',
        'description',
        'price',
        'discount',
        'archived',
    ]
    ordering_fields = [
        'name',
        'price',
        'discount',
    ]

    @method_decorator(cache_page(60*2))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @action(methods=["get"], detail=False)
    def download_csv(self, request: Request):
        response = HttpResponse(content_type='text/csv')
        filename = 'products-export.csv'
        response["Content-Disposition"] = f'attachment; filename={filename}'
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            'name',
            'description',
            'price',
            'discount',
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })

        return response


    @action(
        detail=False,
        methods=["post"],
        parser_classes=[MultiPartParser],
    )
    def upload_csv(self, request: Request):
        products = save_csv_products(
            request.FILES["file"].file,
            encoding=request.encoding,
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Get one product by id",
        description="Retrieves **product**, return 404 if not found",
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description="Empty response, product by id not found"),
        }
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class ShopIndexView(View):
    # @method_decorator(cache_page(60 * 2))
    def get(self, request: HttpRequest) -> HttpResponse:
        products =[
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
            "items": 5
        }
        log.debug('Products for shop index: %s', products)
        log.info('Rendering shop index')
        print("shop index context", context)
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupListView(View):
    def get(self, request: HttpRequest)-> HttpResponse:
        context = {
            "form": GroupForm(),
            "groups": Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest)-> HttpResponse:
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)


class ProductDetailView(DetailView):
    template_name = 'shopapp/products-details.html'
    queryset = Product.objects.prefetch_related('images')
    context_object_name = 'product'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        # Define the directory path
        base_path = os.path.join('uploads', 'products', f'product_{product.id}', 'preview')

        try:
            # Считаем количество изображений в директории
            images_count = len([f for f in listdir(base_path) if isfile(join(base_path, f))])
        except FileNotFoundError:
            images_count = 0

        context['images_count'] = images_count
        return context


class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    fields = 'name', 'price', 'description', 'discount', 'preview'
    permission_required = "shopapp.add_product"
    success_url = reverse_lazy('shopapp:products_list')


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    # fields = 'name', 'price', 'description', 'discount', 'preview'
    template_name_suffix = '_update_form'
    permission_required = 'shopapp.change_product'
    form_class = ProductForm

    def get_success_url(self):
        return reverse(
            'shopapp:product_details',
            kwargs={'pk': self.object.pk},
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_superuser or obj.author == self.request.user


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class ProductsListView(ListView):
    template_name = 'shopapp/products-list.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(archived=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(archived=False)
        return context


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (Order.objects.
                select_related("user").
                prefetch_related("products")
                )


class OrdersDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"
    queryset = (Order.objects.
                select_related("user").
                prefetch_related("products")
                )


class OrderCreateView(CreateView):
    model = Order
    fields = 'user', 'products'
    success_url = reverse_lazy('shopapp:orders_list')


class OrderUpdateView(UpdateView):
    model = Order
    fields = 'user', 'products'
    template_name_suffix = '_update_form1'

    def get_success_url(self):
        return reverse(
            'shopapp:order_details',
            kwargs={'pk': self.object.pk},
        )


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:orders_list')


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        cache_key = "products_data_export"
        products_data = cache.get(cache_key)
        if products_data is None:
            products = Product.objects.order_by("pk").all()
            products_data = [
                {
                    'pk': product.pk,
                    'name': product.name,
                    'price': product.price,
                    'archived': product.archived,
                }
                for product in products
            ]
            elem = products_data[0]
            name = elem["name"]
            print("name:", name)
        cache.set("products_data_export", products_data, 300)
        return JsonResponse({'products': products_data})


class LatestProductsFeed(Feed):
    title = "Shop products (latest)"
    description = "Updates on products card"
    link = reverse_lazy("shopapp:product")

    def items(self):
        return (
            Product.objects
            .filter(created_at__isnull=False)
            .order_by('-created_at')[:5]
        )

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description[:200]


class UserOrdersListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'shopapp/user_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        self.owner = get_object_or_404(User, pk=self.kwargs['user_id'])
        return Order.objects.filter(user=self.owner).order_by('pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = self.owner
        return context


def export_user_orders(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    cache_key = f'user_orders_{user_id}'
    data = cache.get(cache_key)
    if data is None:
        orders = Order.objects.filter(user=user).order_by('pk')
        serializer = OrderSerializer(orders, many=True)
        data = serializer.data
        cache.set(cache_key, data, 300)  # Кэшировать на 5 минут
    return JsonResponse(data, safe=False)
