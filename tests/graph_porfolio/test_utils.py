from urllib.parse import urlencode, urlunparse

from graph_portfolio.utils import URLComponents


def test_create_url_from_components():
    components = URLComponents(
        scheme="https",
        netloc="example.com",
        url="/api/v1",
        path="",
        query=urlencode(
            {
                "name": "example_name",
                "category": "cat1",
            }
        ),
        fragment="anchor",
    )

    expected = "https://example.com/api/v1?name=example_name&category=cat1#anchor"

    assert urlunparse(components) == expected
