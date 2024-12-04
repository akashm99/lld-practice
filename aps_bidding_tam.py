from abc import ABC, abstractmethod
from typing import List, Dict
import random

# Observer Pattern
class BidderObserver(ABC):
    @abstractmethod
    def update(self, ad_request: 'AdRequest'):
        pass

# Strategy Pattern
class BiddingStrategy(ABC):
    @abstractmethod
    def bid(self, ad_request: 'AdRequest') -> float:
        pass

class RandomBiddingStrategy(BiddingStrategy):
    def bid(self, ad_request: 'AdRequest') -> float:
        return random.uniform(0.1, 10.0)

# Factory Pattern
class AdRequestFactory:
    @staticmethod
    def create_ad_request(ad_unit_id: str, size: str) -> 'AdRequest':
        return AdRequest(ad_unit_id, size)

# Singleton Pattern
class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance.timeout = 200  # milliseconds
        return cls._instance

    def get_timeout(self) -> int:
        return self.timeout

class AdRequest:
    def __init__(self, ad_unit_id: str, size: str):
        self.ad_unit_id = ad_unit_id
        self.size = size

class Bidder(BidderObserver):
    def __init__(self, name: str, strategy: BiddingStrategy):
        self.name = name
        self.strategy = strategy

    def update(self, ad_request: AdRequest):
        bid_amount = self.strategy.bid(ad_request)
        print(f"Bidder {self.name} bids ${bid_amount:.2f} for ad unit {ad_request.ad_unit_id}")
        return bid_amount

class TransparentAdMarketplace:
    def __init__(self):
        self.bidders: List[Bidder] = []
        self.config = ConfigManager()

    def add_bidder(self, bidder: Bidder):
        self.bidders.append(bidder)

    def remove_bidder(self, bidder: Bidder):
        self.bidders.remove(bidder)

    def notify_bidders(self, ad_request: AdRequest) -> Dict[str, float]:
        bids = {}
        for bidder in self.bidders:
            bids[bidder.name] = bidder.update(ad_request)
        return bids

    def run_auction(self, ad_request: AdRequest) -> str:
        bids = self.notify_bidders(ad_request)
        winner = max(bids, key=bids.get)
        winning_bid = bids[winner]
        print(f"Auction winner for ad unit {ad_request.ad_unit_id}: {winner} with ${winning_bid:.2f}")
        return winner

class PublisherController:
    def __init__(self):
        self.tam = TransparentAdMarketplace()
        self.ad_request_factory = AdRequestFactory()

    def setup_bidders(self):
        self.tam.add_bidder(Bidder("Amazon", RandomBiddingStrategy()))
        self.tam.add_bidder(Bidder("Google", RandomBiddingStrategy()))
        self.tam.add_bidder(Bidder("AppNexus", RandomBiddingStrategy()))

    def run_auction(self, ad_unit_id: str, size: str):
        ad_request = self.ad_request_factory.create_ad_request(ad_unit_id, size)
        return self.tam.run_auction(ad_request)

# Usage
if __name__ == "__main__":
    controller = PublisherController()
    controller.setup_bidders()

    # Simulate multiple ad requests
    for i in range(3):
        winner = controller.run_auction(f"ad_unit_{i}", "300x250")
        print(f"Ad served by: {winner}\n")
