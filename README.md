# Avancée actuelle

#### Visualisation du débit de parole (speech rate) dans un corpus simple fournit par Simone Fuscone.
Deux fonctions principales permettent cette visualisation :
* ***display_conversation()*** affiche l'évolution du débit de paroles des conversations passées en paramètres (si aucun paramètre, toutes les conversations sont traitées). Voici un exemple de son utilisation:
![Capture 1](https://raw.githubusercontent.com/Antonin-Gaboriau/lpl-data-visualization-api/master/Captures/capture1.PNG)

* ***display_average()*** affiche la courbe moyenne du débit de paroles du corpus (les données sont synchronisées en pourcentage de la conversation). Deux filtres sont disponibles en paramètre pour sélectionner les données à traiter: une liste de conversation *conv* et une liste de locuteurs *speakers*. Voici un exemple de son utilisation:
![Capture 2](https://raw.githubusercontent.com/Antonin-Gaboriau/lpl-data-visualization-api/master/Captures/capture2.PNG)

Le code est visible dans le fichier ![simple_data.py](https://github.com/Antonin-Gaboriau/lpl-data-visualization-api/blob/master/simple_data.py)
