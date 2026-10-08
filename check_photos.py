#!/usr/bin/env python3
"""Проверка фото: python check_photos.py [photo_test_set.csv | photo_manifest.csv]
Показывает, какие файлы манифеста уже лежат в assets/cars, что это настоящие растровые
изображения (WebP/PNG/JPG), их размер, и находит дубликаты (одинаковое содержимое у разных файлов)."""
import csv,sys,os,hashlib
from PIL import Image
here=os.path.dirname(os.path.abspath(__file__))
mf=sys.argv[1] if len(sys.argv)>1 else os.path.join(here,'photo_test_set.csv')
rows=list(csv.DictReader(open(mf,encoding='utf-8-sig')))
ok=miss=bad=0;seen={}
for r in rows:
    p=os.path.join(here,r['file'])
    if not os.path.exists(p): miss+=1; continue
    try:
        im=Image.open(p); im.verify(); w,h=Image.open(p).size
    except Exception as e:
        bad+=1; print('НЕ ИЗОБРАЖЕНИЕ:',r['file'],e); continue
    d=hashlib.md5(open(p,'rb').read()).hexdigest()
    if d in seen: print('ДУБЛИКАТ:',r['file'],'=',seen[d])
    seen[d]=r['file']; ok+=1
    print(f"OK {r['file']} {w}x{h} {os.path.getsize(p)//1024} КБ")
print(f"Готово: {ok}, нет файла: {miss}, повреждено: {bad}, всего в списке: {len(rows)}")
