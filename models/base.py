from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    
    @classmethod
    def __declare_last__(cls):
        """Called after all models are defined."""
        pass
