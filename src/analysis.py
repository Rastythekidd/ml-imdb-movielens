"""Analiza pierwszego etapu: kontrola danych, statystyki i wykresy."""
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import csv, hashlib, html, importlib.metadata, json, re
import numpy as np
from openpyxl import load_workbook
from reportlab.graphics.shapes import Drawing, Rect, Line, Circle, String
from reportlab.graphics import renderPDF
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, Color

ROOT=Path(__file__).resolve().parents[1]
BLUE='#235B83'; TEAL='#19857C'; RED='#BA5454'; INK='#223245'; GRAY='#64748B'
TOKEN=re.compile(r"[a-z]+(?:'[a-z]+)?")
# Jawna lista słów pomijanych; zachowujemy przeczenia no/not/never.
STOP=set("""a an the and or but if then so because as at by for from in into of on to with without about above after again against all also am are be been before being below between both can could did do does doing down during each few further had has have having he her here hers herself him himself his how i im ive id ill is it its itself just me more most my myself now off once only other our ours ourselves out over own same she should some such than that their theirs them themselves there these they this those through too under until up very was we were what when where which while who whom why will would you your yours yourself yourselves dont doesnt didnt cant couldnt wont wouldnt isnt arent wasnt werent thats theres well get got much many even really one two first still think know way thing things people time make makes made see seen watching watched watch film films movie movies""".split())

def setup_fonts():
    choices=[Path('C:/Windows/Fonts/arial.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')]
    p=next((p for p in choices if p.exists()),None)
    if p is None: raise RuntimeError('Zainstaluj Arial lub DejaVu Sans, aby wyświetlić polskie znaki.')
    b=p.with_name('arialbd.ttf' if p.name=='arial.ttf' else 'DejaVuSans-Bold.ttf')
    pdfmetrics.registerFont(TTFont('Project',str(p)))
    pdfmetrics.registerFont(TTFont('ProjectBold',str(b if b.exists() else p)))

def read_book(name):
    file=ROOT/'data/original'/name
    if file.exists():
        w=load_workbook(file,read_only=True,data_only=True)
        rows=list(w.active.iter_rows(values_only=True));w.close()
    else:
        file=file.with_suffix('.csv')
        with file.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.reader(f))
        numeric={'id_uzytkownika','id_filmu','ocena','czas_unix','rok_premiery'}
        rows=[rows[0]]+[[int(v) if k in numeric else v for k,v in zip(rows[0],row)] for row in rows[1:]]
    headers=list(rows[0])
    return headers,[dict(zip(headers,row)) for row in rows[1:] if any(v is not None for v in row)]

def clean_text(s):
    return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',s))).strip()

def tokens(s): return TOKEN.findall(clean_text(s).lower())

def summary(v):
    a=np.asarray(v,dtype=float)
    return dict(n=len(a),mean=float(a.mean()),median=float(np.median(a)),std_sample=float(a.std(ddof=1)),
                min=float(a.min()),q1=float(np.quantile(a,.25)),q3=float(np.quantile(a,.75)),max=float(a.max()))

def ranks(v):
    order=sorted(range(len(v)),key=lambda i:v[i]);a=np.empty(len(v),float);i=0
    while i<len(order):
        j=i+1
        while j<len(order) and v[order[j]]==v[order[i]]:j+=1
        a[order[i:j]]=(i+1+j)/2;i=j
    return a

def quality(headers,rows):
    return dict(rows=len(rows),columns=len(headers),
        missing_by_column={k:sum(r[k] is None or (isinstance(r[k],str) and not r[k].strip()) for r in rows) for k in headers},
        duplicate_full_rows=len(rows)-len({tuple(r[k] for k in headers) for r in rows}),
        python_types={k:sorted({type(r[k]).__name__ for r in rows}) for k in headers})

def csv_write(p,rows):
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def text(d,x,y,s,size=10,color=INK,bold=False,anchor='start'):
    d.add(String(x,y,str(s),fontName='ProjectBold' if bold else 'Project',fontSize=size,fillColor=HexColor(color),textAnchor=anchor))

def base(title,subtitle=''):
    d=Drawing(520,300);d.add(Rect(0,0,520,300,fillColor=HexColor('#FFFFFF'),strokeColor=None))
    text(d,18,279,title,14,bold=True)
    if subtitle:text(d,18,260,subtitle,8.3,GRAY)
    return d

