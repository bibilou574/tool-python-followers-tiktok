import customtkinter as ctk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialiser le driver Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Optionnel: Exécuter le navigateur en mode headless
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

refresh_interval = 60000  # Intervalle de rafraîchissement en millisecondes (1 minute)
auto_refresh = False
time_remaining = refresh_interval / 1000  # Temps restant en secondes

# Fonction pour récupérer les données du compte TikTok
def get_tiktok_data(username):
    url = f'https://www.tiktok.com/@{username}'
    driver.get(url)
    
    time.sleep(5)  # Attendre que la page soit complètement chargée
    
    try:
        # Utiliser des sélecteurs CSS pour trouver le nombre d'Abonnés, d'abonnements, et de "J'aime"
        followers_element = driver.find_element(By.CSS_SELECTOR, 'strong[data-e2e="followers-count"]')
        following_element = driver.find_element(By.CSS_SELECTOR, 'strong[data-e2e="following-count"]')
        likes_element = driver.find_element(By.CSS_SELECTOR, 'strong[data-e2e="likes-count"]')
        
        followers_count = followers_element.text
        following_count = following_element.text
        likes_count = likes_element.text
        
        return followers_count, following_count, likes_count
    except Exception as e:
        log_to_console(f"Erreur : {e}")
        return None, None, None

# Fonction pour mettre à jour le nombre d'Abonnés, d'abonnements, et de "J'aime"
def update_data():
    username = entry.get().strip()  # Enlever les espaces superflus
    if not username:  # Si aucun nom d'utilisateur n'est fourni
        followers_label.configure(text="0 Abonnés")
        following_label.configure(text="0 Abonnements")
        likes_label.configure(text="0 J'aime")
    else:
        followers, following, likes = get_tiktok_data(username)
        if followers and following and likes:
            followers_label.configure(text=f"{followers} Abonnés")
            following_label.configure(text=f"{following} Abonnements")
            likes_label.configure(text=f"{likes} J'aime")
        else:
            followers_label.configure(text="Erreur")
            following_label.configure(text="Erreur")
            likes_label.configure(text="Erreur")

# Fonction pour activer/désactiver le rafraîchissement automatique
def toggle_auto_refresh():
    global auto_refresh
    auto_refresh = not auto_refresh
    if auto_refresh:
        button_refresh.configure(text="Arrêter le rafraîchissement automatique")
        auto_refresh_data()
    else:
        button_refresh.configure(text="Démarrer le rafraîchissement automatique")

# Fonction pour le rafraîchissement automatique
def auto_refresh_data():
    if auto_refresh:
        update_data()
        global time_remaining
        time_remaining = refresh_interval / 1000  # Réinitialiser le compteur
        update_timer()
        app.after(refresh_interval, auto_refresh_data)

# Fonction pour mettre à jour le compteur
def update_timer():
    global time_remaining
    if time_remaining > 0:
        time_remaining -= 1
        timer_label.configure(text=f"Prochain rafraîchissement dans: {int(time_remaining)}s")
        app.after(1000, update_timer)  # Appeler update_timer chaque seconde

# Fonction pour changer le thème de l'application
def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        ctk.set_appearance_mode("dark")
        theme_button.configure(text="Passer au thème clair")
    else:
        ctk.set_appearance_mode("light")
        theme_button.configure(text="Passer au thème sombre")

# Fonction pour ajouter un message à la console
def log_to_console(message):
    console_textbox.insert(ctk.END, message + '\n')
    console_textbox.yview(ctk.END)  # Faire défiler vers le bas

# Initialiser l'interface graphique avec customtkinter
app = ctk.CTk()
app.geometry("800x600")  # Taille de la fenêtre ajustée
app.title("Compteur d'Abonnés, Abonnements et J'aime TikTok")

# Définir le mode sombre comme thème par défaut
dark_mode = True
ctk.set_appearance_mode("dark")

frame = ctk.CTkFrame(app)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Ajouter les widgets dans une grille 4x3
for i in range(4):
    frame.grid_rowconfigure(i, weight=1)
for i in range(3):
    frame.grid_columnconfigure(i, weight=1)

# Label pour le titre
title_label = ctk.CTkLabel(frame, text="Entrez le nom d'utilisateur TikTok", font=("Helvetica", 18, "bold"))
title_label.grid(row=0, column=0, columnspan=3, pady=10)

# Entry pour le nom d'utilisateur
entry = ctk.CTkEntry(frame, width=400)
entry.grid(row=1, column=0, columnspan=3, pady=10)

# Bouton pour obtenir les données du compte
button = ctk.CTkButton(frame, text="Obtenir les données du compte", command=update_data, border_width=2, border_color="#000000")
button.grid(row=2, column=0, padx=10, pady=10)

# Bouton pour démarrer/arrêter le rafraîchissement automatique
button_refresh = ctk.CTkButton(frame, text="Démarrer le rafraîchissement automatique", command=toggle_auto_refresh, border_width=2, border_color="#000000")
button_refresh.grid(row=2, column=1, padx=10, pady=10)

# Bouton pour changer le thème
theme_button = ctk.CTkButton(frame, text="Passer au thème clair", command=toggle_theme, border_width=2, border_color="#000000")
theme_button.grid(row=2, column=2, padx=10, pady=10)

# Labels pour les abonnés, abonnements et les "J'aime" avec le texte associé
followers_label = ctk.CTkLabel(frame, text="0 Abonnés", font=("Helvetica", 18, "bold"))
followers_label.grid(row=3, column=0, padx=10, pady=10)

following_label = ctk.CTkLabel(frame, text="0 Abonnements", font=("Helvetica", 18, "bold"))
following_label.grid(row=3, column=1, padx=10, pady=10)

likes_label = ctk.CTkLabel(frame, text="0 J'aime", font=("Helvetica", 18, "bold"))
likes_label.grid(row=3, column=2, padx=10, pady=10)

# Ajouter le label pour le compteur en haut à droite
timer_label = ctk.CTkLabel(app, text=f"Prochain rafraîchissement dans: {int(time_remaining)}s", font=("Helvetica", 14, "bold"))
timer_label.pack(side="top", anchor="ne", padx=20, pady=10)

# Ajouter une section pour afficher les messages de la console (retiré si non nécessaire)
# console_frame = ctk.CTkFrame(app)
# console_frame.pack(pady=10, padx=20, fill="both", expand=True)

# console_textbox = ctk.CTkTextbox(console_frame, height=10, wrap=ctk.WORD, state=ctk.NORMAL, font=("Helvetica", 12))
# console_textbox.pack(fill="both", expand=True)

# Rediriger les messages de la console vers la textbox (retiré si non nécessaire)
# import sys
# class ConsoleRedirector:
#     def __init__(self, textbox):
#         self.textbox = textbox
#     def write(self, message):
#         log_to_console(message)
#     def flush(self):
#         pass
# sys.stdout = ConsoleRedirector(console_textbox)
# sys.stderr = ConsoleRedirector(console_textbox)

app.mainloop()

# Fermer le driver à la fin de l'application
driver.quit()
