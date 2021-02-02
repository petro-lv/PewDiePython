import os
import instaloader

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

subscription_key = os.getenv('COMPUTERVISION_KEY')
endpoint = os.getenv('COMPUTERVISION_ENDPOINT')

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))


class User:

    def __init__(self, username):

        instance = instaloader.Instaloader()

        self.username = username

        posts = instaloader.Profile.from_username(instance.context, self.username).get_posts()

        self.photos = [i.url for i in posts] #Список посилань на фотографії



    #Аналіз фотографій користувача(не виникає помилок із відео та багатьма фотографіями)
    def analyze(self):

        trending_colors = []
        remote_image_features = ["color"]

        for i in range(3):
            remote_image_url = self.photos[i]
            detect_color_results_remote = computervision_client.analyze_image(remote_image_url, remote_image_features)
            trending_colors.append(Result(detect_color_results_remote.color.dominant_color_foreground, remote_image_url))

        return trending_colors


class User_logged(User):

    def __init__(self, username, password):

        instance = instaloader.Instaloader()

        instance.login(username, password)

        super().__init__(username)

        self.password = password

        self.following = [i.username for i in instaloader.Profile.from_username(instance.context, self.username).get_followees()]

    #Аналіз фотографій популярних людей, на яких підписаний користувач
    def analyze_top(self):

        top_trending_colors = []

        for i in range(3):
            top = User(self.following[i])
            top_trending_colors.append(top.analyze())

        return top_trending_colors


class Result:
    def __init__(self, color, url):
        self.url = url
        self.color = color































