class Container:
    def __init__(self):
        # Stocke les définitions (instance ou factory)
        self._services = {}

        # Stocke les singletons déjà instanciés
        self._singletons = {}

    def register(self, key: str, provider, singleton: bool = True):
        """
        Enregistre un service.

        provider :
            - soit une instance déjà créée
            - soit une factory (callable) qui retourne une instance

        singleton :
            - True  → une seule instance sera créée et réutilisée
            - False → nouvelle instance à chaque resolve()
        """
        self._services[key] = {
            "provider": provider,
            "singleton": singleton
        }

    def resolve(self, key: str):
        """
        Récupère une instance du service.
        """
        if key not in self._services:
            raise KeyError(f"Service '{key}' non enregistré dans le container")

        definition = self._services[key]
        provider = definition["provider"]
        singleton = definition["singleton"]

        # Si singleton déjà instancié
        if singleton and key in self._singletons:
            return self._singletons[key]

        # Si provider est une factory (callable)
        if callable(provider):
            instance = provider()
        else:
            instance = provider

        # Sauvegarde si singleton
        if singleton:
            self._singletons[key] = instance

        return instance