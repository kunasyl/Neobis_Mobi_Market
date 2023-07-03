from . import models


class ProductRepos:
    model = models.Product
    favorites = models.FavoriteProduct

    def get_product(self, product_id):
        return self.model.objects.get(id=product_id)

    def get_user_products(self, user_id):
        return self.model.objects.filter(user_id=user_id)

    def get_favorite_products(self, user_id):
        return self.favorites.objects.filter(user_id=user_id)

    def favorite_product_exist(self, product_id):
        return self.favorites.objects.filter(id=product_id).exists()

    def get_favorite_product(self, product_id):
        return self.favorites.objects.get(id=product_id)