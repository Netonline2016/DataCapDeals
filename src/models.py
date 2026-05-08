from dataclasses import dataclass
from typing import Any


@dataclass
class Deal:
    id: int
    height: int
    timestamp: int
    piece_size: int
    verified_deal: bool
    client: str
    provider: str
    start_epoch: int
    start_timestamp: int
    end_epoch: int
    end_timestamp: int
    storage_price: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Deal":
        return cls(
            id=data["id"],
            height=data["height"],
            timestamp=data["timestamp"],
            piece_size=data["pieceSize"],
            verified_deal=data["verifiedDeal"],
            client=data["client"],
            provider=data["provider"],
            start_epoch=data["startEpoch"],
            start_timestamp=data["startTimestamp"],
            end_epoch=data["endEpoch"],
            end_timestamp=data["endTimestamp"],
            storage_price=data["stroagePrice"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "height": self.height,
            "timestamp": self.timestamp,
            "pieceSize": self.piece_size,
            "verifiedDeal": self.verified_deal,
            "client": self.client,
            "provider": self.provider,
            "startEpoch": self.start_epoch,
            "startTimestamp": self.start_timestamp,
            "endEpoch": self.end_epoch,
            "endTimestamp": self.end_timestamp,
            "stroagePrice": self.storage_price,
        }
