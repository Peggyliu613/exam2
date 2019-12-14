from django.db import models
import re
import bcrypt

class UsersManager(models.Manager):
    
    def validator(self, postdata):
        errors={}
        if not postdata['first_name'] and len(postdata['first_name'])<2 or not postdata['first_name'].isalpha():
            errors['first_name']="First name should be at least 2 characters"
        if not postdata['last_name'] and len(postdata['last_name'])<2 or not postdata['last_name'].isalpha():
            errors['last_name']="Last name should be at least 2 characters"
        if not re.search(".+@.+\..+", postdata['email']):
            errors['email']="invalid email"
        if not postdata['password'] or len(postdata['password'])<8:
            errors['password']="Password should be at least 8 characters"
        if postdata['password']!=postdata['confirmpassword']:
            errors['confirmpassword']="Password does not matched"
        is_email_exit=Users.objects.filter(email=postdata['email'])
        if len(is_email_exit)>0:
            errors['email']="Email is used"
        return errors

    def validator_login(self, postdata):
        errors={}
        try: 
            the_user=Users.objects.get(email=postdata['email'])
            if not bcrypt.checkpw(postdata['password'].encode(), the_user.password.encode()):
                errors['password']="Email/Password does not matched"
            return errors
        except:
            errors['email']="Email/Password does not matched"
            return errors
    
class JobsManager(models.Manager):
    def validator(self, postdata):
        errors={}
        if len(postdata['title'])<3:
            errors['title']="Title should be at least 3 characters"
        if len(postdata['desc'])<3:
            errors['desc']="Description should be at least 3 characters"
        if not postdata['location']:
            errors['location']="A location must be provided"
        return errors


class Users(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    #jobs_uploaded
    #jobs_added

    objects=UsersManager()

class Jobs(models.Model):
    title=models.CharField(max_length=255)
    location=models.CharField(max_length=255)
    desc=models.TextField(null=True)
    uploaded_by=models.ForeignKey(Users, related_name="jobs_uploaded", on_delete=models.CASCADE)
    added_by=models.ManyToManyField(Users, related_name="jobs_added", null=True)
    category=models.CharField(max_length=255, null=True)
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    objects=JobsManager()