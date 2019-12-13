from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from FastBridge_app.models.i_repository import IRepository


class LatinView(View):

    def __init__(self, repository: IRepository):
        self.repository = repository

    def get(self, request):
        # <view logic>
        return HttpResponse('result')

    def post(self, request):
        # <view logic>
        return HttpResponse('result')
    
    def search(self, request):
        '''
        TODO: pass variables into the search form templates
        '''
        return render(request, 'select.html')

    def result(self, request):
        '''
        TODO: pass result data into the html
        '''
        return render(request, 'result.html')
