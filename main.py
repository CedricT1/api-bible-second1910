from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import pandas as pd
import re

app = FastAPI()

# Table de concordance des livres
BOOK_MAPPING = {
    # Ancien Testament
    "gn": "Genèse",
    "ex": "Exode",
    "lv": "Lévitique",
    "nb": "Nombres",
    "dt": "Deutéronome",
    "js": "Josué",
    "jg": "Juges",
    "rt": "Ruth",
    "1s": "1 Samuel",
    "2s": "2 Samuel",
    "1r": "1 Rois",
    "2r": "2 Rois",
    "1ch": "1 Chroniques",
    "2ch": "2 Chroniques",
    "esd": "Esdras",
    "ne": "Néhémie",
    "est": "Esther",
    "jb": "Job",
    "ps": "Psaumes",
    "pr": "Proverbes",
    "ec": "Ecclésiaste",
    "ct": "Cantique des cantiques",
    "es": "Ésaïe",
    "jr": "Jérémie",
    "lm": "Lamentations",
    "ez": "Ézéchiel",
    "dn": "Daniel",
    "os": "Osée",
    "jl": "Joël",
    "am": "Amos",
    "ab": "Abdias",
    "jon": "Jonas",
    "mi": "Michée",
    "na": "Nahum",
    "ha": "Habakuk",
    "so": "Sophonie",
    "ag": "Aggée",
    "za": "Zacharie",
    "ml": "Malachie",
    # Nouveau Testament
    "mt": "Matthieu",
    "mc": "Marc",
    "lc": "Luc",
    "jn": "Jean",
    "ac": "Actes",
    "rm": "Romains",
    "1co": "1 Corinthiens",
    "2co": "2 Corinthiens",
    "ga": "Galates",
    "ep": "Éphésiens",
    "ph": "Philippiens",
    "col": "Colossiens",
    "1th": "1 Thessaloniciens",
    "2th": "2 Thessaloniciens",
    "1tm": "1 Timothée",
    "2tm": "2 Timothée",
    "tt": "Tite",
    "phm": "Philémon",
    "he": "Hébreux",
    "jc": "Jacques",
    "1p": "1 Pierre",
    "2p": "2 Pierre",
    "1jn": "1 Jean",
    "2jn": "2 Jean",
    "3jn": "3 Jean",
    "jd": "Jude",
    "ap": "Apocalypse"
}

# Charger le fichier Parquet au démarrage
df = pd.read_parquet("train-00000-of-00001.parquet")

HOME_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>API Bible Louis Segond 1910</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        .container {
            background-color: #f9f9f9;
            border-radius: 5px;
            padding: 20px;
            margin-top: 20px;
        }
        code {
            background-color: #f0f0f0;
            padding: 2px 5px;
            border-radius: 3px;
        }
        .example {
            margin: 20px 0;
            padding: 15px;
            background-color: #e8f4f8;
            border-left: 4px solid #2980b9;
        }
    </style>
