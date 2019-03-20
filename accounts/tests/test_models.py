from django.test import TestCase

from django.contrib.auth import get_user_model
from accounts.models import Token
from django.db.utils import IntegrityError

User = get_user_model()


class UserModelTest(TestCase):

	def test_user_is_created(self):
		user = User(username="abc", email="ab@cd")
		self.assertEquals("abc", user.username)

		user.save()
		self.assertEquals('abc', User.objects.get(username="abc").username)


	def test_token_must_be_unique( self ):

		Token.objects.create(username="abc", uid="123")
		with self.assertRaises(IntegrityError):
			Token.objects.create(username="abc", uid="123")

