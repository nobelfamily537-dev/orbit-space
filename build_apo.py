import json,re,urllib.parse
meta=json.load(open("/scratch/work/apimg/meta.json"))
import sys; sys.path.insert(0,"/scratch/work")
import apophis_en

SLUG="apophis-2029-close-approach"
EN_T="Apophis 2029: The Asteroid That Will Pass Closer Than Our Satellites"
HI_T="अपोफिस 2029: वह क्षुद्रग्रह जो हमारे सैटेलाइट से भी करीब से गुजरेगा"
EN_D="On 13 April 2029 asteroid Apophis passes 31,600 km above Earth — inside the satellite belt. What you will see, when, and why it is safe."
HI_D="13 अप्रैल 2029 को क्षुद्रग्रह अपोफिस पृथ्वी से 31,600 किमी ऊपर से गुजरेगा — सैटेलाइट पट्टी के अंदर। क्या दिखेगा, कब, और यह सुरक्षित क्यों है।"

def alt(t): return t.replace('"','&quot;').replace("&","&amp;")
def fig(m,w=None):
    return (f'<figure class="fig"><img src="/assets/img/{m["f"]}" alt="{alt(m["title"])}" loading="lazy" '
            f'width="{m["w"]}" height="{m["h"]}"><figcaption>{alt(m["title"])} '
            f'<span class="cr">&#183; {m["lic"]}</span></figcaption></figure>')
def hero():
    m=meta[0]
    return (f'<figure class="fig hero-fig"><img src="/assets/img/{m["f"]}" alt="{alt(m["title"])}" '
            f'loading="eager" fetchpriority="high" width="{m["w"]}" height="{m["h"]}"><figcaption>'
            f'{alt(m["title"])} <span class="cr">&#183; {m["lic"]}</span></figcaption></figure>')
def gallery(): return "".join(fig(m) for m in meta[1:])

def sharebar(title,path):
    t=urllib.parse.quote(title); u=urllib.parse.quote(f"https://space.anipix.me{path}",safe="")
    return (f'<div class="sharebar"><span class="sharelabel">Share</span>\n'
      f'<a class="sbtn" href="https://wa.me/?text={t}%20{u}" target="_blank" rel="noopener">WhatsApp</a>\n'
      f'<a class="sbtn" href="https://t.me/share/url?url={u}&text={t}" target="_blank" rel="noopener">Telegram</a>\n'
      f'<a class="sbtn" href="https://twitter.com/intent/tweet?url={u}&text={t}" target="_blank" rel="noopener">X</a>\n'
      f'<a class="sbtn" href="https://www.facebook.com/sharer/sharer.php?u={u}" target="_blank" rel="noopener">Facebook</a>\n'
      '<button class="sbtn" type="button" onclick="orbitCopy(this)">Copy link</button></div>\n'
      '<script>function orbitCopy(b){var u=location.href;\n'
      'if(navigator.clipboard){navigator.clipboard.writeText(u).then(function(){var o=b.textContent;b.textContent="Link copied";setTimeout(function(){b.textContent=o;},1800);}).catch(function(){prompt("Copy:",u);});}else{prompt("Copy:",u);}}</script>')

NEXT_EN=[("voyager-interstellar","Voyager: The Farthest Objects Humans Have Ever Built"),
         ("search-for-life","Are We Alone? The Search for Life in Space"),
         ("europa-clipper","Europa Clipper: Hunting for Life Under Europa&#x27;s Ice")]
NEXT_HI=[("voyager-interstellar","वॉयेजर: इंसानों की बनाई सबसे दूर की चीज़ें"),
         ("search-for-life","क्या हम अकेले हैं? अंतरिक्ष में जीवन की खोज"),
         ("europa-clipper","यूरोपा क्लिपर: यूरोपा की बर्फ के नीचे जीवन की तलाश")]

def nextblock(items,lang):
    p="/hi/articles/" if lang=="hi" else "/articles/"
    chips="".join(f'<a class="chip" href="{p}{s}.html">{t}</a>' for s,t in items)
    chips+=f'<a class="chip" href="{"/hi/index.html" if lang=="hi" else "/index.html"}">{"सभी लेख →" if lang=="hi" else "All articles →"}</a>'
    return f'<div class="next"><h3>{"आगे पढ़ें" if lang=="hi" else "Keep reading"}</h3><div class="chips">{chips}</div></div>'

