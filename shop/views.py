from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cms.models import Menu, TopBanner, BottomBanner
from shop.forms import ReviewForm, CartForm
from shop.serializers import CategorySerializer
from .models import Category, Product, Cart
from django.db.models import Q


# Create your views here.

class BaseView(View):
    template_context = {
        'menus': Menu.objects.order_by('-weight'),
        'categories': Category.objects.all(),
    }


class Homepage(BaseView):
    def get(self, request):
        self.template_context['top_banners'] = TopBanner.objects.all()
        self.template_context['big_bottom_banner'] = BottomBanner.objects.filter(is_big=True).first()
        self.template_context['small_bottom_banners'] = BottomBanner.objects.filter(is_big=False)[:2]
        self.template_context['deal_products'] = Product.objects.filter(deal_of_the_day=True)
        self.template_context['latest_products'] = Product.objects.order_by('-pub_date')[:8]
        self.template_context['picked_products'] = Product.objects.order_by('?')[:4]

        return render(request, 'index.html', self.template_context)


class ProductView(BaseView):
    def get(self, request, product_id, review_form=None):
        self.template_context['review_form'] = review_form or ReviewForm()
        self.template_context['product'] = Product.objects.get(pk=product_id)
        return render(request, 'product.html', self.template_context)

    def post(self, request, product_id):
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = Product.objects.get(pk=product_id)
            review.save()
            return redirect(reverse('product_page', args=[product_id]))
        return self.get(request, product_id, form)


class CartView(BaseView):
    def post(self, request, product_id):
        form = CartForm(request.POST)
        existing_cart = Cart.objects.filter(Q(product_id=product_id) & Q(user=request.user)).first()
        cart = form.save(commit=False)
        if existing_cart:
            existing_cart.qty += cart.qty
            existing_cart.save()
        else:
            cart.user = request.user
            cart.product = Product.objects.get(pk=product_id)
            cart.save()
        return redirect(reverse('product_page', args=[product_id]))


class CategoryView(BaseView):
    def get(self, request, category_id):
        self.template_context['products'] = Product.objects.filter(category=category_id)
        self.template_context['category_name'] = Category.objects.get(pk=category_id)
        return render(request, 'category.html', self.template_context)


class CategoryAPI(APIView):
    """
    List all category.
    """

    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
