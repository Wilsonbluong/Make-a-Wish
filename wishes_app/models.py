from django.db import models
import re
import bcrypt

# test whether email field matches this pattern
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class userManager(models.Manager):
    def register_validator(self, post_data):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        # checks first name min length
        if len(post_data['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        # checks last name min length
        if len(post_data['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email address!"
        # checks password name min length
        if len(post_data['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        # checks to see if password matches password confirm
        if post_data['password'] != post_data['password_confirm']:
            errors["password_confirm"] = "Password does not match"
        return errors
    
    def login_validator(self, post_data):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        user = User.objects.filter(email=post_data['email']).first()
        print('user:', user)
        # checks is email is in db
        if user == None:
            errors['login']= "Invalid email or password"
        # checks if the hashed password matches
        elif not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
            errors['login']= "Invalid email or password"
        return errors
    
class wishManager(models.Manager):
    def wish_validator(self, post_data):
        errors = {}
        # wish min length
        if len(post_data['wish']) < 3:
            errors["wish"] = "Wish should be at least 3 characters"
        # checks description min length
        if len(post_data['desc']) < 3:
            errors["desc"] = "Description should be at least 3 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = userManager()
    # wishes: a list of wishes associated with the user
    
class Wish(models.Model):
    wish = models.CharField(max_length=255)
    desc = models.CharField(max_length=255, default="")
    grant = models.BooleanField(default=False)
    wisher = models.ForeignKey(User, related_name="wishes", on_delete = models.CASCADE)
    wishers_who_liked = models.ManyToManyField(User, related_name="granted_wishes_liked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = wishManager()
    