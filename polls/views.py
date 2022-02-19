from django.http import HttpResponse
from .models import Question
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from .serializers import RegisterSerializer

from rest_framework import status
from rest_framework import generics
from .serializers import ChangePasswordSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

#FOR RESET PASSWORD
# from django.dispatch import receiver
# from django_rest_passwordreset.signals import reset_password_token_created
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from vuedj.constants import site_url, site_full_name, site_shortcut_name
# from rest_framework.views import APIView
# from rest_framework import parsers, renderers, status
# from rest_framework.response import Response
# from .serializers import CustomTokenSerializer
# from django_rest_passwordreset.models import ResetPasswordToken
# from django_rest_passwordreset.views import get_password_reset_token_expiry_time
# from django.utils import timezone
# from datetime import timedelta 
#RESET PASS END

# Create your views here.
@api_view(['POST'])
def login_api(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user  = serializer.validated_data['user']
    _, token = AuthToken.objects.create(user)
    print('geetting req',request)
    return Response({
        'user_info': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password': user.password
        },
        'token': token
    })

@api_view(['GET'])
def get_user_data(request):
    user=request.user

    if user.is_authenticated:
        return Response({
            'user_info': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password': user.password,
            },
        })
    return Response({'error': 'not authenticated'}, status=400)


@api_view(['POST'])
def register_api(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        _, token = AuthToken.objects.create(user)

        return Response({
            'user_info': {
                'id': user.id,
                'username': user.username,
                'email': user.email
                },
                'token': token
            })
    
from rest_framework.views import APIView
class index(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
        output = ', '.join([q.question_text for q in latest_question_list])
        return HttpResponse(output)

def detail(request, question_id):
    return HttpResponse("You are looking at question %s." %question_id)

def results(request, question_id):
    response = "You are looking at result of the question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You are voting on question %s." % question_id)

def age(request, my_age):
    return HttpResponse("Shobhit Ranjan age is %s. " % my_age)



class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''class CustomPasswordResetView:
    @receiver(reset_password_token_created)
    def password_reset_token_created(sender, reset_password_token, *args, **kwargs):
        """
          Handles password reset tokens
          When a token is created, an e-mail needs to be sent to the user
        """
        # send an e-mail to the user
        context = {
            'current_user': reset_password_token.user,
            'username': reset_password_token.user.username,
            'email': reset_password_token.user.email,
            'reset_password_url': "{}/password-reset/{}".format(site_url, reset_password_token.key),
            'site_name': site_shortcut_name,
            'site_domain': site_url
        }

        # render email text
        email_html_message = render_to_string('email/user_reset_password.html', context)
        email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

        msg = EmailMultiAlternatives(
            # title:
            "Password Reset for {}".format(site_full_name),
            # message:
            email_plaintext_message,
            # from:
            "noreply@{}".format(site_url),
            # to:
            [reset_password_token.user.email]
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()


class CustomPasswordTokenVerificationView(APIView):
    """
      An Api View which provides a method to verifiy that a given pw-reset token is valid before actually confirming the
      reset.
    """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = CustomTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']

        # get token validation time
        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        # find token
        reset_password_token = ResetPasswordToken.objects.filter(key=token).first()

        if reset_password_token is None:
            return Response({'status': 'invalid'}, status=status.HTTP_404_NOT_FOUND)

        # check expiry date
        expiry_date = reset_password_token.created_at + timedelta(hours=password_reset_token_validation_time)

        if timezone.now() > expiry_date:
            # delete expired token
            reset_password_token.delete()
            return Response({'status': 'expired'}, status=status.HTTP_404_NOT_FOUND)

        # check if user has password to change
        if not reset_password_token.user.has_usable_password():
            return Response({'status': 'irrelevant'})

        return Response({'status': 'OK'})'''