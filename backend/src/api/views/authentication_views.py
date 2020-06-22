import random
import string, re
import requests as core_requests

from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from decouple import config
import jwt
import datetime
from django.utils import timezone
import logging
from json import JSONDecodeError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken

from api import models, serializers
from api import permissions

from google.oauth2 import id_token
from google.auth.transport import requests

logger = logging.getLogger(__name__)

# Create your views here.
class HelloApiView(APIView):
	"""Test API View"""

	def get(self, request, *args, **kwargr):
		"""Returns a list of APIView features"""

		an_apiview = [
			'Uses HTTP methods as function (get, post, patch, put, delete',
			'Some other features'
		]

		return Response({"message": "Hello World!", 'an_apiview':an_apiview})

class ActivateAccountView(APIView):
	"""Account activation view"""

	def get(self, request, *args, **kwargr):
		token = kwargr.get("token",None)
		if token is not None:
			try:
				decoded = jwt.decode(token.encode(), config('EMAIL_VERIFICATION_SECRET'), leeway=10, algorithms=['HS256'])
				encoded_jwt = jwt.encode(
					{
						'email': decoded.get('email'),
						'name' : decoded.get('name'),
						'exp': timezone.now() + datetime.timedelta(minutes=3000)
					}, 
					config('EMAIL_VERIFICATION_SECRET'), 
					algorithm='HS256'
				)
				return Response({ 
							"message": "Email verification completed set password to complete registration",
							'token': encoded_jwt.decode()
						})
			except jwt.ExpiredSignatureError:
				return Response({"error":"Link expired"},
					status=status.HTTP_406_NOT_ACCEPTABLE)
			except Exception as e:
				logger.exception("Token exception : %s",e)
				return Response({"error":"Link Broken. Please try again"},
					status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({"error": "Token not found"},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
	
	def post(self, request, *args, **kwargr):
		token = kwargr.get("token",None)
		if token is not None:	
			try:
				logger.info(token)
				decoded = jwt.decode(token.encode(), config('EMAIL_VERIFICATION_SECRET'), leeway=10, algorithms=['HS256'])
				user = models.User(
					email = decoded['email'],
					name = decoded['name']
				)

				if request.data.get("password") ==None:
					return Response({"error":"Password not found in request"},
					status=status.HTTP_400_BAD_REQUEST)

				serializer = serializers.UserProfileSerializer(data={
					"email" : decoded['email'],
					"name" : decoded['name'],
					"password": request.data.get("password")
				})

				if serializer.is_valid():
					user = serializer.save()
					return Response(serializer.data)
				else:
					return Response(
						serializer.errors,
						status=status.HTTP_400_BAD_REQUEST
					)

			except jwt.ExpiredSignatureError:
				return Response({"error":"Request timeout. Please start over"},
					status=status.HTTP_408_REQUEST_TIMEOUT)
			except (jwt.exceptions.DecodeError, JSONDecodeError, ValueError) as e:
				logger.exception("Token value error exception. Token : %s",e)
				return Response({"error":"Invalid token"},
					status=status.HTTP_400_BAD_REQUEST)
			except Exception as e:
				logger.exception("Token exception : %s",e)
				return Response({"error":"Some error occured please try again"},
					status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({"error": "Token not found"},status=status.HTTP_422_UNPROCESSABLE_ENTITY)	

@api_view(["POST",])
def post_email_for_reset_password(request, *args, **kwargr):
	email = request.data.get("email",None)
	if email and re.match(r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$",email):
		if not get_user_model().objects.filter(email=email).exists():
				return Response({'email':["User with this email does not exists."]}, 
								status=status.HTTP_400_BAD_REQUEST)
		encoded_jwt = jwt.encode(
			{
				'email': email,
				'exp': timezone.now() + datetime.timedelta(minutes=3000)
			}, 
			config('PASSWORD_RESET_SECRET'), 
			algorithm='HS256'
		)

			# send email logic

		mail_subject = 'Activate your account.'
		message = render_to_string('pw_reset_email.html', {
			'frontend_url': config("FRONTEND_URL"),
			'token': encoded_jwt.decode()
		})
		email = EmailMessage(
			mail_subject, message,"no-reply@localhost.com", to=[email]
		)
		email.content_subtype = "html"
		try:
			email.send()
		except Exception as e:
			logger.exception("Password reset email sending error : %s",e)
			return Response({"error":"Email coudn't be sent please try again"},
				status=status.HTTP_406_NOT_ACCEPTABLE)

		return Response({"message":"Please click on the link sent to your email to reset password"})	
	else:
		return Response({"error":"Please enter a valid email"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST",])
def reset_password(request, *args, **kwargr):
	token = kwargr.get("token",None)
	password = request.data.get("password",None)
	# import pdb; pdb.set_trace()
	print("Token:  ", token)
	if token is not None:
		if password:
			try:
				validate_password(password)
			except ValidationError as e:
				return Response({"errors": e.error_list}, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({"errors": "Please enter a password"}, status=status.HTTP_400_BAD_REQUEST)
		try:
			decoded = jwt.decode(token.encode(), config('PASSWORD_RESET_SECRET'), leeway=10, algorithms=['HS256'])
			user = get_user_model().objects.get(email = decoded["email"])
			
			user.set_password(password)
			user.save()

			return Response({ 
						"message": "Password reset successful loging with new password",
					})
		except jwt.ExpiredSignatureError:
			return Response({"error":"Link expired"},
				status=status.HTTP_406_NOT_ACCEPTABLE)
		except Exception as e:
			logger.exception("Token exception : %s",e)
			return Response({"error":"Link Broken. Please try again"},
				status=status.HTTP_400_BAD_REQUEST)
	else:
		return Response({"error": "Token not found"},status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class UserProfileViewSet(viewsets.ModelViewSet):
	"""Handle creating and updating user profiles."""

	serializer_class = serializers.UserProfileSerializer 
	queryset = models.User.objects.all()
	# default authentication class is mentioned in settings.py file
	authentication_classes = (JWTAuthentication,)
	permission_classes = (permissions.UpdateOwnProfile,)

	def list(self, request):
		return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
	
	def create(self, request):
		"""Create a new hello message"""
		# logger.info("New user creation request for %s",request.data.get("name"))

		try:
			serializer = serializers.SignUpSerializer(data=request.data)

			if serializer.is_valid():
				if get_user_model().objects.filter(email=serializer.validated_data.get('email')).exists():
					return Response({'email':["user with this email already exists."]}, 
									status=status.HTTP_400_BAD_REQUEST)
				
				encoded_jwt = jwt.encode(
						{
							'email': serializer.validated_data.get('email'),
							'name' : serializer.validated_data.get('name'),
							'exp': timezone.now() + datetime.timedelta(minutes=3000)
						}, 
						config('EMAIL_VERIFICATION_SECRET'), 
						algorithm='HS256'
					)

				# send email logic

				mail_subject = 'Activate your account.'
				message = render_to_string('acc_active_email.html', {
					'frontend_url': config("FRONTEND_URL"),
					'token': encoded_jwt.decode()
				})
				email = EmailMessage(
					mail_subject, message,"no-reply@localhost.com", to=[serializer.validated_data.get('email')]
				)
				email.content_subtype = "html"
				try:
					email.send()
				except Exception as e:
					logger.exception("Signup email verify error : %s",e)
					return Response({"error":"Email coudn't be sent please try again"},
						status=status.HTTP_406_NOT_ACCEPTABLE)

				return Response({"message":"Please click on the link sent to your email to complete the registration"})
			else:
				return Response(
					serializer.errors,
					status=status.HTTP_400_BAD_REQUEST
				)
		except ConnectionAbortedError as e:
			logger.exception("Email Exception exception : %s",e)
			return Response({"error":"Server error on sending email"},
				status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			logger.exception(str(e))
			return Response({"error":"Server error on sending email"},
				status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST",])
def Signin(request):
	try:
		user = authenticate(username=request.data.get("email"), password=request.data.get("password"))
		if user is not None:
			tokenObtainPairObj = TokenObtainPairSerializer()
			data_access_refresh_token_dict = tokenObtainPairObj.validate(request.data)
			data_access_refresh_token_dict.update({"user":serializers.UserProfileSerializer(user).data})
			return Response(data_access_refresh_token_dict)
		else:
			return Response({"error": "Authentication Failure"}, 
					status= status.HTTP_401_UNAUTHORIZED)
	except Exception as e:
		logger.exception("Token exception : %s",e)
		return Response({"error":"Internal Server Error. We are extreamly sorry for the inconvenience. We will be back soon."},
			status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST","GET"])
def Google_Login(request):
	try:
		User = get_user_model()
		idinfo = id_token.verify_oauth2_token(request.data.get("token"), requests.Request(), config("GOOGLE_CLIENT_ID"))
		"""
		JSON Response
		{"iss": "accounts.google.com", "azp": "834282223486-gktfpdnk6taup9ureq3rsh3jk86gbeed.apps.googleusercontent.com",
		 "aud": "834282223486-gktfpdnk6taup9ureq3rsh3jk86gbeed.apps.googleusercontent.com", 
		 "sub": "111898867240311214691", "email": "nirupamdebnath4@gmail.com", "email_verified": true, 
		 "at_hash": "w86x9APgkBzhaRvT0LCSeA", "name": "nirupam debnath", 
		 "picture": "https://lh3.googleusercontent.com/a-/AOh14GhTvRSiPJSq_McvITrnhFll9SNDL_T2EvIICUAZWw=s96-c", 
		 "given_name": "nirupam", "family_name": "debnath", "locale": "en", "iat": 1588447339, 
		 "exp": 1588450939, "jti": "80b33121e879004b17180aeb333576947df644fc"}
		 """
		try:
			user = User.objects.get(email=idinfo.get("email"))
			serializer = serializers.UserProfileSerializer(user)
		except User.DoesNotExist as e:
			serializer = serializers.UserProfileSerializer(data={
					"email" :idinfo.get('email'),
					"name" : idinfo.get('name'),
					"password": ''.join(random.choices(string.ascii_uppercase +
								string.digits, k = 15))
				})

			if serializer.is_valid():
				user = serializer.save()
			else:
				return Response(
					serializer.errors,
					status=status.HTTP_400_BAD_REQUEST
				)

		refresh = RefreshToken.for_user(user)

		return Response({
			'refresh': str(refresh),
			'access': str(refresh.access_token),
			"user":serializer.data
		})


	except Exception as e:
		logger.exception("Google Login Exception : %s",e)
		return Response({"error":"Google Token error please try again!"},
			status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST","GET"])
def Facebook_Login(request):
	try:
		User = get_user_model()
		# PARAMS = {'address':location} 
		userID = request.data.get("userID")
		accessToken = request.data.get("accessToken")
		# sending get request and saving the response as response object 
		# import pdb; pdb.set_trace()
		URL = "https://graph.facebook.com/v2.11/{userID}/?fields=id,name,email&access_token={accessToken}".format(
			userID = userID, accessToken = accessToken
		)
		r = core_requests.get(url = URL) 
		
		# extracting data in json format 
		data = r.json()

		try:
			user = User.objects.get(email=data.get("email"))
			serializer = serializers.UserProfileSerializer(user)
		except User.DoesNotExist as e:
			serializer = serializers.UserProfileSerializer(data={
					"email" :data.get('email'),
					"name" : data.get('name'),
					"password": ''.join(random.choices(string.ascii_uppercase +
								string.digits, k = 15))
				})

			if serializer.is_valid():
				user = serializer.save()
			else:
				return Response(
					serializer.errors,
					status=status.HTTP_400_BAD_REQUEST
				)

		refresh = RefreshToken.for_user(user)

		return Response({
			'refresh': str(refresh),
			'access': str(refresh.access_token),
			"user":serializer.data
		})


	except Exception as e:
		logger.exception("Google Login Exception : %s",e)
		return Response({"error":"Google Token error please try again!"},
			status=status.HTTP_400_BAD_REQUEST)