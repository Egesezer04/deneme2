from abc import ABC, abstractmethod
from typing import List, Tuple
from models import Listing


class AbstractScorer(ABC):
    """Interface for scoring a listing."""
    @abstractmethod
    def score(self, listing: Listing) -> Tuple[float, List[str]]:
        pass


class QualityScorer(AbstractScorer):
    """Implements scoring rules for listings."""
    def score(self, listing: Listing) -> Tuple[float, List[str]]:
        points = 0
        missing: List[str] = []

        points += self._score_title(listing.title, missing)
        points += self._score_price(listing.price, missing)
        points += self._score_description(listing.description, missing)
        points += self._score_images(len(listing.images), missing)

        return max(0, min(100, points)), missing

    @staticmethod
    def _score_title(title: str, missing: List[str]) -> int:
        if title:
            return 10
        missing.append("Title missing")
        return 0

    @staticmethod
    def _score_price(price: float, missing: List[str]) -> int:
        if price is None:
            missing.append("Price missing")
            return 0
        if price < 10:
            missing.append("Price may be low")
        return 20

    @staticmethod
    def _score_description(description: str, missing: List[str]) -> int:
        length = len(description)
        if length >= 100:
            return 20
        if length >= 20:
            return 10
        missing.append("Description too short")
        return 0

    @staticmethod
    def _score_images(count: int, missing: List[str]) -> int:
        if count >= 3:
            return 20
        if count >= 1:
            return 10
        missing.append("No images")
        return 0