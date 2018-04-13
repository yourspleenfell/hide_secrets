# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
PWD_REGEX = re.compile(r'(?=.*[A-Z])(?=.*[0-9])')

# Create your models here.
class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        first = postData['first_name']
        last = postData['last_name']
        username = postData['username']
        email = postData['email']
        pwd = postData['password']
        pwd_con = postData['password_con']
        if len(first) < 3:
            errors['first']="First name must be at least 3 characters"
        elif not NAME_REGEX.match(first):
            errors['first']="First name can consist of only letters"
        if len(last) < 3:
            errors['last']="Last name must be at least 3 characters"
        elif not NAME_REGEX.match(last):
            errors['last']="Last name can consist of only letters"
        if len(username) < 3:
            errors['username_reg']="Username must be at least 3 characters"
        if len(email) is 0:
            errors['email_reg']="You must enter an email address"
        elif not EMAIL_REGEX.match(email):
            errors['email_reg']="Email must follow the standard format"
        elif len(User.objects.filter(email=email)) > 0:
            errors['email_reg']="Email already registered to an account"
        if len(pwd) < 8:
            errors['pwd_reg']="Password must be at least 8 characters"
        elif pwd != pwd_con:
            errors['pwd_reg']="Both passwords must match"
        elif not PWD_REGEX.match(pwd):
            errors['pwd_reg']="Password must contain one capital letter and one number"
        if len(errors) > 0:
            return (False, errors)
        else:
            new_user = self.create (
                first_name = first,
                last_name = last,
                username = username,
                email = email,
                password = bcrypt.hashpw(pwd.encode(),bcrypt.gensalt())
            )
            return (True, new_user)
    def login_validator(self, postData):
        errors = {}
        username = postData['username']
        pwd = postData['password']
        if len(username) is 0:
            errors['username_log'] = "Must enter a username to login"
            return (False, errors)
        if self.filter(username=username):
            user = self.filter(username=username)
            if bcrypt.checkpw(pwd.encode(),user[0].password.encode()):
                user = self.get(username=username)
                return (True, user)
            else:
                errors['pwd_log'] = "Incorrect password entered"
                return (False, errors)
        else:
            errors['username_log'] = "Username not on file"
            return (False, errors)
    def update_validator(self, postData):
        errors = {}
        first = postData['first_name']
        last = postData['last_name']
        username = postData['username']
        email = postData['email']
        pwd = postData['password']
        pwd_con = postData['password_con']
        user = self.get(id=postData['id'])
        if len(first) < 3 and len(first) > 0:
            errors['first']="First name must be at least 3 characters"
            if not NAME_REGEX.match(first):
                errors['first']="First name can consist of only letters"
        elif len(first) is 0:
            first = user.first_name
            print first
        if len(last) < 3 and len(last) > 0:
            errors['last']="Last name must be at least 3 characters"
            if not NAME_REGEX.match(last):
                errors['last']="Last name can consist of only letters"
        elif len(last) is 0:
            last = user.last_name
            print last
        if len(username) < 3 and len(username) > 0:
            errors['username']="Last name must be at least 3 characters"
        elif len(username) is 0:
            username = user.username
            print username
        if len(email) < 3 and len(email) > 0:
            errors['email']="You must enter a valid email address"
            if not EMAIL_REGEX.match(email):
                errors['email']="Email must follow the standard format"
        elif len(email) is 0:
            email = user.email
        if len(pwd) < 8 and len(pwd) > 0:
            errors['pwd_reg']="Password must be at least 8 characters"
            if not PWD_REGEX.match(pwd):
                errors['pwd_reg']="Password must contain one capital letter and one number"
        elif pwd != pwd_con:
            errors['pwd_reg']="Both passwords must match"
        if errors:
            return (False, errors)
        else:
            user.first_name = first
            user.last_name = last
            user.username = username
            user.email = email
            user.password = bcrypt.hashpw(pwd.encode(),bcrypt.gensalt())
            user.save()
            return (True, user)

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class ProductManager(models.Manager):
    def validator(self, postData, id):
        errors = {}
        name = postData['name']
        user = User.objects.get(id = id)
        if len(name) < 3:
            errors['product']="Product name must be at least 3 characters"
            return (False, errors)
        elif len(self.filter(name=name)) > 0:
            product = self.filter(name=name).first()
            return (True, product)
        else:
            new_product = self.create(
                name = name,
                created_by = user,
            )
            return (True, new_product)       

class Product(models.Model):
    name = models.CharField(max_length = 255)
    created_by = models.ForeignKey(User, related_name="products_created")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ProductManager()
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, related_name="wishlist")
    products = models.ManyToManyField(Product, related_name="wishlists")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)