import pandas as pd
import json

df = pd.read_excel('3000(注释版).xlsx')

words = []
for _, row in df.iterrows():
    word = str(row['Word']).strip() if pd.notna(row['Word']) else ''
    uk = str(row['UK Phonetics']).strip() if pd.notna(row['UK Phonetics']) else ''
    us = str(row['US Phonetics']).strip() if pd.notna(row['US Phonetics']) else ''
    paraphrase = str(row['Paraphrase']).strip() if pd.notna(row['Paraphrase']) else ''
    if word:
        words.append({
            'w': word,
            'uk': uk,
            'us': us,
            'p': paraphrase
        })

js_data = f'const WORDS = {json.dumps(words, ensure_ascii=False, indent=2)};'

with open('words_data.js', 'w', encoding='utf-8') as f:
    f.write(js_data)

print(f'Parsed {len(words)} words to words_data.js')
