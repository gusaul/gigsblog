from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.views.generic import ListView, TemplateView, DetailView, View, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from apps.blog.forms import *
from apps.blog.models import *
from mongoengine.queryset import DoesNotExist
from mongoengine.django.auth import MongoEngineBackend
from lib.mixin import *
import lib
# Create your views here.

class Index(Sidebar, TemplateView):
  template_name = 'index.html'

  def get_context_data(self,**kwargs):
    context = super(Index, self).get_context_data(**kwargs)
    # context['form'] = LoginForm
    context['posts'] = Post.objects.filter(is_published=True)
    return context

class CatDetail(Sidebar, TemplateView):
  template_name = 'index.html'

  def get_context_data(self, **kwargs):
    context = super(CatDetail, self).get_context_data(**kwargs)
    category = Category.objects.get(name=self.kwargs['catname'])
    context['posts'] = Post.objects.filter(is_published=True, categories=category)
    return context

class TagDetail(Sidebar, TemplateView):
  template_name = 'index.html'

  def get_context_data(self, **kwargs):
    context = super(TagDetail, self).get_context_data(**kwargs)
    tag = Tag.objects.get(name=self.kwargs['tagname'])
    context['posts'] = Post.objects.filter(is_published=True, tags=tag)
    return context

class Login(FormView):
  template_name = 'login.html'
  form_class = LoginForm

  # def get_context_data(self, **kwargs):
  #   context = super(Login, self).get_context_data(**kwargs)
  #   context['signup'] = SignUpForm
  #   return context

  def form_valid(self, form):
    if self.request.method == 'POST':
      user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
      if user is not None:
        login(self.request, user)
        message = 'Logged in as %s' % user.username
      else:
        message = "Error"

    messages.success(self.request, message)

    return super(Login, self).form_valid(form)

  def get_success_url(self):
    if self.request.GET.get('next','/') != '/':
      return self.request.GET.get('next','/')
    else :
      return reverse('admin')

  def get_context_data(self, **kwargs):
    context = super(Login, self).get_context_data(**kwargs)
    return context

class SignUp(CreateView):
  model = Author
  form_class = SignUpForm
  template_name = 'signup.html'

  def form_valid(self, form):
    author = form.save()
    author.set_password(author.password)

    messages.success(self.request, "Pendaftaran Berhasil")
    return super(SignUp, self).form_valid(form)

  def get_success_url(self):
    return reverse('signUp')


class PostDetail(Sidebar, DetailView):
  model = Post
  context_object_name = "post"

  def get_template_names(self):
      return ["detail.html"]

  def get_context_data(self, **kwargs):
    context = super(PostDetail, self).get_context_data(**kwargs)
    return context

  def get_object(self):
      return Post.objects.get(id=self.kwargs['pk'], slug=self.kwargs['slug'])

class AddPost(LoggedInMixin, SendRequest, CreateView):
  model = Post
  form_class = PostForm
  template_name = 'admin/add_post.html'

  def get_success_url(self):
    return reverse('admin')

  def form_valid(self, form):
    self.object = form.save()
    self.object.user = Author.objects.get(pk=self.request.user.id)
    self.object.save()
    messages.success(self.request, "Post Created")
    return super(AddPost, self).form_valid(form)

class UpdatePost(LoggedInMixin, SendRequest, UpdateView):
  model = Post
  form_class = PostForm
  template_name = 'admin/add_post.html'

  def get_success_url(self):
    return reverse('admin')

  def form_valid(self, form):
    self.object = form.save()
    self.object.save()
    messages.success(self.request, "Post Updated.")
    return super(UpdatePost, self).form_valid(form)

  def get_object(self):
    return Post.objects.get(id=self.kwargs['pk'])

class DeletePost(LoggedInMixin, DeleteView):
  model = Post

  def get_succes_url(self):
    return reverse('admin')
    
  def delete(self, request, *args, **kwargs):
    self.object = Post.objects.get(id=self.kwargs['pk'])
    self.object.delete()
    messages.success(self.request, "Post Removed.")
    return redirect(self.get_succes_url())

  def get(self, *args, **kwargs):
    return self.delete(self.request, *args, **kwargs)

