import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile

# Classe personnalisée pour la page du navigateur
class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)

    def accept_navigation_request(self, url):
        return True  # Accepter toutes les requêtes sans aucune demande d'autorisation

# Classe principale du navigateur
class Navigateur(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Navigateur Custom")
        self.setGeometry(100, 100, 1200, 800)

        # Crée un profil qui accepte les permissions
        profile = QWebEngineProfile.defaultProfile()
        self.browser = QWebEngineView()
        self.browser.setPage(CustomWebEnginePage(profile, self))  # Utilise la nouvelle page personnalisée
        self.browser.setUrl(QUrl("https://www.google.fr"))

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Rechercher ou entrer une URL...")
        self.search_bar.returnPressed.connect(self.load_search)

        self.history_button = QPushButton("🕓 Historique")
        self.history_button.clicked.connect(self.show_history)

        layout = QVBoxLayout()
        layout.addWidget(self.history_button)
        layout.addWidget(self.search_bar)
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.history = []

    def load_search(self):
        query = self.search_bar.text()
        if not query.startswith("http://") and not query.startswith("https://"):
            query = f"https://www.google.fr/search?q={query}"  # Recherche Google par défaut
        else:
            self.history.append(query)  # Ajout de l'URL à l'historique

        self.browser.setUrl(QUrl(query))

        # Enregistrer dans l'historique
        with open("historique.txt", "a") as file:
            file.write(query + "\n")

    def show_history(self):
        try:
            with open("historique.txt", "r") as file:
                history_content = "<br>".join(file.readlines())
            self.browser.setHtml(f"<h1>Historique des recherches et URLs</h1><p>{history_content}</p>")
        except FileNotFoundError:
            self.browser.setHtml("<h1>Aucun historique trouvé.</h1>")

# Point d'entrée de l'application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Navigateur()
    window.show()
    sys.exit(app.exec_())
