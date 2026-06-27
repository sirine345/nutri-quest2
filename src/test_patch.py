path = r'C:\Users\fzahi\Desktop\nutri-quest2\src\App.jsx'
with open(path, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()
start_idx = content.find('/* \u2550\u2550 DASHBOARD \u2550\u2550 */')
end_idx = content.find('export default function App()')
print(f'start={start_idx} end={end_idx}')