def bars(labels,values,title,subtitle='',color=BLUE,horizontal=False):
    d=base(title,subtitle);limit=max(values)*1.18 or 1
    left,bottom,width,height=(135,38,355,205) if horizontal else (50,48,440,190)
    for k in range(5):
        if horizontal:
            x=left+width*k/4;d.add(Line(x,bottom,x,bottom+height,strokeColor=HexColor('#E5EAF0')))
            text(d,x,bottom-15,f'{limit*k/4:.0f}',11,GRAY,anchor='middle')
        else:
            y=bottom+height*k/4;d.add(Line(left,y,left+width,y,strokeColor=HexColor('#E5EAF0')))
            text(d,left-8,y-3,f'{limit*k/4:.0f}',8,GRAY,anchor='end')
    for i,(lab,val) in enumerate(zip(labels,values)):
        if horizontal:
            step=height/len(values);y=bottom+height-(i+1)*step+step*.18
            d.add(Rect(left,y,width*val/limit,step*.62,fillColor=HexColor(color),strokeColor=None))
            text(d,left-8,y+step*.18,lab,11,anchor='end');text(d,left+width*val/limit+4,y+step*.18,str(val),8)
        else:
            step=width/len(values);x=left+i*step+step*.2
            d.add(Rect(x,bottom,step*.6,height*val/limit,fillColor=HexColor(color),strokeColor=None))
            text(d,x+step*.3,bottom+height*val/limit+6,str(val),9,anchor='middle')
            text(d,x+step*.3,bottom-17,lab,11,anchor='middle')
    return d

def boxes(groups):
    d=base('Długość recenzji według sentymentu','Wąsy: do 1,5 IQR; punkty: wartości odstające. Długość = liczba tokenów angielskich.')
    left,bottom,width,height=55,55,430,180;limit=max(max(v) for v in groups.values())*1.08
    for k in range(5):
        y=bottom+height*k/4;d.add(Line(left,y,left+width,y,strokeColor=HexColor('#E5EAF0')))
        text(d,left-8,y-3,f'{limit*k/4:.0f}',8,GRAY,anchor='end')
    text(d,12,240,'słowa',8,GRAY)
    for i,(label,vals) in enumerate(groups.items()):
        a=np.asarray(vals);q1,med,q3=np.quantile(a,[.25,.5,.75]);iqr=q3-q1
        low=min(a[a>=q1-1.5*iqr]);high=max(a[a<=q3+1.5*iqr]);x=left+width*(i+.5)/len(groups)
        yy=lambda v:bottom+height*v/limit
        d.add(Line(x,yy(low),x,yy(high),strokeColor=HexColor(INK)))
        for v in (low,high):d.add(Line(x-16,yy(v),x+16,yy(v),strokeColor=HexColor(INK)))
        d.add(Rect(x-42,yy(q1),84,yy(q3)-yy(q1),fillColor=HexColor('#DDECF2'),strokeColor=HexColor(BLUE)))
        d.add(Line(x-42,yy(med),x+42,yy(med),strokeColor=HexColor(TEAL),strokeWidth=2))
        for v in a[(a<q1-1.5*iqr)|(a>q3+1.5*iqr)]:d.add(Circle(x,yy(v),2,fillColor=HexColor(RED),strokeColor=None))
        text(d,x,bottom-20,label,10,anchor='middle');text(d,x,yy(med)+6,f'mediana: {med:.1f}'.replace('.',','),9,anchor='middle')
    return d

