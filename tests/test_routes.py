import pytest
from app import app, db, Product  # Assuming the app is in app.py, and Product is the model
from factories import create_fake_product, create_fake_products

@pytest.fixture
def client():
    # Setup the Flask app testing client
    with app.test_client() as client:
        yield client

@pytest.fixture
def init_db():
    # Setup the database for testing
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()

# Task 3a: Provide GitHub URL of tests/test_routes.py showing the code snippet for READ test case
def test_read_product(client, init_db):
    # Creating a fake product and adding it to the database
    fake_product = create_fake_product()
    db.session.add(fake_product)
    db.session.commit()

    # Perform a GET request to fetch the product by ID
    response = client.get(f"/products/{fake_product.id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data['name'] == fake_product.name
    assert data['description'] == fake_product.description
    assert data['category'] == fake_product.category
    assert data['price'] == fake_product.price
    assert data['availability'] == fake_product.availability

# Task 3b: Provide GitHub URL of tests/test_routes.py showing the code snippet for UPDATE test case
def test_update_product(client, init_db):
    # Creating a fake product and adding it to the database
    fake_product = create_fake_product()
    db.session.add(fake_product)
    db.session.commit()

    # Prepare new data to update the product
    updated_data = {
        'name': 'Updated Product Name',
        'description': 'Updated description',
        'category': 'Updated category',
        'price': 150,
        'availability': False
    }

    # Perform a PUT request to update the product by ID
    response = client.put(f"/products/{fake_product.id}", json=updated_data)
    data = response.get_json()

    assert response.status_code == 200
    assert data['name'] == updated_data['name']
    assert data['description'] == updated_data['description']
    assert data['category'] == updated_data['category']
    assert data['price'] == updated_data['price']
    assert data['availability'] == updated_data['availability']

# Task 3c: Provide GitHub URL of tests/test_routes.py showing the code snippet for DELETE test case
def test_delete_product(client, init_db):
    # Creating a fake product and adding it to the database
    fake_product = create_fake_product()
    db.session.add(fake_product)
    db.session.commit()

    # Perform a DELETE request to delete the product by ID
    response = client.delete(f"/products/{fake_product.id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data['message'] == "Product deleted successfully"

    # Ensure the product no longer exists in the database
    deleted_product = Product.query.get(fake_product.id)
    assert deleted_product is None

# Task 3d: Provide GitHub URL of tests/test_routes.py showing the code snippet for LIST ALL test case
def test_list_all_products(client, init_db):
    # Creating multiple fake products and adding them to the database
    fake_products = create_fake_products(5)
    db.session.bulk_save_objects(fake_products)
    db.session.commit()

    # Perform a GET request to list all products
    response = client.get("/products")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 5  # Check that the list contains 5 products

# Task 3e: Provide GitHub URL of tests/test_routes.py showing the code snippet for LIST BY NAME test case
def test_list_products_by_name(client, init_db):
    # Creating fake products and adding them to the database
    fake_product1 = create_fake_product()
    fake_product2 = create_fake_product()
    fake_product1.name = "Unique Product Name"
    db.session.add(fake_product1)
    db.session.add(fake_product2)
    db.session.commit()

    # Perform a GET request to list products by name
    response = client.get("/products?name=Unique Product Name")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 1  # Ensure only one product is returned
    assert data[0]['name'] == "Unique Product Name"

# Task 3f: Provide GitHub URL of tests/test_routes.py showing the code snippet for LIST BY CATEGORY test case
def test_list_products_by_category(client, init_db):
    # Creating fake products and adding them to the database
    fake_product1 = create_fake_product()
    fake_product2 = create_fake_product()
    fake_product1.category = "Electronics"
    fake_product2.category = "Electronics"
    db.session.add(fake_product1)
    db.session.add(fake_product2)
    db.session.commit()

    # Perform a GET request to list products by category
    response = client.get("/products?category=Electronics")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 2  # Ensure both products belong to the Electronics category

# Task 3g: Provide GitHub URL of tests/test_routes.py showing the code snippet for LIST BY AVAILABILITY test case
def test_list_products_by_availability(client, init_db):
    # Creating fake products and adding them to the database
    fake_product1 = create_fake_product()
    fake_product2 = create_fake_product()
    fake_product1.availability = True
    fake_product2.availability = False
    db.session.add(fake_product1)
    db.session.add(fake_product2)
    db.session.commit()

    # Perform a GET request to list products by availability
    response = client.get("/products?availability=True")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 1  # Ensure only one product is available (True)

    response = client.get("/products?availability=False")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 1  # Ensure only one product is unavailable (False)

