from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Div,Submit,HTML,Button,Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from apps.blog.models import *
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput())

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			raise forms.ValidationError(
				mark_safe(
					('User not found. Registere <a href="{0}">Here</a>').format(reverse('signUp'))
				)
			)
		return username

	def clean_password(self):
		username = self.cleaned_data.get('username',None)
		password = self.cleaned_data['password']
		try:
			user = User.objects.get(username=username)
		except:
			user = None
		if user is not None and not user.check_password(password):
			raise forms.ValidationError("Invalid Password")
		elif user is None:
			pass
		else:
			return password

	helper = FormHelper()
	helper.form_method = 'POST'
	helper.form_class = 'form-horizontal'
	helper.layout = Layout(
	  	Field('username', css_class='input-lg-4'),
	  	Field('password', css_class='input-lg-4'),
	  	FormActions(Submit('login', 'Login', css_class='btn btn-primary')),
	  )

class SignUpForm(forms.Form):
	username = forms.CharField(max_length=45)
	password = forms.CharField(widget=forms.PasswordInput())
	firstname = forms.CharField(max_length=45)
	lastname = forms.CharField(max_length=45)
	email = forms.CharField(widget=forms.EmailInput())

	def __init__(self, *args, **kwargs):
		self.instance = kwargs.pop('instance', None)
		super(SignUpForm, self).__init__(*args, **kwargs)

	helper = FormHelper()
	helper.form_method = 'POST'
	helper.form_calss = 'form_horizontal'
	helper.layout = Layout(
		Field('username'),
		Field('password'),
		Field('firstname'),
		Field('lastname'),
		Field('email'),
		FormActions(Submit('signup', 'Sign Up', css_class='btn btn-primary'))
	)

	def save(self):
		author = Author()
		author.username = self.cleaned_data['username']
		author.password = self.cleaned_data['password']
		author.firstname = self.cleaned_data['firstname']
		author.lastname = self.cleaned_data['lastname']
		author.email = self.cleaned_data['email']
		return author

class TagForm(forms.Form):
	name = forms.CharField(max_length=200)

	helper = FormHelper()
	helper.form_method = 'POST'
	helper.form_class = 'form_horizontal'

	def __init__(self, *args, **kwargs):
		self.instance = kwargs.pop('instance', None)
		super(TagForm, self).__init__(*args, **kwargs)
		self.fields['name'].label = "Tag Name"

		if self.instance:
			self.fields['name'].initial = self.instance.name
			self.helper.layout = Layout(
				Field('name'),
				FormActions(Submit('add', 'Update', css_class='btn btn-primary'))
			)
		else :
			self.helper.layout = Layout(
				Field('name'),
				FormActions(Submit('add', 'Add', css_class='btn btn-primary'))
			)


	def save(self):
		tag = self.instance if self.instance else Tag()
		if self.instance :
			tag.name = self.cleaned_data['name']
			return tag
		else :
			try:
				cek = Tag.objects.get(name=self.cleaned_data['name'])
			except:
				tag.name = self.cleaned_data['name']
				return tag
			return None

class CategoryForm(forms.Form):
	name = forms.CharField(max_length=200)

	helper = FormHelper()
	helper.form_method = 'POST'
	helper.form_class = 'form_horizontal'

	def __init__(self, *args, **kwargs):
		self.instance = kwargs.pop('instance', None)
		super(CategoryForm, self).__init__(*args, **kwargs)
		self.fields['name'].label = "Category Name"

		if self.instance:
			self.fields['name'].initial = self.instance.name
			self.helper.layout = Layout(
				Field('name'),
				FormActions(Submit('add', 'Update', css_class='btn btn-primary'))
			)
		else :
			self.helper.layout = Layout(
				Field('name'),
				FormActions(Submit('add', 'Add', css_class='btn btn-primary'))
			)


	def save(self):
		cats = self.instance if self.instance else Category()
		if self.instance :
			cats.name = self.cleaned_data['name']
			return cats
		else :
			try:
				cek = Category.objects.get(name=self.cleaned_data['name'])
			except:
				cats.name = self.cleaned_data['name']
				return cats
			return None

class PostForm(forms.Form):
	title = forms.CharField(max_length=200)
	content = forms.CharField(widget=forms.widgets.Textarea())
	categories = forms.ChoiceField(widget=forms.widgets.Select(), required=False)
	tags = forms.MultipleChoiceField(widget=forms.widgets.CheckboxSelectMultiple(), required=False)
	is_published = forms.ChoiceField(widget=forms.widgets.Select(), required=False)

	helper = FormHelper()
	helper.form_method = 'POST'
	helper.form_class = 'form_horizontal'

	def __init__(self, *args, **kwargs):
		self.instance = kwargs.pop('instance', None)
		super(PostForm, self).__init__(*args, **kwargs)
		self.fields['tags'].choices = [(tag.id, tag.name) for tag in Tag.objects]
		self.fields['categories'].choices = [(cats.id, cats.name) for cats in Category.objects]
		self.fields['is_published'].choices = [('0', 'Draft'), ('1', 'Publish')]
		self.fields['is_published'].label = "Publish ?"

		if self.instance:
			self.fields['title'].initial = self.instance.title
			self.fields['content'].initial = self.instance.content
			self.fields['tags'].initial = [tag.id for tag in self.instance.tags]
			self.fields['categories'].initial = self.instance.categories.id
			self.fields['is_published'].initial = 1 if self.instance.is_published else 0
			self.helper.layout = Layout(
				Field('title'),
				Field('content'),
				Field('categories'),
				Field('tags', style="padding-left: 30px;"),
				Field('is_published'),
				FormActions(Submit('update', 'Update', css_class='btn btn-primary'))
			)
		else :
			self.helper.layout = Layout(
				Field('title'),
				Field('content'),
				Field('categories'),
				Field('tags', style="padding-left: 30px;"),
				Field('is_published'),
				FormActions(Submit('add', 'Add', css_class='btn btn-primary'))
			)

	def save(self):
		post = self.instance if self.instance else Post()
		post.title = self.cleaned_data['title']
		post.content = self.cleaned_data['content']
		post.categories = Category.objects(id=self.cleaned_data['categories'])[0]
		post.tags = Tag.objects(id__in=self.cleaned_data['tags'])
		post.is_published = True if self.cleaned_data['is_published'] == '1' else False
		return post