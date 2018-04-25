# Avancée actuelle

#### Visualisation du débit de parole (speech rate) avec le corpus *Switchboard*
La visualisation des données se fait en deux étapes: création d'un objet *VisualizationData* en selectionnant les données souhaitées, puis affichage de cette objet à l'aide des fonctions d'affichage de la classe abstraite *Display*
* ***VisualizationData*** est un objet qui peut être visualisé par toutes les fonctions d'affichage. Sa construction necessite le nom du répertoire qui contient toutes les données, ainsi que des filtres optionnels. Quand un filtre est renseigné, il limite les données sélectionnées, par exemple : 
```python
data1 = VisualizationData("data_directory")
data2 = VisualizationData("data_directory", conversation=[2001,2002,2003], speaker=[1040])
```
*data1* contient toutes les données du répertoire *data_directory* tandis que *data2* ne contient que les donnée provenants à la fois du locuteur 1040 et des conversations 2001, 2002 et 2003.

*corpus* et *data_type* sont aussi des filtres disponibles.

* **Fonctions d'affichage de la classe *Display*** 
  * ***Display.conversation*** affiche l'évolution du débit de parole des conversations composées des données selectionnées par l'objet *VisualizationData* passé en paramètre à coté de l'optionnel paramètre binaire *linked* qui à *True* synchronise l'affichage de chaque conversations, c'est à dire que l'on se déplace et selectionnent dans tous les graphiques à la fois de façons à ce que que la plages des abscisses et ordonnés restent les mêmes. Un second paramètre optionnel est *color_palette* pour definir les couleur utilsées dans le graphes (voir exemple dans la capture ci-dessous).
  * ***Display.average*** affiche la courbe moyenne du débit de parole des données de l'objet *VisualizationData* passé en paramètre.
  * Dans les deux fonctions, cliquer sur la légende fait aparaitre/disparaitre les courbes. La finesse du lissage (*smoothing_window*) et le nombre de points de la courbe (*points_number*) sont modifiables en paramètres optionnels.
 
Le code se situe dans le notebook ![notebook.ipynb](https://raw.githubusercontent.com/Antonin-Gaboriau/lpl-data-visualization-api/master/notebook.ipynb) pour Jupyter. Voici un exemple de son utilisation sur:
![Capture](https://raw.githubusercontent.com/Antonin-Gaboriau/lpl-data-visualization-api/master/Captures/25avril.PNG)
