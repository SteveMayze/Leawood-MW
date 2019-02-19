from django.test import TestCase

from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):

	def test_user_is_created(self):
		user = User(username="abc")
		self.assertEquals("abc", user.username)

		user.save()
		self.assertEquals('abc', User.objects.get(username="abc").username)


