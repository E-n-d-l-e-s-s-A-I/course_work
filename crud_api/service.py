from abc import ABC, abstractmethod

from pydantic import BaseModel


class Service(ABC):
    """Абстрактный класс для реализации бизнес-логики http-методов."""

    @abstractmethod
    def get_objects(self) -> BaseModel:
        """Логика извлечения нескольких сущностей http-методом get."""
        ...

    # @abstractmethod
    # def get_object(self) -> BaseModel:
    #     """Логика извлечения одной сущности http-методом get."""
    #     ...

    # @abstractmethod
    # def create_object(self) -> BaseModel:
    #     """Логика создания сущности http-методом post."""
    #     ...

    # @abstractmethod
    # def update_object(self) -> BaseModel:
    #     """Логика создания сущности http-методом put."""
    #     ...

    # @abstractmethod
    # def delete_object(self) -> BaseModel:
    #     """Логика удаления сущности http-методом delete."""
    #     ...
