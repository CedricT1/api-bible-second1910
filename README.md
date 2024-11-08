# Bible API - Louis Segond 1910

Une API REST simple pour accéder aux versets de la Bible Louis Segond 1910.

## 🚀 Installation

### Prérequis
- Docker
- Un fichier Parquet contenant le texte de la Bible (`train-00000-of-00001.parquet`)

### Installation avec Docker

```bash
# Cloner le repository
git clone https://github.com/votre-username/bible-api

# Se déplacer dans le dossier
cd bible-api

# Construire l'image Docker
docker build -t bible-service .

# Lancer le conteneur
docker run -p 8000:8000 bible-service
```

## 📖 Utilisation

L'API est accessible à l'adresse `http://localhost:8000`

### Format des requêtes

```
http://localhost:8000/bible/{livre}_{chapitre}:{verset}[-{verset_fin}]
```

### Exemples
- Un seul verset : `/bible/jn_3:16`
- Plage de versets : `/bible/ps_23:1-6`
- Premier chapitre : `/bible/gn_1:1-31`

### Abréviations des livres

#### Ancien Testament
| Abréviation | Livre |
|-------------|-------|
| gn | Genèse |
| ex | Exode |
| lv | Lévitique |
| nb | Nombres |
| dt | Deutéronome |
| js | Josué |
| jg | Juges |
| rt | Ruth |
| 1s | 1 Samuel |
| 2s | 2 Samuel |
| [...]  | [...] |

#### Nouveau Testament
| Abréviation | Livre |
|-------------|-------|
| mt | Matthieu |
| mc | Marc |
| lc | Luc |
| jn | Jean |
| ac | Actes |
| rm | Romains |
| [...]  | [...] |

[Liste complète des abréviations](ABBREVIATIONS.md)

## 🔍 Exemple de réponse

```json
{
    "reference": "Jean 3:16",
    "verses": [
        {
            "reference": "Jean 3:16",
            "text": "Car Dieu a tant aimé le monde qu'il a donné son Fils unique, afin que quiconque croit en lui ne périsse point, mais qu'il ait la vie éternelle."
        }
    ]
}
```

## 🛠️ Technologies utilisées

- Python 3.9
- FastAPI
- Pandas
- Docker

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push sur la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Notes

- Cette API utilise la traduction Louis Segond 1910 de la Bible
- Le texte source est stocké dans un fichier Parquet
- Les requêtes sont sensibles à la casse pour les abréviations des livres

## ⚠️ Limitations connues

- Seule la version Louis Segond 1910 est disponible
- Les requêtes doivent suivre exactement le format spécifié
- Les accents dans les URLs ne sont pas supportés (d'où l'utilisation des abréviations)

## 📞 Contact

Cédric Trachsel 

Lien du projet: [https://github.com/votre-username/bible-api](https://github.com/votre-username/bible-api)

