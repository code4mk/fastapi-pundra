"""Base seeder class that all seeders inherit from."""

import logging
from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

logger = logging.getLogger("fastapi_pundra.seeder")


class BaseSeeder(ABC):
    """
    Abstract base for database seeders.

    Subclasses implement `run()` to insert seed data.
    The runner auto-discovers all subclasses and executes them sorted by `order`.
    """

    order: int = 50

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable seeder name for logging."""

    @abstractmethod
    def run(self, session: Session) -> None:
        """Insert seed data into the database."""

    def should_seed(self, session: Session) -> bool:
        """Override to skip seeding when data already exists (idempotent guard)."""
        return True

    def execute(self, session: Session) -> None:
        """Run the seeder with logging and idempotency check."""
        if not self.should_seed(session):
            logger.info("[Seeder] Skipping %s — data already exists", self.name)
            return

        logger.info("[Seeder] Running %s...", self.name)
        self.run(session)
        logger.info("[Seeder] Completed %s", self.name)
