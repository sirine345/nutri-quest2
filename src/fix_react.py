path = r'C:\Users\fzahi\Desktop\nutri-quest2\src\App.jsx'
with open(path, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

content = content.replace('React.useState(', 'useState(')
content = content.replace('React.useEffect(', 'useEffect(')
content = content.replace('React.useRef(', 'useRef(')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('OK corrige !')
