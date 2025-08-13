from flask import Flask, render_template_string, request, jsonify
import stripe

# -------- CONFIG --------
STRIPE_SECRET_KEY = "sk_test_51RvQBcEFDJeGszw3nkAi1LfCpH5elkDKHMU7Q0IBGkMaJKFfQICFtpgHQZ8ZhP2m2BpCvxm8V9RZqLdPIuGXCYvE00YFYkAj2L"
stripe.api_key = STRIPE_SECRET_KEY
CURRENCY = "mxn"
AMOUNT = 2000  # 20.00 MXN

app = Flask(__name__)

LOGOS_SVG = """
<div style="display:flex; justify-content:center; gap:50px; margin-bottom:40px;">
  <!-- Visa -->
  <svg xmlns="http://www.w3.org/2000/svg" width="130" height="55" viewBox="0 0 130 55" style="filter: drop-shadow(0 3px 3px rgba(0,0,0,0.25)); cursor: default;">
    <rect width="130" height="55" rx="12" ry="12" fill="#4b506d" />
    <text x="65" y="37" fill="#c1c4dc" font-family="Arial Black, sans-serif" font-size="32" font-weight="900" text-anchor="middle" letter-spacing="7" style="user-select:none;">
      VISA
    </text>
  </svg>

  <!-- Mastercard -->
  <svg xmlns="http://www.w3.org/2000/svg" width="130" height="55" viewBox="0 0 130 55" style="filter: drop-shadow(0 3px 3px rgba(0,0,0,0.25)); cursor: default;">
    <circle cx="50" cy="27" r="23" fill="#af1f1f"/>
    <circle cx="80" cy="27" r="23" fill="#cd9e42"/>
    <circle cx="65" cy="27" r="14" fill="#b86600" style="mix-blend-mode: multiply;"/>
    <text x="65" y="50" fill="#e5e5e5" font-family="Arial Black, sans-serif" font-size="16" font-weight="900" text-anchor="middle" letter-spacing="0" style="user-select:none;">
      Mastercard
    </text>
  </svg>
</div>
"""

