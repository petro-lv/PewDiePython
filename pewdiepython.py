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

        #Потрібно логінитись (юзернейм, пароль)
        # self.following = [i for i in instaloader.Profile.from_username(instance.context, self.username).get_followees()] #Cписок юзернеймів популярних людей

    #Аналіз фотографій користувача(не виникає помилок із відео та багатьма фотографіями)
    def analyze(self):

        trending_colors = []
        remote_image_features = ["color"]

        for i in range(3):
            remote_image_url = self.photos[i]
            detect_color_results_remote = computervision_client.analyze_image(remote_image_url, remote_image_features)
            trending_colors.append([detect_color_results_remote.color.dominant_color_foreground, f'{i+1} фотографія', remote_image_url])

        return trending_colors

    #Аналіз фотографій популярних людей, на яких підписаний користувач
    def analyze_top(self):

        top_trending_colors = []

        # for i in self.following:
        #     top = User(i)
        #     top_trending_colors.append(top.analyze_user())

        return top_trending_colors



























