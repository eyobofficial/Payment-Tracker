from collections import namedtuple, Counter

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, \
    DetailView

from shared.constants import ROLE_ADMIN, ROLE_MANAGEMENT, ROLE_STAFF
from shared.models import Unit
from purchases.models import Supplier, Product

from orders.forms import BatchForm
from orders.mixins import BaseBatchesView
from orders.models import Batch


class BaseBatchListView(BaseBatchesView, ListView):
    """Abstract base class for open & closed batch list views."""
    model = Batch
    paginate_by = 10
    page_name = 'batches'
    status = None

    def get_queryset(self):
        qs = super().get_queryset()
        product_pk = self.request.GET.get('product')
        search_query = self.request.GET.get('search')
        user = self.request.user

        if user.role and user.role.name == ROLE_SUPPLIER:
            qs = qs.filter(supplier=user.supplier)

        if product_pk is not None:
            qs = qs.filter(product__pk=product_pk)

        if search_query is not None:
            qs = self.get_search_result(search_query)

        return qs

    def get_context_data(self, **kwargs):
        kwargs.update({
            'product_list': Product.objects.filter(
                batches__status=self.status).distinct(),
            'selected_product': self.request.GET.get('product'),
            'batch_count': self.queryset.count(),
            'search_query': self.request.GET.get('search', '').strip()
        })
        return super().get_context_data(**kwargs)

    def get_search_result(self, query):
        """Returns matching batches using search query."""
        search_qs = self.queryset.filter(
            Q(name__istartswith=query) | Q(lc_number__istartswith=query) )
        return search_qs


class OpenBatchListView(BaseBatchListView):
    """List view of OPEN purchasing batches (lots)."""
    template_name = 'orders/open_batch_list.html'
    queryset = Batch.objects.exclude(is_deleted=True).filter(status=Batch.OPEN)
    status = Batch.OPEN
    access_roles = '__all__'


class ClosedBatchListView(BaseBatchListView):
    """List view of CLOSED purchasing batches (lots)."""
    template_name = 'orders/open_batch_list.html'
    queryset = Batch.objects.exclude(
        is_deleted=True).filter(status=Batch.CLOSED)
    status = Batch.CLOSED
    access_roles = '__all__'


class BatchDetailView(BaseBatchesView, DetailView):
    """Detail view for a purchasing batch instance."""
    template_name = 'orders/batch_detail.html'
    model = Batch
    page_name = 'batches'
    access_roles = [ROLE_ADMIN, ROLE_MANAGEMENT, ROLE_STAFF]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.exclude(is_deleted=True)
        return qs

    def get_context_data(self, **kwargs):
        kwargs['active_pk'] = self.get_active_tab()
        return super().get_context_data(**kwargs)

    def get_active_tab(self):
        """
        Returns the id of the delivery order that should be
        displayed in the active tab.
        """
        active_pk = self.request.GET.get('active_delivery_order')
        if active_pk is None:
            batch = self.get_object()
            default_delivery_order = batch.delivery_orders.first()
            if default_delivery_order is not None:
                active_pk = default_delivery_order.pk
        return active_pk


class BatchCreateView(BaseBatchesView, SuccessMessageMixin, CreateView):
    """Create view for creating purchasing batch."""
    template_name = 'orders/modals/batches/batch_form.html'
    form_class = BatchForm
    model = Batch
    success_url = reverse_lazy('purchases:batch-list')
    success_message = 'A new LOT record is successfully created.'
    page_name = 'batches'
    access_roles = [ROLE_ADMIN, ROLE_STAFF]

    def get_context_data(self, **kwargs):
        kwargs.update({
            'supplier_list': Supplier.objects.all(),
            'product_list': Product.objects.all(),
            'year_choice_list': Batch.YEAR_CHOICES
        })
        return super().get_context_data(**kwargs)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = 400
        return response


class BatchUpdateView(BaseBatchesView, SuccessMessageMixin, UpdateView):
    """Update view for editing purchasing batch."""
    template_name = 'orders/modals/batches/batch_form.html'
    form_class = BatchForm
    model = Batch
    success_url = reverse_lazy('purchases:batch-list')
    success_message = 'The LOT data is successfully updated.'
    page_name = 'batches'
    access_roles = [ROLE_ADMIN, ROLE_STAFF]

    def get_context_data(self, **kwargs):
        kwargs.update({
            'supplier_list': Supplier.objects.all(),
            'product_list': Product.objects.all(),
            'year_choice_list': Batch.YEAR_CHOICES
        })
        return super().get_context_data(**kwargs)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = 400
        return response


class BatchDeleteView(BaseBatchesView, SuccessMessageMixin, DeleteView):
    """Delete view to delete purchasing batch."""
    template_name = 'orders/modals/batches/batch_delete_form.html'
    model = Batch
    success_url = reverse_lazy('purchases:batch-list')
    success_message = 'The selected LOT is successfully deleted.'
    page_name = 'batches'
    access_roles = [ROLE_ADMIN, ROLE_STAFF]

    def delete(self, request, *args, **kwargs):
        """Overwrites delete method to change is_delete status `True`."""
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        success_url = self.get_success_url()
        messages.success(request, self.success_message)
        return redirect(success_url)