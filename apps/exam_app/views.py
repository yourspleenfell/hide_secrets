# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def index(request):
    if 'id' in request.session:
        return redirect(reverse('app:user', kwargs={'id': request.session['id'] }))
    return render(request, 'exam_app/index.html')

def create_user(request):
    errors = User.objects.validator(request.POST)
    if len(errors) > 0:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/main')
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    pwd_hash = bcrypt.hashpw(password.encode(),bcrypt.gensalt())
    user = User.objects.create(first_name = first_name, last_name = last_name, username = username, email = email, password = pwd_hash)
    Wishlist.objects.create(user = user)
    request.session['id'] =  user.id
    request.session['name'] = user.first_name + ' ' + user.last_name
    request.session['username'] = user.username
    return redirect(reverse('app:user', kwargs={'id': user.id }))

def login(request):
    user_login = User.objects.login_validator(request.POST)
    if user_login[0]:
        user = user_login[1]
        request.session['id'] = user.id
        request.session['name'] = user.first_name + ' ' + user.last_name
        request.session['username'] = user.username
        return redirect(reverse('app:user', kwargs={'id': user.id }))
    elif not user_login[0]:
        for tag, item in user_login[1].iteritems():
            messages.error(request, item, extra_tags=tag)
            return redirect('/main')

def show_user(request, id):
    if 'id' not in request.session:
        return redirect('/main')
    elif int(id) != int(request.session['id']):
        return redirect(reverse('app:user', kwargs={'id': request.session['id'] }))
    wishlist = {
        'user_list': Wishlist.objects.get(user_id=id).products.all(),
        'other_items': Product.objects.all(),
    }
    return render(request, 'exam_app/dashboard.html', wishlist)

def logout(request):
    messages.success(request, 'Thanks for visiting, ' + request.session['name'])
    request.session.clear()
    return redirect('/main')

def create_item(request):
    if 'id' not in request.session:
        return redirect('/main')
    return render(request, 'exam_app/create_item.html')

def submit_item(request, id):
    product = Product.objects.validator(request.POST, id)
    if product[0]:
        Wishlist.objects.get(user_id=id).products.add(product[1])
        messages.success(request, 'Successfully added ' + product[1].name + ' to your wishlist', extra_tags='wishlist')
        return redirect(reverse('app:user', kwargs={'id': id }))
    if not product[0]:
        for tag, item in product[1].iteritems():
            messages.error(request, item, extra_tags=tag)
        return redirect('/wish_items/create')

def add_item(request, id):
    product = Product.objects.get(id=id)
    messages.success(request, 'Successfully added ' + product.name + ' to your wishlist', extra_tags='wishlist')
    Wishlist.objects.get(user_id=request.session['id']).products.add(product)
    return redirect(reverse('app:user', kwargs={'id': request.session['id'] }))

def remove_item(request, id):
    product = Product.objects.get(id=id)
    messages.success(request, 'Successfully removed ' + product.name + ' from your wishlist', extra_tags='wishlist')
    Wishlist.objects.get(user_id=request.session['id']).products.remove(product)
    return redirect(reverse('app:user', kwargs={'id': request.session['id'] }))

def delete_item(request, id):
    product = Product.objects.get(id=id)
    messages.success(request, 'Successfully deleted ' + product.name + ' from catalog', extra_tags='wishlist')
    product.delete()
    return redirect(reverse('app:user', kwargs={'id': request.session['id'] }))

def show_item(request, id):
    if 'id' not in request.session:
        return redirect('/main')
    product = {
        'item': Product.objects.get(id=id),
        'wishlists': Wishlist.objects.filter(products=id),
    }
    return render(request, 'exam_app/product.html', product)

def show_user_list(request, id):
    if 'id' not in request.session:
        return redirect('/main')
    user = {
        'user': User.objects.get(id=id),
        'wishlist': Wishlist.objects.get(user_id=id).products.all(),
        'user_list': Wishlist.objects.get(user_id=request.session['id']).products.all(),
    }
    return render(request, 'exam_app/user.html', user)

def update_user(request, id):
    if 'id' not in request.session:
        return redirect('/main')
    elif int(id) == int(request.session['id']):
        user = {
            'user': User.objects.get(id=id),
            'wishlist': Wishlist.objects.get(user_id=id).products.all(),
            'user_list': Wishlist.objects.get(user_id=request.session['id']).products.all(),
        }
        return render(request, 'exam_app/edit_user.html', user)
    else:
        return redirect(reverse('app:user', kwargs={'id': request.session['id'] }))

def submit_update(request, id):
    errors = User.objects.update_validator(request.POST)
    if len(errors) > 0:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect(reverse('app:update_user', kwargs={'id': request.session['id'] }))
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    pwd_hash = bcrypt.hashpw(password.encode(),bcrypt.gensalt())
    user = User.objects.get(id=id)
    user.first_name = first_name
    user.last_name = last_name
    user.username = username
    user.email = email
    user.password = pwd_hash
    user.save()
    request.session['id'] =  user.id
    request.session['name'] = user.first_name + ' ' + user.last_name
    request.session['username'] = user.username
    return redirect(reverse('app:user_list', kwargs={'id': request.session['id'] }))