class AdminPostList(LoggedInMixin, SendRequest, ListView):
  model = Post
  template_name = 'admin/index.html'
  context_object_name = 'postlist'

  def get_queryset(self):
    active_user = Author.objects.get(pk=self.request.user.id)
    return Post.objects.filter(user=active_user)


class TagView(LoggedInMixin, SendRequest, CreateView):
  model = Tag
  form_class = TagForm
  template_name = 'admin/tag.html'

  def get_success_url(self):
    return reverse('tag')

  def get_context_data(self, **kwargs):
    active_user = Author.objects.get(pk=self.request.user.id)
    kwargs['taglist'] = self.model.objects.filter(user=active_user)
    return super(TagView, self).get_context_data(**kwargs)

  def form_valid(self, form):
    self.object = form.save()
    if self.object is not None :
      self.object.user = Author.objects.get(pk=self.request.user.id)
      self.object.save()
      messages.success(self.request, "Tag Added.")
    else :
      messages.error(self.request, "Failed Add Tag. Maybe Name Existed", extra_tags='danger')
    return super(TagView, self).form_valid(form)

class UpdateTag(LoggedInMixin, SendRequest, UpdateView):
  model = Tag
  form_class = TagForm
  template_name = 'admin/tag.html'

  def get_success_url(self):
    return reverse('tag')

  def get_context_data(self, **kwargs):
    active_user = Author.objects.get(pk=self.request.user.id)
    kwargs['taglist'] = self.model.objects.filter(user=active_user)
    return super(UpdateTag, self).get_context_data(**kwargs)

  def form_valid(self, form):
    self.object = form.save()
    self.object.save()
    messages.success(self.request, "Tag Updated.")
    return super(UpdateTag, self).form_valid(form)

  def get_object(self):
    return Tag.objects.get(id=self.kwargs['pk'])

class DeleteTag(LoggedInMixin, DeleteView):
  model = Tag

  def get_succes_url(self):
    return reverse('tag')

  def get_object(self):
    return Tag.objects.get(id=self.kwargs['pk'])

  def delete(self, request, *args, **kwargs):
    self.object = self.get_object()
    self.object.delete()
    messages.success(self.request, "Tag Removed.")
    return redirect(self.get_succes_url())

  def get(self, *args, **kwargs):
    return self.delete(self.request, *args, **kwargs)

class CategoryView(LoggedInMixin, SendRequest, CreateView):
  model = Category
  form_class = CategoryForm
  template_name = 'admin/category.html'

  def get_success_url(self):
    return reverse('category')

  def get_context_data(self, **kwargs):
    active_user = Author.objects.get(pk=self.request.user.id)
    kwargs['catslist'] = self.model.objects.filter(user=active_user)
    return super(CategoryView, self).get_context_data(**kwargs)

  def form_valid(self, form):
    self.object = form.save()
    if self.object is not None :
      self.object.user = Author.objects.get(pk=self.request.user.id)
      self.object.save()
      messages.success(self.request, "Category Added.")
    else :
      messages.error(self.request, "Failed Add Category. Maybe Name Existed", extra_tags='danger')
    return super(CategoryView, self).form_valid(form)

class UpdateCategory(LoggedInMixin, SendRequest, UpdateView):
  model = Category
  form_class = CategoryForm
  template_name = 'admin/category.html'

  def get_success_url(self):
    return reverse('category')

  def get_context_data(self, **kwargs):
    active_user = Author.objects.get(pk=self.request.user.id)
    kwargs['catslist'] = self.model.objects.filter(user=active_user)
    return super(UpdateCategory, self).get_context_data(**kwargs)

  def form_valid(self, form):
    self.object = form.save()
    self.object.save()
    messages.success(self.request, "Category Updated.")
    return super(UpdateCategory, self).form_valid(form)

  def get_object(self):
    return Category.objects.get(id=self.kwargs['pk'])

class DeleteCategory(LoggedInMixin, DeleteView):
  model = Category

  def get_succes_url(self):
    return reverse('category')

  def get_object(self):
    return Category.objects.get(id=self.kwargs['pk'])

  def delete(self, request, *args, **kwargs):
    self.object = self.get_object()
    self.object.delete()
    messages.success(self.request, "Category Removed.")
    return redirect(self.get_succes_url())

  def get(self, *args, **kwargs):
    return self.delete(self.request, *args, **kwargs)