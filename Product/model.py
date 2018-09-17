from google.appengine.ext import ndb


class Product(ndb.Model):
    sku = ndb.IntegerProperty(indexed=False)
    name = ndb.StringProperty(indexed=False)
    categoryPath = ndb.JsonProperty(indexed=False, repeated=True)
    prices = ndb.JsonProperty(indexed=False, repeated=True)
    lowest_price = ndb.JsonProperty(indexed=False)
    highest_price = ndb.JsonProperty(indexed=False)


