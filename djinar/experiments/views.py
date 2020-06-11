import asyncio

from django.views.generic import TemplateView, View
from django.http.response import HttpResponse
from django.utils.decorators import classonlymethod
from braces.views import CsrfExemptMixin


class WebcamView(TemplateView):
    """
    """
    template_name = 'experiments/webcam.html'


class OfferView(CsrfExemptMixin, View):
    """
    """
    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view

    async def post(self, request, *args, **kwargs):
        """
        """
        await asyncio.sleep(2)
        return HttpResponse('Hello fro async Post')
