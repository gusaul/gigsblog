from django.db import models
from datetime import datetime
# from django.contrib.auth.models import AbstractBaseUser
from mongoengine import *
from mongoengine.django.auth import *
from slugify import slugify
from django.core.urlresolvers import reverse

class Author(User):
	firstname = StringField(required=True, max_length=45)
	lastname = StringField(required=True, max_length=45)
	email = EmailField(required=True, max_length=45)

	def __unicode__(self):
		return self.firstname+" "+self.lastname

class Category(Document):
	user = ReferenceField(Author)
	name = StringField(max_length=200,required=True)
  
	def __unicode__(self):
		return self.name

class Tag(Document):
	user = ReferenceField(Author)
	name = StringField(max_length=200,required=True)

	def __unicode__(self):
		return self.name

class Post(Document):
	user = ReferenceField(User, reverse_delete_rule=CASCADE)
	title = StringField(max_length=200, required=True)
	content = StringField(required=True)
	date_modified = DateTimeField(default=datetime.now)
	is_published = BooleanField()
	slug = StringField(max_length=200)
	# image_url = StringField(max_length=200)
	categories = ReferenceField(Category)
	tags = ListField(ReferenceField(Tag),default=list)

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		return super(Post, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('blog:detail',args=[self.id])

class Comment(Document):
	user = ReferenceField(User,reverse_delete_rule=CASCADE)
	post = ReferenceField(Post, reverse_delete_rule=CASCADE)
	text = StringField(required=True)
	date = DateTimeField(default=datetime.now)

	def __unicode__(self):
		return self.text