def build(lang):
    tpl = "hi/articles/voyager-interstellar.html" if lang=="hi" else "articles/voyager-interstellar.html"
    t=open(tpl,encoding="utf-8").read()
    head=t[:t.index('<span class="badge">')].replace("voyager-interstellar",SLUG)
    title = HI_T if lang=="hi" else EN_T
    desc  = HI_D if lang=="hi" else EN_D
    badge = "&#9670; NASA &#183; क्षुद्रग्रह" if lang=="hi" else "&#9670; NASA &#183; Near-Earth asteroid"
    date  = "16 नवंबर 2026 को अपडेट" if lang=="hi" else "Updated 16 November 2026"
    read  = "9 मिनट पढ़ें" if lang=="hi" else "9 min read"
    body  = open("hi_apo.txt",encoding="utf-8").read() if lang=="hi" else apophis_en.APO_BODY
    nxt   = NEXT_HI if lang=="hi" else NEXT_EN
    head=re.sub(r'<title>.*?</title>', f'<title>{title}</title>', head, count=1, flags=re.S)
    head=re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{desc}">', head, count=1, flags=re.S)
    head=re.sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{title}">', head, count=1, flags=re.S)
    head=re.sub(r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="{desc}">', head, count=1, flags=re.S)
    tail=t[t.index('<footer>'):]
    urlp=("/hi/articles/" if lang=="hi" else "/articles/")+SLUG+".html"
    credit=("छवियां: NASA / JPL-Caltech / ESA / Wikimedia Commons (सार्वजनिक डोमेन व CC लाइसेंस)।" if lang=="hi"
            else "Images: NASA / JPL-Caltech / ESA / Wikimedia Commons (public domain and CC licensed).")
    main=(f'\n<span class="badge">{badge}</span>\n<h1>{title}</h1>\n'
          f'<div class="meta"><span>{date}</span><i></i><span>{read}</span></div>\n'
          + sharebar(title,urlp)+"\n"+hero()+"\n"
          + "<article>"+body+"</article>\n"
          + '<h2 class="sec">' + ("फोटो गैलरी" if lang=="hi" else "Photo gallery") + '</h2><div class="gallery">'
          + gallery() + '</div><p class="credit">'+credit+'</p>\n'
          + nextblock(nxt,lang) + "\n\n")
    out = f"hi/articles/{SLUG}.html" if lang=="hi" else f"articles/{SLUG}.html"
    open(out,"w",encoding="utf-8").write(head+main+tail)
    print(f"{out}: {len(head+main+tail)} bytes")

def card(lang):
    if lang=="hi":
        path="hi/index.html"
        c=(f'<a class="card" href="/hi/articles/{SLUG}.html"><span class="k">NASA &#183; क्षुद्रग्रह</span>'
           f'<h3>{HI_T}</h3><p>{HI_D}</p></a>')
        row=(f'<a class="mrow" href="/hi/articles/{SLUG}.html"><div class="yr">2026</div>'
             f'<div><h3>{HI_T}</h3><p>{HI_D}</p></div></a>')
    else:
        path="index.html"
        c=(f'<a class="card" href="/articles/{SLUG}.html"><span class="k">Asteroid &#183; Apophis</span>'
           f'<h3>{EN_T}</h3><p>{EN_D}</p></a>')
        row=(f'<a class="mrow" href="/articles/{SLUG}.html"><div class="yr">2026</div>'
             f'<div><h3>{EN_T}</h3><p>{EN_D}</p></div></a>')
    s=open(path,encoding="utf-8").read()
    if SLUG in s: return
    s=s.replace('<div class="grid">','<div class="grid">'+c,1)
    s=s.replace('<div class="mlist">','<div class="mlist">'+row,1)
    open(path,"w",encoding="utf-8").write(s)

build("en"); build("hi"); card("en"); card("hi")
sm=open("sitemap.xml",encoding="utf-8").read()
for pre in ("articles","hi/articles"):
    u=f"https://space.anipix.me/{pre}/{SLUG}.html"
    if u not in sm:
        sm=sm.replace("</urlset>",f'  <url><loc>{u}</loc><lastmod>2026-11-16</lastmod><changefreq>monthly</changefreq><priority>0.9</priority></url>\n</urlset>')
open("sitemap.xml","w",encoding="utf-8").write(sm)
print("sitemap urls:",sm.count("<url>"))
