class CategorieService:
    def __init__(self, categorie_repository):
        self.categorie_repository = categorie_repository

    def liste_tout_categories(self):
        return self.categorie_repository.get_list_all_categories()