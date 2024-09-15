import os
import requests
import json
import svgwrite
from svgwrite import cm, mm

# GitHub GraphQL API URL
url = 'https://api.github.com/graphql'

# Authentifizierungstoken aus Umgebungsvariablen
token = os.getenv('GITHUB_TOKEN')
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

# GraphQL-Abfrage
query = """
{
  viewer {
    repositories(first: 100) {
      edges {
        node {
          name
          languages(first: 10) {
            edges {
              node {
                name
              }
            }
          }
        }
      }
    }
  }
}
"""

# Anfrage an die API
response = requests.post(url, headers=headers, json={'query': query})
data = response.json()

# Sammeln der Sprachdaten
languages = {}
repos = data.get('data', {}).get('viewer', {}).get('repositories', {}).get('edges', [])

for repo in repos:
    repo_node = repo.get('node', {})
    lang_edges = repo_node.get('languages', {}).get('edges', [])
    for lang_edge in lang_edges:
        lang_name = lang_edge.get('node', {}).get('name', 'Unknown')
        if lang_name in languages:
            languages[lang_name] += 1
        else:
            languages[lang_name] = 1

# Erstellen des SVG-Dokuments
dwg = svgwrite.Drawing('top-langs.svg', profile='tiny', size=(210*mm, 297*mm))

x_start = 10
y_start = 10
x_offset = 80
y_offset = 20

# Zeichnen der Sprachstatistiken
for index, (lang, count) in enumerate(languages.items()):
    y = y_start + index * y_offset
    dwg.add(dwg.text(f"{lang}: {count}", insert=(x_start, y), fill='black'))

# Speichern der SVG-Datei
dwg.save()
