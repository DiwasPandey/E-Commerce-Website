from django.forms import ModelForm

from shop.models import ProductHasReview, Cart


class ReviewForm(ModelForm):
    class Meta:
        model = ProductHasReview
        fields = ('rating', 'comment')

class CartForm(ModelForm):
    class Meta:
        model = Cart
        fields = ('qty',)
