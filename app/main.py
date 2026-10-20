# RoleType: para elegir el rol de cada usuario nuevo
from app.models.user import RoleType
# la implementación en memoria del repository
from app.repositories.user_repository import InMemoryUserRepository
# el service con las reglas de negocio
from app.services.user_service import UserService


def main() -> None:
    # arma el service y le inyecta el repository en memoria
    service = UserService(InMemoryUserRepository())

    # Fase 1: crear, listar, cambiar rol, desactivar
    # tres usuarios, uno por rol; el email de ana llega con mayúsculas a propósito
    ana = service.create_user("ana", "Ana@TaskFlow.com", RoleType.ADMIN)
    gregory = service.create_user("gregory","gs@gmail.com",RoleType.ADMIN)
    beto = service.create_user("beto", "beto@taskflow.com", RoleType.EDITOR)
    service.create_user("carla", "carla@taskflow.com", RoleType.VIEWER)

    # imprime los activos; print usa el __str__ de User
    for user in service.list_users():
        print(user)

    # consulta permisos a través del rol que cada usuario contiene
    print("¿Ana administra usuarios?", ana.has_permission("manage_users"))
    print("¿Beto puede borrar?", beto.has_permission("delete"))
    print("gregory puede borrar usuarios?", gregory.has_permission("delete"))
    # sube a beto a admin; el rol llega como texto, igual que desde un formulario
    service.change_role(beto.id, "admin")
    # el rol nuevo trae los permisos de admin
    print("Beto ahora:", beto.role.name.value, beto.role.permissions)

    # desactiva a carla (id 3): sigue guardada, pero ya no cuenta como activa
    service.deactivate_user(3)
    # activos contra todos: la diferencia es carla
    print("Activos:", [user.username for user in service.list_users()])
    print("Todos:", [user.username for user in service.list_users(active_only=False)])


# solo corre main() cuando ejecutas el módulo, no cuando alguien lo importa
if __name__ == "__main__":
    main()