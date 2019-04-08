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
from bs4 import BeautifulSoup
import requests
from .models import Search, Product
from ast import literal_eval




class ABC(FormView):

    template_name = 'core/home.html'
    form_class = SearchForm

    def form_valid(self, form):
        query = form.cleaned_data.get('query', None)
        #qq = input()
        q = { 'q' : query}

        url = "https://www.google.com/search?{}".format(urlencode(q))
        raw = get(url).text

        page = fromstring(raw)
        allinks = []
        for result in page.cssselect(".r a"):
            url = result.get("href")
            if url.startswith("/url?"):
                url = parse_qs(urlparse(url).query)['q']
                a = url[0]
                sites = ['amazon', 'flipkart']
                allinks.append(a)
                aallinks = [i for e in sites for i in allinks if e in i]
        data = {
            'squery': query,
            'urls':str(aallinks),
        }
        Search.objects.update_or_create(**data)
        # instance = Search(**data)
        # instance.save()
        return render(self.request, self.template_name, {'a':aallinks,  'squery': query,})


def spider(request):
    query = request.GET.get('links')
    qs = Search.objects.get(squery=query)
    a = qs.urls
    b = literal_eval(a)
    print(a)
    for links in b:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        r = requests.get(links, headers=headers)
        data = r.text
        soup = BeautifulSoup(data, 'html5lib')

        if soup.find('span', attrs={"class":"_35KyD6"}) is not None:
            name = (soup.find('span', attrs={"class":"_35KyD6"})).text # flipkart
        elif soup.find('h1', attrs={"class":"a-size-large a-spacing-none"}) is not None:
            name = (soup.find('h1', attrs={"class":"a-size-large a-spacing-none"})).text # Amazo
        else:
            name = " "
        
        if soup.find('div', attrs={"class":"_1vC4OE _3qQ9m1"}) is not None:
            price = (soup.find('div', attrs={"class":"_1vC4OE _3qQ9m1"})).text #flipkart
        elif soup.find('span', attrs={"id":"priceblock_ourprice"}) is not None:
            price = (soup.find('span', attrs={"class":"a-size-medium a-color-price priceBlockBuyingPriceString"})).text  #amazon
        elif soup.find('span', attrs={"class":"a-color-price"}) is not None:
            price = (soup.find('span', attrs={"class":"a-color-price"})).text # Amazon
        else:
            price = " "


        if soup.find('div', attrs={"class":"MocXoX"}) is not None:
            specifications = (soup.find('div', attrs={"class":"MocXoX"})).text #flipkart
        elif soup.find('span', attrs={"id":"priceblock_ourprice"}) is not None:
            price = (soup.find('span', attrs={"class":"a-size-medium a-color-price priceBlockBuyingPriceString"})).text  #amazon
        elif soup.find('span', attrs={"class":"a-color-price"}) is not None:
            price = (soup.find('span', attrs={"class":"a-color-price"})).text # Amazon
        else:
            price = " "
        
        context = {'search':qs,'product_name': name , 'price': price}
        Product.objects.update_or_create(**context)
        
        dta = Product.objects.filter(search=qs)
    return render(request, 'core/data.html', {'dta':dta})

        
class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'