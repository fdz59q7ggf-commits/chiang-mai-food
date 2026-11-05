#!/usr/bin/env python3
"""由 foods.json 產生 README.md、food.kml（可匯入 Google 我的地圖）與 index.html（美食總圖）。"""
import json, html, urllib.parse, pathlib

D = pathlib.Path(__file__).parent
foods = json.loads((D / 'foods.json').read_text(encoding='utf-8'))

def gmap(s):
    q = s['name'] + (' Chiang Rai' if s['area'] == '清萊' else ' Chiang Mai')
    return 'https://www.google.com/maps/search/?api=1&query=' + urllib.parse.quote(q) + '&hl=en'

for s in foods:
    s['gmap'] = gmap(s)
    s['gmap_th'] = s['gmap'].replace('&hl=en', '&hl=th')
    s.setdefault('klook', '')

AREAS = ['夜市/長康路', '濱江區', '古城', '古城南/Wualai', '寧曼', '郊區', '清萊', '清邁（位置未確認）']
MIC = {'Bib Gourmand': '🍽️ 必比登', '米其林推薦': '⭐ 米其林推薦', '—': ''}

# ---------- README ----------
n_bib = sum(s['michelin'] == 'Bib Gourmand' for s in foods)
n_sel = sum(s['michelin'] == '米其林推薦' for s in foods)
md = ['# 清邁・清萊美食總圖', '',
      f'6 人清邁行程（2026/11/11–11/18，住長康路夜市旁）用的美食清單，共 **{len(foods)} 家**：米其林必比登 {n_bib} 家、米其林推薦 {n_sel} 家，其他是在地人氣店、市場和咖啡。', '',
      '- 🌐 **網址**：https://fdz59q7ggf-commits.github.io/chiang-mai-food/',
      '- 🗺️ **互動總地圖**：打開 [`index.html`](index.html)，可以依區域、類型、米其林篩選；金框標記＝米其林',
      '- 🛺 **給司機看**：每家店都有「給司機看（泰文）」按鈕，大字泰文店名＋泰文 Google 地圖',
      '- 📍 **Google 我的地圖版**：[Google 我的地圖](https://www.google.com/maps/d/) → 建立新地圖 → 匯入 → 上傳 [`food.kml`](food.kml)', '',
      '> ⚠️ 地圖標記為概略位置，精確位置以每家的 Google 地圖連結為準；「位置未確認」的店不會出現在地圖上。米其林標示依 2026 版報導與網路資料整理，沒辦法逐家對照官網；營業時間、價格可能變動，出發前請再確認。', '',
      '## 必吃泰北菜', '',
      '| 菜名 | 是什麼 | 哪裡吃 |', '|---|---|---|',
      '| Khao Soi 咖哩麵 | 椰奶咖哩湯麵＋炸脆麵，清邁代表 | Khao Soi Mae Sai、Khun Yai、Khao Soi Islam、清萊 Phor Jai |',
      '| Khanom Jeen Nam Ngiao | 米線配番茄排骨辣湯，在地人的早餐 | Sanpakoi Kanomjeen、清萊 Paa Suk |',
      '| Sai Ua 泰北香腸 | 香茅、檸檬葉香料豬肉腸 | 瓦洛洛市場、Tong Tem Toh、各大夜市 |',
      '| Nam Prik Noom 青辣椒醬 | 烤青辣椒搗的沾醬，配炸豬皮、蔬菜 | Huen Muan Jai、Tong Tem Toh |',
      '| Gaeng Hang Lay 豬肉咖哩 | 緬甸風、不辣、帶薑和羅望子的燉豬肉 | Aroon Rai、Huen Phen |',
      '| Khao Kha Moo 豬腳飯 | 滷豬腳配酸菜、滷蛋 | 北門牛仔帽阿姨、清邁門夜市 |',
      '| Gai Yang 炭烤雞 | 配青木瓜沙拉、糯米飯 | SP Chicken、Cherng Doi |',
      '| Khantoke 帝王餐 | 矮桌上一整桌泰北菜＋傳統舞蹈 | 老清邁文化中心（一日遊選單「輕鬆日」） |', '']
for area in AREAS:
    rows = [s for s in foods if s['area'] == area]
    if not rows: continue
    md += [f'## {area}', '', '| 店名 | 類型 | 米其林 | 必點 | 價格(銖/人) | 營業時間 | 行程 | 地圖 |', '|---|---|---|---|---|---|---|---|']
    for s in rows:
        th = f"<br>{s['name_th']}" if s['name_th'] else ''
        md.append(f"| **{s['zh']}**<br>{s['name']}{th} | {s['cat']} | {MIC[s['michelin']] or '—'} | {s['dish']} | {s['price']} | {s['hours']} | {s['trip'] or '—'} | [📍 英文]({s['gmap']})<br>[🛺 泰文]({s['gmap_th']}) |")
    md.append('')
md += ['## 資料來源', '',
       '- MICHELIN Guide Thailand 2026 Bib Gourmand 報導（Khaosod English、Chiang Mai Citylife）',
       '- Eating Thai Food、2foodtrippers、Will Fly for Food、Lonely Planet、Time Out Chiang Mai 等美食文章',
       '- 原行程網頁「米其林＆美食清單」', '',
       '## 相關網站', '',
       '- 清邁行程規劃：https://github.com/fdz59q7ggf-commits/Chiang-Mai',
       '- 清邁按摩總圖：https://fdz59q7ggf-commits.github.io/chiang-mai-massage/', '',
       '## 更新方式', '', '編輯 `foods.json` 後執行 `python3 build.py`，會重新產生 README.md、food.kml、index.html。', '']
(D / 'README.md').write_text('\n'.join(md), encoding='utf-8')

# ---------- KML ----------
e = html.escape
pm = {}
for s in foods:
    if not s['located']: continue
    d = f"{s['name']}<br>{s['name_th']}<br>{MIC[s['michelin']]}<br>必點：{s['dish']}<br>{s['desc']}<br>價格：{s['price']} 銖/人<br>營業：{s['hours']}<br>{s['gmap']}"
    pm[s['id']] = f"<Placemark><name>{e(s['zh'])}</name><description><![CDATA[{d}]]></description><Point><coordinates>{s['lng']},{s['lat']},0</coordinates></Point></Placemark>"
folders = ''.join(f"<Folder><name>{e(a)}</name>" + ''.join(pm[s['id']] for s in foods if s['area'] == a and s['id'] in pm) + '</Folder>' for a in AREAS)
(D / 'food.kml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>清邁清萊美食總圖</name>{folders}</Document></kml>\n', encoding='utf-8')

# ---------- index.html ----------
tpl = (D / 'template.html').read_text(encoding='utf-8')
(D / 'index.html').write_text(tpl.replace('/*SHOPS*/[]', json.dumps(foods, ensure_ascii=False)), encoding='utf-8')
print('built', len(foods), 'places,', len(pm), 'on map')
