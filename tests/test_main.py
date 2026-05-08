import json
from unittest.mock import Mock, patch
from src.main import main

def test_main_cli(tmp_path, monkeypatch):
    mock_response = Mock()
    mock_response.json.return_value = {
        "totalCount": 1,
        "deals": [
            {"id": 1, "height": 100, "timestamp": 1600000000, "pieceSize": 34359738368,
             "verifiedDeal": True, "client": "f1abc", "provider": "f01313",
             "startEpoch": 200, "startTimestamp": 1600000100, "endEpoch": 300,
             "endTimestamp": 1600000200, "stroagePrice": "0"},
        ]
    }
    mock_response.raise_for_status.return_value = None

    with patch("requests.Session.get", return_value=mock_response):
        monkeypatch.chdir(tmp_path)
        main(["--address", "f01313", "--output-dir", str(tmp_path / "out"), "--delay", "0"])

        json_path = tmp_path / "out" / "f01313_deals.json"
        csv_path = tmp_path / "out" / "f01313_deals.csv"
        assert json_path.exists()
        assert csv_path.exists()

        with open(json_path) as f:
            data = json.load(f)
        assert len(data) == 1
