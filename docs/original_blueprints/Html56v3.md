---
fable_schema: "5.1.0"
urn: "urn:tgn:blueprint:dashboard_app:39a918c5-03e0-4437-a220-608698836d36"
title: "Domestic Opportunity Matrix Interactive Dashboard v3 (Self-Contained LTR)"
transport: "HybridBridge"
concurrency:
  paradigm: "AsyncIO"
  max_throughput_est: "100 req/s"
fsm:
  defined: false
  states: []
  storage_driver: "Memory"
dependencies:
  external:
    - "chart.js>=4.0.0"
    - "tailwindcss>=3.3.0"
    - "lucide-icons>=0.263.0"
  internal_urns:
    - "urn:tgn:blueprint:dashboard_app:761f20c6-84e9-4da6-8dc4-f2e7faf3b4f4"
    - "urn:tgn:blueprint:market_inventory:2dccf812-2d1b-425a-80b6-0504ec1e1009"
breaking_changes_detected: []
verification_checksum: "ff50bbd460305c23f457442b12e7018737f2ecc20d482ee1d1131de01cd89729"
---
Below is the **final self-contained `index.html`**.  
It uses the 56-row Rubika/Baleh opportunity dataset from `pasted-text.txt` lines 3–56 and KONKRED brand direction from `KONKRED.XYZ DEVELOPMENT.md`.

Save as:

```bash
index.html
```

Then open directly in browser. No npm, CDN, internet, backend, or external asset is required.