LANDING_PAGE = f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>AN0M4LY</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Source+Code+Pro:wght@700&display=swap');
  * {{
    box-sizing: border-box;
  }}
  body, html {{
    margin: 0; padding: 0;
    height: 100%;
    background: linear-gradient(135deg, #2c3e50, #4b6a78);
    font-family: 'Source Code Pro', monospace;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #bec8d2;
    user-select: none;
  }}
  .container {{
    text-align: center;
    width: 350px;
  }}
  h1 {{
    font-size: 80px;
    font-weight: 900;
    letter-spacing: 16px;
    margin-bottom: 50px;
    color: #a9bacd;
    user-select:none;
  }}
  button {{
    font-size: 26px;
    padding: 18px 60px;
    background: #4b506d;
    border: 3px solid #bec8d2;
    border-radius: 15px;
    color: #bec8d2;
    cursor: pointer;
    font-weight: 900;
    transition: background 0.3s ease, box-shadow 0.3s ease;
    width: 100%;
    max-width: 350px;
  }}
  button:hover {{
    background: #bec8d2;
    color: #2c3e50;
    box-shadow:
      0 0 15px #bec8d2,
      inset 0 0 8px #bec8d2;
  }}
</style>
</head>
<body>
  <div class="container">
    {LOGOS_SVG}
    <h1>AN0M4LY</h1>
    <button onclick="window.location.href='/checker'">Ingresar</button>
  </div>
</body>
</html>
"""

CHECKER_PAGE = f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>AN0M4LY CHECK</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Source+Code+Pro:wght@700&display=swap');
  * {{
    box-sizing: border-box;
  }}
  body {{
    margin: 0; padding: 0;
    min-height: 100vh;
    background: linear-gradient(135deg, #283046, #1a2433);
    font-family: 'Source Code Pro', monospace;
    color: #a9bacd;
    user-select: none;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}
  .container {{
    margin-top: 40px;
    background: rgba(40, 48, 70, 0.95);
    border-radius: 16px;
    box-shadow:
      0 0 20px 5px rgba(169, 186, 205, 0.35),
      inset 0 0 12px 2px rgba(169, 186, 205, 0.5);
    padding: 30px 40px 40px;
    width: 400px;
    max-width: 90vw;
  }}
  .logos-top {{
    display: flex;
    justify-content: center;
    gap: 50px;
    margin-bottom: 40px;
  }}
  h1 {{
    text-align: center;
    font-size: 44px;
    font-weight: 900;
    letter-spacing: 5px;
    margin-bottom: 35px;
    color: #bec8d2;
    user-select:none;
  }}
  textarea {{
    width: 100%;
    height: 150px;
    background: #1f2a3a;
    border: 2px solid #a9bacd;
    border-radius: 12px;
    padding: 15px;
    font-family: monospace;
    font-size: 18px;
    color: #d0d8e8;
    resize: none;
    outline: none;
    box-shadow: inset 0 0 8px #a9bacd;
    transition: border-color 0.3s ease;
  }}
  textarea:focus {{
    border-color: #bec8d2;
    box-shadow: 0 0 12px #bec8d2;
  }}
  button {{
    width: 100%;
    margin-top: 20px;
    padding: 16px;
    background: #4b506d;
    border: none;
    border-radius: 14px;
    font-weight: 900;
    font-size: 20px;
    color: #bec8d2;
    cursor: pointer;
    box-shadow: 0 0 15px #4b506d;
    transition: background 0.3s ease, box-shadow 0.3s ease;
  }}
  button:hover {{
    background: #bec8d2;
    box-shadow:
      0 0 25px #bec8d2,
      inset 0 0 15px #bec8d2;
    color: #1a2433;
  }}
  #results {{
    margin-top: 30px;
    max-height: 240px;
    overflow-y: auto;
    padding-right: 10px;
  }}
  .result-item {{
    background: rgba(169, 186, 205, 0.15);
    padding: 14px 20px;
    border-radius: 14px;
    margin-bottom: 14px;
    font-weight: 700;
    font-size: 17px;
    user-select: text;
    box-shadow: 0 0 8px rgba(169, 186, 205, 0.2);
  }}
  .live {{
    color: #a9bacd;
    font-weight: 900;
  }}
  .dead {{
    color: #c97878;
    font-weight: 900;
  }}
  .contacts {{
    text-align: center;
    margin-top: 50px;
    font-weight: 700;
    font-size: 15px;
    user-select:none;
  }}
  .contacts a {{
    color: #a9bacd;
    margin: 0 15px;
    text-decoration: none;
    font-weight: 800;
    transition: color 0.3s ease;
  }}
  .contacts a:hover {{
    color: #bec8d2;
  }}
  /* Scrollbar estilizada para resultados */
  #results::-webkit-scrollbar {{
    width: 8px;
  }}
  #results::-webkit-scrollbar-track {{
    background: transparent;
  }}
  #results::-webkit-scrollbar-thumb {{
    background-color: #4b506d;
    border-radius: 20px;
  }}

  /* Progress bar container */
  #progressContainer {{
    width: 100%;
    background-color: #2f3a52;
    border-radius: 12px;
    margin-top: 15px;
    height: 14px;
    overflow: hidden;
  }}

  /* Progress bar */
  #progressBar {{
    height: 14px;
    width: 0%;
    background-color: #bec8d2;
    border-radius: 12px;
    transition: width 0.25s ease;
  }}
</style>
</head>
<body>
  <div class="container">
    {LOGOS_SVG}
    <h1>AN0M4LY CHECK</h1>
    <form onsubmit="return checkBatch(event);">
      <textarea id="cardsInput" placeholder="Número|MM|AAAA|CVC" autocomplete="off" spellcheck="false"></textarea>
      <button type="submit">CHECK</button>
    </form>
    <div id="progressContainer" style="display:none;">
      <div id="progressBar"></div>
    </div>
    <div id="results"></div>
    <div class="contacts">
      Contacto creador: <a href="https://t.me/LooKsCrazy0" target="_blank" rel="noopener">@LooKsCrazy0</a> |
      Canal oficial: <a href="https://t.me/AN0M4LY_404" target="_blank" rel="noopener">@AN0M4LY_404</a>
    </div>
  </div>

<script>
async function checkBatch(e) {{
  e.preventDefault();
  const input = document.getElementById("cardsInput").value.trim();
  const resultsDiv = document.getElementById("results");
  const progressContainer = document.getElementById("progressContainer");
  const progressBar = document.getElementById("progressBar");
  resultsDiv.innerHTML = "";
  progressBar.style.width = "0%";
  progressContainer.style.display = "block";

  if (!input) {{
    alert("Por favor, pega al menos una tarjeta.");
    progressContainer.style.display = "none";
    return false;
  }}

  const lines = input.split("\\n").map(l => l.trim()).filter(l => l.length > 0);

  if (lines.length > 3) {{
    alert("Solo puedes pegar hasta 3 tarjetas.");
    progressContainer.style.display = "none";
    return false;
  }}

  const cards = [];
  for (let i = 0; i < lines.length; i++) {{
    const parts = lines[i].split("|");
    if (parts.length !== 4) {{
      alert(`Formato incorrecto en la línea ${{i+1}}. Debe ser Número|MM|AAAA|CVC`);
      progressContainer.style.display = "none";
      return false;
    }}
    const [number, mm, yyyy, cvc] = parts.map(p => p.trim());
    if (!/^\\d{{12,19}}$/.test(number)) {{
      alert(`Número inválido en línea ${{i+1}}.`);
      progressContainer.style.display = "none";
      return false;
    }}
    if (!/^\\d{{2}}$/.test(mm) || parseInt(mm) < 1 || parseInt(mm) > 12) {{
      alert(`Mes inválido en línea ${{i+1}}. Debe ser MM entre 01 y 12.`);
      progressContainer.style.display = "none";
      return false;
    }}
    if (!/^\\d{{4}}$/.test(yyyy) || parseInt(yyyy) < 2023) {{
      alert(`Año inválido en línea ${{i+1}}. Debe ser AAAA >= 2023.`);
      progressContainer.style.display = "none";
      return false;
    }}
    if (!/^\\d{{3,4}}$/.test(cvc)) {{
      alert(`CVC inválido en línea ${{i+1}}. Debe tener 3 o 4 dígitos.`);
      progressContainer.style.display = "none";
      return false;
    }}
    cards.push({{number, exp_month: mm, exp_year: yyyy, cvc}});
  }}

  resultsDiv.innerHTML = "<p style='color:#a9bacd; font-weight:700; text-align:center;'>Verificando...</p>";

  let completed = 0;
  const total = cards.length;

  for (let idx = 0; idx < cards.length; idx++) {{
    const card = cards[idx];
    try {{
      const res = await fetch("/check", {{
        method: "POST",
        headers: {{"Content-Type": "application/json"}},
        body: JSON.stringify(card)
      }});
      const data = await res.json();
      const div = document.createElement("div");
      div.className = "result-item " + (data.status === "live" ? "live" : "dead");
      div.textContent = `Tarjeta ${{idx + 1}}: ${{card.number}} | ${{card.exp_month}}/${{card.exp_year}} | ${{card.cvc}} → ${{data.status.toUpperCase()}}`;
      resultsDiv.appendChild(div);
    }} catch {{
      const div = document.createElement("div");
      div.className = "result-item dead";
      div.textContent = `Tarjeta ${{idx + 1}}: ${{card.number}} → ERROR`;
      resultsDiv.appendChild(div);
    }}
    completed++;
    progressBar.style.width = ((completed / total) * 100) + "%";
  }}

  progressContainer.style.display = "none";
  return false;
}}
</script>

</body>
</html>
"""

# ------- ROUTES -------
@app.route("/")
def landing():
    return LANDING_PAGE

@app.route("/checker")
def checker():
    return render_template_string(CHECKER_PAGE)

@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()
    try:
        pm = stripe.PaymentMethod.create(
            type="card",
            card={
                "number": data["number"],
                "exp_month": int(data["exp_month"]),
                "exp_year": int(data["exp_year"]),
                "cvc": data["cvc"],
            }
        )
        pi = stripe.PaymentIntent.create(
            amount=AMOUNT,
            currency=CURRENCY,
            payment_method=pm.id,
            confirm=True,
            capture_method="automatic"
        )
        stripe.Refund.create(payment_intent=pi.id)
        return jsonify({"status": "live"})
    except stripe.error.CardError:
        return jsonify({"status": "dead"})
    except Exception:
        return jsonify({"status": "dead"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
