from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.blog.models import *

class LoggedInMixin(object):

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(LoggedInMixin, self).dispatch(*args, **kwargs)

class Sidebar(object):

  def get_context_data(self,**kwargs):
    context = super(Sidebar, self).get_context_data(**kwargs)
    context['categories'] = Category.objects
    context['tags'] = Tag.objects
    return context

class SendRequest(object):

	def get_context_data(self,**kwargs):
		context = super(SendRequest, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context