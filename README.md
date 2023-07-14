# 1. Présentation générale du projet

Le but de ce projet est de fournir un outil client-serveur permettant de corriger automatiquement des exercices de code. Le projet a pour but de ressembler au fonctionnement du logiciel `examshell` de l'école 42. Le but est de le rendre le plus personnalisable possible

# 2. État d'avancement du projet

Le projet est actuellement hardcodé pour corriger des projets en C. Il est également hardcodé pour tester avec la norminette, les flags de GCC, ...
Le projet est fonctionnel dans ce cadre mais reste basique et demande encore du travail pour le rendre plus agréable à utiliser.

# 3. Utilisation du projet

## 3.1. Installation

Pour fonctionner, le projet nécessite d'avoir d'installer sur l'ordinateur serveur:

-   `gcc` (ou autre compilateur qui devra être configuré pour chaque sujet)
-   `norminette`
-   `diff`
-   `nm`

## 3.2. Préparation

### 3.2.1. Serveur

Avant de lancer le serveur, il faut configurer le fichier `config.json` avec le port sur lequel le serveur doit écouter

### 3.2.2. Sujets

Les sujets sont à ranger dans le dossier server en respectant l'arborescence suivante:

```
server
└───subjects
	└───levelX
		└───YY
		    ├───subject.txt
		    ├───main.c
		    ├───function.c
		    ├───config.json
```

Précisions sur les fichiers:

-   Il est important de commencer par le `level0`
-   Le `YY` correspond au nom de l'exercice, il ne doit pas contenir d'espace et se limiter aux caractères ASCII
-   Le `subject.txt` est le sujet de l'exercice, il peut être au format de votre choix
-   Le `main.c` est le fichier main de l'exercice, il doit utiliser la fonction demandée et écrire le résultat sur la sortie standard. Il doit inclure le prototype de la fonction à tester
-   Le `function.c` est le fichier contenant la fonction de référence, celle-ci doit être prototypée de la même façon que demandé dans le sujet
-   Le `config.json` est facultatif, il peut contenir les clés suivantes:
    -   `send_trace` (booléen) Si `true`, le serveur enverra la trace de l'exécution du programme au client [WIP]
    -   `authorized_functions` (tableau de chaînes de caractères) Liste des symboles autorisées dans le fichier `function.c` retournés par `nm -u`. Attention les symboles doivent respectés le formatage de `nm -u` (ex: `_write`)
    -   `compiler` (chaîne de caractères) Commande à utiliser pour compiler le programme
    -   `compiler_flags` (chaîne de caractères) Liste des flags à utiliser pour compiler le programme

### 3.2.3. Clients

Les ordinateurs clients n'ont besoin que du dossier `client`. Le fichier `config.json` doit être configuré avec l'adresse IP du serveur et le port sur lequel le serveur écoute

### 3.2.4. Avertissement

Le client modifiera les dossier `~/rendu` et `~/subject`. Veillez à ne pas avoir de fichiers importants dans ces dossiers

## 3.3. Commandes

### 3.3.1. Serveur

Sur le serveur, les commandes disponibles sont les suivantes:

-   `help` Affiche l'aide
-   `infos` Affiche les informations sur le serveur
-   `clients` Affiche les clients connectés et leur état
-   `subject <client id> <level> [subject name]` Permet de modifier le sujet d'un client. Si le sujet n'est pas précisé, il sera choisi aléatoirement

### 3.3.2. Client

Sur le client, les commandes disponibles sont les suivantes:

-   `help` Affiche l'aide
-   `grademe` Envoie les fichiers au serveur et lance la correction
