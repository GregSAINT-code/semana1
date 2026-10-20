# el modelo que crea y modifica el service
from app.models.user import Role, RoleType, User
# el contrato del repository: el service depende de él, no de una implementación
from app.repositories.user_repository import UserRepository


class UserService:
    """Las reglas del negocio. TIENE un repository y no sabe cómo guarda."""

    # recibe el repository desde afuera (composición): no lo crea
    def __init__(self, repository: UserRepository) -> None:
        self._repo = repository

    def create_user(self, username: str, email: str, role_type: RoleType) -> User:
        # arma el usuario con el siguiente id libre del repository
        user = User(
            id=self._repo.next_id(),
            username=username,
            # regla de negocio: el email se guarda sin espacios y en minúsculas
            email=email.strip().lower(),
            # cada usuario recibe su propio Role, con los permisos del catálogo
            role=Role(role_type),
        )
        # lo guarda y devuelve el usuario ya guardado
        return self._repo.add(user)

    def get_user(self, user_id: int) -> User | None:
        # delega en el repository: si no existe, devuelve None tal cual
        return self._repo.get(user_id)

    def list_users(self, active_only: bool = True) -> list[User]:
        # pide todos los usuarios al repository
        users = self._repo.list_all()
        # por defecto filtra a los activos (los desactivados siguen guardados)
        if active_only:
            return [user for user in users if user.is_active]
        # con active_only=False devuelve todos, también los desactivados
        return users

    def deactivate_user(self, user_id: int) -> User | None:
        # busca al usuario; puede no existir
        user = self._repo.get(user_id)
        # soft delete: si existe, lo marca inactivo en vez de borrarlo
        if user is not None:
            user.is_active = False
        # devuelve el usuario, o None si no existía
        return user

    def change_role(self, user_id: int, role_name: str) -> User | None:
        # busca al usuario; puede no existir
        user = self._repo.get(user_id)
        # RoleType("admin") convierte el texto al enum; el Role nuevo trae sus permisos
        if user is not None:
            user.role = Role(RoleType(role_name))
        # devuelve el usuario, o None si no existía
        return user