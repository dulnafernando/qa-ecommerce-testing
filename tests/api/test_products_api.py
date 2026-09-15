import pytest
import requests

pytestmark = [pytest.mark.api]

BASE_URL = "https://automationexercise.com/api"


def test_get_all_products_list_success():
    """Verify GET /api/productsList returns 200 with non-empty product catalog and expected schema."""
    response = requests.get(f"{BASE_URL}/productsList", timeout=10)

    # 1. Transport layer assertions
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    assert response.elapsed.total_seconds() < 3.0, "Response time exceeded 3.0 second SLA"

    # 2. Application layer & schema assertions
    data = response.json()
    assert data.get("responseCode") == 200, f"Expected payload responseCode 200, got {data.get('responseCode')}"
    assert isinstance(data.get("products"), list), "Expected 'products' to be a list"
    assert len(data["products"]) > 0, "Products list should not be empty"

    first_product = data["products"][0]
    for required_key in ["id", "name", "price", "brand", "category"]:
        assert required_key in first_product, f"Product schema missing required field: '{required_key}'"


def test_post_all_products_list_method_not_allowed():
    """Negative test: Calling POST on /api/productsList must return 405 Method Not Supported."""
    response = requests.post(f"{BASE_URL}/productsList", timeout=10)

    # Transport layer returns 200 on this application, but payload communicates 405
    assert response.status_code == 200, f"Expected HTTP 200 transport code, got {response.status_code}"

    data = response.json()
    assert data.get("responseCode") == 405, f"Expected business responseCode 405, got {data.get('responseCode')}"
    assert data.get("message") == "This request method is not supported."


def test_get_all_brands_list_success():
    """Verify GET /api/brandsList returns 200 with non-empty brands array and valid schema."""
    response = requests.get(f"{BASE_URL}/brandsList", timeout=10)

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    data = response.json()
    assert data.get("responseCode") == 200, f"Expected payload responseCode 200, got {data.get('responseCode')}"
    assert isinstance(data.get("brands"), list), "Expected 'brands' to be a list"
    assert len(data["brands"]) > 0, "Brands list should not be empty"

    first_brand = data["brands"][0]
    assert "id" in first_brand, "Brand schema missing 'id'"
    assert "brand" in first_brand, "Brand schema missing 'brand'"


def test_post_search_product_valid_term():
    """Verify POST /api/searchProduct returns matching products for a search term."""
    search_term = "top"
    response = requests.post(
        f"{BASE_URL}/searchProduct",
        data={"search_product": search_term},
        timeout=10,
    )

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    data = response.json()
    assert data.get("responseCode") == 200, f"Expected payload responseCode 200, got {data.get('responseCode')}"
    assert isinstance(data.get("products"), list), "Expected 'products' list in search response"
    assert len(data["products"]) > 0, f"Expected search results for '{search_term}', found none"


def test_post_search_product_missing_parameter():
    """Negative test: Calling POST /api/searchProduct without parameter returns 400 Bad Request."""
    response = requests.post(f"{BASE_URL}/searchProduct", timeout=10)

    assert response.status_code == 200, f"Expected HTTP 200 transport code, got {response.status_code}"

    data = response.json()
    assert data.get("responseCode") == 400, f"Expected payload responseCode 400, got {data.get('responseCode')}"
    assert "search_product parameter is missing" in data.get("message", "")
