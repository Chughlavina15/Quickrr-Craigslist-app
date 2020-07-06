import find

import requests

from django.shortcuts import render
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
#to type a success message after the account is created
from django.contrib import messages
#to authenticate login,logout
from django.contrib.auth import authenticate,login,logout

from .models import *
#creating views here
from .forms import CreateUserForm

#function index is for register page
def index(request):
    form = CreateUserForm()

    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            #user=form.get_initial_for_field('username')
            messages.success(request,'Account was successfully created')
            return redirect('home')
    context = {'home': home}
    return render(request,'my_app/index.html',context)

def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            redirect('home')
    context={}
    return render(request,'my_app/login.html',context)


main_url='https://mumbai.craigslist.org/search/?query={}'
base_image="https://images.craigslist.org/{}_300x300.jpg"

def home(request):
    context = {'home': home}
    return render(request,'base.html',context)

# Create your views here.
def new_search(request):
    search=request.POST.get('search')
    final_url=main_url.format(quote_plus(search))
    response=requests.get(final_url)
    data=response.text
    soup=BeautifulSoup(data,features='html.parser')
    post_listings = soup.find_all('li', {'class': 'result-row'})
    #print(post_listings)

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price =post.find(class_='result-price').text
        else:
            post_price='N/A'
        if post.find(class_='result-image').get('data-ids'):
            post_image_id=post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            #print(post_image_url)
            post_image_url=base_image.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url='https://craigslist.org/images/peace.jpg'

        final_postings.append((post_title,post_url,post_price,post_image_url))
        #print(final_postings)




    res_frontend={'search':search,
                    'final_postings':final_postings}
    return render(request,'my_app/new_search.html',res_frontend)

