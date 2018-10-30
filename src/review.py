class Review(object):

    def __init__(self, title, author, rate, text, url):
        self.title = title
        self.author = author
        self.rate = rate
        self.text = text
        self.url = url

    def __hash__(self):
        return hash(self.url)

    def __eq__(self, other):
        if isinstance(other, Review):
            return self.url == other.url
        return False
