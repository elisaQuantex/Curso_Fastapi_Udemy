def requier_auth(func):
    def wrapper(user):
        if user.lower() == "admin":
            return func(user)
        else:
            return "Acceso denegado"
    return wrapper

@requier_auth
def admin_dashboard(user):
    return f"Bienvenido al panel, {user}"

print(admin_dashboard("Admin"))
print(admin_dashboard("Invitado"))