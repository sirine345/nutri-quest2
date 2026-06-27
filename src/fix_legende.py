path = r'C:\Users\fzahi\Desktop\nutri-quest2\src\App.jsx'
with open(path, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

old = '<Card title="Distribution MEDAS"><div style={{ position:"relative", height:190 }}><canvas id="barMedas" role="img" aria-label="MEDAS dist">MEDAS dist</canvas></div></Card>'

new = '''<Card title="Distribution MEDAS">
  <Leg items={[
    ["#e53935","0-2 : tres faible adhesion"],
    ["#f57c00","3-5 : faible"],
    ["#ffcc00","6-8 : moderee"],
    ["#9ACD32","9-11 : bonne"],
    ["#2e7d32","12-14 : excellente"]
  ]} />
  <div style={{ position:"relative", height:190 }}><canvas id="barMedas" role="img" aria-label="MEDAS dist">MEDAS dist</canvas></div>
</Card>'''

if old in content:
    content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('OK legende ajoutee !')
else:
    print('ERREUR bloc non trouve')
