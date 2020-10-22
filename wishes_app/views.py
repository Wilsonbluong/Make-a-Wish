from django.shortcuts import render, redirect
from .models import User, Wish
from django.contrib import messages
import bcrypt

# Create your views here.

### LOGIN/REGISTRATION PAGE ###
def index(request):
    print('*'*100)
    print('On the login/reg page...')
    print(request.POST)
    # if user is in session redirect to wishes page to make wishes!
    if 'uid' in request.session:
        return redirect('/wishes')
    else:
        return render(request, 'index.html')

### REGISTRATION ###
def register(request):
    print('*'*100)
    print('Registering...')
    errors = User.objects.register_validator(request.POST)
    # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        # hash user password
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        
        # create a user
        user_just_registered = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashed_pw,
        )
        
        print("hashbrown password is:", hashed_pw)
        
        # create session
        request.session['uid'] = user_just_registered.id
        request.session['first_name'] = user_just_registered.first_name
        
        return redirect('/wishes')
    
### LOGIN ###
def login(request):
    print('*'*100)
    print('Logging in...')
    errors = User.objects.login_validator(request.POST)
    # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        user = User.objects.filter(email=request.POST['email']).first()
        
        #start user in session
        request.session['uid'] = user.id
        request.session['first_name'] = user.first_name
        
        return redirect('/wishes')

### WISHES PAGE ###
def wishes(request):
    print('*'*100)
    print('On the wishes page...')
    print(request.POST)
    # if user not in session redirect to login/reg page
    if 'uid' not in request.session:
        return redirect('/')
    else:
        logged_in_user = User.objects.get(id=request.session['uid'])

        context = {
            "granted_wishes": Wish.objects.filter(grant=True),
            "my_wishes": logged_in_user.wishes.filter(grant = False)
        }
        return render(request, "wishes.html", context)

### NEW WISHES PAGE ###
def new_wishes(request):
    print('*'*100)
    print('On wishes page...')
    return render(request, 'new_wishes.html')

### ADD NEW WISHES ###
def add_wishes(request):
    print('*'*100)
    print('Adding new wish...')
    errors = Wish.objects.wish_validator(request.POST)
    # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/wishes/new')
    else:
        print(request.POST)
        
        logged_in_user = User.objects.get(id=request.session['uid'])
        
        # create instance of object
        Wish.objects.create(
            wish = request.POST['wish'],
            desc = request.POST['desc'],
            wisher = logged_in_user
        )
        # print(new_wish.grant)
        
        return redirect('/wishes')
    
### EDIT WISHES PAGE ###
def edit(request, wish_id):
    print('*'*100)
    print('Edit wish page...')
    context = {
        "wish": Wish.objects.get(id=wish_id)
    }
    
    return render(request, 'edit_wishes.html', context)

### UPDATING EXISTING WISH ###
def update(request, wish_id):
    print('*'*100)
    print('Updating wish...')
    errors = Wish.objects.wish_validator(request.POST)
    # check if the errors dictionary has anything in it
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect(f'/wishes/{ wish_id }/edit')
    else:
        # updating and saving wish
        wish = Wish.objects.get(id = wish_id)
        wish.wish = request.POST['wish']
        wish.desc = request.POST['desc']
        wish.save()
    
    return redirect('/wishes')

### GRANT WISH ###
def grant(request, wish_id):
    print('*'*100)
    print('Granting wish...')
    
    # change wish to granted wish
    wish = Wish.objects.get(id = wish_id)
    wish.grant = True
    wish.save()
    
    return redirect('/wishes')

### DELETE WISH ###
def delete(request, wish_id):
    print('*'*100)
    print('Deleting wish...')
    wish = Wish.objects.get(id = wish_id)
    # delete wish from table
    wish.delete()
    return redirect('/wishes')

## LIKES ###
def like(request, wish_id):
    print('*'*100)
    print('Liking a granted wish...')
    
    # create instance of like and user
    logged_in_user = User.objects.get(id=request.session['uid'])
    granted_wish = Wish.objects.get(id=wish_id)
    
    # many to many relationship
    granted_wish.wishers_who_liked.add(logged_in_user)
    
    return redirect('/wishes')

### LOGOUT ###
def logout(request):
    print('*'*100)
    print('Logging out...')
    # delete user from session
    request.session.clear()
    return redirect('/')