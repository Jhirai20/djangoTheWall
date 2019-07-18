from __future__ import unicode_literals
from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX =re.compile(r'^[a-zA-Z]+$') 

class Manager(models.Manager):
    def basic_validator(self, postData):
        
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if not NAME_REGEX.match(postData['first_name']):
            errors["first_name"] = "Name can only contain letters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if not NAME_REGEX.match(postData['last_name']):
            errors["last_name"] = "Name can only contain letters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email']= "Please enter a valid email!"
        if len(postData['password']) < 8:
            errors['password']="Password is too short!"
        if postData['password']!=postData['confirm_password']:
            errors['password']= "Passwords do not match!"
        if len(postData['message']<1):
            errors['message']="Messages cannot be blank!"
        if len(postData['comment']<1):
            errors['comment']="Comments cannot be blank!"
        return errors
        

class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    objects = Manager()

class Messages(models.Model):
    user = models.ForeignKey(Users, related_name='messages')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    objects = Manager()

class Comments(models.Model):
    message = models.ForeignKey(Messages, related_name='comments')
    user= models.ForeignKey(Users, related_name='comments')
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    objects = Manager()

