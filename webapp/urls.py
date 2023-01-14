from django.urls import path
from webapp.views import ProductsView, ProductView, CreateProduct, UpdateProduct, DeleteProduct, CreateReview, \
    UpdateReviewModerator, DeleteReview, UpdateReview, UnmoderatedReviews

app_name = 'webapp'

urlpatterns = [
    path('', ProductsView.as_view(), name='index'),
    path('product_view/<int:pk>/', ProductView.as_view(), name='product_view'),
    path('create_product/', CreateProduct.as_view(), name='create_product'),
    path('update_product/<int:pk>/', UpdateProduct.as_view(), name='update_product'),
    path('delete_product/<int:pk>/', DeleteProduct.as_view(), name='delete_product'),
    path('create_review/<int:pk>/', CreateReview.as_view(), name='create_review'),
    path('update_review_moderator/<int:pk>/', UpdateReviewModerator.as_view(), name='update_review_moderator'),
    path('update_review/<int:pk>/', UpdateReview.as_view(), name='update_review'),
    path('delete_review/<int:pk>/', DeleteReview.as_view(), name='delete_review'),
    path('review_list/', UnmoderatedReviews.as_view(), name='review_list'),
]