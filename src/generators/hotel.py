from src.generators.base import BaseGenerator


class HotelGenerator(BaseGenerator):

    def __init__(self, location_id):
        self.location_id = location_id

    def __iter__(self):

        for city_id in self._city_id_generator(self.location_id):
            for hotel_id in self._hotel_id_generator(city_id):
                yield city_id, hotel_id

    def _hotel_id_generator(self, city_id):

        gen = self._id_generators(
                ids=city_id,                                            # noqa
                pattern="^/Hotel_Review-g[0-9]+-d([0-9]+).*\.html$",    # noqa
                base_url="https://pl.tripadvisor.com/Hotels-g{}-oa{}",  # noqa
                offset_step=30)

        for hotel_id in gen:
            yield hotel_id

    def _city_id_generator(self, location_id):

        soup = self.get_soup(
                "https://pl.tripadvisor.com/Hotels-g{}".format(location_id))

        if not soup.find("div", attrs={"class": "leaf_geo_list_wrapper"}):
            print("Only id of continet or country is supported "
                  "(ie. Europe, Italy)")
            quit()

        gen = self._id_generators(
                ids=location_id,                                                # noqa
                pattern="^/Hotels-g([0-9]+)-(?!d[0-9]+).*\.html$",              # noqa
                base_url="https://pl.tripadvisor.com/Hotels-g{}-oa{}",          # noqa
                offset_step=20)

        for city_id in gen:
            if city_id != location_id:
                yield city_id
