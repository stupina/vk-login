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
            base_url='https://api.vk.com/method/'
        )
        self.oauth_session = None

    def authorize(self):
        url = self.service.get_authorize_url(
            scope='friends',
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
        token = params.get('access_token')
        version = '5.103'
        photo_name = 'photo_200_orig'
        user_data = 'users.get?user_ids={}&fields={}&access_token={}&v={}'.format(
            uid,
            photo_name,
            token,
            version,
        )
        url = self.service.base_url + user_data
        result = oauth_session.get(url=url).json()
        response = result.get('response')[0]
        image_url = response.get(photo_name)
        name = response.get('first_name')
        friends_data = 'friends.get?user_id={}&count={}&access_token={}&fields={}&v={}'.format(
            uid,
            5,
            token,
            'nickname',
            version,
        )
        url = self.service.base_url + friends_data
        result = oauth_session.get(url=url).json()
        response = result.get('response')
        friends = response.get('items')
        return (uid, name, image_url, friends)

    def get_callback_url(self):
        result = url_for(
            'callback',
            _external=True,
        )
        return result
