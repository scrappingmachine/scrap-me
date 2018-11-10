import pytest

from src.review import Review
from src.generators.review import ReviewGenerator


reviews = [
    ("pl", 274808, 624801, 630953010),
    ("pl", 274808, 624801, 629557445),
    ("pl", 274808, 624801, 629278094),
    ("pl", 274772, 7932764, 632126490),
    ("pl", 274772, 7932764, 629561203),
    ("pl", 274772, 7932764, 624959031),
    ("eng", 187792, 230612, 599309623),
    ("eng", 187791, 230612, 603150737),
    ("eng", 187791, 205044, 629973241),
    ("eng", 34438, 8788134, 614364820),
    ("eng", 642170, 1174439, 630995025)]

domains = {
    "pl": "https://pl.tripadvisor.com",
    "eng": "https://www.tripadvisor.com"}


@pytest.mark.parametrize("language, city_id, hotel_id, review_id", reviews)
def test_review_scrapping(language, city_id, hotel_id, review_id):

    for domain, url in domains.items():
        review_gen = ReviewGenerator(city_id, hotel_id, domains[domain])
        review = review_gen.scrap_review(city_id, hotel_id, review_id)

        if domain == language:
            assert isinstance(review, Review)
        else:
            assert review is None
