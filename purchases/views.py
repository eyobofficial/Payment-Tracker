from collections import namedtuple, Counter

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, \
    DetailView

from shared.constants import ROLE_ADMIN, ROLE_MANAGEMENT, ROLE_STAFF, ROLE_GUEST
from shared.models import Unit

from .forms import SupplierForm
from .mixins import BasePurchasesView
from .models import ProductCategory, Product, Supplier


class ProductListView(BasePurchasesView, ListView):
    """List view of fertilier products."""
    template_name = 'purchases/product_list.html'
    model = Product
    paginate_by = 10
    page_name = 'products'
    queryset = Product.objects.all()
    access_roles = [ROLE_STAFF, ROLE_MANAGEMENT, ROLE_ADMIN, ROLE_GUEST]

    def get_queryset(self):
        qs = super().get_queryset()
        category_pk = self.request.GET.get('category')
        search_query = self.request.GET.get('search')

        if category_pk is not None:
            qs = qs.filter(category__pk=category_pk)

        if search_query is not None:
            qs = self.get_search_result(search_query)

        return qs

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = ProductCategory.objects.all()
        kwargs['selected_category'] = self.request.GET.get('category')
        kwargs['product_count'] = self.queryset.count()
        kwargs['search_query'] = self.request.GET.get('search', '').strip()
        return super().get_context_data(**kwargs)

    def get_search_result(self, query):
        """Returns matching products using search query."""
        return self.queryset.filter(name__istartswith=query)


class ProductCreateView(BasePurchasesView, SuccessMessageMixin, CreateView):
    """Create view for creating product."""
    template_name = 'purchases/modals/products/product_form.html'
    model = Product
    fields = ('name', 'category', 'unit')
    success_url = reverse_lazy('purchases:product-list')
    success_message = 'A new product is successfully created.'
    page_name = 'products'
    access_roles = [ROLE_ADMIN, ROLE_STAFF]

    def get_context_data(self, **kwargs):
        kwargs.update({
            'category_list': ProductCategory.objects.all(),
            'unit_list': Unit.objects.all()
        })
        return super().get_context_data(**kwargs)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = 400
        return response


class ProductUpdateView(BasePurchasesView, SuccessMessageMixin, UpdateView):
    """Update view for editing existing product."""
    template_name = 'purchases/modals/products/product_form.html'
    model = Product
    fields = ('name', 'category', 'unit')
    success_url = reverse_lazy('purchases:product-list')
    success_message = 'The selected product is successfully updated.'
    page_name = 'products'
    access_roles = [ROLE_ADMIN, ROLE_STAFF]

    def get_context_data(self, **kwargs):
        kwargs.update({
            'category_list': ProductCategory.objects.all(),
            'unit_list': Unit.objects.all()
        })
        return super().get_context_data(**kwargs)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = 400
        return response


class ProductDeleteView(BasePurchasesView, SuccessMessageMixin, DeleteView):
    """Delete view to delete a product."""
    template_name = 'purchases/modals/products/product_delete_form.html'
    model = Product
    success_url = reverse_lazy('purchases:product-list')
    success_message = 'The selected product is successfully deleted.'
    page_name = 'products'
    access_roles = [ROLE_ADMIN, ROLE_STAFF]

    def delete(self, request, *args, **kwargs):
        """Overwrites delete method to send success message."""
        self.object = self.get_object()
        self.object.delete()
        success_url = self.get_success_url()
        messages.success(request, self.success_message)
        return redirect(success_url)


class SupplierListView(BasePurchasesView, ListView):
    """List view of fertilier suppliers."""
    template_name = 'purchases/supplier_list.html'
    model = Supplier
    paginate_by = 10
    page_name = 'suppliers'
    queryset = Supplier.objects.all()
    access_roles = [ROLE_STAFF, ROLE_MANAGEMENT, ROLE_ADMIN, ROLE_GUEST]

    def get_queryset(self):
        qs = super().get_queryset()
        country = self.request.GET.get('country')

        if country is not None:
            qs = qs.filter(country=country)

        search_query = self.request.GET.get('search')
        if search_query is not None:
            qs = self.get_search_result(search_query)
        return qs

    def get_context_data(self, **kwargs):
        supplier_countries = [s.country for s in Supplier.objects.all()]
        countries_count = Counter(supplier_countries)
        Country = namedtuple('Country', ['name', 'code', 'count'])
        kwargs['country_list'] = [
            Country(name=c.name, code=c.code, count=count)
            for c, count in countries_count.items()
        ]
        kwargs['selected_country'] = self.request.GET.get('country')
        kwargs['suppliers_count'] = self.queryset.count()
        kwargs['search_query'] = self.request.GET.get('search', '').strip()
        return super().get_context_data(**kwargs)

    def get_search_result(self, query):
        """Returns matching suppliers using search query."""
        search_qs = self.queryset.filter(
            Q(name__istartswith=query) | Q(short_name__istartswith=query)
        )
        return search_qs


class SupplierCreateView(BasePurchasesView, SuccessMessageMixin, CreateView):
    """Create view for creating new supplier."""
    template_name = 'purchases/modals/suppliers/supplier_form.html'
    model = Supplier
    form_class = SupplierForm
    success_url = reverse_lazy('purchases:supplier-list')
    success_message = 'A new supplier is successfully created.'
    page_name = 'suppliers'
    access_roles = [ROLE_ADMIN, ROLE_STAFF]

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = 400
        return response


class SupplierUpdateView(BasePurchasesView, SuccessMessageMixin, UpdateView):
    """Update view for editing existing supplier."""
    template_name = 'purchases/modals/suppliers/supplier_form.html'
    model = Supplier
    form_class = SupplierForm
    success_url = reverse_lazy('purchases:supplier-list')
    success_message = 'The selected supplier is successfully updated.'
    page_name = 'suppliers'
    access_roles = [ROLE_ADMIN, ROLE_STAFF]

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = 400
        return response


class SupplierDeleteView(BasePurchasesView, SuccessMessageMixin, DeleteView):
    """Delete view to delete a supplier."""
    template_name = 'purchases/modals/suppliers/supplier_delete_form.html'
    model = Supplier
    success_url = reverse_lazy('purchases:supplier-list')
    success_message = 'The selected supplier is successfully deleted.'
    page_name = 'suppliers'
    access_roles = [ROLE_ADMIN, ROLE_STAFF]

    def delete(self, request, *args, **kwargs):
        """Overwrites delete method to send success message."""
        self.object = self.get_object()
        self.object.delete()
        success_url = self.get_success_url()
        messages.success(request, self.success_message)
        return redirect(success_url)
