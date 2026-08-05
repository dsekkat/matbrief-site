# test_mobile_390.py — passe mobile v6.71 : la maquette doit tenir dans 390 px (iPhone 14/15)
# Sert le dossier en http local (comme le lien d'essai) et mesure l'overflow horizontal
# écran par écran ; échoue si un écran déborde de plus de 6 px.
import http.server, socketserver, threading, os, sys
from playwright.sync_api import sync_playwright

os.chdir(os.path.dirname(os.path.abspath(__file__)))
PORT = 8932
srv = socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler)
threading.Thread(target=srv.serve_forever, daemon=True).start()

PUBLIC = ['home','matieres','polymeres','composer','demande','login','contact',
          'apropos','methodo','precision','faq','cgv','calendrier','glossaire']
CLIENT_TABS = ['bulletin','actus','graphs','archives','scope','compte']

fails, report = [], []

def width(pg):
    return pg.evaluate("Math.max(document.documentElement.scrollWidth, document.body.scrollWidth)")

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width':390, 'height':844}, device_scale_factor=2,
                    is_mobile=True, has_touch=True)
    pg.goto(f'http://localhost:{PORT}/Maquette_Site_v1.html')
    pg.wait_for_timeout(900)

    # bandeau : sur http, texte d'essai (jamais « visible par Driss »)
    ban = pg.inner_text('#mb-banner')
    if 'Driss' in ban: fails.append('bandeau privé visible sur http !')
    report.append(f"bandeau http : {ban[:60]!r}")

    for p in PUBLIC:
        pg.evaluate(f"go('{p}')"); pg.wait_for_timeout(350)
        w = width(pg); report.append(f"public/{p:<12} scrollWidth={w}")
        if w > 396: fails.append(f'public/{p} déborde ({w}px)')
        if p in ('home','composer'): pg.screenshot(path=f'shot_mob_{p}.png', full_page=False)

    # Espace client simulé (layout uniquement — pas d'appels API, garde SESSION_TOKEN)
    pg.evaluate("""() => {
        ACCOUNT={nom:'Test',societe:'Selfmatic',email:'t@x.com',lang:'fr'};
        setRole('client'); go('client');
    }""")
    pg.wait_for_timeout(500)
    for t in CLIENT_TABS:
        pg.evaluate(f"""() => {{
            const btns=[...document.querySelectorAll('.cl-tabs button')];
            const b=btns.find(x=>(x.getAttribute('onclick')||'').includes("'{t}'"));
            if(b) b.click();
        }}""")
        pg.wait_for_timeout(400)
        w = width(pg); report.append(f"client/{t:<12} scrollWidth={w}")
        if w > 396: fails.append(f'client/{t} déborde ({w}px)')
        if t in ('bulletin','graphs','scope'): pg.screenshot(path=f'shot_mob_cl_{t}.png')

    # admin (onglets internes + vue interne)
    pg.evaluate("setRole('admin')"); pg.wait_for_timeout(300)
    for t in ['users','demandes']:
        pg.evaluate(f"""() => {{
            const btns=[...document.querySelectorAll('.cl-tabs button')];
            const b=btns.find(x=>(x.getAttribute('onclick')||'').includes("'{t}'"));
            if(b) b.click();
        }}""")
        pg.wait_for_timeout(400)
        w = width(pg); report.append(f"admin/{t:<12} scrollWidth={w}")
        if w > 396: fails.append(f'admin/{t} déborde ({w}px)')
    pg.evaluate("go('dash')"); pg.wait_for_timeout(500)
    w = width(pg); report.append(f"admin/dash        scrollWidth={w}")
    if w > 396: fails.append(f'admin/dash déborde ({w}px)')
    pg.screenshot(path='shot_mob_admin_dash.png')

    # ouverture LOCALE (file:) : le bandeau privé de Driss doit rester
    pg2 = b.new_page(viewport={'width':390, 'height':844})
    pg2.goto('file://' + os.path.abspath('Maquette_Site_v1.html'))
    pg2.wait_for_timeout(600)
    ban2 = pg2.inner_text('#mb-banner')
    if 'Driss' not in ban2: fails.append('bandeau privé PERDU en ouverture file: !')
    report.append(f"bandeau file: {ban2[:60]!r}")
    b.close()

srv.shutdown()
print('\n'.join(report))
print('FAIL:\n  ' + '\n  '.join(fails) if fails else 'PASS — tous les écrans tiennent dans 390 px')
sys.exit(1 if fails else 0)
