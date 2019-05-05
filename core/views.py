from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import FormView
from .forms import SearchForm, FeedbackForm
from urllib.parse import urlencode, urlparse, parse_qs
from lxml.html import fromstring
from requests import get
from bs4 import BeautifulSoup
import requests
from .models import Search, Product, Review , Feedback
from ast import literal_eval
from .fusioncharts import FusionCharts
from datetime import datetime


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
                sites = ['amazon.in', 'flipkart.com']
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
    qs = Search.objects.filter(squery=query).latest("squery")
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
        elif soup.find('div', attrs={"class":"section techD"}) is not None:
            specifications = (soup.find('div', attrs={"class":"section techD"})).text  #amazon
        #elif soup.find('div', attrs={"class":"section techD"}) is not None:
        #    specifications = (soup.find('span', attrs={"class":"section techD"})).text # Amazon
        else:
            specifications = " "
        

        if soup.find('div', attrs={"class":"_1i0wk8"}) is not None:
           rating = (soup.find('div', attrs={"class":"_1i0wk8"})).text # flipkart
        elif soup.find('span', attrs={"class":"arp-rating-out-of-text a-color-base"}) is not None:
           rating = (soup.find('span', attrs={"class":"arp-rating-out-of-text a-color-base"})).text # Amazo
        else:
           rating = " "

        if soup.find('span', attrs={"class":"_38sUEc"}) is not None:
           no_reviews = (soup.find('span', attrs={"class":"_38sUEc"})).text # flipkart
        elif soup.find('h2', attrs={"data-hook":"total-review-count"}) is not None:
           no_reviews = (soup.find('h2', attrs={"data-hook":"total-review-count"})).text # Amazo
        else:
           no_reviews = " "

########################## star code
        if soup.find_all('div', attrs={"class":"CamDho"}):
           stard = soup.find_all('div', attrs={"class":"CamDho"}) # flipkart
           print(stard)
           print(type(stard))
           star5 = (stard[0]).text
           print(star5)
        elif soup.find('a', attrs={"class": "a-size-base a-link-normal 5star histogram-review-count a-color-secondary"})is not None:
            star5 = (soup.find('a', attrs={"class": "a-size-base a-link-normal 5star histogram-review-count a-color-secondary"})).text #amazon
        else:
            star5 = None

        if soup.find_all('div', attrs={"class":"CamDho"}):
           starf = soup.find_all('div', attrs={"class":"CamDho"}) # flipkart
           star4 = (starf[1]).text
        elif soup.find('a', attrs={'class': 'a-size-base a-link-normal 4star histogram-review-count a-color-secondary'})is not None: 
            star4 = (soup.find('a', attrs={'class': 'a-size-base a-link-normal 4star histogram-review-count a-color-secondary'})).text #amazon
        else:
            star4 = None

        if soup.find_all('div', attrs={"class":"CamDho"}):
           starg = (soup.find_all('div', attrs={"class":"CamDho"})) # flipkart
           star3 = (starg[2]).text
        elif soup.find('a', attrs={'class': 'a-size-base a-link-normal 3star histogram-review-count a-color-secondary'})is not None:
            star3 = (soup.find('a', attrs={'class': 'a-size-base a-link-normal 3star histogram-review-count a-color-secondary'})).text #amazon
        else:
            star3 = None
        

        if soup.find_all('div', attrs={"class":"CamDho"}):
           starj = soup.find_all('div', attrs={"class":"CamDho"}) # flipkart
           star2 = (starj[3]).text
        elif soup.find('a', attrs={'class': 'a-size-base a-link-normal 2star histogram-review-count a-color-secondary'})is not None:
            star2 = (soup.find('a', attrs={'class': 'a-size-base a-link-normal 2star histogram-review-count a-color-secondary'})).text #amazon
        else:
            star2 = None


        if soup.find_all('div', attrs={"class":"CamDho"}):
           stark = soup.find_all('div', attrs={"class":"CamDho"}) # flipkart
           star1 = (stark[4]).text
        elif soup.find('a', attrs={'class': 'a-size-base a-link-normal 1star histogram-review-count a-color-secondary'})is not None:
            star1 = (soup.find('a', attrs={'class': 'a-size-base a-link-normal 1star histogram-review-count a-color-secondary'})).text #amazon
        else:
            star1 = None


       
        context = {"url":links,
                    'rating': rating,
                    'no_reviews': no_reviews,
                    'star5': star5,
                    'star4': star4,
                    'star3': star3,
                    'star2':star2,
                    'star1':star1,
                    'search':qs,
                    'product_name': name ,
                    'price': price ,
                    'specifications': specifications}
        
        # print(context)
        Product.objects.update_or_create(**context)
       
        
        dta = Product.objects.filter(search=qs)
    
    return render(request, 'core/data.html', {'dta':dta} )

