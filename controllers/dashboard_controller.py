class DashboardController:
    def __init__(self, view, container):
        self.view = view
        self.dashboard_service = container.resolve("dashboard_service")