```html
<!doctype html>
<html lang="en" dir="ltr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover" />
  <meta name="theme-color" content="#070a12" />
  <title>KONKRED.xyz — Iran Opportunity Intelligence Dashboard</title>
  <style>
    :root{
      --bg:#070a12;
      --bg2:#0b1020;
      --panel:rgba(255,255,255,.07);
      --panel2:rgba(255,255,255,.095);
      --line:rgba(255,255,255,.13);
      --text:#eef5ff;
      --muted:#9aa8c7;
      --soft:#d6e1ff;
      --cyan:#28d7ff;
      --violet:#8f66ff;
      --emerald:#27e1a1;
      --amber:#ffbd4a;
      --rose:#ff5f8f;
      --blue:#5d8cff;
      --shadow:0 24px 90px rgba(0,0,0,.45);
      --radius:24px;
      --r2:16px;
      --font:Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
    }
    *{box-sizing:border-box}
    html{scroll-behavior:smooth}
    body{
      margin:0;
      background:
        radial-gradient(circle at 12% -10%, rgba(40,215,255,.20), transparent 32%),
        radial-gradient(circle at 82% 0%, rgba(143,102,255,.23), transparent 34%),
        radial-gradient(circle at 55% 45%, rgba(39,225,161,.08), transparent 35%),
        linear-gradient(180deg,var(--bg),#090d18 42%,#05070d);
      color:var(--text);
      font-family:var(--font);
      min-height:100vh;
      overflow-x:hidden;
    }
    body:before{
      content:"";
      position:fixed;inset:0;pointer-events:none;z-index:-1;
      background-image:
        linear-gradient(rgba(255,255,255,.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.035) 1px, transparent 1px);
      background-size:42px 42px;
      mask-image:linear-gradient(to bottom,rgba(0,0,0,.9),transparent 80%);
    }
    a{color:inherit;text-decoration:none}
    button,input,select{font:inherit}
    .loader{
      position:fixed;inset:0;z-index:50;
      display:grid;place-items:center;
      background:radial-gradient(circle at center, #101833, #05070d 68%);
      animation:loaderOut .75s ease 1.65s forwards;
    }
    .loader-card{text-align:center;animation:loaderPulse 1.3s ease-in-out infinite}
    .mark{
      width:92px;height:92px;border-radius:30px;margin:0 auto 18px;
      display:grid;place-items:center;
      background:linear-gradient(135deg,rgba(40,215,255,.24),rgba(143,102,255,.24));
      border:1px solid rgba(255,255,255,.18);
      box-shadow:0 0 80px rgba(40,215,255,.24);
      position:relative;overflow:hidden;
    }
    .mark:before{
      content:"";position:absolute;inset:-40%;
      background:conic-gradient(from 0deg,transparent,var(--cyan),var(--violet),var(--emerald),transparent);
      animation:spin 2.2s linear infinite;
    }
    .mark:after{
      content:"K";position:absolute;inset:8px;border-radius:24px;
      display:grid;place-items:center;background:#080c17;
      color:#fff;font-size:42px;font-weight:950;letter-spacing:-.08em;
    }
    .loader h1{margin:0;font-size:28px;letter-spacing:-.04em}
    .loader p{margin:8px 0 0;color:var(--muted);font-size:13px;text-transform:uppercase;letter-spacing:.18em}
    @keyframes spin{to{transform:rotate(360deg)}}
    @keyframes loaderPulse{50%{transform:translateY(-5px);filter:saturate(1.35)}}
    @keyframes loaderOut{to{opacity:0;visibility:hidden}}
    .wrap{width:min(1440px,calc(100% - 32px));margin:auto}
    header{
      position:sticky;top:0;z-index:20;
      backdrop-filter:blur(22px);
      background:linear-gradient(180deg,rgba(7,10,18,.9),rgba(7,10,18,.58));
      border-bottom:1px solid rgba(255,255,255,.08);
    }
    .nav{height:76px;display:flex;align-items:center;justify-content:space-between;gap:18px}
    .brand{display:flex;align-items:center;gap:13px;min-width:0}
    .brand-logo{
      width:42px;height:42px;border-radius:15px;display:grid;place-items:center;
      background:linear-gradient(135deg,rgba(40,215,255,.22),rgba(143,102,255,.25));
      border:1px solid rgba(255,255,255,.15);font-weight:950;
      box-shadow:0 0 34px rgba(40,215,255,.15);
    }
    .brand b{display:block;font-size:17px;letter-spacing:-.035em}
    .brand span{display:block;color:var(--muted);font-size:12px;margin-top:1px}
    .nav-links{display:flex;gap:8px;align-items:center}
    .nav-links a,.pill,.btn{
      border:1px solid rgba(255,255,255,.12);
      background:rgba(255,255,255,.055);
      color:var(--soft);border-radius:999px;padding:10px 13px;font-size:13px;
    }
    .btn{cursor:pointer;transition:.22s ease}
    .btn:hover{transform:translateY(-1px);background:rgba(255,255,255,.1)}
    .btn.primary{
      color:#041016;background:linear-gradient(135deg,var(--cyan),var(--emerald));
      border:0;font-weight:850;box-shadow:0 10px 30px rgba(40,215,255,.18);
    }
    .hero{padding:70px 0 34px;position:relative}
    .hero-grid{display:grid;grid-template-columns:1.08fr .92fr;gap:28px;align-items:stretch}
    .eyebrow{display:flex;flex-wrap:wrap;gap:9px;margin-bottom:18px}
    .chip{
      display:inline-flex;align-items:center;gap:8px;
      padding:8px 12px;border-radius:999px;
      border:1px solid rgba(255,255,255,.12);
      background:rgba(255,255,255,.055);
      color:var(--soft);font-size:12.5px;font-weight:650;
    }
    .dot{width:8px;height:8px;border-radius:999px;background:var(--cyan);box-shadow:0 0 18px currentColor}
    h1{
      margin:0;font-size:clamp(40px,7vw,88px);line-height:.92;letter-spacing:-.075em;
    }
    .grad{background:linear-gradient(135deg,#fff,var(--cyan) 35%,var(--violet) 75%,#fff);-webkit-background-clip:text;background-clip:text;color:transparent}
    .lead{
      margin:24px 0 0;color:#bdc8e6;
      font-size:clamp(16px,2vw,20px);line-height:1.65;max-width:820px;
    }
    .hero-actions{display:flex;flex-wrap:wrap;gap:12px;margin-top:28px}
    .glass{
      background:linear-gradient(180deg,rgba(255,255,255,.095),rgba(255,255,255,.045));
      border:1px solid rgba(255,255,255,.13);
      border-radius:var(--radius);
      box-shadow:var(--shadow);
    }
    .mission{padding:22px;position:relative;overflow:hidden}
    .mission:before{
      content:"";position:absolute;inset:-1px;
      background:radial-gradient(circle at top right,rgba(40,215,255,.20),transparent 42%);
      pointer-events:none;
    }
    .mission h2{margin:0 0 12px;font-size:18px}
    .mission p{margin:0;color:var(--muted);line-height:1.7;font-size:14px}
    .pillar-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:18px}
    .pillar{padding:16px;border-radius:18px;background:rgba(255,255,255,.055);border:1px solid rgba(255,255,255,.1)}
    .pillar b{display:block;font-size:14px;margin-bottom:7px}
    .pillar span{display:block;color:var(--muted);font-size:12px;line-height:1.45}
    .kpis{display:grid;grid-template-columns:repeat(6,1fr);gap:14px;margin:22px 0 24px}
    .kpi{padding:18px;border-radius:20px;background:rgba(255,255,255,.065);border:1px solid rgba(255,255,255,.11)}
    .kpi small{display:block;color:var(--muted);font-size:12px;margin-bottom:8px}
    .kpi strong{display:block;font-size:26px;letter-spacing:-.04em}
    .kpi em{display:block;color:var(--muted);font-style:normal;font-size:12px;margin-top:4px}
    .section{padding:22px 0}
    .section-head{display:flex;align-items:end;justify-content:space-between;gap:18px;margin-bottom:16px}
    .section-head h2{margin:0;font-size:26px;letter-spacing:-.04em}
    .section-head p{margin:7px 0 0;color:var(--muted);font-size:14px}
    .insights{display:grid;grid-template-columns:1.1fr .9fr .9fr;gap:16px}
    .card{padding:20px;border-radius:var(--radius);background:rgba(255,255,255,.065);border:1px solid rgba(255,255,255,.11);overflow:hidden}
    .card h3{margin:0 0 14px;font-size:16px;letter-spacing:-.02em}
    .bars{display:grid;gap:10px}
    .bar-row{display:grid;grid-template-columns:120px 1fr 46px;gap:10px;align-items:center;font-size:12px;color:var(--soft)}
    .bar{height:10px;border-radius:999px;background:rgba(255,255,255,.08);overflow:hidden}
    .bar i{display:block;height:100%;border-radius:999px;background:linear-gradient(90deg,var(--cyan),var(--violet))}
    .top-list{display:grid;gap:10px}
    .top-item{display:flex;justify-content:space-between;gap:12px;padding:12px;border-radius:16px;background:rgba(255,255,255,.055);border:1px solid rgba(255,255,255,.08)}
    .top-item b{font-size:13px}
    .top-item span{color:var(--muted);font-size:12px}
    .score-badge{
      min-width:48px;height:34px;border-radius:13px;display:grid;place-items:center;
      background:rgba(39,225,161,.13);color:#7dffd3;border:1px solid rgba(39,225,161,.28);font-weight:900;
    }
    .heat{display:grid;grid-template-columns:repeat(14,1fr);gap:7px}
    .cell{aspect-ratio:1;border-radius:9px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.08);position:relative;cursor:pointer}
    .cell[data-level="high"]{background:rgba(39,225,161,.35);border-color:rgba(39,225,161,.45)}
    .cell[data-level="mid"]{background:rgba(255,189,74,.30);border-color:rgba(255,189,74,.42)}
    .cell[data-level="low"]{background:rgba(255,95,143,.22);border-color:rgba(255,95,143,.36)}
    .cell:hover:after{
      content:attr(data-tip);position:absolute;bottom:115%;left:50%;transform:translateX(-50%);
      width:220px;padding:9px 10px;border-radius:12px;background:#0d1324;border:1px solid var(--line);
      color:#fff;font-size:12px;z-index:5;box-shadow:var(--shadow)
    }
    .controls{display:grid;grid-template-columns:1.6fr repeat(4,1fr) auto;gap:10px;margin-bottom:14px}
    .field{
      width:100%;height:44px;border-radius:15px;
      border:1px solid rgba(255,255,255,.12);
      background:rgba(255,255,255,.065);
      color:#fff;padding:0 13px;outline:0;
    }
    select.field option{background:#0b1020;color:#fff}
    .view-toggle{display:flex;gap:8px;align-items:center;justify-content:flex-end}
    .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
    .opp{
      position:relative;padding:18px;border-radius:22px;
      background:linear-gradient(180deg,rgba(255,255,255,.085),rgba(255,255,255,.045));
      border:1px solid rgba(255,255,255,.11);
      transition:.22s ease;overflow:hidden;
    }
    .opp:hover{transform:translateY(-4px);border-color:rgba(40,215,255,.3);box-shadow:0 20px 60px rgba(0,0,0,.3)}
    .opp:before{content:"";position:absolute;inset:0;background:radial-gradient(circle at top right,rgba(40,215,255,.12),transparent 45%);pointer-events:none}
    .opp-head{display:flex;align-items:start;justify-content:space-between;gap:12px;position:relative}
    .opp h3{margin:0;font-size:16px;line-height:1.35;letter-spacing:-.025em}
    .meta{display:flex;flex-wrap:wrap;gap:7px;margin:12px 0}
    .tag{font-size:11px;padding:6px 8px;border-radius:999px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.1);color:var(--soft)}
    .tag.rubika{color:#84efff;border-color:rgba(40,215,255,.22);background:rgba(40,215,255,.08)}
    .tag.baleh{color:#c7b3ff;border-color:rgba(143,102,255,.25);background:rgba(143,102,255,.1)}
    .tag.hot{color:#91ffd9;border-color:rgba(39,225,161,.28);background:rgba(39,225,161,.1)}
    .desc{color:var(--muted);font-size:13px;line-height:1.6;min-height:62px}
    .mini{display:grid;gap:8px;margin:14px 0}
    .mini-row{display:grid;grid-template-columns:74px 1fr 34px;gap:9px;align-items:center;color:var(--muted);font-size:11px}
    .opp-foot{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:14px;position:relative}
    .rev{font-size:12px;color:var(--muted)}
    .rev b{color:#fff;font-size:14px}
    .table-wrap{display:none;overflow:auto;border-radius:22px;border:1px solid rgba(255,255,255,.1)}
    table{width:100%;border-collapse:collapse;min-width:1080px;background:rgba(255,255,255,.045)}
    th,td{padding:14px 12px;border-bottom:1px solid rgba(255,255,255,.08);text-align:left;font-size:13px;vertical-align:top}
    th{position:sticky;top:0;background:#10172a;color:#dce7ff;z-index:1}
    td{color:#b9c5df}
    td b{color:#fff}
    .table-mode .grid{display:none}
    .table-mode .table-wrap{display:block}
    .modal{
      position:fixed;inset:0;z-index:40;display:none;align-items:center;justify-content:center;
      padding:20px;background:rgba(0,0,0,.62);backdrop-filter:blur(14px);
    }
    .modal.show{display:flex}
    .modal-box{
      width:min(980px,100%);max-height:min(86vh,900px);overflow:auto;
      border-radius:28px;background:linear-gradient(180deg,#11182b,#080c16);
      border:1px solid rgba(255,255,255,.14);box-shadow:var(--shadow);
    }
    .modal-top{padding:22px;border-bottom:1px solid rgba(255,255,255,.1);display:flex;justify-content:space-between;gap:16px}
    .modal-top h2{margin:0;font-size:26px;letter-spacing:-.04em}
    .modal-body{padding:22px}
    .detail-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
    .detail{padding:15px;border-radius:18px;background:rgba(255,255,255,.055);border:1px solid rgba(255,255,255,.09)}
    .detail small{display:block;color:var(--muted);font-size:12px;margin-bottom:7px}
    .detail p{margin:0;color:#d9e4ff;line-height:1.55;font-size:14px}
    .audit{margin-top:14px;padding:16px;border-radius:18px;background:linear-gradient(135deg,rgba(39,225,161,.12),rgba(40,215,255,.08));border:1px solid rgba(39,225,161,.24)}
    .audit b{display:block;margin-bottom:6px}
    .close{width:42px;height:42px;border-radius:15px;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.07);color:#fff;cursor:pointer}
    footer{padding:38px 0 50px;color:var(--muted)}
    .foot{display:flex;justify-content:space-between;gap:18px;align-items:center;border-top:1px solid rgba(255,255,255,.1);padding-top:24px}
    .hidden{display:none!important}
    @media(max-width:1100px){
      .hero-grid,.insights{grid-template-columns:1fr}
      .kpis{grid-template-columns:repeat(3,1fr)}
      .grid{grid-template-columns:repeat(2,1fr)}
      .controls{grid-template-columns:1fr 1fr}
      .view-toggle{justify-content:start}
    }
    @media(max-width:720px){
      .wrap{width:min(100% - 20px,1440px)}
      .nav{height:auto;padding:12px 0}
      .nav-links a{display:none}
      .hero{padding-top:38px}
      .pillar-grid,.kpis,.grid,.detail-grid{grid-template-columns:1fr}
      .controls{grid-template-columns:1fr}
      .heat{grid-template-columns:repeat(8,1fr)}
      .foot{flex-direction:column;align-items:flex-start}
      .modal{padding:10px}
      .modal-top{padding:18px}
      .modal-body{padding:18px}
    }
  </style>
</head>
<body>
  <div class="loader" aria-hidden="true">
    <div class="loader-card">
      <div class="mark"></div>
      <h1>KONKRED.xyz</h1>
      <p>Iran Market Intelligence Layer</p>
    </div>
  </div>

  <header>
    <div class="wrap nav">
      <a class="brand" href="#">
        <div class="brand-logo">K</div>
        <div>
          <b>KONKRED.xyz</b>
          <span>Structural AI Capital · Iran Market</span>
        </div>
      </a>
      <nav class="nav-links">
        <a href="#insights">Insights</a>
        <a href="#explorer">Explorer</a>
        <a href="#audit">Audit</a>
        <button class="btn primary" onclick="document.querySelector('#explorer').scrollIntoView()">Explore 56 Ideas</button>
      </nav>
    </div>
  </header>

  <main>
    <section class="hero wrap">
      <div class="hero-grid">
        <div>
          <div class="eyebrow">
            <span class="chip"><i class="dot"></i> Rubika × Baleh</span>
            <span class="chip"><i class="dot" style="background:var(--emerald)"></i> 56 Opportunity Rows</span>
            <span class="chip"><i class="dot" style="background:var(--violet)"></i> Offline Production HTML</span>
          </div>
          <h1>Iran Opportunity <span class="grad">Intelligence</span> Dashboard</h1>
          <p class="lead">
            A KONKRED-grade strategic dashboard for mapping, scoring, filtering, and validating business opportunities inside
            Iran’s messaging-commerce ecosystems: <b>Rubika</b> and <b>Baleh</b>.
          </p>
          <div class="hero-actions">
            <button class="btn primary" onclick="document.querySelector('#explorer').scrollIntoView()">Open Opportunity Explorer</button>
            <button class="btn" onclick="resetFilters()">Reset Filters</button>
            <span class="pill">Verified dataset: pasted-text.txt lines 3–56</span>
          </div>
        </div>

        <aside class="glass mission">
          <h2>KONKRED Strategic Frame</h2>
          <p>
            Built around KONKRED’s platform pillars: Marketplace, Forge, and Academy. This view translates raw market ideas into
            founder-ready execution paths for sellers, creators, tutors, SMEs, paid communities, and enterprise teams in Iran.
          </p>
          <div class="pillar-grid">
            <div class="pillar"><b style="color:var(--emerald)">Marketplace</b><span>Demand, discovery, commerce, listings, take-rate potential.</span></div>
            <div class="pillar"><b style="color:var(--amber)">Forge</b><span>MVP path, tooling feasibility, workflow automation, build readiness.</span></div>
            <div class="pillar"><b style="color:var(--violet)">Academy</b><span>Templates, training, enablement, certification, SOP monetization.</span></div>
          </div>
        </aside>
      </div>

      <div class="kpis" id="kpis"></div>
    </section>

    <section class="section wrap" id="insights">
      <div class="section-head">
        <div>
          <h2>Executive Intelligence</h2>
          <p>Fast-read distribution, top opportunities, score heatmap, and Iran-market prioritization.</p>
        </div>
      </div>
      <div class="insights">
        <div class="card">
          <h3>Category Distribution</h3>
          <div class="bars" id="categoryBars"></div>
        </div>
        <div class="card">
          <h3>Top Opportunities</h3>
          <div class="top-list" id="topList"></div>
        </div>
        <div class="card">
          <h3>Score Heatmap</h3>
          <div class="heat" id="heatmap"></div>
        </div>
      </div>
    </section>

    <section class="section wrap" id="explorer">
      <div class="section-head">
        <div>
          <h2>Opportunity Explorer</h2>
          <p>Search, filter, sort, switch card/table view, and open detailed validation logic.</p>
        </div>
        <div class="view-toggle">
          <button class="btn primary" id="cardBtn" onclick="setView('card')">Cards</button>
          <button class="btn" id="tableBtn" onclick="setView('table')">Table</button>
        </div>
      </div>

      <div class="controls">
        <input class="field" id="q" placeholder="Search idea, category, customer, pain..." oninput="render()" />
        <select class="field" id="category" onchange="render()"><option value="">All categories</option></select>
        <select class="field" id="verdict" onchange="render()"><option value="">All verdicts</option></select>
        <select class="field" id="score" onchange="render()">
          <option value="">All scores</option>
          <option value="80">80+ highest priority</option>
          <option value="75">75+ strong</option>
          <option value="70">70+ viable</option>
          <option value="0">Below 70 / test carefully</option>
        </select>
        <select class="field" id="sort" onchange="render()">
          <option value="score-desc">Sort: Score high → low</option>
          <option value="score-asc">Sort: Score low → high</option>
          <option value="rev-desc">Sort: Revenue high → low</option>
          <option value="id-asc">Sort: Original order</option>
        </select>
        <button class="btn" onclick="resetFilters()">Reset</button>
      </div>

      <div id="results" class="grid"></div>

      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>#</th><th>Idea</th><th>Category</th><th>Customer</th><th>Pain</th><th>Revenue</th><th>Score</th><th>Verdict</th><th></th>
            </tr>
          </thead>
          <tbody id="tableBody"></tbody>
        </table>
      </div>
    </section>

    <section class="section wrap" id="audit">
      <div class="card">
        <h3>Verified by KONKRED AUDIT — Strategic Notes</h3>
        <p style="color:var(--muted);line-height:1.8;margin:0">
          This dashboard is optimized for Iran’s Rubika and Baleh market context: mobile-first users, messaging-led commerce,
          creator/community monetization, paid education, operational templates, manual-first validation, and micro-SaaS paths
          where platform APIs may be uncertain. Data source: <b style="color:#fff">pasted-text.txt lines 3–56</b>.
          Brand direction aligns with KONKRED’s marketplace, forge, and academy platform pillars.
        </p>
      </div>
    </section>
  </main>

  <div class="modal" id="modal" onclick="if(event.target.id==='modal')closeModal()">
    <div class="modal-box">
      <div class="modal-top">
        <div>
          <h2 id="mTitle"></h2>
          <div class="meta" id="mMeta"></div>
        </div>
        <button class="close" onclick="closeModal()">✕</button>
      </div>
      <div class="modal-body" id="mBody"></div>
    </div>
  </div>

  <footer class="wrap">
    <div class="foot">
      <div>
        <b style="color:#fff">KONKRED.xyz</b>
        <div>Iran Opportunity Intelligence Dashboard · Rubika × Baleh</div>
      </div>
      <div>Self-contained HTML · No external dependencies · Production-ready offline build</div>
    </div>
  </footer>

<script>
const DATA = [
{id:1,name:"FAQ & Ready Replies Pack for Sellers",cat:"Template/Productized Asset",platform:"Both",target:"Informal sellers, channel shops",pain:"Repetitive questions waste time",desc:"Ready-made replies for price, stock, shipping, payment and objections.",mon:"One-time sale, bundles",rev:5,score:78,verdict:"Build First as Side Hustle",validation:"DM 30 sellers and offer 10 free samples + paid full pack",risk:"Seen as commodity, easy copying"},
{id:2,name:"Sales Channel Organization Kit",cat:"Template/Productized Asset",platform:"Both",target:"Channel admins, shop owners",pain:"Messy pricing, ordering rules, scattered posts",desc:"Post templates, pinned post structure, order rules, return policy templates.",mon:"One-time sale",rev:6,score:77,verdict:"Build First as Side Hustle",validation:"Sell mockup to 10 active channels",risk:"Perceived as just content"},
{id:3,name:"Mini CRM Sheet for Order Tracking",cat:"Seller Tool",platform:"Both",target:"Small sellers",pain:"Orders get lost in DMs",desc:"Sheet to track order, payment, shipping and follow-up.",mon:"One-time sale, setup fee, subscription later",rev:8,score:81,verdict:"Build First as Side Hustle",validation:"Offer manual setup to 5 sellers for discounted fee",risk:"Users may not maintain data entry"},
{id:4,name:"Paid Membership Renewal Tracker",cat:"Membership Tool",platform:"Both",target:"Paid channels, tutors, paid communities",pain:"Renewals forgotten, member expiry unmanaged",desc:"Expiry tracker, renewal message templates and member sheet.",mon:"Setup fee + monthly subscription",rev:10,score:79,verdict:"Good Micro-SaaS Candidate",validation:"Audit 3 paid groups and show missed renewals manually",risk:"Users may expect full automated access control"},
{id:5,name:"Educational Community Onboarding Pack",cat:"Education Tool",platform:"Both",target:"Tutors, course owners, class admins",pain:"New members ask same questions repeatedly",desc:"Welcome message, rules, study map, FAQ and pinned post templates.",mon:"One-time sale",rev:5,score:79,verdict:"Build First as Side Hustle",validation:"Offer free sample welcome kit to 10 tutors",risk:"High request for customization"},
{id:6,name:"Order Intake Form Setup",cat:"Seller Tool",platform:"Both",target:"DM-based sellers",pain:"Addresses/products/details get lost in chat",desc:"Simple order form linked to structured sheet.",mon:"Setup fee, template sale",rev:7,score:80,verdict:"Build First as Side Hustle",validation:"Manually set up 5 forms for active sellers",risk:"Buyers may refuse filling forms"},
{id:7,name:"Appointment Booking Kit for Service Providers",cat:"Service Tool",platform:"Both",target:"Beauty clinics, tutors, repairmen, consultants",pain:"Booking through chat is messy",desc:"Intake form, schedule rules and confirmation messages.",mon:"Setup + monthly",rev:10,score:79,verdict:"Good Micro-SaaS Candidate",validation:"Offer free setup to 2 salons/tutors for testimonial",risk:"Each vertical needs custom workflow"},
{id:8,name:"30-Day Content Calendar Pack",cat:"Creator Tool",platform:"Both",target:"Creators, channel admins",pain:"No publishing consistency, idea fatigue",desc:"Ready content calendar with post ideas, CTA and caption prompts.",mon:"One-time sale",rev:4,score:72,verdict:"Build First as Side Hustle",validation:"Post sample 7-day plan and ask for preorders",risk:"Pain not directly tied to revenue"},
{id:9,name:"Group Rules & Anti-Spam Pack",cat:"Community Tool",platform:"Both",target:"Group admins",pain:"Repeated rule violations, manual warnings",desc:"Rules template, warning scripts and moderation policy checklist.",mon:"One-time sale",rev:3,score:66,verdict:"Test Cheaply",validation:"Interview 15 group admins about moderation pain",risk:"Admins often low willingness to pay"},
{id:10,name:"Trust Mini-Landing for Sellers",cat:"Seller Tool",platform:"Both",target:"Informal sellers lacking trust signals",pain:"Buyers don’t trust unknown sellers",desc:"Mini landing page with rules, FAQs, reviews and buying steps.",mon:"Setup fee + optional hosting",rev:8,score:76,verdict:"Good Agency/Service Candidate",validation:"Create before/after trust page for 3 sellers",risk:"Hard to prove direct conversion lift"},
{id:11,name:"Sales Follow-up & Win-back Message Bank",cat:"Template/Productized Asset",platform:"Both",target:"Sellers, SMEs",pain:"No system for following up leads/customers",desc:"Messages for reminders, upsells, win-back and payment nudges.",mon:"One-time sale",rev:5,score:78,verdict:"Build First as Side Hustle",validation:"Send 10-message sample to 30 sellers",risk:"Commodity risk"},
{id:12,name:"Manual Channel Analytics Sheet",cat:"Analytics Tool",platform:"Both",target:"Channel admins, creators",pain:"Can’t tell what content performs or sells",desc:"Tracking sheet for post type, response and conversions.",mon:"Template sale, subscription later",rev:4,score:70,verdict:"Test Cheaply",validation:"Give sheet to 5 admins for 7 days",risk:"Manual data entry fatigue"},
{id:13,name:"Paid Educational Channel Launch Kit",cat:"Education Tool",platform:"Both",target:"Tutors, experts, creators",pain:"Don’t know how to structure paid community",desc:"Pricing, offers, launch messaging, content plan and renewal flow.",mon:"One-time sale, consulting upsell",rev:8,score:78,verdict:"Build First as Side Hustle",validation:"Interview 10 tutors considering paid community",risk:"Founders may just want free advice"},
{id:14,name:"Niche Directory of Channels/Groups",cat:"Marketplace",platform:"Both",target:"Users, advertisers, admins",pain:"Good channels/groups hard to discover",desc:"Curated directory by topic and quality.",mon:"Ads, paid listing, sponsorship",rev:5,score:60,verdict:"Test Cheaply",validation:"Launch one niche directory and collect 50 submissions",risk:"Monetization weak early, quality control"},
{id:15,name:"Done-for-You Seller Ops Setup",cat:"Manual Service",platform:"Both",target:"Small sellers",pain:"Business runs chaotically in chat",desc:"Manual setup of FAQ, order form, CRM sheet and policy posts.",mon:"Setup fee",rev:15,score:74,verdict:"Good Agency/Service Candidate",validation:"Offer setup service to 5 sellers manually",risk:"Turns into custom service swamp"},
{id:16,name:"DM Customer Support Outsourcing for Sellers",cat:"Customer Support Tool",platform:"Both",target:"Sellers, SMEs",pain:"Owner overwhelmed by buyer questions",desc:"Outsourced manual support handling.",mon:"Monthly retainer",rev:20,score:63,verdict:"Too Operational",validation:"Pilot with 1 seller for one week",risk:"24/7 expectations, burnout, quality inconsistency"},
{id:17,name:"Payment Receipt Verification Service",cat:"Manual Service",platform:"Both",target:"Paid groups, course sellers",pain:"Manually matching receipts is painful",desc:"Human verification of receipts and membership status.",mon:"Monthly retainer, per-transaction fee",rev:18,score:61,verdict:"Too Operational",validation:"Manual reconciliation for 2 communities for 1 week",risk:"Financial errors create trust issues"},
{id:18,name:"Membership Access Management Service",cat:"Manual Service",platform:"Both",target:"Paid communities, tutors",pain:"Manually add/remove members based on payment",desc:"Founder/operator manages access lists and renewals.",mon:"Monthly management fee",rev:20,score:58,verdict:"Too Operational",validation:"Concierge pilot for 1 paid group",risk:"Missed removals/additions, high manual burden"},
{id:19,name:"Moderation-as-a-Service for Groups",cat:"Agency Service",platform:"Both",target:"Large communities",pain:"Spam, abuse, chaos, repetitive enforcement",desc:"Human moderators plus rule enforcement playbook.",mon:"Monthly retainer",rev:20,score:59,verdict:"Too Operational",validation:"Moderate 1 busy group for 1 week",risk:"Hard labor, low defensibility, admin politics"},
{id:20,name:"Seller Storefront Builder for Messaging Commerce",cat:"Seller Tool",platform:"Both",target:"Informal sellers",pain:"No proper catalog/storefront",desc:"Simple storefront page with catalog, FAQs and order links.",mon:"Setup fee + subscription",rev:15,score:77,verdict:"Good Micro-SaaS Candidate",validation:"Build 3 demo storefronts and pre-sell setup",risk:"Sellers may stay with pure chat flow"},
{id:21,name:"Inventory & Price Update Dashboard",cat:"Seller Tool",platform:"Both",target:"Sellers with many SKUs",pain:"Outdated prices/stock create chaos",desc:"Central sheet/dashboard for stock, price and status updates.",mon:"Subscription + setup",rev:12,score:75,verdict:"Good Micro-SaaS Candidate",validation:"Interview 15 sellers with >20 products",risk:"Manual updates may not sustain"},
{id:22,name:"Broadcast Campaign Planner for Sellers",cat:"Seller Tool",platform:"Both",target:"Sellers, channel marketers",pain:"No system for promos, launches, reminders",desc:"Campaign calendar and segmented message templates.",mon:"Kit sale, setup, subscription later",rev:6,score:71,verdict:"Test Cheaply",validation:"Sell promo template to 10 channels before software",risk:"Without automation, value may feel limited"},
{id:23,name:"Cross-Platform Social Commerce Ops Kit",cat:"Seller Tool",platform:"Both",target:"Sellers on Rubika, Baleh, Telegram, Instagram",pain:"Fragmented order/support workflow",desc:"Unified manual workflow kit for leads, orders and FAQs.",mon:"Setup fee + subscription",rev:12,score:78,verdict:"Good Micro-SaaS Candidate",validation:"Recruit 5 multichannel sellers for workflow interviews",risk:"Wider scope increases complexity"},
{id:24,name:"Tutor/Class Admin Operations Kit",cat:"Education Tool",platform:"Both",target:"Tutors, institute admins",pain:"Class scheduling, reminders, delivery are messy",desc:"Attendance, schedule, homework and reminder kit.",mon:"Template sale, setup, subscription",rev:8,score:76,verdict:"Good Micro-SaaS Candidate",validation:"Offer ops setup to 5 tutors before software",risk:"Too broad if not niche-focused"},
{id:25,name:"Homework Submission & Tracking Workflow",cat:"Education Tool",platform:"Both",target:"Tutors, coaching groups",pain:"Homework gets buried in chats",desc:"Standardized homework submission process.",mon:"Subscription, setup",rev:10,score:72,verdict:"Good Micro-SaaS Candidate",validation:"Pilot with 2 tutors and 30 students",risk:"Students may ignore structured process"},
{id:26,name:"Creator Membership Operations Stack",cat:"Membership Tool",platform:"Both",target:"Creators with paid communities",pain:"Content delivery, renewal and onboarding fragmented",desc:"Member tracker, welcome flow, content calendar and renewal SOP.",mon:"Setup + monthly subscription",rev:12,score:77,verdict:"Good Micro-SaaS Candidate",validation:"Recruit 3 paid creators for ops audit",risk:"Creators expect all-in-one automation"},
{id:27,name:"Channel Growth Audit Service",cat:"Agency Service",platform:"Both",target:"Creators, sellers, admins",pain:"Low growth, poor conversions, no diagnosis",desc:"Audit content, trust, posting, CTA and conversion leaks.",mon:"Audit fee, consulting retainer",rev:12,score:75,verdict:"Good Agency/Service Candidate",validation:"Free mini-audit to 5 channels and pitch full audit",risk:"Results may be subjective"},
{id:28,name:"Sales Funnel Audit for Messaging Sellers",cat:"Agency Service",platform:"Both",target:"Sellers",pain:"Poor conversion from viewer to buyer",desc:"Analyze trust, pricing flow, order friction and follow-up gaps.",mon:"Audit fee, implementation fee",rev:15,score:78,verdict:"Good Agency/Service Candidate",validation:"Audit 3 sellers and show lost conversions",risk:"Clients may want guarantees"},
{id:29,name:"Channel Post Template Studio",cat:"Creator Tool",platform:"Both",target:"Creators, shops, admins",pain:"Weak formatting and repetitive post creation",desc:"Branded post/caption templates for messaging channels.",mon:"Template pack, custom pack",rev:6,score:70,verdict:"Build First as Side Hustle",validation:"Post 10 templates and sell full pack to 20 admins",risk:"Low defensibility, copyability"},
{id:30,name:"Admin SOP & Operations Manual Pack",cat:"Community Tool",platform:"Both",target:"Admins, small businesses, course operators",pain:"Everything depends on memory and ad hoc actions",desc:"SOP pack for replies, onboarding, ordering and moderation.",mon:"One-time sale, customization upsell",rev:5,score:74,verdict:"Build First as Side Hustle",validation:"Offer SOP sample to 10 admins/businesses",risk:"Perceived as just docs"},
{id:31,name:"Messaging Commerce CRM SaaS",cat:"SaaS",platform:"Both",target:"Growing sellers, small teams",pain:"No structured CRM for messaging-led commerce",desc:"Lead/order/customer CRM around channel and DM workflows.",mon:"Monthly subscription",rev:20,score:83,verdict:"Good Funded Startup Candidate",validation:"Run concierge CRM for 5 sellers before coding",risk:"Users may stick to spreadsheets; integration uncertainty"},
{id:32,name:"Paid Community Membership SaaS",cat:"SaaS",platform:"Both",target:"Course owners, creators, premium communities",pain:"Managing paid members and renewals manually is painful",desc:"Member lifecycle tool for onboarding, renewal, expiry and segmentation.",mon:"Subscription + setup",rev:20,score:82,verdict:"Good Funded Startup Candidate",validation:"Pilot manual member management for 3 communities",risk:"Access automation/API dependence"},
{id:33,name:"Messaging-Based Customer Support Desk",cat:"Customer Support Tool",platform:"Both",target:"SMEs using Rubika/Baleh for support",pain:"Support requests scattered across chats",desc:"Inbox/helpdesk for ticketing and team replies.",mon:"Subscription",rev:18,score:79,verdict:"Good Funded Startup Candidate",validation:"Interview 15 SMEs handling support in chat",risk:"Deep integration may be blocked"},
{id:34,name:"Chatbot for FAQs and Lead Qualification",cat:"Bot",platform:"Both",target:"Sellers, service providers, communities",pain:"Repetitive inbound questions",desc:"Bot that answers FAQs and collects lead/order info.",mon:"Setup + subscription",rev:12,score:74,verdict:"Needs Platform/API Verification",validation:"Test bot demand with fake demo and preorders",risk:"No API/support for real bot deployment"},
{id:35,name:"Auto Reminder Bot for Renewals/Payments",cat:"Bot",platform:"Both",target:"Paid groups, tutors, sellers",pain:"Reminders are manual and inconsistent",desc:"Bot for expiry, payment and order reminders.",mon:"Subscription",rev:10,score:75,verdict:"Needs Platform/API Verification",validation:"Manually run reminders for 3 customers before automating",risk:"Automation access unknown"},
{id:36,name:"Group Moderation Bot",cat:"Bot",platform:"Both",target:"Large groups",pain:"Spam and rule-breaking are constant",desc:"Bot to warn, filter and auto-respond to violations.",mon:"Subscription",rev:8,score:69,verdict:"Needs Platform/API Verification",validation:"Interview 15 admins and show fake moderation dashboard",risk:"Blocked by API/policy, noisy edge cases"},
{id:37,name:"Community Discovery & Recommendation App",cat:"Marketplace",platform:"Both",target:"Ordinary users, advertisers, communities",pain:"Discovering quality groups/channels is inefficient",desc:"App/site recommending communities by interest.",mon:"Ads, lead gen, featured listings",rev:100,score:68,verdict:"Good Funded Startup Candidate",validation:"Build one niche directory and track retention",risk:"Cold start and traffic challenge"},
{id:38,name:"Rubika/Baleh Ad Network for Channels",cat:"Funded Startup Idea",platform:"Both",target:"Advertisers, channel owners",pain:"Buying ads in channels is fragmented and untrusted",desc:"Marketplace for channel ads, placements and reporting.",mon:"Take rate, managed campaigns",rev:150,score:77,verdict:"Good Funded Startup Candidate",validation:"Broker 5 manual ad deals",risk:"Trust, fraud, reporting uncertainty"},
{id:39,name:"Escrow/Trusted Deal Layer for Informal Sellers",cat:"Funded Startup Idea",platform:"Both",target:"Buyers and sellers in informal commerce",pain:"Trust is low in chat commerce",desc:"Escrow-like payment and dispute system.",mon:"Fee per transaction",rev:200,score:73,verdict:"Good Funded Startup Candidate",validation:"Concierge middleman pilot on small transactions",risk:"Extreme legal/trust/compliance risk"},
{id:40,name:"Informal Commerce Marketplace Built on Messaging Demand",cat:"Marketplace",platform:"Both",target:"Buyers, informal sellers",pain:"Fragmented supply and no standardized shopping",desc:"Marketplace aggregating sellers active in messaging apps.",mon:"Take rate, ads, seller plans",rev:300,score:71,verdict:"Good Funded Startup Candidate",validation:"Start with one curated product niche and manual order relay",risk:"Trust, logistics, disputes, chicken-and-egg"},
{id:41,name:"Channel/Group Benchmarking Intelligence Tool",cat:"Analytics Tool",platform:"Both",target:"Large creators, agencies, advertisers",pain:"No benchmark data on channel performance",desc:"Compare communities by growth, engagement proxies and monetization indicators.",mon:"Report sales, subscription",rev:15,score:76,verdict:"Good Funded Startup Candidate",validation:"Sell 3 custom benchmark reports before building tool",risk:"Hard data may be inaccessible or noisy"},
{id:42,name:"Seller Credit Scoring / Trust Index",cat:"Analytics Tool",platform:"Both",target:"Buyers, marketplaces, lenders",pain:"Hard to know if seller is trustworthy",desc:"Reputation profile based on behavior, reviews and consistency.",mon:"Subscription, API, verification fee",rev:100,score:70,verdict:"Good Funded Startup Candidate",validation:"Test if buyers value trust badges with mock profiles",risk:"Data validity and legal exposure"},
{id:43,name:"Local Creator CRM for Paid Communities",cat:"Creator Tool",platform:"Both",target:"Creators, coaches, educators",pain:"Creator business ops fragmented across chat",desc:"CRM for leads, members, content schedule and renewals.",mon:"Subscription",rev:15,score:80,verdict:"Good Funded Startup Candidate",validation:"Onboard 3 creators with concierge CRM setup",risk:"Creators may be too small to pay"},
{id:44,name:"Message Template Generator by Industry",cat:"Creator Tool",platform:"Both",target:"Sellers, service providers, tutors",pain:"Need tailored replies but generic packs are weak",desc:"Generator that outputs message banks by niche/tone.",mon:"One-time pack, subscription later",rev:6,score:77,verdict:"Build First as Side Hustle",validation:"Pre-sell 3 niche packs before generator",risk:"Commoditized, AI alternatives"},
{id:45,name:"Channel Monetization Consultant for Creators",cat:"Agency Service",platform:"Both",target:"Creators/admins",pain:"Don’t know how to monetize audience",desc:"Consulting on offers, memberships, ads and funnels.",mon:"Consulting fee, retainer",rev:15,score:73,verdict:"Good Agency/Service Candidate",validation:"Offer 5 free mini-monetization reviews",risk:"Advisory hard to productize"},
{id:46,name:"Seller Training Course for Messaging Commerce",cat:"Education Tool",platform:"Both",target:"Beginner sellers",pain:"No structured know-how for selling in chat ecosystems",desc:"Course on setup, FAQ, trust, follow-up and order ops.",mon:"Course sales",rev:8,score:72,verdict:"Build First as Side Hustle",validation:"Run one live workshop and see paid attendance",risk:"Info-product saturation"},
{id:47,name:"Community Manager Training & Certification",cat:"Education Tool",platform:"Both",target:"Aspiring admins, community operators",pain:"No standards for running groups/channels",desc:"Training on moderation, onboarding, member ops and growth.",mon:"Tuition, certification fee",rev:30,score:68,verdict:"Test Cheaply",validation:"Survey 50 admins for training interest",risk:"Weak credential value"},
{id:48,name:"Shared Admin Inbox for Small Teams",cat:"Customer Support Tool",platform:"Both",target:"SMEs with multiple admins",pain:"Multiple people reply inconsistently",desc:"Shared inbox/process layer with assignment and notes.",mon:"Subscription",rev:15,score:78,verdict:"Good Funded Startup Candidate",validation:"Run manual shared inbox pilot with 1 SME team",risk:"Integration constraints severe"},
{id:49,name:"Lead Capture & Qualification Workflow for Service Businesses",cat:"Customer Support Tool",platform:"Both",target:"Clinics, consultants, real estate, tutors",pain:"Leads come in but are unqualified and lost",desc:"Structured intake, qualification and follow-up process.",mon:"Setup + monthly",rev:12,score:80,verdict:"Good Micro-SaaS Candidate",validation:"Offer manual lead qualification setup to 5 service businesses",risk:"Clients may still respond ad hoc"},
{id:50,name:"Channel Revenue Leak Audit",cat:"Agency Service",platform:"Both",target:"Sellers, creators, paid groups",pain:"Invisible operational leaks reduce revenue",desc:"Audit missed renewals, ignored leads, weak follow-up and unclear offers.",mon:"Audit fee, implementation fee",rev:12,score:77,verdict:"Good Agency/Service Candidate",validation:"Do 3 free leak audits showing missed money",risk:"ROI may be hard to prove"},
{id:51,name:"Local Payments + Membership Ops Layer",cat:"Funded Startup Idea",platform:"Both",target:"Creators, course sellers, communities",pain:"Payment and access are disconnected",desc:"Payment confirmation plus membership lifecycle infrastructure.",mon:"Subscription + transaction fee",rev:250,score:76,verdict:"Good Funded Startup Candidate",validation:"Manual payment-confirmation pilot for 2 creators",risk:"Payment errors, compliance, platform dependency"},
{id:52,name:"Seller Reputation & Review Collection Tool",cat:"Seller Tool",platform:"Both",target:"Informal sellers",pain:"Hard to prove credibility and collect testimonials",desc:"Tool/process for collecting and displaying buyer feedback.",mon:"Setup, subscription",rev:7,score:76,verdict:"Good Micro-SaaS Candidate",validation:"Build 3 sample review pages and pitch sellers",risk:"Fake reviews or low data trust"},
{id:53,name:"Messaging Commerce Training + Templates Subscription",cat:"Creator Tool",platform:"Both",target:"Sellers, admins, creators",pain:"Need ongoing operational playbooks and copy assets",desc:"Monthly templates, SOPs, scripts and mini-trainings.",mon:"Monthly subscription",rev:8,score:73,verdict:"Build First as Side Hustle",validation:"Open waitlist for monthly toolkit membership",risk:"Churn and content treadmill"},
{id:54,name:"Rubika/Baleh Business Ops Agency",cat:"Agency Service",platform:"Both",target:"SMEs using messaging as primary channel",pain:"Lack internal systems for chat-based sales/support",desc:"Full-stack setup and ongoing optimization for messaging operations.",mon:"Setup + monthly retainer",rev:40,score:75,verdict:"Good Agency/Service Candidate",validation:"Land 1 client with clear scope package",risk:"Scope creep, team dependency, ops heaviness"},
{id:55,name:"Enterprise Messaging Compliance / Archiving Layer",cat:"Enterprise/B2B Tool",platform:"More likely Baleh",target:"Regulated SMEs, finance, education, healthcare-adjacent teams",pain:"Lack controlled recordkeeping in chat workflows",desc:"Archive, SOP and governance layer for organizational messaging.",mon:"Licensing + services",rev:150,score:74,verdict:"Good Funded Startup Candidate",validation:"Interview 10 organizations using Baleh internally",risk:"Enterprise sales long and uncertain"},
{id:56,name:"Messaging Commerce ERP-lite for Small Sellers",cat:"SaaS",platform:"Both",target:"Growing small sellers",pain:"Juggling orders, stock, support and promos manually",desc:"Lightweight all-in-one seller workspace for messaging commerce.",mon:"Subscription",rev:20,score:81,verdict:"Good Funded Startup Candidate",validation:"Run operator-managed workspace for 3 sellers",risk:"Broad scope, risk of bloated product"}
];

const $ = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];

function scoreLevel(s){ return s>=78?'high':s>=70?'mid':'low'; }
function fitTag(platform){ return platform.includes('Baleh') ? 'baleh' : 'rubika'; }
function opportunityType(o){
  if(o.score>=80) return "Priority";
  if(o.verdict.includes("Funded")) return "Funded";
  if(o.verdict.includes("Micro")) return "Micro-SaaS";
  if(o.verdict.includes("Agency")) return "Agency";
  if(o.verdict.includes("Side")) return "Side Hustle";
  return "Test";
}
function formatRev(n){ return n+"M toman/mo"; }

function init(){
  const cats=[...new Set(DATA.map(o=>o.cat))].sort();
  const verdicts=[...new Set(DATA.map(o=>o.verdict))].sort();
  $('#category').innerHTML += cats.map(c=>`<option>${c}</option>`).join('');
  $('#verdict').innerHTML += verdicts.map(v=>`<option>${v}</option>`).join('');
  renderKpis();
  renderInsights();
  render();
}
function renderKpis(){
  const avg=Math.round(DATA.reduce((a,o)=>a+o.score,0)/DATA.length);
  const high=DATA.filter(o=>o.score>=78).length;
  const micro=DATA.filter(o=>o.verdict.includes("Micro")).length;
  const funded=DATA.filter(o=>o.verdict.includes("Funded")).length;
  const rev=DATA.reduce((a,o)=>a+o.rev,0);
  const k=[
    ["Total Opportunities",DATA.length,"Rubika × Baleh"],
    ["Average Score",avg+"/100","Strategic composite"],
    ["High Priority",high,"Score ≥ 78"],
    ["Micro-SaaS Paths",micro,"Lean scalable plays"],
    ["Funded Startup Paths",funded,"Larger capital plays"],
    ["Total Realistic Revenue",rev+"M","Combined monthly"]
  ];
  $('#kpis').innerHTML=k.map(x=>`<div class="kpi"><small>${x[0]}</small><strong>${x[1]}</strong><em>${x[2]}</em></div>`).join('');
}
function renderInsights(){
  const catCounts={};
  DATA.forEach(o=>catCounts[o.cat]=(catCounts[o.cat]||0)+1);
  const max=Math.max(...Object.values(catCounts));
  $('#categoryBars').innerHTML=Object.entries(catCounts).sort((a,b)=>b[1]-a[1]).slice(0,9).map(([c,n])=>`
    <div class="bar-row"><span>${c}</span><div class="bar"><i style="width:${n/max*100}%"></i></div><b>${n}</b></div>
  `).join('');
  $('#topList').innerHTML=[...DATA].sort((a,b)=>b.score-a.score).slice(0,6).map(o=>`
    <div class="top-item" onclick="openModal(${o.id})" style="cursor:pointer">
      <div><b>${o.name}</b><br><span>${o.cat} · ${formatRev(o.rev)}</span></div>
      <div class="score-badge">${o.score}</div>
    </div>
  `).join('');
  $('#heatmap').innerHTML=DATA.map(o=>`
    <div class="cell" data-level="${scoreLevel(o.score)}" data-tip="#${o.id} · ${o.name} · ${o.score}/100" onclick="openModal(${o.id})"></div>
  `).join('');
}
function getFiltered(){
  const q=$('#q').value.trim().toLowerCase();
  const cat=$('#category').value;
  const verdict=$('#verdict').value;
  const score=$('#score').value;
  const sort=$('#sort').value;
  let arr=DATA.filter(o=>{
    const text=[o.name,o.cat,o.target,o.pain,o.desc,o.verdict,o.risk].join(' ').toLowerCase();
    const scoreOk = score==="" ? true : score==="0" ? o.score<70 : o.score>=Number(score);
    return (!q || text.includes(q)) && (!cat || o.cat===cat) && (!verdict || o.verdict===verdict) && scoreOk;
  });
  arr.sort((a,b)=>{
    if(sort==="score-asc") return a.score-b.score;
    if(sort==="rev-desc") return b.rev-a.rev;
    if(sort==="id-asc") return a.id-b.id;
    return b.score-a.score;
  });
  return arr;
}
function render(){
  const arr=getFiltered();
  $('#results').innerHTML=arr.map(o=>`
    <article class="opp">
      <div class="opp-head">
        <h3>${o.id}. ${o.name}</h3>
        <div class="score-badge">${o.score}</div>
      </div>
      <div class="meta">
        <span class="tag ${fitTag(o.platform)}">${o.platform}</span>
        <span class="tag">${o.cat}</span>
        <span class="tag hot">${opportunityType(o)}</span>
      </div>
      <p class="desc">${o.desc}</p>
      <div class="mini">
        <div class="mini-row"><span>Score</span><div class="bar"><i style="width:${o.score}%"></i></div><b>${o.score}</b></div>
        <div class="mini-row"><span>Revenue</span><div class="bar"><i style="width:${Math.min(o.rev/300*100,100)}%;background:linear-gradient(90deg,var(--emerald),var(--cyan))"></i></div><b>${o.rev}M</b></div>
      </div>
      <div class="opp-foot">
        <div class="rev">Realistic revenue<br><b>${formatRev(o.rev)}</b></div>
        <button class="btn primary" onclick="openModal(${o.id})">Details</button>
      </div>
    </article>
  `).join('') || `<div class="card"><h3>No matching opportunities</h3><p style="color:var(--muted)">Try resetting filters.</p></div>`;

  $('#tableBody').innerHTML=arr.map(o=>`
    <tr>
      <td>${o.id}</td>
      <td><b>${o.name}</b></td>
      <td>${o.cat}</td>
      <td>${o.target}</td>
      <td>${o.pain}</td>
      <td>${formatRev(o.rev)}</td>
      <td><b>${o.score}</b></td>
      <td>${o.verdict}</td>
      <td><button class="btn primary" onclick="openModal(${o.id})">Open</button></td>
    </tr>
  `).join('');
}
function setView(mode){
  document.body.classList.toggle('table-mode',mode==='table');
  $('#cardBtn').classList.toggle('primary',mode==='card');
  $('#tableBtn').classList.toggle('primary',mode==='table');
}
function resetFilters(){
  ['q','category','verdict','score'].forEach(id=>$('#'+id).value='');
  $('#sort').value='score-desc';
  render();
}
function openModal(id){
  const o=DATA.find(x=>x.id===id);
  $('#mTitle').textContent=o.name;
  $('#mMeta').innerHTML=`
    <span class="tag ${fitTag(o.platform)}">${o.platform}</span>
    <span class="tag">${o.cat}</span>
    <span class="tag hot">${opportunityType(o)}</span>
    <span class="tag">Score ${o.score}/100</span>
    <span class="tag">${formatRev(o.rev)}</span>
  `;
  const pillar = getPillar(o);
  $('#mBody').innerHTML=`
    <div class="detail-grid">
      <div class="detail"><small>Target Customer</small><p>${o.target}</p></div>
      <div class="detail"><small>Customer Pain</small><p>${o.pain}</p></div>
      <div class="detail"><small>Product / Service</small><p>${o.desc}</p></div>
      <div class="detail"><small>Monetization</small><p>${o.mon}</p></div>
      <div class="detail"><small>First Validation Test</small><p>${o.validation}</p></div>
      <div class="detail"><small>Main Risks</small><p>${o.risk}</p></div>
      <div class="detail"><small>Verdict</small><p>${o.verdict}</p></div>
      <div class="detail"><small>KONKRED Pillar Fit</small><p>${pillar}</p></div>
    </div>
    <div class="audit">
      <b>Verified by KONKRED AUDIT</b>
      <div style="color:var(--muted);line-height:1.7">
        Recommended execution path: validate manually first inside Rubika/Baleh communities, avoid platform-API dependency until demand is proven,
        then productize into template, service, micro-SaaS, or funded infrastructure based on retention and willingness to pay.
      </div>
    </div>
  `;
  $('#modal').classList.add('show');
  document.body.style.overflow='hidden';
}
function getPillar(o){
  const c=o.cat.toLowerCase();
  if(c.includes('marketplace')||c.includes('funded')) return "Marketplace-led: discovery, transactions, listings, trust, or take-rate potential.";
  if(c.includes('education')||c.includes('template')||c.includes('creator')||c.includes('community')) return "Academy-led: templates, SOPs, training, enablement, and knowledge productization.";
  return "Forge-led: workflow tool, MVP system, automation layer, operational dashboard, or SaaS pathway.";
}
function closeModal(){
  $('#modal').classList.remove('show');
  document.body.style.overflow='';
}
document.addEventListener('keydown',e=>{ if(e.key==='Escape') closeModal(); });
init();
</script>
</body>
</html>
```