</head>
<body>
    <h1>API Bible Louis Segond 1910</h1>
    
    <div class="container">
        <h2>Mode d'emploi</h2>
        <p>Cette API permet d'accéder aux versets de la Bible Louis Segond 1910.</p>
        
        <h3>Format de la requête</h3>
        <p>Pour accéder à un passage, utilisez l'URL suivante :</p>
        <code>/bible/[livre]_[chapitre]:[verset-verset]</code>
        
        <div class="example">
            <h3>Exemples de requêtes valides :</h3>
            <ul>
                <li><code>/bible/jn_3:16</code> - Jean 3:16</li>
                <li><code>/bible/1jn_3:5-8</code> - 1 Jean 3:5-8</li>
                <li><code>/bible/gn_1:1-3</code> - Genèse 1:1-3</li>
            </ul>
        </div>
        
        <h3>Abréviations courantes</h3>
        <ul>
            <!-- Ancien Testament -->
            <li><code>gn</code> - Genèse</li>
            <li><code>ex</code> - Exode</li>
            <li><code>lv</code> - Lévitique</li>
            <li><code>nb</code> - Nombres</li>
            <li><code>dt</code> - Deutéronome</li>
            <li><code>js</code> - Josué</li>
            <li><code>jg</code> - Juges</li>
            <li><code>rt</code> - Ruth</li>
            <li><code>1s</code> - 1 Samuel</li>
            <li><code>2s</code> - 2 Samuel</li>
            <li><code>1r</code> - 1 Rois</li>
            <li><code>2r</code> - 2 Rois</li>
            <li><code>1ch</code> - 1 Chroniques</li>
            <li><code>2ch</code> - 2 Chroniques</li>
            <li><code>esd</code> - Esdras</li>
            <li><code>ne</code> - Néhémie</li>
            <li><code>est</code> - Esther</li>
            <li><code>jb</code> - Job</li>
            <li><code>ps</code> - Psaumes</li>
            <li><code>pr</code> - Proverbes</li>
            <li><code>ec</code> - Ecclésiaste</li>
            <li><code>ct</code> - Cantique des cantiques</li>
            <li><code>es</code> - Ésaïe</li>
            <li><code>jr</code> - Jérémie</li>
            <li><code>lm</code> - Lamentations</li>
            <li><code>ez</code> - Ézéchiel</li>
            <li><code>dn</code> - Daniel</li>
            <li><code>os</code> - Osée</li>
            <li><code>jl</code> - Joël</li>
            <li><code>am</code> - Amos</li>
            <li><code>ab</code> - Abdias</li>
            <li><code>jon</code> - Jonas</li>
            <li><code>mi</code> - Michée</li>
            <li><code>na</code> - Nahum</li>
            <li><code>ha</code> - Habakuk</li>
            <li><code>so</code> - Sophonie</li>
            <li><code>ag</code> - Aggée</li>
            <li><code>za</code> - Zacharie</li>
            <li><code>ml</code> - Malachie</li>

            <!-- Nouveau Testament -->
            <li><code>mt</code> - Matthieu</li>
            <li><code>mc</code> - Marc</li>
            <li><code>lc</code> - Luc</li>
            <li><code>jn</code> - Jean</li>
            <li><code>ac</code> - Actes</li>
            <li><code>rm</code> - Romains</li>
            <li><code>1co</code> - 1 Corinthiens</li>
            <li><code>2co</code> - 2 Corinthiens</li>
            <li><code>ga</code> - Galates</li>
            <li><code>ep</code> - Éphésiens</li>
            <li><code>ph</code> - Philippiens</li>
            <li><code>col</code> - Colossiens</li>
            <li><code>1th</code> - 1 Thessaloniciens</li>
            <li><code>2th</code> - 2 Thessaloniciens</li>
            <li><code>1tm</code> - 1 Timothée</li>
            <li><code>2tm</code> - 2 Timothée</li>
            <li><code>tt</code> - Tite</li>
            <li><code>phm</code> - Philémon</li>
            <li><code>he</code> - Hébreux</li>
            <li><code>jc</code> - Jacques</li>
            <li><code>1p</code> - 1 Pierre</li>
            <li><code>2p</code> - 2 Pierre</li>
            <li><code>1jn</code> - 1 Jean</li>
            <li><code>2jn</code> - 2 Jean</li>
            <li><code>3jn</code> - 3 Jean</li>
            <li><code>jd</code> - Jude</li>
            <li><code>ap</code> - Apocalypse</li>
        </ul>
    </div>
</body>
</html>
"""

def parse_reference(reference: str):
    """Parse une référence biblique du type 'jn_3:16', 'jn_3:16-20' ou 'jn_3'"""
    pattern = r"([1-3]?[a-z]+)_(\d+)(?::(\d+)(?:-(\d+))?)?"
    match = re.match(pattern, reference)
    if not match:
        raise HTTPException(status_code=400, detail="Format de référence invalide")
    
    book_abbr = match.group(1).lower()
    if book_abbr not in BOOK_MAPPING:
        raise HTTPException(status_code=400, detail="Livre non reconnu")
    
    book = BOOK_MAPPING[book_abbr]
    chapter = int(match.group(2))
    start_verse = int(match.group(3)) if match.group(3) else None
    end_verse = int(match.group(4)) if match.group(4) else start_verse
    
    return book, chapter, start_verse, end_verse

@app.get("/bible/{reference}")
async def get_bible_passage(reference: str):
    try:
        book, chapter, start_verse, end_verse = parse_reference(reference)
        
        verses = []
        if start_verse is None:
            # Si aucun verset n'est spécifié, récupérez tout le chapitre
            chapter_verses = df[df['input_text'].str.startswith(f"{book} {chapter}:")]
            for _, row in chapter_verses.iterrows():
                ref = row['input_text']
                verse_text = row['target_text'].strip().strip('"')  # Supprime les espaces et les guillemets au début et à la fin
                verses.append({
                    "reference": ref,
                    "text": verse_text
                })
        else:
            # Sinon, récupérez les versets spécifiés
            for verse in range(start_verse, (end_verse or start_verse) + 1):
                ref = f"{book} {chapter}:{verse}"
                verse_row = df[df['input_text'] == ref]
                if not verse_row.empty:
                    verse_text = verse_row['target_text'].iloc[0].strip().strip('"')  # Supprime les espaces et les guillemets au début et à la fin
                    verses.append({
                        "reference": ref,
                        "text": verse_text
                    })
        
        if not verses:
            return HTMLResponse(content=HOME_PAGE)
            
        return {
            "reference": f"{book} {chapter}" if start_verse is None else f"{book} {chapter}:{start_verse}-{end_verse or start_verse}",
            "verses": verses
        }
        
    except Exception as e:
        return HTMLResponse(content=HOME_PAGE)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)