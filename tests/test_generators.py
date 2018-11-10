import itertools
import pytest
import requests

from src.generators.hotel import HotelGenerator
from src.generators.review import ReviewGenerator


@pytest.fixture(scope="module")
def city_ids():
    hotel_gen = HotelGenerator(4)._city_id_generator(4)
    result = []
    for i in range(5):
        result.append(next(hotel_gen))

    return result


@pytest.fixture(scope="module")
def hotel_ids(city_ids):
    result = []
    for city in city_ids:
        hotel_gen = HotelGenerator(4)._hotel_id_generator(city)
        for i in range(5):
            result.append((city, next(hotel_gen)))

    return result


@pytest.fixture(scope="module")
def review_ids(hotel_ids):
    result = []
    for city, hotel in hotel_ids:
        review_gen = ReviewGenerator(city, hotel)._review_id_generator(
            city, hotel)
        for review in itertools.islice(review_gen, 5):
            result.append((city, hotel, review))

    return result


def test_city_id_gen(city_ids):
    for city in city_ids:
        base_url = r"https://pl.tripadvisor.com/Hotels-g{}".format(city)
        request = requests.get(base_url)
        assert(request.status_code == 200)


def test_hotel_id_gen(hotel_ids):
    for city, hotel in hotel_ids:
        base_url = r"https://pl.tripadvisor.com/Hotel_Review-g{}-d{}".format(
            city, hotel)
        request = requests.get(base_url)
        assert(request.status_code == 200)


def test_review_id_get(review_ids):
    for city, hotel, review in review_ids:
        base_url = (
            "https://pl.tripadvisor.com/ShowUserReviews-"
            "g{}-d{}-r{}.html").format(city, hotel, review)
        request = requests.get(base_url)
        assert(request.status_code == 200)
