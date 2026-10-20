# dataclass y field: generan el __init__ y los defaults de cada campo
from dataclasses import dataclass, field
# datetime: para la fecha de creación de cada usuario
from datetime import datetime
# Enum: para que los roles válidos sean una lista cerrada
from enum import Enum


# los tres roles válidos; cualquier otro texto no es un RoleType
class RoleType(Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


# el catálogo: qué permisos trae cada rol por defecto
ROLE_PERMISSIONS: dict[RoleType, list[str]] = {
    # admin puede todo, incluso administrar usuarios
    RoleType.ADMIN: ["read", "write", "delete", "manage_users"],
    # editor lee y escribe; viewer solo lee
    RoleType.EDITOR: ["read", "write"],
    RoleType.VIEWER: ["read"],
}


# @dataclass genera el __init__ y el __repr__ a partir de los campos
@dataclass
class Role:
    """El usuario TIENE un rol (composición): cambiar Role no toca a User."""

    # qué rol es, como valor del enum
    name: RoleType
    # default_factory: cada Role recibe su propia lista vacía, nunca una compartida
    permissions: list[str] = field(default_factory=list)

    # corre justo después del __init__ que generó la dataclass
    def __post_init__(self) -> None:
        # Si no te pasan permisos, toma los del catálogo de ese rol
        if not self.permissions:
            # list(...) hace una copia: modificarla no toca el catálogo
            self.permissions = list(ROLE_PERMISSIONS[self.name])


# la misma dataclass: los campos de abajo arman su __init__
@dataclass
class User:
    # identificador único; lo asigna el repository
    id: int
    # nombre visible y email (el service lo guarda normalizado)
    username: str
    email: str
    # composición: el usuario TIENE un Role, no hereda de él
    role: Role
    # soft delete: desactivar pone False en vez de borrar
    is_active: bool = True
    # default_factory llama a datetime.now al crear cada usuario, no una sola vez
    created_at: datetime = field(default_factory=datetime.now)

    # le pregunta al rol que contiene si incluye ese permiso
    def has_permission(self, permission: str) -> bool:
        return permission in self.role.permissions

    # lo que imprime print(user): nombre, email y rol, legible para humanos
    def __str__(self) -> str:
        return f"{self.username} <{self.email}> [{self.role.name.value}]"