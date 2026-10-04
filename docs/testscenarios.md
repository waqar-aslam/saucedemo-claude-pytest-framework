# Simple E-commerce Website – Test Automation Requirements

use website https://www.saucedemo.com/ and  automate the following end-to-end business scenario using Playwright with Python and Pytest.

## Technology

- Use sample ecomerce website saucedemo.com. 
- Use the credentials available on the login page.
---

# Main Business Scenario

Automate the following complete customer journey:

**Login → Dashboard → Select Product → Add to Cart → Checkout → Place Order → Order History → Validate Order**

## 1. Login

Create a login page with:

- Username/email field
- Password field
- Login button

Use a valid test user.

### Test

1. Navigate to the login page.
2. Enter valid credentials.
3. Click Login.
4. Verify successful navigation to the dashboard.
5. Capture the login API response.
6. Validate that the API response indicates successful authentication.
7. Verify that the UI displays the logged-in user's information.

Do not rely only on URL validation. Use the API response wherever practical.

---

# 2. Dashboard

After successful login:

- Display the user's name.
- Display a list of available products.
- Each product should contain:
  - Product name
  - Product ID
  - Price
  - Add to Cart button

### Test

1. Capture the API response used to load the products.
2. Extract product information from the API response.
3. Verify that products displayed in the UI match the API response.

For example:

**API:**

```json
{
  "id": 101,
  "name": "Wireless Headphones",
  "price": 59.99
}
```

The UI should display:

```text
Wireless Headphones
$59.99
```

The test should compare the UI values against the API response rather than using hard-coded expected values.

---

# 3. Select Product

Select one product from the dashboard.

For example:

```text
Product: Wireless Headphones
Product ID: 101
Price: $59.99
```

The test should obtain the product information dynamically from the API response.

Do not hard-code the product name or price if the information is available through the API.

---

# 4. Add Product to Cart

Click **Add to Cart**.

### Validate

1. Capture the Add-to-Cart API request/response.
2. Verify that the API confirms the product was added successfully.
3. Open the cart.
4. Verify that:
   - Product ID matches the API response.
   - Product name matches the API response.
   - Quantity is correct.
   - Price is correct.
   - Cart total is correct.

The API should be treated as the source of truth for the product and cart information.

---

# 5. Checkout

Click **Checkout**.

Create a simple checkout page containing:

- Product information
- Quantity
- Total amount
- Customer name
- Shipping address
- Payment method
- Place Order button

### Test

Before placing the order:

1. Capture the cart API response.
2. Compare the UI cart information against the API response.
3. Verify:
   - Product name
   - Product ID
   - Quantity
   - Unit price
   - Total price

The test should fail if the UI displays information that does not match the API response.

---

# 6. Place Order

Click **Place Order**.

The backend should create an order through an API.

Example API response:

```json
{
  "success": true,
  "orderId": "ORD-10025",
  "productId": 101,
  "productName": "Wireless Headphones",
  "quantity": 1,
  "total": 59.99
}
```

### Test

Capture the order creation API response.

Extract:

- Order ID
- Product ID
- Product name
- Quantity
- Total amount

Do not hard-code the Order ID.

The Order ID must be obtained dynamically from the API response.

---

# 7. Order Confirmation

After placing the order, the UI should display an order confirmation page.

For example:

```text
Order Placed Successfully

Order ID: ORD-10025
Product: Wireless Headphones
Total: $59.99
```

Validate the UI against the order creation API response.

The test should verify:

```text
UI Order ID      == API Order ID
UI Product Name  == API Product Name
UI Total         == API Total
```

---

# 8. Order History

Navigate to the **Order History** page.

The page should retrieve orders through an API.

Example:

```json
{
  "orders": [
    {
      "orderId": "ORD-10025",
      "productName": "Wireless Headphones",
      "quantity": 1,
      "total": 59.99
    }
  ]
}
```

### Test

1. Capture the Order History API response.
2. Find the order created during the current test.
3. Extract the order information from the API.
4. Compare it with the UI.

Validate at minimum:

```text
Order ID
Product Name
Quantity
Total
```

The test must confirm that the order created during checkout appears in Order History.

---

# 9. Complete End-to-End Validation

The final automated test should demonstrate this complete flow:

```text
Login
   ↓
Dashboard
   ↓
Get Products API
   ↓
Select Product
   ↓
Add to Cart
   ↓
Get Cart API
   ↓
Checkout
   ↓
Place Order
   ↓
Order Creation API
   ↓
Order Confirmation
   ↓
Order History
   ↓
Order History API
   ↓
Compare API Data with UI
```

---

# API vs UI Validation Strategy

Use API responses as the source of truth wherever possible.

Do not write tests like:

```python
assert product_name == "Wireless Headphones"
```

when the product information can be obtained from the API.

Prefer:

```python
api_product_name = product_response["name"]

ui_product_name = product_name_locator.inner_text()

assert ui_product_name == api_product_name
```

Similarly, for the order:

```python
api_order_id = order_response["orderId"]

ui_order_id = order_id_locator.inner_text()

assert ui_order_id == api_order_id
```

---

# Automation Framework Requirements

Implement the automation using a clean Playwright Python framework.

Use:

- Pytest
- Playwright
- Page Object Model
- Fixtures
- API response interception
- Request/response handling
- Reusable utilities
- Configuration management
- Clear assertions
- Logging where useful

Avoid:

- Hard-coded product IDs
- Hard-coded prices
- Hard-coded order IDs
- Duplicate code
- Fixed sleeps such as `time.sleep()`

Use Playwright's built-in waiting mechanisms.

---

# Test Data

Keep test data separate from test implementation where practical.

For example:

```text
config/
test_data/
pages/
tests/
api/
utils/
```

Use dynamically generated or API-provided values whenever possible.

---

# Expected Result

The final framework should contain at least one complete end-to-end test that:

1. Logs in.
2. Validates login using the API.
3. Reads product information from the API.
4. Selects a product.
5. Adds the product to the cart.
6. Validates the cart against the API.
7. Proceeds to checkout.
8. Places the order.
9. Gets the Order ID from the order API response.
10. Validates the confirmation page against the API response.
11. Opens Order History.
12. Gets the order from the Order History API.
13. Validates the Order ID and Product Name displayed in the UI against the API response.

The purpose of this project is to demonstrate **API + UI combined validation**, not just UI automation.