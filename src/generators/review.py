from src.review import Review
from src.generators.base import BaseGenerator

import re


class ReviewGenerator(BaseGenerator):

    def __init__(self, city_id, hotel_id):
        self.city_id = city_id
        self.hotel_id = hotel_id

    def __iter__(self):
        for review_id in self._review_id_generator(
                self.city_id, self.hotel_id):
            url = (
                "https://pl.tripadvisor.com/ShowUserReviews-"
                "g{}-d{}-r{}.html").format(
                    self.city_id, self.hotel_id, review_id)
            soup = self.get_soup(url)
            try:
                rating = soup.find("span", attrs={
                    "class": "ui_bubble_rating"}).get("class")[1]
                rating = re.search(r"bubble_(\d\d)", rating).group(1)
                author = soup.find("div", attrs={
                    "class": "info_text"}).find("div").text
                title = soup.find("h1", attrs={
                    "class": "title"}).text
                text = soup.find("span", attrs={
                    "class": "fullText"}).text
            except AttributeError:
                continue

            if text:
                print(url)
                yield Review(title, author, rating, text, url)
            else:
                print("Ommiting {} - "
                      "translation from another language".format(url))

    def _review_id_generator(self, city_id, hotel_id):
        gen = self._id_generators(
            ids=(city_id, hotel_id),
            pattern=r"^/ShowUserReviews-g{}-d{}-r([0-9]+).*\.html$".format(
                city_id, hotel_id),
            base_url="https://pl.tripadvisor.com/"
                     "Hotel_Review-g{}-d{}-Reviews-or{}",
            offset_step=5)

        for review_id in gen:
            yield review_id
