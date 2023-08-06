# -*- coding: utf-8 -*-
"""
Authentication backend for handling firebase user.idToken from incoming
Authorization header, verifying, and locally authenticating
"""
import json
import uuid
import firebase_admin

from firebase_admin import auth

from django.conf import settings
from django.utils.encoding import smart_text
from django.utils import timezone

from rest_framework import HTTP_HEADER_ENCODING, exceptions

settings_auth = settings.AUTHENTICATION
firebase_credentials = firebase_admin.credentials.Certificate(
    settings_auth["FIREBASE_SERVICE_ACCOUNT_KEY"]
)
firebase = firebase_admin.initialize_app(firebase_credentials)


class TonicAuthentication():
    www_authenticate_realm = 'api'

    def get_authorization_header(self, request):
        """
        Return request's 'Authorization:' header, as a bytestring.

        Hide some test client ickyness where the header can be unicode.
        """
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        if isinstance(auth, str):
            # Work around django test client oddness
            auth = auth.encode(HTTP_HEADER_ENCODING)
        return auth

    def authenticate(self, request):
        """
        With ALLOW_ANONYMOUS_REQUESTS, set request.user to an AnonymousUser,
        allowing us to configure access at the permissions level.
        """
        authorization_header = self.get_authorization_header(request)
        if settings_auth["ALLOW_ANONYMOUS_REQUESTS"] and not authorization_header:
            return (None, None)
        """
        Returns a tuple of len(2) of `User` and the decoded firebase token if
        a valid signature has been supplied using Firebase authentication.
        """

        firebase_token = self.get_token(request)

        decoded_token = self.decode_token(firebase_token)

        return (decoded_token, None)

    def get_token(self, request):
        """
        Parse Authorization header and retrieve JWT
        """
        authorization_header = self.get_authorization_header(request).split()
        auth_header_prefix = \
            settings_auth["FIREBASE_AUTH_HEADER_PREFIX"].lower()

        if not authorization_header or len(authorization_header) != 2:
            raise exceptions.AuthenticationFailed(
                'Invalid Authorization header format, expecting: JWT <token>.'
            )

        if smart_text(authorization_header[0].lower()) != auth_header_prefix:
            raise exceptions.AuthenticationFailed(
                'Invalid Authorization header prefix, expecting: JWT.'
            )

        return authorization_header[1]

    def decode_token(self, firebase_token):
        """
        Attempt to verify JWT from Authorization header with Firebase and
        return the decoded token
        """
        try:
            return auth.verify_id_token(
                firebase_token,
                check_revoked=settings_auth["FIREBASE_CHECK_JWT_REVOKED"]
            )
        except ValueError as exc:
            raise exceptions.AuthenticationFailed(
                'JWT was found to be invalid, or the App’s project ID cannot '
                'be determined.'
            )
        except (auth.InvalidIdTokenError,
                auth.ExpiredIdTokenError,
                auth.RevokedIdTokenError,
                auth.CertificateFetchError) as exc:
            if exc.code == 'ID_TOKEN_REVOKED':
                raise exceptions.AuthenticationFailed(
                    'Token revoked, inform the user to reauthenticate or '
                    'signOut().'
                )
            else:
                raise exceptions.AuthenticationFailed('Token is invalid.')
