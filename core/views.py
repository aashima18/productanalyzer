from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import FormView
from .forms import SearchForm
from urllib.parse import urlencode, urlparse, parse_qs
from lxml.html import fromstring
from requests import get
 
class ABC(FormView):

    template_name = 'core/home.html'
    form_class = SearchForm

    def form_valid(self, form):
        query = form.cleaned_data.get('query', None)
        print(query)
        #return render(self.request, self.template_name)
        qq = input(query)
        q = { 'q' : qq}

        url = "https://www.google.com/search?{}".format(urlencode(q))
        raw = get(url).text

        page = fromstring(raw)

        for result in page.cssselect(".r a"):
            url = result.get("href")
            if url.startswith("/url?"):
                url = parse_qs(urlparse(url).query)['q']
            print(url[0])
        return render(self.request, self.template_name)

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'