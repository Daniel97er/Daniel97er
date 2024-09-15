 import os
import requests
import svgwrite

# GitHub API URL für alle Repositories
url = 'https://api.github.com/user/repos?type=all'

# GitHub Personal Access Token
token = os.getenv('TOKEN_GITHUB')
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

# Anfrage an die API
response = requests.get(url, headers=headers)
repos = response.json()

# Sammeln der Sprachdaten
languages = {}
for repo in repos:
    lang_url = repo['languages_url']
    lang_response = requests.get(lang_url, headers=headers)
    repo_languages = lang_response.json()

    for lang in repo_languages:
        if lang in languages:
            languages[lang] += repo_languages[lang]
        else:
            languages[lang] = repo_languages[lang]

# Erstellen des SVG-Dokuments
dwg = svgwrite.Drawing('top-langs.svg', profile='tiny', size=(195, 195))

x_start = 10
y_start = 10
x_offset = 80
y_offset = 20

# Zeichnen der Sprachstatistiken
for index, (lang, count) in enumerate(sorted(languages.items(), key=lambda item: item[1], reverse=True)):
    y = y_start + index * y_offset
    dwg.add(dwg.text(f"{lang}: {count}", insert=(x_start, y), fill='black'))

# Speichern der SVG-Datei
dwg.save()
