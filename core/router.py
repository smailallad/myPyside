from PySide6.QtWidgets import QMessageBox

class Router:
    def __init__(self, stacked_widget, container, auth_manager):
        self.stacked_widget = stacked_widget
        self.container = container
        self.auth_manager = auth_manager

        self.routes = {}      # config routes
        self.instances = {}   # lazy instances

    def register(self, name, view_class, controller_class, roles=None):
        self.routes[name] = {
            "view": view_class,
            "controller": controller_class,
            "roles": roles or []
        }

    def navigate(self, name):
        if name not in self.routes:
            raise ValueError(f"Route '{name}' not registered")

        route = self.routes[name]

        # 🔐 Véri# self.service = servicefication des rôles
        if route["roles"]:
            if not self.auth_manager.has_role(route["roles"]):
                QMessageBox.warning(None, "Access Denied", "Permission refusée")
                return

        # ⚡ Lazy loading
        if name not in self.instances:
            # print(f"Instanciation de la route '{name}'")
            view = route["view"]()
            controller = route["controller"](view, self.container)
            # self.instances[name] = view
            self.instances[name] = {
                "view": view,
                "controller": controller
            }
            self.stacked_widget.addWidget(view)

        # print(f"Navigation vers '{name}'")
        self.stacked_widget.setCurrentWidget(self.instances[name]["view"])