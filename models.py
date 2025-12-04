from typing import List


class BaseModel:
    """Base class with unique ID."""
    def __init__(self):
        self.id = None


class Listing(BaseModel):
    """Represents a product/listing."""
    def __init__(self, title: str, price: float = 0, description: str = "", images: List[str] = None):
        super().__init__()
        self.title = title or "No title"
        self.price = price or 0
        self.description = description or "No description"
        self.images = images or []

    def summary(self, detailed: bool = False) -> str:
        """Return a summary string of the listing."""
        if detailed:
            return f"Title: {self.title}, Price: {self.price}, Description: {self.description}, Images: {len(self.images)}"
        return f"Title: {self.title}, Price: {self.price}, Images: {len(self.images)}"
