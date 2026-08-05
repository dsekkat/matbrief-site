# test_otp_paste.py — v6.72 : coller ou autofiller le code OTP remplit les 6 cases
import http.server, socketserver, threading, os, sys
from playwright.sync_api import sync_playwright

os.chdir(os.path.dirname(os.path.abspath(__file__)))
PORT = 8941
srv = socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler)
threading.Thread(target=srv.serve_forever, daemon=True).start()

fails = []
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page()
    pg.goto(f'http://localhost:{PORT}/Maquette_Site_v1.html'); pg.wait_for_timeout(700)
    pg.evaluate("go('login')")
    pg.evaluate("document.getElementById('login-step1').classList.add('hidden');"
                "document.getElementById('login-step2').classList.remove('hidden');")
    boxes = pg.locator('#login-step2 .otp')

    # 1) collage système (événement paste) sur la 1re case
    boxes.nth(0).focus()
    pg.evaluate("""() => {
      const dt = new DataTransfer(); dt.setData('text/plain','4 8 3 9 2 0');
      document.querySelector('#login-step2 .otp').dispatchEvent(
        new ClipboardEvent('paste',{clipboardData:dt,bubbles:true,cancelable:true}));
    }""")
    v1 = [boxes.nth(i).input_value() for i in range(6)]
    if v1 != list('483920'): fails.append(f'paste 1re case: {v1}')

    # 2) AUTOFILL simulé : tout le code atterrit dans la 3e case via input (pas de paste)
    pg.evaluate("document.querySelectorAll('#login-step2 .otp').forEach(b=>b.value='')")
    pg.evaluate("""() => {
      const bx = document.querySelectorAll('#login-step2 .otp')[2];
      bx.value = '571236';
      bx.dispatchEvent(new Event('input',{bubbles:true}));
    }""")
    v2 = [boxes.nth(i).input_value() for i in range(6)]
    if v2 != list('571236'): fails.append(f'autofill case 3: {v2}')

    # 3) saisie manuelle : 1 chiffre par case, avance auto intacte
    pg.evaluate("document.querySelectorAll('#login-step2 .otp').forEach(b=>b.value='')")
    boxes.nth(0).focus()
    for d in '123456': pg.keyboard.type(d, delay=30)
    v3 = [boxes.nth(i).input_value() for i in range(6)]
    if v3 != list('123456'): fails.append(f'saisie manuelle: {v3}')

    # 4) autocomplete=one-time-code présent sur la 1re case de chaque groupe
    ac = pg.evaluate("['#login-step2','#login-step3','#login-enroll'].map(s=>"
                     "document.querySelector(s+' .otp').getAttribute('autocomplete'))")
    if ac != ['one-time-code']*3: fails.append(f'autocomplete: {ac}')
    b.close()
srv.shutdown()
print('FAIL: '+'; '.join(fails) if fails else 'PASS — collage, autofill, saisie manuelle, autocomplete OK')
sys.exit(1 if fails else 0)
