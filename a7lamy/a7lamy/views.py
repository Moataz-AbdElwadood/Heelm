from django.shortcuts import render
from django.views import View  

class IndexView(View):
    def get(self, request):            
        # TODO: after integrating wit frontend make it route to its index not this index page
        return render(request, 'index.html')