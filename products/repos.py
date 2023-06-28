from . import models


class ProductRepos:
    model = models.Product

    def get_product(self, product_id):
        return self.model.objects.get(id=product_id)

    def get_user_products(self, user_id):
        return self.model.objects.filter(user_id=user_id)
