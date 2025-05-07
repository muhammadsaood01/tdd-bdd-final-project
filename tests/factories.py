from faker import Faker
from app import db, Product  # Assuming your app is named 'app' and Product is the model

fake = Faker()

def create_fake_product():
    """
    Creates a fake product for testing purposes.
    :return: Fake Product instance
    """
    product = Product(
        name=fake.word(),
        description=fake.sentence(),
        category=fake.word(),
        price=fake.random_number(digits=2),
        availability=fake.boolean()
    )
    return product

def create_fake_products(n=10):
    """
    Creates a list of fake products.
    :param n: Number of fake products to generate (default is 10)
    :return: List of fake Product objects
    """
    products = []
    for _ in range(n):
        product = create_fake_product()
        products.append(product)
    return products

# Example of usage (for testing)
if __name__ == "__main__":
    # Just printing out the fake products for demonstration
    fake_products = create_fake_products(5)
    for product in fake_products:
        print(f"Product Name: {product.name}, Price: {product.price}")
