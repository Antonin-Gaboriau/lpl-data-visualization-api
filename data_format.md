# FORMAT DES DONNÉES
### Toutes les données
* Fichiers d’extension csv dans un même dossier
###	Métadonnées
* Un fichier dont le nom contient «metadata» (par exemple «CID_metadataexample.csv» est correct)
*	Une ligne pour chaque fichier de données (lignes d’en-tête facultatives)
*	Toujours le même nombre de colonnes (délimiteur de colonnes au choix, comme par exemple «\t»)
*	Au minimum les quatre colonnes : 
    *	nom du corpus
    *	type de donnée
    *	identifiant de la conversation
    *	identifiant du locuteur (qui peut être son identifiant dans le corpus ou dans la conversation)
###	Données
*	Les noms de fichiers sont composés d’informations déjà présentes dans les métadonnées (même 
composition de nom pour tous les fichiers)
*	Un même délimiteur entre les informations au choix (par exemple «CID_001A.csv» est incorrect 
si 001 et A sont deux informations différentes)
*	Au moins 2 lignes (sans compte l’en-tête facultatif) 
*	À chaque ligne, au minimum une information sur le temps et une information de valeur 
*	Toujours le même nombre de colonnes (délimiteur au choix, par forcement comme les 
métadonnées)
