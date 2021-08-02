import redis
from django.conf import settings
from .models import Product

# connect to redis
r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


class Recommender:

    def get_product_key(self, id):
        return f'product:{id}:purchased_with'

    def products_bought(self, products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                # get the other products bought with each product
                if product_id != with_id:
                    # increment score for product purchased together
                    r.zincrby(self.get_product_key(product_id), 1, with_id)
                    # zincrby(name, amount, value): Increment the score of value in sorted set name by amount

    def suggest_products_for(self, products, max_results=6):
        product_ids = [p.id for p in products]
        if len(products) == 1:
            # only 1 product
            suggestions = r.zrange(self.get_product_key(product_ids[0]), 0, -1, desc=True)[:max_results]
            print('suggestions:len=1:', suggestions)
            print('Type:', type(suggestions))
            # zrange(name, start, end, desc=False, withscores=False, score_cast_func=<type 'float'>)
            # Return a range of values from sorted set name between start and end sorted in ascending order.
            # https://redis-py.readthedocs.io/en/stable/
        else:
            # generate a temporary key
            flat_ids = ''.join([str(id) for id in product_ids])
            print('flat IDs:', flat_ids)
            tmp_key = f'tmp_{flat_ids}'
            print('tmp_key:', tmp_key)
            # multiple products, combine scores of all products
            # store the resulting sorted set in a temporary key
            keys = [self.get_product_key(id) for id in product_ids]
            print('keys:', keys)
            print('zunionstore:', r.zunionstore(tmp_key, keys))
            # remove ids for the products the recommendation is for
            r.zrem(tmp_key, *product_ids)
            # get the product ids by their score, descendant sort
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            print('suggestions:len>1:', suggestions)
            # remove the temporary key
            r.delete(tmp_key)
        suggested_products_ids = [int(id) for id in suggestions]
        # get suggested products and sort by order of appearance
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        print('suggested products:', suggested_products)
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))
