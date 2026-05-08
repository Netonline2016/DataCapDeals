from unittest.mock import Mock, patch
from src.api import FilfoxClient

def test_get_deals_single_page():
    mock_response = Mock()
    mock_response.json.return_value = {
        "totalCount": 2,
        "deals": [
            {"id": 1, "height": 100, "timestamp": 1600000000, "pieceSize": 34359738368,
             "verifiedDeal": True, "client": "f1abc", "provider": "f01313",
             "startEpoch": 200, "startTimestamp": 1600000100, "endEpoch": 300,
             "endTimestamp": 1600000200, "stroagePrice": "0"},
            {"id": 2, "height": 101, "timestamp": 1600000001, "pieceSize": 34359738368,
             "verifiedDeal": True, "client": "f1abc", "provider": "f01313",
             "startEpoch": 201, "startTimestamp": 1600000101, "endEpoch": 301,
             "endTimestamp": 1600000201, "stroagePrice": "0"},
        ]
    }
    mock_response.raise_for_status.return_value = None

    with patch("requests.Session.get", return_value=mock_response) as mock_get:
        client = FilfoxClient()
        deals = client.get_deals("f01313", page_size=100, delay_ms=0)

    assert len(deals) == 2
    assert deals[0].id == 1
    assert deals[1].id == 2
    assert mock_get.call_count == 1


def test_get_deals_multiple_pages():
    def mock_get(url, params=None, **kwargs):
        resp = Mock()
        resp.raise_for_status.return_value = None
        page = params.get("page", 0)
        if page == 0:
            resp.json.return_value = {
                "totalCount": 150,
                "deals": [{"id": i, "height": 100, "timestamp": 1600000000, "pieceSize": 34359738368,
                           "verifiedDeal": True, "client": "f1abc", "provider": "f01313",
                           "startEpoch": 200, "startTimestamp": 1600000100, "endEpoch": 300,
                           "endTimestamp": 1600000200, "stroagePrice": "0"} for i in range(100)]
            }
        else:
            resp.json.return_value = {
                "totalCount": 150,
                "deals": [{"id": i + 100, "height": 100, "timestamp": 1600000000, "pieceSize": 34359738368,
                           "verifiedDeal": True, "client": "f1abc", "provider": "f01313",
                           "startEpoch": 200, "startTimestamp": 1600000100, "endEpoch": 300,
                           "endTimestamp": 1600000200, "stroagePrice": "0"} for i in range(50)]
            }
        return resp

    with patch("requests.Session.get", side_effect=mock_get):
        client = FilfoxClient()
        deals = client.get_deals("f01313", page_size=100, delay_ms=0)

    assert len(deals) == 150
