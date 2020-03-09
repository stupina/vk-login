import json
import os

from flask import redirect, request, url_for
from rauth import OAuth2Service


ID = os.getenv('ID')
SECRET = os.getenv('SECRET')


class VkSignIn(object):

    def __init__(self):
        self.client_id = ID
        self.consumer_secret = SECRET
        self.service = OAuth2Service(
            name='vk',
            client_id=self.client_id,
            client_secret=self.consumer_secret,
            authorize_url='https://oauth.vk.com/authorize',
            access_token_url='https://oauth.vk.com/access_token',
            base_url='https://api.vk.com/method/friends.get'
        )

    def authorize(self):
        url = self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url(),
        )
        return redirect(url)

    def callback(self):
        def decode_json(payload):
            return json.loads(payload.decode('utf-8'))

        if 'code' not in request.args:
            return None, None, None

        data = {
            'code': request.args['code'],
            'client_id': self.client_id,
            'client_secret': self.consumer_secret,
            'redirect_uri': self.get_callback_url()
        }
        oauth_session = self.service.get_auth_session(
            data=data,
            decoder=decode_json,
        )
        params = oauth_session.access_token_response.json()
        uid = params.get('user_id')
        email = params.get('email')
        token = params.get('access_token')
        version = '5.103'
        data = '?user_id={}&access_token={}&fields={}&v={}'.format(
            uid,
            token,
            'nickname',
            version,
        )
        url = self.service.base_url + data
        result = oauth_session.get(url=url).json()
        response = result.get('response')
        friends_count = response.get('count')
        return (uid, email, friends_count)

    def get_callback_url(self):
        result = url_for(
            'callback',
            _external=True,
        )
        return result
