from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseNotAllowed
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.base import ContextMixin
from django.http import JsonResponse


class UserIsAdminCheckMixin(View):
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserIsAdminCheckMixin, self).dispatch(request, *args, **kwargs)


class UserIsModeratorCheckMixin(View):
    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_active and request.user.is_staff:
            return super(UserIsModeratorCheckMixin, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseNotAllowed(request.method)


class UserLoginCheckMixin(View):
    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_active:
            return super(UserLoginCheckMixin, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseNotAllowed(request.method)


class AjaxableResponseMixin(View):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response


class BaseClassContextMixin(ContextMixin):
    title = ''

    def get_context_data(self, **kwargs):
        context = super(BaseClassContextMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context
