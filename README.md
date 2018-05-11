# Avancée actuelle

> La visualisation des données se fait en deux étapes: création d'un objet *VisualizationData* en selectionnant les données souhaitées, puis affichage de cette objet à l'aide de différentes fonctions de visualisation de la classe abstraite *Display*
### VisualizationData
C'est un objet qui peut être visualisé par toutes les fonctions de visualisation. Sa construction nécessite :
* le nom du répertoire contenant tous les fichiers de données. Il s'agit du seul paramètre obligatoire et non nomé
* des filtres optionnels. Quand un filtre est renseigné, il limite les données sélectionnées, par exemple si l'on ne veut que les données qui proviennent à la fois du locuteur 1040 et des conversations 2001, 2002 et 2003:   (*des filtres corpus et data_type sont aussi disponibles*)
```python
vdata = VisualizationData("data_directory", conversations=[2001,2002,2003], speakers=[1040])
```
* le format des donnée (paramètres *data_format* et *ddata_delimiter*), des métadonnées (paramètre *metadata_format*) et des noms de fichiers (paramètres *file_name_format* et *file_name_delimiter*). Voici un exemple:
```python
vdata = VisualizationData("data_directory", data_format=['id','time','values'], file_name_format=['corpus','id_conv','id_speaker'], file_name_delimiter="_")
```
Pour simplifier, il existe des formats préenregistrés pour chaque corpus (pour l'instant seulement Switchboard et CID) tout en laissant la possibilité de paramétrer chaque détail du format, on utilisera alors simplement par exemple:
```python
vdata = VisualizationData("data_directory", format="CID")
```

### Fonctions d'affichage de la classe Display
* ***Display.conversation()*** affiche les conversations composées des données sélectionnées par l'objet *VisualizationData* passé en paramètre. Il est possible de renseigner le paramètre optionnel *linked* qui à *True* synchronise l'affichage de chaque conversations, c'est à dire que l'on se déplace et selectionnent dans tous les graphiques à la fois de façons à ce que que la plages des abscisses et ordonnés restent les mêmes. Un second paramètre optionnel est *color_palette* pour définir les couleurs utilsées dans le graphes (voir exemple dans la capture ci-dessous).
* ***Display.average()*** affiche la courbe moyenne de toutes les données de l'objet *VisualizationData* passé en paramètre.
* Dans les deux fonctions, cliquer sur la légende fait aparaitre/disparaitre les courbes. La finesse du lissage (*smoothing_window*) et le nombre de points de la courbe (*points_number*) sont modifiables en paramètres optionnels.
 
 
Le code se situe dans le notebook ![notebook.ipynb](https://raw.githubusercontent.com/Antonin-Gaboriau/lpl-data-visualization-api/master/notebook.ipynb) pour Jupyter. Voici un exemple de son utilisation avec le corpus CID:
![Capture](https://raw.githubusercontent.com/Antonin-Gaboriau/lpl-data-visualization-api/master/Captures/11mai.png)