def graph(request):
    query = request.GET.get('links')
    qs = Product.objects.get(id=query)
    if 'amazon' in qs.url:
        totalrating = qs.no_reviews
        if ',' in totalrating:
            a = (totalrating.replace(',', ' ')).split(' ')
            # a = a.split(' ')
            b = a[0] + a[1]
        else:
            a = totalrating.split(' ')
            b = a[0]   
        b = int(b)
        # print(b)
        starww5 = qs.star5
        starw5 = starww5.replace('%' , '')
        # print(starw5)
        starw5 = str((b*int(starw5))/100)
        # print(starw5)
        starw4 = str((b*int((qs.star4).replace('%' , '')))/100)
        # print(starw4)
        starw3 = str((b*int((qs.star3).replace('%' , '')))/100)
        # print(starw3)
        starw2 = str((b*int((qs.star2).replace('%' , '')))/100)
        # print(starw2)
        starw1 = str((b*int((qs.star1).replace('%' , '')))/100)
        # print(starw1)
    else:
        starww5 = qs.star5
        # print(type(starw5))
        starw5 = starww5.replace(',' , '')
        starw4 = qs.star4
        starw3 = qs.star3 
        starw2 = qs.star2
        starw1 = qs.star1
        
    pie3d = FusionCharts("pie3d", "ex2" , "100%", "600", "chart-1", "json", 
        { 
            "chart": {
                "caption": "Rating Distribution",
                # "subCaption" : "from fl - updated -",
                "showValues":"1",
                "showPercentInTooltip" : "0",
                "numberPrefix" : "count ",
                "enableMultiSlicing":"1",
                "theme": "fusion"
            },
            "data": [{
                "label": "1 star",
                "value": starw1
            }, {
                "label": "2 star",
                "value": starw2
            }, {
                "label": "3 star",
                "value": starw3
            }, {
                "label": "4 star",
                "value": starw4
            }, {
                "label": "5 star",
                "value": starw5
            }]
        })
    context = {
        'output' : pie3d.render(),
        'chartTitle': 'Pie 3D Chart'
    }
    return render(request, 'core/graph.html', context)

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def index(request):
    return render(request,'core/index.html')


def about(request):
    return render(request,'core/about-us.html')  


def contact(request):
    return render(request,'core/contact.html')



# def feedback(request):
#     form = FeedbackForm(request.POST or None)
#     print(form)
#     if form.is_valid():
#         abc = form.save(commit=False)
#         abc.save()
#         return render(request, 'core/contactform.html', {'form':form})  
#     else:
#         return render(request,'core/contactform.html', {'form' : form})

def feedback(request):
    if request.method == 'POST':
        if request.POST.get('name') and request.POST.get('email') and request.POST.get('message'):
            post=Feedback()
            post.name= request.POST.get('name')
            post.email= request.POST.get('email')
            post.message= request.POST.get('message')
            post.save()
            return render(request, 'core/contactform.html')  

    else:
        return render(request,'core/contactform.html')



# def contactform(request):
#     return render(request, 'core/contactform.html')



