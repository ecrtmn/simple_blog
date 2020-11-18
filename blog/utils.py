from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from .models import *

class ObjectDetailMixin:
    model = None
    path = None
    def get(self, request, slug):
            obj = get_object_or_404(self.model, slug__iexact=slug)
            return render(request, self.path, context={self.model.__name__.lower(): obj, 'edit_object': obj, 'detail': True})

class ObjectCreateMixin:
    model = None
    path = None

    def get(self, request):
            obj = self.model()
            return render(request, self.path, context={'form': obj})

    def post(self, request):
        bound_obj = self.model(request.POST)

        if bound_obj.is_valid():
            val_obj = bound_obj.save()
            return redirect(val_obj)

        return render(request, self.path, context={'form': bound_obj})


class ObjectUpdateMixin:
    model = None
    model_form = None
    template = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(instance=obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(request.POST, instance=obj)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})


class ObjectDeleteMixin:
    model = None
    template = None
    redirect_url = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse(self.redirect_url))
