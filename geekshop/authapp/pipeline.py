from datetime import datetime
from authapp.models import ShopUserProfile
import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden



def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'facebook':
        return
    resp = requests.get(
        f"https://graph.facebook.com/{response['id']}?fields=gender,birthday&access_token={response['access_token']}"
    )
    data = resp.json()
    user.shopuserprofile.gender = ShopUserProfile.MALE if data["gender"] == "male" else ShopUserProfile.FEMALE
    bdate = datetime.strptime(data["birthday"], '%m/%d/%Y').date()
    age = timezone.now().date().year - bdate.year
    if age < 18:
        user.delete()
        raise AuthForbidden("social_core.backends.facebook.FacebookOAuth2")
    user.age = age
    user.save()
