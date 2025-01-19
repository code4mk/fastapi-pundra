import strawberry
from typing import List, Optional, TypeVar, Generic

T = TypeVar('T')

@strawberry.type(description="Generic list type with pagination")
class PaginatedList(Generic[T]):
    data: List[T]
    total: int
    current_page: int
    next_page: Optional[int]
    prev_page: Optional[int]
    per_page: int
    last_page: int
    from_item: Optional[int]
    to_item: Optional[int]