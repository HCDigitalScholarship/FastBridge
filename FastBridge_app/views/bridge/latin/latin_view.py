from django.http import HttpResponse
from django.views import View
from ....models.i_repository import IRepository


class LatinView(View):

    def __init__(self, repository: IRepository):
        self.repository = repository

    def get(self, request):
        # <view logic>
        return HttpResponse('result')

    def post(self, request):
        # <view logic>
        return HttpResponse('result')
