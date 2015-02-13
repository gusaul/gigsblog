from apps.blog.models import User
def login_check(username,password):
	try:
		user = User.objects.get(username=username, password=password)
	except User.DoesNotExist:
		user = None
	return user