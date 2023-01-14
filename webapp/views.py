from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.forms import ProductForm, ReviewForm
from webapp.models import Product, Review


class ProductsView(ListView):
    model = Product
    template_name = 'products/index.html'
    context_object_name = 'products'
    ordering = ('category', 'title')
    paginate_by = 5
    paginate_orphans = 1


class ProductView(DetailView):
    model = Product
    template_name = 'products/product_view.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        context['reviews'] = Review.objects.filter(product=product)
        return context


class CreateProduct(PermissionRequiredMixin, CreateView):
    form_class = ProductForm
    template_name = 'products/create_product.html'
    permission_required = 'webapp.add_product'


class UpdateProduct(PermissionRequiredMixin, UpdateView):
    form_class = ProductForm
    template_name = 'products/update_product.html'
    model = Product
    permission_required = 'webapp.change_product'


class DeleteProduct(PermissionRequiredMixin, DeleteView):
    model = Product
    context_object_name = 'product'
    template_name = 'products/delete_product.html'
    success_url = reverse_lazy('webapp:index')
    permission_required = 'webapp.delete_product'


class CreateReview(LoginRequiredMixin, CreateView):
    form_class = ReviewForm
    template_name = 'reviews/create_review.html'
    model = Review

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        user = self.request.user
        form.instance.product = product
        form.instance.author = user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:product_view', kwargs={'pk': self.object.product.pk})


class UpdateReviewModerator(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        review = get_object_or_404(Review, pk=kwargs.get('pk'))
        context = {
            'review': review,
        }
        return render(request, 'reviews/update_review_with_moderator.html', context=context)

    def post(self, request, *args, **kwargs):
        review = get_object_or_404(Review, pk=kwargs.get('pk'))
        description = request.POST.get('description')
        grade = request.POST.get('grade')
        moderated = request.POST.get('moderated')
        review.objects.update(author=self.request.user, description=description,
                              grade=grade, moderated=moderated)
        return redirect('webapp:index')


class UpdateReview(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        review = get_object_or_404(Review, pk=kwargs.get('pk'))
        context = {
            'review': review,
        }
        return render(request, 'reviews/update_review.html', context=context)

    def post(self, request, *args, **kwargs):
        review = get_object_or_404(Review, pk=kwargs.get('pk'))
        description = request.POST.get('description')
        grade = request.POST.get('grade')
        review.objects.update(author=self.request.user, description=description,
                              grade=grade, moderated=False)
        return redirect('webapp:index')


class DeleteReview(LoginRequiredMixin, DeleteView):
    template_name = 'reviews/delete_review.html'
    context_object_name = 'review'
    success_url = reverse_lazy('webapp:index')


class UnmoderatedReviews(PermissionRequiredMixin, ListView):
    model = Review
    template_name = 'reviews/review_list.html'
    context_object_name = 'reviews'
    permission_required = 'can_view_moderated_to_the_review'

