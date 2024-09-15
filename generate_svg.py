import os
import requests
import svgwrite

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

# Berechnen der Gesamtzahl der Repositories
total_repos = sum(languages.values())

# Erstellen des SVG-Dokuments im Dark Theme
dwg = svgwrite.Drawing('top-langs.svg', profile='tiny', size=(210*svgwrite.mm, 297*svgwrite.mm))
dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='black'))

x_start = 10
y_start = 10
x_offset = 80
y_offset = 20
bar_height = 15
max_bar_width = 150

# Farben für die Sprachen
colors = [
    '#FF5733', '#33FF57', '#3357FF', '#F333FF', '#33FFF5',
    '#FF33A1', '#A1FF33', '#FF8C33', '#8C33FF', '#33FF8C'
]

# Zeichnen der Sprachstatistiken
for index, (lang, count) in enumerate(languages.items()):
    y = y_start + index * y_offset
    bar_width = (count / total_repos) * max_bar_width
    color = colors[index % len(colors)]
    
    # Zeichnen des Balkens
    dwg.add(dwg.rect(insert=(x_start, y), size=(bar_width, bar_height), fill=color))
    
    # Zeichnen des Textes
    dwg.add(dwg.text(f"{lang}: {count} ({(count / total_repos) * 100:.2f}%)", insert=(x_start + bar_width + 10, y + bar_height - 2), fill='white', font_size='15px', font_family='Arial'))

# Speichern der SVG-Datei
dwg.save()
