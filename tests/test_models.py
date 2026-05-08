from src.models import Deal

def test_deal_from_dict():
    data = {
        "id": 123,
        "height": 100,
        "timestamp": 1600000000,
        "pieceSize": 34359738368,
        "verifiedDeal": True,
        "client": "f1abc",
        "provider": "f01313",
        "startEpoch": 200,
        "startTimestamp": 1600000100,
        "endEpoch": 300,
        "endTimestamp": 1600000200,
        "stroagePrice": "0"
    }
    deal = Deal.from_dict(data)
    assert deal.id == 123
    assert deal.provider == "f01313"
    assert deal.verified_deal is True
