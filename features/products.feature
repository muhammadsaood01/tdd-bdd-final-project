Feature: The product store service back-end
  As a Product Store Owner
  I need a RESTful catalog service
  So that I can keep track of all my products

Background:
  Given the following products
    | name       | description     | price   | available | category   |
    | Hat        | A red fedora    | 59.95   | True      | CLOTHS     |
    | Shoes      | Blue shoes      | 120.50  | False     | CLOTHS     |
    | Big Mac    | 1/4 lb burger   | 5.99    | True      | FOOD       |
    | Sheets     | Full bed sheets | 87.00   | True      | HOUSEWARES |

Scenario: The server is running
  When I visit the "Home Page"
  Then I should see "Product Catalog Administration" in the title
  And I should not see "404 Not Found"

Scenario: Create a Product
  When I visit the "Home Page"
  And I set the "Name" to "Hammer"
  And I set the "Description" to "Claw hammer"
  And I select "True" in the "Available" dropdown
  And I select "Tools" in the "Category" dropdown
  And I set the "Price" to "34.95"
  And I press the "Create" button
  Then I should see the message "Success"
  When I copy the "Id" field
  And I press the "Clear" button
  Then the "Id" field should be empty
  And the "Name" field should be empty
  And the "Description" field should be empty
  When I paste the "Id" field
  And I press the "Retrieve" button
  Then I should see the message "Success"
  And I should see "Hammer" in the "Name" field
  And I should see "Claw hammer" in the "Description" field
  And I should see "True" in the "Available" dropdown
  And I should see "Tools" in the "Category" dropdown
  And I should see "34.95" in the "Price" field

Scenario: Reading a Product
  Given I am on the product page for "Hammer"
  When I retrieve the product details
  Then I should see "Hammer" in the "Name" field
  And I should see "Claw hammer" in the "Description" field
  And I should see "True" in the "Available" dropdown
  And I should see "Tools" in the "Category" dropdown
  And I should see "34.95" in the "Price" field

Scenario: Updating a Product
  Given I am on the product page for "Hammer"
  When I set the "Price" to "39.95"
  And I press the "Update" button
  Then I should see the message "Success"
  When I retrieve the product details for "Hammer"
  Then I should see "Hammer" in the "Name" field
  And I should see "Claw hammer" in the "Description" field
  And I should see "True" in the "Available" dropdown
  And I should see "Tools" in the "Category" dropdown
  And I should see "39.95" in the "Price" field

Scenario: Deleting a Product
  Given I am on the product page for "Hammer"
  When I press the "Delete" button
  Then I should see the message "Success"
  When I try to retrieve the product details for "Hammer"
  Then I should see the message "Product not found"

Scenario: Listing All Products
  Given I am on the product catalog page
  When I retrieve all products
  Then I should see "Hammer" in the list
  And I should see "Hat" in the list
  And I should see "Shoes" in the list
  And I should see "Big Mac" in the list
  And I should see "Sheets" in the list

Scenario: Searching a Product based on Category
  Given I am on the product catalog page
  When I filter products by category "CLOTHS"
  Then I should see "Hat" in the list
  And I should see "Shoes" in the list
  And I should not see "Big Mac" in the list
  And I should not see "Sheets" in the list

Scenario: Searching a Product based on Availability
  Given I am on the product catalog page
  When I filter products by availability "True"
  Then I should see "Hat" in the list
  And I should see "Big Mac" in the list
  And I should see "Sheets" in the list
  And I should not see "Shoes" in the list

Scenario: Searching a Product based on Name
  Given I am on the product catalog page
  When I search for "Hat"
  Then I should see "Hat" in the list
  And I should not see "Shoes" in the list
  And I should not see "Big Mac" in the list
  And I should not see "Sheets" in the list
