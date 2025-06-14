import requests
from behave import given

# HTTP Return Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204

@given('the following products')
def step_impl(context):
    """ Delete all Products and load new ones """
    #
    # List all of the products and delete them one by one
    #
    rest_endpoint = f"{context.base_url}/products"
    context.resp = requests.get(rest_endpoint)
    assert(context.resp.status_code == HTTP_200_OK)
    for product in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{product['id']}")
        assert(context.resp.status_code == HTTP_204_NO_CONTENT)

    #
    # load the database with new products
    #
    for row in context.table:
        #
        # Extract product details from the table
        product_data = {
            'name': row['name'],
            'description': row['description'],
            'category': row['category'],
            'price': row['price'],
            'availability': row['availability'] == 'True'  # Convert 'True'/'False' string to boolean
        }

        # Create a new product using POST request
        context.resp = requests.post(rest_endpoint, json=product_data)
        assert(context.resp.status_code == HTTP_201_CREATED)