def scatter(rows,rho):
    d=base('Rok premiery a ocena MovieLens',f'Punkt = ocena; przesunięcie pionowe tylko dla czytelności. Korelacja Spearmana: {rho:.3f}.')
    left,bottom,width,height=52,50,440,185;years=[r['rok_premiery'] for r in rows];lo=min(years)-2;hi=max(years)+2
    for rating in range(1,6):
        y=bottom+height*(rating-1)/4;d.add(Line(left,y,left+width,y,strokeColor=HexColor('#E5EAF0')))
        text(d,left-10,y-3,str(rating),9,anchor='end')
    for year in range((lo//10+1)*10,hi+1,10):
        text(d,left+width*(year-lo)/(hi-lo),bottom-18,str(year),8,GRAY,anchor='middle')
    rng=np.random.default_rng(42)
    for r in rows:
        x=left+width*(r['rok_premiery']-lo)/(hi-lo);y=bottom+height*(r['ocena']-1+rng.uniform(-.1,.1))/4
        d.add(Circle(x,y,2.5,fillColor=Color(.14,.36,.51,alpha=.5),strokeColor=None))
    text(d,270,14,'Rok premiery',9,GRAY,anchor='middle')
    return d

def main():
    setup_fonts();results=ROOT/'results';figdir=results/'figures';derived=ROOT/'data/derived'
    for p in (results,figdir,derived):p.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((ROOT/'sources/source_manifest.json').read_text(encoding='utf-8'))
    loaded={name:read_book(name) for name in ['IMDb_recenzje.xlsx','MovieLens_liczby.xlsx','MovieLens_filmy.xlsx']}
    imdb=loaded['IMDb_recenzje.xlsx'][1];num=loaded['MovieLens_liczby.xlsx'][1];view=loaded['MovieLens_filmy.xlsx'][1]
    checks={name:quality(*pair) for name,pair in loaded.items()}
    hashes={}
    for name,(headers,records) in loaded.items():
        file=ROOT/'data/original'/name
        if file.exists():
            digest=hashlib.sha256(file.read_bytes()).hexdigest()
            assert digest==manifest['input_file_sha256'][name],f'Niezgodna suma kontrolna arkusza: {name}'
            hashes[name]=digest
        else:
            file=file.with_suffix('.csv');hashes[file.name]=hashlib.sha256(file.read_bytes()).hexdigest()
        canonical=json.dumps([[r[k] for k in headers] for r in records],ensure_ascii=False,separators=(',',':')).encode('utf-8')
        assert hashlib.sha256(canonical).hexdigest()==manifest['canonical_rows_sha256'][name],f'Niezgodne wartości wierszy: {name}'
    for name,q in checks.items():
        assert q['rows']==200 and q['duplicate_full_rows']==0,(name,q)
        assert not any(q['missing_by_column'].values()),(name,q)
    numcols=loaded['MovieLens_liczby.xlsx'][0]
    same=all(all(a[k]==b[k] for k in numcols) for a,b in zip(num,view))
    assert same,'Widoki MovieLens zawierają różne dane.'
    assert all(isinstance(v,int) and not isinstance(v,bool) for r in num for v in r.values())
    assert all(1<=r['ocena']<=5 and r['id_filmu']>0 and r['id_uzytkownika']>0 for r in num)
    assert len({(r['id_uzytkownika'],r['id_filmu']) for r in num})==200
    for r,s in zip(imdb,manifest['imdb_rows']):
        assert hashlib.sha256(r['tekst_recenzji'].encode()).hexdigest()==s['text_sha256']
        assert r['id_imdb']==s['id_imdb'] and r['tytul_filmu']==s['title_snapshot']
        assert r['sentyment']==s['sentiment']
        assert r['link_imdb']=='https://www.imdb.com/title/'+r['id_imdb']+'/'
    assert len({r['tekst_recenzji'] for r in imdb})==200
    assert len({clean_text(r['tekst_recenzji']).lower() for r in imdb})==200
    assert Counter(r['sentyment'] for r in imdb)=={'negatywny':100,'pozytywny':100}
    features=[];counts={};dfs={};groups={};frequency_rows=[]
    for label in ['negatywny','pozytywny']:
        subset=[r for r in imdb if r['sentyment']==label]
        groups[label]=[len(tokens(r['tekst_recenzji'])) for r in subset]
        content=[[t for t in tokens(r['tekst_recenzji']) if len(t)>2 and t not in STOP] for r in subset]
        counts[label]=Counter(t for ts in content for t in ts)
        dfs[label]=Counter(t for ts in content for t in sorted(set(ts)))
        for word,count in sorted(counts[label].items(),key=lambda item:(-item[1],item[0])):
            frequency_rows.append(dict(sentiment=label,word=word,token_count=count,documents=dfs[label][word]))
    for i,r in enumerate(imdb):
        features.append(dict(row_index=i,id_imdb=r['id_imdb'],sentiment=r['sentyment'],
            word_count=len(tokens(r['tekst_recenzji'])),character_count=len(clean_text(r['tekst_recenzji'])),
            contained_html=bool(re.search(r'<[^>]+>',r['tekst_recenzji']))))
    enriched=[]
    for r in view:
        dt=datetime.fromtimestamp(r['czas_unix'],tz=timezone.utc)
        assert r['rok_premiery']<=dt.year
        enriched.append({**r,'data_oceny_utc':dt.isoformat(),'wiek_filmu_w_latach':dt.year-r['rok_premiery']})
    ratings=[r['ocena'] for r in num];years=[r['rok_premiery'] for r in num]
    rho=float(np.corrcoef(ranks(years),ranks(ratings))[0,1])
    film_summary=[]
    for mid in sorted({r['id_filmu'] for r in num}):
        rows=[r for r in view if r['id_filmu']==mid]
        film_summary.append(dict(id_filmu=mid,tytul_filmu=rows[0]['tytul_filmu'],rok_premiery=rows[0]['rok_premiery'],
            liczba_ocen=len(rows),srednia_ocena=float(np.mean([r['ocena'] for r in rows]))))
    film_rho=float(np.corrcoef(ranks([r['rok_premiery'] for r in film_summary]),ranks([r['srednia_ocena'] for r in film_summary]))[0,1])
    users=Counter(r['id_uzytkownika'] for r in num);films=Counter(r['id_filmu'] for r in num);imdb_films=Counter(r['id_imdb'] for r in imdb)
    decades=[]
    for decade in sorted({y//10*10 for y in years}):
        vals=[r['ocena'] for r in num if r['rok_premiery']//10*10==decade]
        decades.append(dict(decade=decade,n=len(vals),mean=float(np.mean(vals)),median=float(np.median(vals))))
    out=dict(analysis_date='2026-10-27',quality=checks,input_sha256=hashes,movielens_views_identical=same,
      imdb=dict(n=len(imdb),classes=dict(Counter(r['sentyment'] for r in imdb)),unique_titles=len(imdb_films),
        max_reviews_per_title=max(imdb_films.values()),titles_with_multiple_reviews=sum(v>1 for v in imdb_films.values()),
        html_reviews=sum(f['contained_html'] for f in features),word_counts={k:summary(v) for k,v in groups.items()},
        overall_word_count=summary([f['word_count'] for f in features]),
        median_difference_positive_minus_negative=float(np.median(groups['pozytywny'])-np.median(groups['negatywny'])),
        top_tokens={k:counts[k].most_common(12) for k in counts},
        top_document_frequency={k:dfs[k].most_common(12) for k in dfs},
        metadata_types=dict(Counter(r['title_metadata']['title_type'] for r in manifest['imdb_rows']))),
      movielens=dict(n=len(num),unique_users=len(users),unique_movies=len(films),rating_summary=summary(ratings),
        year_summary=summary(years),rating_counts=dict(sorted(Counter(ratings).items())),
        rating_date_min_utc=min(r['data_oceny_utc'] for r in enriched),rating_date_max_utc=max(r['data_oceny_utc'] for r in enriched),
        rating_counts_per_user=dict(sorted(Counter(users.values()).items())),rating_counts_per_movie=dict(sorted(Counter(films.values()).items())),
        single_rating_movies=sum(v==1 for v in films.values()),single_rating_users=sum(v==1 for v in users.values()),
        max_ratings_per_movie=max(films.values()),max_ratings_per_user=max(users.values()),
        spearman_year_rating=rho,spearman_year_film_mean=film_rho,decades=decades,
        rating_share_4_5=sum(v>=4 for v in ratings)/len(ratings)))
    csv_write(derived/'imdb_features.csv',features);csv_write(derived/'movielens_enriched.csv',enriched)
    csv_write(results/'word_frequencies.csv',frequency_rows);csv_write(results/'movie_statistics.csv',film_summary)
    csv_write(results/'ratings_by_decade.csv',decades)
    (results/'summary.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    (results/'stopwords.txt').write_text('\n'.join(sorted(STOP))+'\n',encoding='utf-8')
    drawings={
      '01_sentiment_balance':bars(['Negatywne','Pozytywne'],[100,100],'Skład próby IMDb','Równowaga klas wynika z doboru próby, a nie z rozkładu opinii w IMDb.',TEAL),
      '02_review_length':boxes(groups),
      '03_rating_distribution':bars([str(i) for i in range(1,6)],[ratings.count(i) for i in range(1,6)],'Rozkład ocen MovieLens','200 ocen użytkownik-film; skala porządkowa od 1 do 5.'),
      '04_release_decades':bars([str(r['decade']) for r in decades],[r['n'] for r in decades],'Liczba ocen według dekady premiery','Jedna obserwacja = jedna ocena, nie jeden unikalny film.'),
      '05_year_rating':scatter(num,rho),
      '06_negative_words':bars([w for w,c in dfs['negatywny'].most_common(10)],[c for w,c in dfs['negatywny'].most_common(10)],'Słowa w recenzjach negatywnych','Liczba recenzji zawierających słowo; po odfiltrowaniu jawnej listy stopwords.',RED,True),
      '07_positive_words':bars([w for w,c in dfs['pozytywny'].most_common(10)],[c for w,c in dfs['pozytywny'].most_common(10)],'Słowa w recenzjach pozytywnych','Liczba recenzji zawierających słowo; po odfiltrowaniu jawnej listy stopwords.',TEAL,True)}
    for name,d in drawings.items():renderPDF.drawToFile(d,str(figdir/(name+'.pdf')))
    versions={m:importlib.metadata.version(m) for m in ['numpy','openpyxl','reportlab']}
    (results/'environment.json').write_text(json.dumps(versions,indent=2),encoding='utf-8')
    print('Analiza gotowa: 200 recenzji, 200 ocen; wyniki zapisano w results.')

if __name__=='__main__':main()
