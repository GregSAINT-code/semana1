# ABC y abstractmethod: para declarar un contrato que no se puede instanciar
from abc import ABC, abstractmethod

# el modelo que guarda este repository
from app.models.user import User


# hereda de ABC: es un contrato, no se instancia
class UserRepository(ABC):
    """El contrato: cualquier almacenamiento (memoria hoy, una base de datos mañana)."""

    # reserva el siguiente id libre
    @abstractmethod
    def next_id(self) -> int: ...

    # guarda un usuario y lo devuelve
    @abstractmethod
    def add(self, user: User) -> User: ...

    # busca por id; None si no existe
    @abstractmethod
    def get(self, user_id: int) -> User | None: ...

    # busca por email; None si no existe
    @abstractmethod
    def get_by_email(self, email: str) -> User | None: ...

    # devuelve todos los usuarios guardados
    @abstractmethod
    def list_all(self) -> list[User]: ...


# "es un" UserRepository: hereda el contrato y lo cumple completo
class InMemoryUserRepository(UserRepository):
    """Guarda los usuarios en un dict. Se borran al terminar el programa."""

    def __init__(self) -> None:
        # el almacenamiento: un dict de id a usuario
        self._users: dict[int, User] = {}
        # el contador de ids empieza en 1
        self._next_id = 1

    def next_id(self) -> int:
        # toma el id actual y avanza el contador: dos usuarios nunca comparten id
        user_id = self._next_id
        self._next_id += 1
        return user_id

    def add(self, user: User) -> User:
        # guarda al usuario bajo su id y lo devuelve
        self._users[user.id] = user
        return user

    def get(self, user_id: int) -> User | None:
        # dict.get devuelve None si el id no existe, sin lanzar KeyError
        return self._users.get(user_id)

    def get_by_email(self, email: str) -> User | None:
        # recorre los usuarios y devuelve el primero con ese email
        for user in self._users.values():
            if user.email == email:
                return user
        # nadie lo tiene: None
        return None

    def list_all(self) -> list[User]:
        # una lista nueva: quien la reciba no modifica el dict interno
        return list(self._users.values())