FROM python:3.9-slim

WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Installer d'abord numpy
RUN pip install --no-cache-dir numpy==1.23.5

# Copier les fichiers de requirements
COPY requirements.txt .

# Installer les autres dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code et les données
COPY . .

# Exposer le port
EXPOSE 8000

# Lancer l'application
CMD ["python", "main.py"]