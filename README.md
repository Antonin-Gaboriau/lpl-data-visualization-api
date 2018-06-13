# Avancée actuelle

La visualisation des données se fait en deux étapes: création d'un objet *VisualizationData* en selectionnant les données souhaitées, puis affichage de cette objet à l'aide de différentes fonctions de visualisation de la classe abstraite *Display*
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
Le format accépté des données lues est spécifié dans le fichier ![data_format.md](https://github.com/Antonin-Gaboriau/lpl-data-visualization-api/blob/master/data_format.md).

### Fonctions d'affichage de la classe Display
* ***Display.conversation()*** affiche les conversations composées des données sélectionnées par l'objet *VisualizationData* passé en paramètre. Il est possible de renseigner les paramètres optionnels *linked* qui à *True* synchronise les axes de chaque conversations et *color_palette* pour définir les couleurs utilsées dans le graphes. La finesse du lissage est aussi paramètrable en renseignant les paramètres optionnels *smoothing_window* et *points_number* ou dynamiquement avec un widget si l'on passe le paramètre *interactive* à *True* 
* ***Display.average()*** affiche la courbe moyenne de toutes les données de l'objet *VisualizationData* passé en paramètre, la répartition de ces données via une bande écart-type, et toutes les données brutes. Pour chaques courbes tracées, survoler la ligne avec le curseur permet d'afficher toutes ses méta-informations. Si l'on renseigne le parmaètre *interactive* à *True*, des widgets pour chaques méta-information des données apparaissent, des listes déroulantes pour les méta-informations textuelle et des double curseurs linéaire pour les méta-informations numériques. Ces widgets permettent de filtrer dynamiquement les données affiché, par exemple en isolant les données de locuteur masculin de moins de 30 ans. Des widgets en dessous du graphique permettent d'exporter les données filtrées dans une variable de sortie *output* sous un nom choisi, pour ensuite pouvoir comparer différentes données filtrées sur un même graphique avec la fonction *Display.comparison*.
* ***Display.comparison()*** affiche l'évolution moyenne et la répartition par écart type des données filtrées de la variable passée en paramètre, variable issue des exportation de la fonction *Display.average()* via *output*. Voir l'exemple de la capture ci-dessous pour meiux comprendre.
* Dans toutes ces fonctions, cliquer sur la légende fait aparaitre/disparaitre les courbes tracées sur les graphiques.
 
 
Le code se situe dans le notebook Jupyter ![notebook.ipynb](https://raw.githubusercontent.com/Antonin-Gaboriau/lpl-data-visualization-api/master/notebook.ipynb). Voici un exemple d'utilisation de toutes ces fonctions de l'API :![Capture](https://raw.githubusercontent.com/Antonin-Gaboriau/lpl-data-visualization-api/master/capture.png)

