from models import Product

class ProductController:
    @staticmethod
    def get_all_products():
        return Product.objects()

    @staticmethod
    def get_product_by_id(product_id):
        return Product.objects(id=product_id).first()

    @staticmethod
    def create_product(name, description, price, image_url=None):
        product = Product(
            name=name, 
            description=description, 
            price=price,
            image_url=image_url or "https://via.placeholder.com/300x200?text=No+Image"
        )
        product.save()
        return product

    @staticmethod
    def update_product(product_id, name=None, description=None, price=None, image_url=None):
        product = Product.objects(id=product_id).first()
        if product:
            if name: product.name = name
            if description: product.description = description
            if price: product.price = price
            if image_url: product.image_url = image_url
            product.save()
        return product

    @staticmethod
    def delete_product(product_id):
        product = Product.objects(id=product_id).first()
        if product:
            product.delete()
            return True
        return False