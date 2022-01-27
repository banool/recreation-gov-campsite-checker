import pytwitter
from pytwitter import Api
api = Api(
  consumer_key="gvqGNz7dQfUKI3o70LuoG5L19",
  consumer_secret="M9IRpqvlLqf5IVNdj6gBN0JzVvEJIm38B1CyQixtz6QTlGSLNA",
  access_token="1486580434527928321-HhUhuy8azD8nucvkKhWS2OZ43PfdLH",
  access_secret="YL0Iiy0fyzuZTbG9QQvm3MgoI5cfQ9yOHeVDrmc9qkr9Q"
)

print(api.get_users(usernames="Twitter,TwitterDev"))
api.create_tweet(text="Hello world!2")
