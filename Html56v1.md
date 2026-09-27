عالی — حالا همه ردیف‌ها را داریم و می‌توانم فایل نهایی را بدهم.

چون شما گفتی فقط «فایل HTML کامل و production-ready» می‌خواهی، مستقیم خود فایل را می‌دهم.  
این نسخه:

- همه 56 ردیف را دارد
- سرچ زنده دارد
- فیلتر بر اساس Category / Platform Fit / Business Type / Verdict دارد
- sortable columns دارد
- responsive است
- dark/light theme toggle دارد
- sticky header دارد
- export CSV دارد
- بدون dependency خارجی است
- فقط یک فایل HTML است

> نکته: چون در پیام قبلی شما ردیف‌های 44 تا 56 را فرستادی و قبل‌تر 32 تا 43 هم آمده بود، این نسخه را به‌صورت self-contained ساختم.  
> اگر خواستی مرحله بعدی، من همین را به نسخه‌های زیر هم تبدیل می‌کنم:
> - `index.html + data.json`
> - نسخه با pagination
> - نسخه با cards/table switch
> - نسخه با score heatmap
> - نسخه فارسی RTL

---

## فایل `index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Master Opportunity Table — Rubika & Baleh</title>
  <style>
    :root {
      --bg: #0b1020;
      --panel: #121933;
      --panel-2: #182142;
      --text: #e8ecf8;
      --muted: #a8b3cf;
      --border: #2a3563;
      --accent: #6ea8fe;
      --accent-2: #7ee787;
      --warn: #ffd166;
      --danger: #ff6b6b;
      --shadow: 0 8px 24px rgba(0,0,0,.25);
    }

    body.light {
      --bg: #f5f7fb;
      --panel: #ffffff;
      --panel-2: #f1f4fb;
      --text: #111827;
      --muted: #5b6475;
      --border: #d9e0ef;
      --accent: #2563eb;
      --accent-2: #059669;
      --warn: #d97706;
      --danger: #dc2626;
      --shadow: 0 8px 24px rgba(16,24,40,.08);
    }

    * { box-sizing: border-box; }
    html, body { margin: 0; padding: 0; }
    body {
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.45;
    }

    .container {
      max-width: 1600px;
      margin: 0 auto;
      padding: 24px;
    }

    .topbar {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 16px;
      align-items: start;
      margin-bottom: 20px;
    }

    .title h1 {
      margin: 0 0 8px;
      font-size: 28px;
      line-height: 1.2;
    }

    .title p {
      margin: 0;
      color: var(--muted);
      font-size: 14px;
    }

    .actions {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      justify-content: flex-end;
    }

    button, select, input {
      border: 1px solid var(--border);
      background: var(--panel);
      color: var(--text);
      border-radius: 12px;
      padding: 10px 12px;
      font-size: 14px;
      outline: none;
    }

    button {
      cursor: pointer;
      transition: .2s ease;
    }

    button:hover {
      transform: translateY(-1px);
      border-color: var(--accent);
    }

    .toolbar {
      display: grid;
      grid-template-columns: 2fr repeat(4, 1fr);
      gap: 12px;
      margin-bottom: 16px;
    }

    .card {
      background: linear-gradient(180deg, var(--panel), var(--panel-2));
      border: 1px solid var(--border);
      border-radius: 18px;
      box-shadow: var(--shadow);
    }

    .stats {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 12px;
      margin-bottom: 16px;
    }

    .stat {
      padding: 14px 16px;
    }

    .stat .label {
      font-size: 12px;
      color: var(--muted);
      margin-bottom: 6px;
    }

    .stat .value {
      font-size: 24px;
      font-weight: 700;
    }

    .table-wrap {
      overflow: auto;
      border-radius: 18px;
      border: 1px solid var(--border);
      box-shadow: var(--shadow);
      background: var(--panel);
    }

    table {
      width: 100%;
      border-collapse: collapse;
      min-width: 1800px;
    }

    thead th {
      position: sticky;
      top: 0;
      background: rgba(18, 25, 51, 0.96);
      backdrop-filter: blur(6px);
      z-index: 2;
    }

    body.light thead th {
      background: rgba(255, 255, 255, 0.96);
    }

    th, td {
      padding: 10px 12px;
      border-bottom: 1px solid var(--border);
      border-right: 1px solid var(--border);
      text-align: left;
      vertical-align: top;
      font-size: 13px;
    }

    th:last-child, td:last-child { border-right: none; }

    th {
      user-select: none;
      cursor: pointer;
      white-space: nowrap;
    }

    tbody tr:hover {
      background: rgba(110, 168, 254, 0.06);
    }

    .muted { color: var(--muted); }
    .tag {
      display: inline-block;
      padding: 4px 8px;
      border: 1px solid var(--border);
      border-radius: 999px;
      font-size: 12px;
      white-space: nowrap;
      background: rgba(255,255,255,.03);
    }

    .score {
      font-weight: 700;
      padding: 4px 8px;
      border-radius: 999px;
      display: inline-block;
      min-width: 48px;
      text-align: center;
    }

    .score.high { background: rgba(126,231,135,.15); color: var(--accent-2); }
    .score.mid { background: rgba(255,209,102,.12); color: var(--warn); }
    .score.low { background: rgba(255,107,107,.12); color: var(--danger); }

    .small {
      font-size: 12px;
      color: var(--muted);
    }

    .footer-note {
      margin-top: 12px;
      color: var(--muted);
      font-size: 12px;
      text-align: right;
    }

    @media (max-width: 1200px) {
      .toolbar { grid-template-columns: 1fr 1fr; }
      .stats { grid-template-columns: repeat(2, 1fr); }
      .topbar { grid-template-columns: 1fr; }
      .actions { justify-content: flex-start; }
    }

    @media (max-width: 720px) {
      .container { padding: 14px; }
      .toolbar { grid-template-columns: 1fr; }
      .stats { grid-template-columns: 1fr; }
      .title h1 { font-size: 22px; }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="topbar">
      <div class="title">
        <h1>Master Opportunity Table — Rubika & Baleh</h1>
        <p>
          Search, sort, filter, and export a structured opportunity landscape for messaging-based products and services.
        </p>
      </div>

      <div class="actions">
        <button id="themeToggle">Toggle Theme</button>
        <button id="resetFilters">Reset Filters</button>
        <button id="exportCsv">Export CSV</button>
      </div>
    </div>

    <div class="stats">
      <div class="card stat">
        <div class="label">Visible Ideas</div>
        <div class="value" id="visibleCount">0</div>
      </div>
      <div class="card stat">
        <div class="label">Average Score</div>
        <div class="value" id="avgScore">0</div>
      </div>
      <div class="card stat">
        <div class="label">Top Category</div>
        <div class="value" id="topCategory">—</div>
      </div>
      <div class="card stat">
        <div class="label">Top Verdict</div>
        <div class="value" id="topVerdict">—</div>
      </div>
      <div class="card stat">
        <div class="label">Platform Focus</div>
        <div class="value" id="topPlatform">—</div>
      </div>
    </div>

    <div class="toolbar">
      <input id="searchInput" type="text" placeholder="Search across all fields..." />
      <select id="categoryFilter"><option value="">All Categories</option></select>
      <select id="platformFilter"><option value="">All Platforms</option></select>
      <select id="businessTypeFilter"><option value="">All Business Types</option></select>
      <select id="verdictFilter"><option value="">All Verdicts</option></select>
    </div>

    <div class="table-wrap card">
      <table id="ideasTable">
        <thead>
          <tr id="headerRow"></tr>
        </thead>
        <tbody id="tableBody"></tbody>
      </table>
    </div>

    <div class="footer-note">
      Single-file HTML • No external dependencies • Client-side search/filter/sort/export
    </div>
  </div>

  <script>
    const columns = [
      "#","Idea Name","Category","Platform Fit","Target Customer","Customer Pain","Product/Service Description",
      "Simplest MVP","Full Version / Scaled Version","Business Type","Founder Type Fit","Budget Needed",
      "Team Needed","Needs Funding?","Needs API/Integration?","Setup Complexity 1-5","Operational Complexity 1-5",
      "Maintenance 1-5","Support Burden 1-5","Sales Difficulty 1-5","Trust/Legal Risk 1-5","Platform Dependency Risk 1-5",
      "Time to MVP","Time to Full Product","Initial Workload","Weekly Work After Launch","Monetization Model",
      "Suggested Price Range","Conservative Monthly Revenue","Realistic Monthly Revenue","Optimistic Monthly Revenue",
      "Income-to-Work Ratio 1-5","Pain Severity 1-5","Frequency of Pain 1-5","Willingness to Pay 1-5",
      "Scalability 1-5","Defensibility 1-5","Zero-Budget Feasibility 1-5","Side-Hustle Fit 1-5",
      "Startup/Funding Fit 1-5","Overall Score /100","Verdict","First Validation Test","First 3 Launch Tasks",
      "Main Risks","Kill Criteria","Notes"
    ];

    const data = [
      [1,"FAQ & Ready Replies Pack for Sellers","Template/Productized Asset","Both","informal sellers, channel shops","repetitive questions waste time","ready-made replies for price, stock, shipping, payment, objections","PDF/Doc with 50-100 reply templates","searchable library + niche packs + generator","B2B","Zero-budget solo founder, Side-hustle founder","Zero","1","No","No",1,1,1,1,2,1,1,"1-2 days","2-4 weeks","low","very low","one-time sale, bundles","300k-1.2M",1,5,20,5,4,5,3,4,2,5,5,2,78,"Build First as Side Hustle","DM 30 sellers and offer 10 free samples + paid full pack","write 50 replies, create sample PDF, DM 30 sellers","seen as commodity, easy copying","<3 serious leads from 30 DMs","one of the cleanest low-friction products"],
      [2,"Sales Channel Organization Kit","Template/Productized Asset","Both","channel admins, shop owners","messy pricing, ordering rules, scattered posts","post templates, pinned post structure, order rules, return policy templates","PDF + checklist + copy-ready post set","vertical-specific kits + brand-customized version","B2B","Zero-budget solo founder, Side-hustle founder","Zero","1","No","No",1,1,1,1,2,1,1,"2-3 days","2-3 weeks","low","very low","one-time sale","400k-1.5M",1,6,20,5,4,4,3,4,2,5,5,2,77,"Build First as Side Hustle","sell mockup to 10 active channels","collect messy channel examples, create before/after kit, outreach to 20 admins","perceived as “just content”","nobody pays after seeing clear before/after","stronger if niche-specific: fashion, cosmetics, education"],
      [3,"Mini CRM Sheet for Order Tracking","Seller Tool","Both","small sellers","orders get lost in DMs","sheet to track order, payment, shipping, follow-up","Excel/Google Sheet template","lightweight web CRM with statuses + reminders","Hybrid","Zero-budget solo founder, Technical solo founder","Zero","1","Not initially","Optional",2,2,2,2,3,2,1,"1-3 days","1-3 months","low","low","one-time sale, setup fee, subscription later","500k-2.5M",2,8,30,4,5,5,4,4,3,5,4,3,81,"Build First as Side Hustle","offer manual setup to 5 sellers for discounted fee","build sheet, record 5-min tutorial, message sellers using DM-based ordering","users may not maintain data entry","sellers stop using after 3 days","strong bridge from template to micro-SaaS"],
      [4,"Paid Membership Renewal Tracker","Membership Tool","Both","paid channels, tutors, paid communities","renewals forgotten, member expiry unmanaged","expiry tracker + renewal message templates + member sheet","Excel/Sheet + reminder templates","dashboard + auto reminders + access workflows","Hybrid","Side-hustle founder, Technical solo founder, Small team","Very Low","1-2","Not initially","Requires verification",2,3,2,2,3,3,3,"2-4 days","2-4 months","medium","low","setup fee + monthly subscription","700k-3M",2,10,40,4,5,4,4,4,3,4,4,4,79,"Good Micro-SaaS Candidate","audit 3 paid groups and show missed renewals manually","create renewal sheet, prepare reminder scripts, approach 10 course/community owners","users may expect full automated access control","nobody cares enough to pay for reminder discipline","access automation depends on permissions/API"],
      [5,"Educational Community Onboarding Pack","Education Tool","Both","tutors, course owners, class admins","new members ask same questions repeatedly","welcome message, rules, study map, FAQ, pinned post templates","PDF/Doc pack for 3 education niches","onboarding generator + LMS-lite integration","Creator Economy","Zero-budget solo founder, Side-hustle founder","Zero","1","No","No",1,1,1,1,2,1,1,"1-2 days","2-4 weeks","low","very low","one-time sale","500k-2M",1,5,15,5,4,4,4,4,2,5,5,2,79,"Build First as Side Hustle","offer free sample welcome kit to 10 tutors","draft education-specific pack, create sample, outreach in tutor groups","high request for customization","all leads ask for free advice only","better in exam/language/skills niches"],
      [6,"Order Intake Form Setup","Seller Tool","Both","DM-based sellers","addresses/products/details get lost in chat","create simple order form linked to structured sheet","form + sheet + usage guide","branded multi-step checkout-like intake system","Hybrid","Zero-budget solo founder, Non-technical operator","Zero","1","No","Optional",2,2,2,2,2,2,1,"1 day","1-2 months","low","low","setup fee, template sale","500k-1.5M",2,7,25,4,5,5,4,4,2,5,5,3,80,"Build First as Side Hustle","manually set up 5 forms for active sellers","build generic form, make 1 demo, message sellers with “orders getting lost?”","buyers may refuse filling forms","sellers report low buyer completion rate","very practical if niche already has purchase intent"],
      [7,"Appointment Booking Kit for Service Providers","Service Tool","Both","beauty clinics, tutors, repairmen, consultants","booking through chat is messy and time-consuming","intake form + schedule rules + confirmation messages","form + calendar + templates","booking SaaS with reminders and rescheduling","Hybrid","Side-hustle founder, Technical solo founder, Small team","Very Low","1-2","Not initially","Optional",2,2,2,2,3,2,1,"2-4 days","2-3 months","low","low","setup + monthly","700k-3M",3,10,35,4,4,4,4,4,3,5,4,4,79,"Good Micro-SaaS Candidate","offer free setup to 2 salons/tutors in exchange for testimonial","build booking form, create confirmation templates, pitch service providers","each vertical needs custom workflow","<2 willing pilots after 20 outreaches","works beyond Rubika/Baleh too"],
      [8,"30-Day Content Calendar Pack","Creator Tool","Both","creators, channel admins","no publishing consistency, idea fatigue","ready content calendar with post ideas, CTA, caption prompts","PDF/Sheet pack","niche-specific planner + AI assistant","Creator Economy","Zero-budget solo founder","Zero","1","No","No",1,1,1,1,3,1,1,"1-2 days","2-4 weeks","low","very low","one-time sale","300k-1M",0.5,4,12,5,3,4,3,4,2,5,5,2,72,"Build First as Side Hustle","post sample 7-day content plan and ask for preorders","create one niche pack, publish samples, DM creators","pain not directly tied to revenue","very low conversion to paid","better as upsell, not standalone core business"],
      [9,"Group Rules & Anti-Spam Pack","Community Tool","Both","group admins","repeated rule violations, manual warnings","rules template, warning scripts, moderation policy checklist","PDF + spreadsheet","moderation workflow tool + bot if possible","B2B","Zero-budget solo founder, Agency/operator","Zero","1","No","Requires verification",1,2,1,2,3,2,3,"1-2 days","1-2 months","low","low","one-time sale","300k-1M",0.5,3,10,4,3,4,2,3,2,5,4,2,66,"Test Cheaply","interview 15 group admins about moderation pain","create rules pack, warning templates, outreach to communities","admins often low willingness to pay","no admin agrees to even small payment","works better as service add-on"],
      [10,"Trust Mini-Landing for Sellers","Seller Tool","Both","informal sellers lacking trust signals","buyers don’t trust unknown sellers","mini landing page with rules, FAQs, reviews, buying steps","simple HTML/Notion-like page","hosted storefront/profile pages with trust badges","Hybrid","Side-hustle founder, Small agency, Small team","Very Low","1-2","Not initially","Optional",2,2,2,2,3,3,2,"2-5 days","2-3 months","medium","low","setup fee + optional hosting","1M-3M",2,8,30,4,4,3,4,4,3,4,4,4,76,"Good Agency/Service Candidate","create before/after trust page for 3 sellers and ask for paid setup","build sample page, collect testimonial layout, outreach to active shops","hard to prove direct conversion lift","low perceived ROI","stronger for higher-ticket categories"],
      [11,"Sales Follow-up & Win-back Message Bank","Template/Productized Asset","Both","sellers, SMEs","no system for following up leads/customers","messages for reminders, upsells, win-back, payment nudges","PDF/Doc","segmented CRM-driven campaign assistant","B2B","Zero-budget solo founder","Zero","1","No","No",1,1,1,1,2,1,1,"1 day","2-4 weeks","low","very low","one-time sale","300k-900k",1,5,20,5,4,5,3,4,2,5,5,2,78,"Build First as Side Hustle","send 10-message free sample to 30 sellers","write 100 messages, group by scenario, send teaser sample","commodity risk","zero paid uptake after free interest","easy bundle with CRM/form products"],
      [12,"Manual Channel Analytics Sheet","Analytics Tool","Both","channel admins, creators","can’t tell what content performs or sells","simple tracking sheet for post type, response, conversions","spreadsheet + dashboard","automated analytics platform","Hybrid","Zero-budget solo founder, Technical solo founder","Zero","1","Not initially","Requires verification",2,2,2,2,3,1,3,"2-3 days","2-4 months","low","low","template sale, subscription later","500k-1.5M",1,4,15,4,3,3,3,4,3,5,4,4,70,"Test Cheaply","give sheet to 5 admins for 7 days and ask if they continue usage","build dashboard, create tutorial, recruit 5 testers","manual data entry fatigue","testers stop using after trial","automation potential depends on data access"],
      [13,"Paid Educational Channel Launch Kit","Education Tool","Both","tutors, experts, creators","don’t know how to structure paid channel/community","pricing, offers, launch messaging, content plan, renewal flow","PDF + sheet + scripts","creator membership platform toolkit","Creator Economy","Zero-budget solo founder, Side-hustle founder, Small team","Zero","1","No","Optional",1,1,1,1,3,2,2,"2-4 days","1-2 months","low","very low","one-time sale, consulting upsell","900k-3M",2,8,25,5,5,3,4,4,3,5,4,3,78,"Build First as Side Hustle","interview 10 tutors considering paid community","make launch checklist, create sample sales page copy, DM tutors","founders may just want free advice","no preorders from interested tutors","better with niche-specific examples"],
      [14,"Niche Directory of Channels/Groups","Marketplace","Both","users, advertisers, admins","good channels/groups hard to discover","curated directory by topic/quality","simple list/channel/site","searchable marketplace + ranking + ads","Marketplace","Side-hustle founder, Small team","Very Low","1-2","Helpful","Optional",2,3,3,2,4,2,3,"3-7 days","3-6 months","medium","medium","ads, paid listing, sponsorship","200k-5M",0.5,5,50,2,3,3,2,4,2,4,2,4,60,"Test Cheaply","launch one niche directory and collect 50 signups/submissions","choose one niche, curate 50 communities, sell 5 featured spots","monetization weak early, quality control","no submissions/no advertisers","only good if highly niche or traffic-rich"],
      [15,"Done-for-You Seller Ops Setup","Manual Service","Both","small sellers","business runs chaotically in chat","manual setup of FAQ, order form, CRM sheet, policy posts","one-time setup package","productized operations agency","Agency/Service","Agency/operator, Non-technical operator","Very Low","1","No","Optional",2,4,3,3,3,2,1,"2-5 days","1-2 months","medium","medium","setup fee","2M-8M",4,15,50,3,5,5,4,2,3,4,3,3,74,"Good Agency/Service Candidate","offer setup service to 5 sellers manually","define package scope, create checklist, outreach to shops","turns into custom service swamp","each client demands endless tweaks","profitable but not passive"],
      [16,"DM Customer Support Outsourcing for Sellers","Customer Support Tool","Both","sellers, SMEs","owner overwhelmed by buyer questions","outsourced manual support handling","concierge support for one seller","support team + SOP software","Agency/Service","Agency/operator, Small team","Low","1-3","Helpful","Optional",2,5,4,5,3,3,2,"2-5 days","2-6 months","high","high","monthly retainer","3M-20M",5,20,80,2,5,5,4,2,2,3,1,3,63,"Too Operational","pilot with 1 seller for one week","define coverage hours, prepare response SOP, onboard one client","24/7 expectations, burnout, quality inconsistency","poor margins or nonstop support load","attractive revenue, dangerous operations"],
      [17,"Payment Receipt Verification Service","Manual Service","Both","paid groups, course sellers","manually matching receipts is painful","human verification of receipts and membership status","concierge receipt matching","semi-automated finance ops platform","Agency/Service","Agency/operator, Small team","Low","1-2","Helpful","Requires verification",2,5,4,4,3,4,3,"2-4 days","3-6 months","high","medium-high","monthly service fee","2M-15M",4,18,70,3,5,5,4,2,3,3,2,4,72,"Operational but Real Pain","manually process receipts for 2 course sellers","build verification flow, define turnaround SLA, onboard pilot","high ops load, payment proof ambiguity","too many disputes or slow turnaround","real pain but ops-heavy"],
      [18,"Simple Seller SOP Pack","Template/Productized Asset","Both","small sellers, new admins","no documented operating process","SOPs for order handling, support, follow-up, refund handling","PDF/Doc SOP pack","interactive SOP builder","B2B","Zero-budget solo founder, Side-hustle founder","Zero","1","No","No",1,1,1,1,2,1,1,"1-2 days","2-4 weeks","low","very low","one-time sale","300k-1.2M",1,5,18,5,4,4,3,4,2,5,5,2,76,"Build First as Side Hustle","sell SOP starter pack to 10 sellers","create 5 SOPs, make sample preview, outreach","copyability","no paid conversion after interest","good bundle with forms and reply packs"],
      [19,"Lead Tracking Sheet for Service Providers","Service Tool","Both","consultants, clinics, tutors","leads fall through cracks in chat","sheet for lead stage, follow-up, status","sheet + short tutorial","mini CRM for service businesses","Hybrid","Zero-budget solo founder, Side-hustle founder","Zero","1","Not initially","Optional",2,2,2,2,3,1,1,"1-2 days","1-2 months","low","low","template + setup","500k-2M",2,7,25,4,4,5,4,4,3,5,5,3,79,"Good Micro-SaaS Candidate","set up for 3 clinics/tutors manually","build lead tracker, define stages, outreach","requires user discipline","users abandon manual updates","great bridge into service CRM"],
      [20,"Channel Audit & Improvement Report","Agency Service","Both","channel owners, sellers, educators","don’t know why channel underperforms","audit content, funnel, trust, conversion blockers","one-off report","retained channel growth advisory","Agency/Service","Agency/operator, Small agency","Very Low","1","No","No",2,3,2,3,3,2,1,"2-4 days","1-2 months","medium","low","audit fee","2M-10M",3,12,40,4,4,4,4,2,3,5,4,3,75,"Good Agency/Service Candidate","do 3 free audits and upsell fixes","create audit checklist, sample report, outreach","hard to prove ROI fast","nobody buys implementation after audit","good entry service"],
      [21,"Micro-CRM for Rubika/Baleh Sellers","Seller Tool","Both","small-to-mid sellers using chat for orders","DMs and order follow-ups are chaotic","lightweight CRM for tracking leads, orders, statuses, reminders","manual spreadsheet + status workflow","micro-SaaS CRM with reminders, canned replies, customer history","SaaS","Technical solo founder, Small team","Low-Medium","1-2","Helpful","Requires verification",3,3,3,3,3,2,3,"2-4 weeks","4-8 months","medium","medium","subscription","1M-6M/mo",3,15,100,4,5,5,4,5,4,3,4,5,82,"Strong SaaS Candidate","pilot a manual CRM workflow with 5 sellers","define stages, build sheet MVP, recruit pilot users","platform integration limitations","pilots don’t maintain usage","best direct bridge from service problem to software"],
      [22,"Comment/DM Auto-Responder Assistant","Seller Tool","Both","busy sellers, creators","slow response loses sales","tool layer for fast suggested replies and lead tagging","manual assistant + macro bank","AI-assisted inbox companion","SaaS","Technical solo founder","Low-Medium","1-2","Helpful","Requires verification",3,3,3,3,3,2,4,"2-4 weeks","4-8 months","medium","medium","subscription","1M-5M/mo",2,12,80,4,4,5,4,4,3,2,4,4,76,"Needs Platform/API Verification","test response-speed value with manual concierge","make canned-reply workflow, pilot with 3 sellers","API and automation limits","no measurable speed/conversion gain","good if assistant sits outside platform rather than deep integration"],
      [23,"Seller Analytics & Conversion Dashboard","Analytics Tool","Both","serious sellers, growth-focused channel owners","no visibility into funnel and conversion bottlenecks","dashboard for inquiries, orders, conversion rate, repeat buyers","manual spreadsheet with weekly review","analytics SaaS with benchmarks and recommendations","SaaS","Technical solo founder, Small team","Low-Medium","1-2","Helpful","Requires verification",3,3,3,2,3,1,3,"2-4 weeks","4-8 months","medium","low-medium","subscription","1M-8M/mo",2,14,90,4,4,4,4,5,4,3,4,5,78,"Good SaaS Candidate","manually build dashboards for 3 sellers and charge monthly","define metrics, create sample dashboards, recruit pilots","manual data collection burden","users won’t input data regularly","works best bundled with CRM or order tracker"],
      [24,"Receipt Matching + Access Granting Workflow","Membership Tool","Both","paid groups, course/channel owners","payment confirmation and access granting are manual","workflow for verifying receipts, tracking payment status, granting membership","human-in-the-loop ops service","semi-automated operator dashboard + workflow tool","Hybrid","Agency/operator, Technical founder","Low-Medium","1-2","Helpful","Requires verification",3,5,4,4,3,4,4,"1-2 weeks","4-8 months","high","medium-high","setup + monthly service","2M-12M/mo",4,20,120,3,5,5,4,4,3,2,3,4,77,"Strong Service-to-SaaS Bridge","run manual payment confirmation for 2 paid communities","map payment workflow, create operator sheet, define SLA","high operational burden, disputes","too many errors or manual load","promising if narrowed to a niche like tutors"],
      [25,"Membership Renewal & Churn Prevention Tool","Membership Tool","Both","creators, tutors, paid communities","members silently expire and churn","renewal reminders, save offers, churn tracking, follow-up workflows","manual reminder + renewal tracking sheet","subscription software with churn automation","SaaS","Technical solo founder, Small team","Low-Medium","1-2","Helpful","Requires verification",3,3,3,3,3,2,3,"2-4 weeks","4-8 months","medium","medium","subscription","1M-8M/mo",3,14,100,4,5,4,4,5,4,3,4,5,80,"Strong Micro-SaaS Candidate","manually recover expired members for 3 communities","build churn workflow, create reminder templates, recruit pilots","owners may not feel churn enough","no measurable recovery improvement","strong recurring pain where paid membership exists"],
      [26,"Channel Sales Funnel Setup Service","Agency Service","Both","sellers, tutors, creators","no clear path from visitor to buyer","service to design offers, pinned posts, lead capture, follow-up flow","manual funnel setup","productized funnel agency + software tooling","Agency/Service","Agency/operator, Small agency","Low","1-2","No","Optional",2,4,3,3,3,2,1,"1-2 weeks","2-4 months","medium","medium","setup fee + upsell","3M-15M",4,18,80,3,4,4,4,3,3,4,3,3,73,"Good Agency Candidate","set up funnels for 3 clients manually","create funnel checklist, before/after examples, outreach","customization overload","clients don’t attribute sales lift","good service cash flow, weaker software angle"],
      [27,"Seller Trust Badge / Proof Pack","Seller Tool","Both","small sellers with trust issues","buyers hesitate without proof","package of testimonials, policies, proof assets, trust formatting","done-for-you trust asset pack","software/profile layer for trust verification","Hybrid","Side-hustle founder, Small agency","Very Low","1","Not initially","Optional",2,2,2,2,3,3,2,"2-5 days","1-2 months","medium","low","setup fee","1M-4M",2,9,35,4,4,4,4,4,3,4,4,4,77,"Good Side-Hustle/Service Candidate","create 3 sample trust packs and pitch sellers","define trust elements, build examples, outreach","benefit may feel intangible","no seller believes conversion impact","works best in higher-trust-sensitive categories"],
      [28,"Pre-Sales Qualification Flow for Service Businesses","Service Tool","Both","clinics, consultants, tutors, real estate agents","time wasted on low-quality inquiries","structured qualification intake and response workflow","form + script + sheet","qualification SaaS with routing and reminders","Hybrid","Zero-budget solo founder, Technical solo founder","Zero-Very Low","1","Not initially","Optional",2,2,2,2,2,1,1,"2-4 days","1-2 months","low","low","setup fee + template","700k-3M",2,8,30,4,4,5,4,4,3,5,5,3,80,"Strong Low-Cost Opportunity","set up qualification workflow for 3 service providers","create form, define qualification logic, outreach","providers may still prefer ad hoc chat","no reduction in wasted inquiries","especially good for appointment-based businesses"],
      [29,"Broadcast Content Ops Tool for Channels","Creator Tool","Both","content-heavy channels","publishing and planning are inconsistent","workflow tool for content planning, asset tracking, posting cadence","sheet + content calendar MVP","creator ops SaaS with collaboration and scheduling","SaaS","Technical solo founder, Small team","Low-Medium","1-2","Helpful","Requires verification",3,3,3,2,3,1,3,"2-4 weeks","4-8 months","medium","low-medium","subscription","1M-6M/mo",2,10,70,4,3,4,3,4,3,3,4,4,72,"Moderate SaaS Candidate","pilot planning workflow with 3 active channels","create planning board, recruit creators, test retention","pain may not be monetizable enough","weak retention after novelty","better as part of creator suite"],
      [30,"Channel Growth Experiment Tracker","Analytics Tool","Both","admins, creators, growth operators","no memory of what growth experiments worked","logging system for experiments, results, learnings","Notion/sheet tracker","growth OS with templates and insights","Hybrid","Zero-budget solo founder, Technical solo founder","Zero","1","No","No",1,1,1,1,3,1,1,"1-2 days","2-4 weeks","low","very low","template sale","300k-1M",0.5,3,10,5,3,3,2,3,2,5,5,2,65,"Bundle/Upsell Material","sell tracker as add-on to audit/consulting","make experiment tracker, pair with content planner, outreach","not painful enough standalone","no one uses after download","useful only bundled with more urgent tools"],
      [31,"Paid Community Admin OS","Membership Tool","Both","admins of paid communities","member management and support are chaotic","workspace for member list, support issues, renewals, content ops","sheet + SOP system","admin operating system for paid communities","Hybrid","Technical solo founder, Small team","Low-Medium","1-2","Helpful","Requires verification",3,4,3,3,3,2,3,"2-4 weeks","4-8 months","medium","medium","subscription + setup","1M-8M/mo",3,15,100,4,5,4,4,4,4,3,4,5,79,"Strong Niche SaaS Candidate","operate 2 paid communities manually using your system","define workflows, build dashboard mockup, recruit pilot admins","niche may be too small initially","admins unwilling to formalize ops","strong if paid communities grow"],
      [32,"Paid Community Membership SaaS","SaaS","Both","course owners, creators, premium communities","managing paid members and renewals manually is painful","member lifecycle tool for onboarding, renewal, expiry, segmentation","sheet + reminder MVP","full SaaS with billing/workflows/access logic","SaaS","Technical solo founder, Small team, Funded startup","Medium","2-4","Likely","Requires verification",4,3,3,3,4,3,4,"1-2 months","6-12 months","high","medium","subscription + setup","1M-10M/mo per client",4,20,150,4,5,4,4,5,4,2,3,5,82,"Good Funded Startup Candidate","pilot manual member management for 3 communities","define member states, build operator dashboard mockup, recruit creators","access automation/API dependence","communities too small to pay SaaS price","good if creator economy grows inside Iran"],
      [33,"Messaging-Based Customer Support Desk","Customer Support Tool","Both","SMEs using Rubika/Baleh for support","support requests scattered across chats","inbox/helpdesk for ticketing and team replies","manual tagging sheet + SOP","omnichannel helpdesk with SLA and canned replies","SaaS","Technical solo founder, Small team, Funded startup","Medium","2-4","Likely","Requires verification",4,4,3,4,4,3,4,"1-2 months","6-12 months","high","medium-high","subscription","1M-8M/mo per client",3,18,120,3,5,5,4,5,4,2,2,5,79,"Good Funded Startup Candidate","interview 15 SMEs handling support in chat","define ticket workflow, mock inbox UI, run manual shared inbox pilot","deep integration may be blocked","no meaningful team-support use case","bigger opportunity than seller FAQ packs"],
      [34,"Chatbot for FAQs and Lead Qualification","Bot","Both","sellers, service providers, communities","repetitive inbound questions","bot that answers FAQs and collects lead/order info","scripted flow prototype","AI-assisted bot with analytics and routing","SaaS","Technical solo founder, Small team","Low-Medium","1-3","Helpful","Requires verification",4,3,3,3,3,2,4,"2-4 weeks","4-8 months","medium-high","medium","setup + subscription","1M-6M",2,12,80,3,4,5,4,5,3,2,2,4,74,"Needs Platform/API Verification","test bot demand with fake demo and preorders","pick 1 use case, script flow, show demo to 20 prospects","no API/support for real bot deployment","preorders absent despite interest","demand likely real; execution uncertain"],
      [35,"Auto Reminder Bot for Renewals/Payments","Bot","Both","paid groups, tutors, sellers","reminders are manual and inconsistent","bot for expiry/payment/order reminders","manual reminder concierge MVP","fully automated reminder system","SaaS","Technical solo founder, Small team","Low-Medium","1-2","Helpful","Requires verification",4,2,3,2,3,2,4,"2-4 weeks","3-6 months","medium","low-medium","subscription","500k-4M",2,10,60,4,4,4,4,5,3,2,3,4,75,"Needs Platform/API Verification","manually run reminders for 3 customers before automating","define trigger list, build dashboard mockup, recruit 3 pilots","automation access unknown","customers happy with manual reminders only","strong if messaging APIs allow outbound workflows"],
      [36,"Group Moderation Bot","Bot","Both","large groups","spam and rule-breaking are constant","bot to warn, filter, auto-respond to violations","moderation policy + manual action MVP","full moderation bot with admin panel","SaaS","Technical solo founder, Small team","Low-Medium","1-2","Helpful","Requires verification",4,3,3,3,3,2,5,"3-5 weeks","4-8 months","medium-high","medium","subscription","500k-5M",1,8,50,3,4,5,3,5,3,1,2,4,69,"Needs Platform/API Verification","interview 15 admins and show fake moderation dashboard","define moderation rules, create prototype UI, recruit 3 pilot groups","blocked by API/policy, noisy edge cases","no deployable access path","attractive but high platform dependence"],
      [37,"Community Discovery & Recommendation App","Marketplace","Both","ordinary users, advertisers, communities","discovering quality groups/channels is inefficient","app/site recommending communities by interest","curated list MVP","algorithmic discovery + ads + paid placement","Marketplace","Small team, Funded startup","Medium","2-4","Likely","Optional",4,4,4,3,5,2,3,"1-2 months","6-12 months","high","medium","ads, lead gen, featured listings","0",10,100,500,2,3,4,2,5,3,2,1,5,68,"Good Funded Startup Candidate","build one niche directory and track retention","curate 200 communities, publish ranking, sell featured slots","cold start and traffic challenge","no repeat traffic after launch","more media business than clean SaaS"],
      [38,"Rubika/Baleh Ad Network for Channels","Funded Startup Idea","Both","advertisers, channel owners","buying ads in channels is fragmented and untrusted","marketplace for channel ads, placements, reporting","manual brokerage MVP","full ad network with analytics and escrow","Marketplace","Small team, Funded startup, Platform partner","Medium-High","3-5","Yes","Requires verification",4,5,4,4,5,4,4,"1-2 months","6-12 months","high","high","take rate, managed campaigns","0",20,150,"1B+",3,4,4,4,5,4,1,1,5,77,"Good Funded Startup Candidate","broker 5 manual ad deals between channels and advertisers","build channel inventory sheet, create media kit, secure first advertisers","trust, fraud, reporting uncertainty","no repeat advertisers or severe disputes","big upside, messy execution"],
      [39,"Escrow/Trusted Deal Layer for Informal Sellers","Funded Startup Idea","Both","buyers and sellers in informal commerce","trust is low in chat commerce","escrow-like payment and dispute system","manual trusted middleman MVP","regulated escrow/payment protection platform","Marketplace","Funded startup, Platform partner","High","3-5","Yes","Platform partnership likely required",5,5,5,5,5,5,5,"2-3 months","9-18 months","very high","very high","fee per transaction","0",20,200,"2B+",2,5,5,5,5,5,1,1,5,73,"Good Funded Startup Candidate","test trust demand with concierge middleman pilot on small transactions","interview buyers/sellers, map fraud cases, run tiny pilot","extreme legal/trust/compliance risk","disputes too costly, no legal safe path","huge pain, huge risk"],
      [40,"Informal Commerce Marketplace Built on Messaging Demand","Marketplace","Both","buyers, informal sellers","fragmented supply and no standardized shopping experience","marketplace aggregating sellers active in messaging apps","curated listings MVP","full commerce marketplace with reviews, logistics, payments","Marketplace","Small team, Funded startup","High","3-5","Yes","Platform partnership likely required",5,5,5,5,5,5,4,"2-3 months","9-18 months","very high","very high","take rate, ads, seller plans","0",30,300,"3B+",2,4,5,4,5,4,1,1,5,71,"Good Funded Startup Candidate","start with one curated product niche and manual order relay","choose niche, onboard 20 sellers, build listing site","trust, logistics, disputes, chicken-and-egg","weak liquidity or too many support issues","seductive idea, operational monster"],
      [41,"Channel/Group Benchmarking Intelligence Tool","Analytics Tool","Both","large creators, agencies, advertisers","no benchmark data on channel performance","compare communities by growth, engagement proxies, monetization indicators","manual benchmark report","analytics SaaS + intelligence subscriptions","Enterprise/B2B Tool","Technical solo founder, Small team, Funded startup","Medium","2-4","Helpful","Requires verification",4,3,3,2,4,2,4,"2-4 weeks","4-8 months","medium-high","medium","report sales, subscription","2M-20M",3,15,120,4,4,4,4,4,4,2,2,5,76,"Good Funded Startup Candidate","sell 3 custom benchmark reports before building tool","select 50 channels, define metrics, pitch agencies/brands","hard data may be inaccessible or noisy","no one pays for intelligence reports","strong if ad market matures"],
      [42,"Seller Credit Scoring / Trust Index","Analytics Tool","Both","buyers, marketplaces, lenders","hard to know if seller is trustworthy","reputation profile based on behavior, reviews, consistency","manual scorecard MVP","trust index API/embedded badge system","B2B2C","Small team, Funded startup, Platform partner","Medium-High","2-4","Likely","Platform partnership likely required",5,4,4,3,5,5,5,"1-2 months","6-12 months","high","medium-high","subscription, API, verification fee","0",10,100,800,3,4,4,4,5,5,1,1,5,70,"Good Funded Startup Candidate","test if buyers value trust badges with mock profiles","define trust criteria, create sample profiles, recruit 10 sellers","data validity and legal exposure","no measurable buyer trust lift","requires data credibility to work"],
      [43,"Local Creator CRM for Paid Communities","Creator Tool","Both","creators, coaches, educators","creator business ops fragmented across chat","CRM for leads, members, content schedule, renewals","Notion/sheet operator MVP","creator OS SaaS tailored to Iranian messaging platforms","SaaS","Technical solo founder, Small team","Medium","2-3","Helpful","Requires verification",4,3,3,3,4,2,3,"1 month","4-8 months","high","medium","subscription","1M-8M",3,15,100,4,5,4,4,5,4,2,3,5,80,"Good Funded Startup Candidate","onboard 3 creators with concierge CRM setup","map creator ops, create dashboard mockup, run pilot","creators may be too small to pay","no retention or low usage","solid if creator economy buyers exist"],
      [44,"Message Template Generator by Industry","Creator Tool","Both","sellers, service providers, tutors","need tailored replies but generic packs are weak","generator that outputs message banks by niche/tone","PDF pack by industry MVP","app/tool to generate scripts dynamically","SaaS","Zero-budget solo founder, Technical solo founder","Zero-Very Low","1","Not initially","Optional",2,1,2,1,2,1,1,"2-4 days","1-2 months","low","very low","one-time pack, subscription later","300k-1.5M",1,6,25,5,4,5,3,4,3,5,5,3,77,"Build First as Side Hustle","pre-sell 3 niche packs before making generator","pick 3 industries, create sample outputs, post offer","commoditized, AI alternatives","low paid conversion despite interest","cleaner version of vague “message tools”"],
      [45,"Channel Monetization Consultant for Creators","Agency Service","Both","creators/admins","don’t know how to monetize audience","consulting on offers, memberships, ads, funnels","one-off strategy call/report","full retained growth and monetization advisory","Agency/Service","Agency/operator, Small agency","Very Low","1","No","No",2,2,2,2,4,2,1,"2-5 days","1-2 months","medium","low","consulting fee, retainer","1M-10M",3,15,60,4,4,3,4,2,3,5,4,3,73,"Good Agency/Service Candidate","offer 5 free mini-monetization reviews","develop monetization checklist, publish case examples, outreach to creators","advisory hard to productize","low close rate if no proof","works better with niche expertise"],
      [46,"Seller Training Course for Messaging Commerce","Education Tool","Both","beginner sellers","no structured know-how for selling in chat ecosystems","course on channel setup, FAQ, trust, follow-up, order ops","webinar/live workshop","recorded academy + community + templates","Creator Economy","Zero-budget solo founder, Side-hustle founder","Very Low","1","No","No",2,2,2,2,3,1,1,"1 week","1-2 months","medium","low","course sales","500k-3M",1,8,30,4,4,4,3,4,3,4,4,3,72,"Build First as Side Hustle","run one live workshop and see paid attendance","outline curriculum, create promo post, invite 30 sellers","info-product saturation","no paid signups for workshop","best when bundled with templates/tools"],
      [47,"Community Manager Training & Certification","Education Tool","Both","aspiring admins, community operators","no standards for running groups/channels","training on moderation, onboarding, member ops, growth","workshop + handbook","certification ecosystem + hiring marketplace","B2B2C","Side-hustle founder, Small team","Low","1-2","Helpful","No",2,2,2,2,4,2,1,"1-2 weeks","3-6 months","medium","low","tuition, certification fee","0",5,30,120,4,3,3,3,4,3,3,3,4,68,"Test Cheaply","survey 50 admins for training interest","build syllabus, run pilot cohort, collect outcomes","weak credential value","poor student outcomes or low placement","more ecosystem play than direct painkiller"],
      [48,"Shared Admin Inbox for Small Teams","Customer Support Tool","Both","SMEs with multiple admins","multiple people reply inconsistently from shared accounts","shared inbox/process layer with assignment and notes","SOP + spreadsheet MVP","full shared inbox SaaS with roles","SaaS","Technical solo founder, Small team","Medium","2-3","Helpful","Requires verification",4,4,3,4,4,3,4,"1 month","4-8 months","high","medium-high","subscription","1M-8M",3,15,100,3,5,4,4,5,4,2,2,5,78,"Good Funded Startup Candidate","run one manual “shared inbox” pilot with 1 SME team","map support handoff issues, mock team inbox, recruit pilot","integration constraints severe","team doesn’t need enough coordination to pay","real B2B pain if message access is possible"],
      [49,"Lead Capture & Qualification Workflow for Service Businesses","Customer Support Tool","Both","clinics, consultants, real estate, tutors","leads come in but are unqualified and lost","structured intake, qualification, and follow-up process","form + qualification script + tracker","lead management SaaS with routing and reminders","Hybrid","Side-hustle founder, Technical solo founder, Small team","Very Low","1-2","Not initially","Optional",2,2,2,2,3,2,1,"2-4 days","2-4 months","low","low","setup + monthly","1M-5M",3,12,45,4,5,5,4,4,3,5,4,4,80,"Good Micro-SaaS Candidate","offer manual lead qualification setup to 5 service businesses","build intake form, write qualification script, outreach to local providers","clients may still respond ad hoc","no measurable reduction in lost leads","one of the strongest service-business plays"],
      [50,"Channel Revenue Leak Audit","Agency Service","Both","sellers, creators, paid groups","invisible operational leaks reduce revenue","audit missed renewals, ignored leads, weak follow-up, unclear offers","one-off leak report","recurring ops optimization retainer","Agency/Service","Agency/operator, Small agency","Very Low","1","No","No",2,2,2,2,3,2,1,"2-5 days","1-2 months","medium","low","audit fee, implementation fee","1M-8M",3,12,40,4,5,4,4,2,3,5,4,3,77,"Good Agency/Service Candidate","do 3 free leak audits showing missed money","create audit checklist, quantify 3 leak types, pitch channels","ROI may be hard to prove","no upgrade to paid fix after free audit","clearer positioning than generic consulting"],
      [51,"Local Payments + Membership Ops Layer","Funded Startup Idea","Both","creators, course sellers, communities","collecting payment and granting access are disconnected","payment confirmation + membership lifecycle infrastructure","manual ops + dashboard MVP","payments + membership software stack","Hybrid","Small team, Funded startup, Platform partner","High","3-5","Yes","Platform partnership likely required",5,5,4,4,5,5,5,"2-3 months","9-18 months","very high","high","subscription + transaction fee","0",30,250,"2B+",3,5,5,5,5,5,1,1,5,76,"Good Funded Startup Candidate","run manual payment-confirmation + membership pilot for 2 creators","map payment flow, recruit creators, define service-level promise","payment errors, compliance, platform dependency","no scalable/legal path emerges","one of the most valuable infra ideas if feasible"],
      [52,"Seller Reputation & Review Collection Tool","Seller Tool","Both","informal sellers","hard to prove credibility and collect testimonials","tool/process for collecting and displaying buyer feedback","manual review page + template","review widget/profile system across messaging commerce","Hybrid","Side-hustle founder, Technical solo founder, Small team","Very Low","1-2","Helpful","Optional",2,2,2,2,3,3,2,"3-5 days","2-4 months","low","low","setup, subscription","500k-3M",1,7,30,4,4,4,4,4,4,4,4,4,76,"Good Micro-SaaS Candidate","build 3 sample review pages and pitch sellers","design review format, collect 5 sample testimonials, outreach","fake reviews or low data trust","no seller sees conversion benefit","trust-building angle can materially help sales"],
      [53,"Messaging Commerce Training + Templates Subscription","Creator Tool","Both","sellers, admins, creators","need ongoing operational playbooks and copy assets","monthly subscription for templates, SOPs, scripts, mini-trainings","paid Telegram/Rubika/Baleh content channel MVP","recurring content membership with downloads","Creator Economy","Side-hustle founder, Agency/operator","Zero-Very Low","1","No","No",2,2,2,2,3,1,1,"1 week","1-2 months","medium","low","monthly subscription","200k-1M/mo",1,8,40,4,4,4,3,4,2,5,4,3,73,"Build First as Side Hustle","open waitlist for monthly toolkit membership","define monthly deliverables, publish sample pack, invite first 20 members","churn and content treadmill","fewer than 10 paid subscribers after launch","good recurring model if audience exists"],
      [54,"Rubika/Baleh Business Ops Agency","Agency Service","Both","SMEs using messaging as a primary channel","lack internal systems for chat-based sales/support","full-stack setup and ongoing optimization for messaging operations","one client done manually","niche agency with SOPs, dashboards, support and growth","Agency/Service","Agency/operator, Small agency","Low","2-5","Helpful","Optional",3,5,4,4,4,3,2,"2-4 weeks","3-6 months","high","high","setup + monthly retainer","5M-50M",10,40,200,3,5,5,4,3,4,2,2,4,75,"Good Agency/Service Candidate","land 1 client with clear scope package","define service packages, create case-study style demo, outreach to SMEs","scope creep, team dependency, ops heaviness","margins collapse from custom work","strong cash business, weak passivity"],
      [55,"Enterprise Messaging Compliance / Archiving Layer","Enterprise/B2B Tool","More likely Baleh","regulated SMEs, finance, education, healthcare-adjacent teams","lack of controlled recordkeeping in chat workflows","archive, SOP, governance layer for organizational messaging use","advisory + manual policy pack","enterprise compliance software + audit trail","Enterprise/B2B Tool","Small team, Funded startup","Medium-High","2-4","Likely","Requires verification",5,4,4,3,5,4,4,"1-2 months","6-12 months","high","medium","licensing + services","0",20,150,"1B+",4,4,4,4,4,5,1,1,5,74,"Good Funded Startup Candidate","interview 10 organizations using Baleh internally","define governance checklist, build advisory offer, test enterprise interest","enterprise sales long and uncertain","no buyer urgency or blocked integrations","more relevant if Baleh has institutional adoption"],
      [56,"Messaging Commerce ERP-lite for Small Sellers","SaaS","Both","growing small sellers","juggling orders, stock, support, promos manually","lightweight all-in-one seller workspace built around messaging commerce","sheet-based “ERP-lite” MVP","SaaS with inventory, CRM, templates, reminders, analytics","SaaS","Technical solo founder, Small team","Medium","2-4","Likely","Requires verification",4,4,3,3,4,2,3,"1-2 months","6-12 months","high","medium","subscription","1M-8M",3,20,120,4,5,5,4,5,4,2,2,5,81,"Good Funded Startup Candidate","run one operator-managed workspace for 3 sellers","combine CRM+inventory+campaign sheet, recruit pilots, track retention","broad scope, risk of bloated product","pilots only want narrow feature","promising if narrowed to a niche first"]
    ];

    const state = {
      rows: [...data],
      filtered: [...data],
      sortIndex: null,
      sortDir: "asc",
      theme: localStorage.getItem("theme") || "dark"
    };

    const els = {
      headerRow: document.getElementById("headerRow"),
      tableBody: document.getElementById("tableBody"),
      searchInput: document.getElementById("searchInput"),
      categoryFilter: document.getElementById("categoryFilter"),
      platformFilter: document.getElementById("platformFilter"),
      businessTypeFilter: document.getElementById("businessTypeFilter"),
      verdictFilter: document.getElementById("verdictFilter"),
      resetFilters: document.getElementById("resetFilters"),
      exportCsv: document.getElementById("exportCsv"),
      themeToggle: document.getElementById("themeToggle"),
      visibleCount: document.getElementById("visibleCount"),
      avgScore: document.getElementById("avgScore"),
      topCategory: document.getElementById("topCategory"),
      topVerdict: document.getElementById("topVerdict"),
      topPlatform: document.getElementById("topPlatform")
    };

    function init() {
      if (state.theme === "light") document.body.classList.add("light");

      injectIntro();
      renderHeaders();
      populateFilters();
      bindEvents();
      applyFilters();
    }

    function injectIntro() {
      const intro = document.createElement("div");
      intro.className = "intro-screen";
      intro.innerHTML = `
        <div class="intro-card">
          <div class="orb"></div>
          <div class="intro-kicker">Opportunity Intelligence Dashboard</div>
          <h2>56 Rubika/Baleh Business Ideas</h2>
          <p>Search, score, filter, compare, and export startup/service opportunities.</p>
          <button id="enterDashboard">Enter Dashboard</button>
        </div>
      `;

      const style = document.createElement("style");
      style.textContent = `
        .intro-screen {
          position: fixed;
          inset: 0;
          z-index: 9999;
          display: grid;
          place-items: center;
          background:
            radial-gradient(circle at 20% 20%, rgba(110,168,254,.25), transparent 35%),
            radial-gradient(circle at 80% 40%, rgba(126,231,135,.18), transparent 35%),
            var(--bg);
          transition: opacity .5s ease, transform .5s ease;
        }

        .intro-screen.hidden {
          opacity: 0;
          transform: scale(1.03);
          pointer-events: none;
        }

        .intro-card {
          width: min(720px, calc(100% - 32px));
          padding: 42px;
          border-radius: 30px;
          background: linear-gradient(145deg, rgba(255,255,255,.09), rgba(255,255,255,.025));
          border: 1px solid var(--border);
          box-shadow: 0 30px 100px rgba(0,0,0,.35);
          text-align: center;
          animation: introUp .7s ease both;
          position: relative;
          overflow: hidden;
        }

        .intro-card::before {
          content: "";
          position: absolute;
          inset: -2px;
          background: linear-gradient(90deg, transparent, rgba(110,168,254,.25), transparent);
          transform: translateX(-100%);
          animation: shine 2.5s ease infinite;
        }

        .orb {
          width: 90px;
          height: 90px;
          margin: 0 auto 22px;
          border-radius: 999px;
          background:
            radial-gradient(circle at 30% 30%, #fff, transparent 22%),
            linear-gradient(135deg, var(--accent), var(--accent-2));
          box-shadow: 0 0 60px rgba(110,168,254,.5);
          animation: floatOrb 3s ease-in-out infinite;
        }

        .intro-kicker {
          color: var(--accent-2);
          font-size: 13px;
          font-weight: 700;
          letter-spacing: .14em;
          text-transform: uppercase;
          margin-bottom: 12px;
        }

        .intro-card h2 {
          margin: 0 0 12px;
          font-size: clamp(32px, 6vw, 62px);
          line-height: 1;
        }

        .intro-card p {
          color: var(--muted);
          max-width: 520px;
          margin: 0 auto 26px;
          font-size: 16px;
        }

        #enterDashboard {
          padding: 14px 22px;
          border-radius: 999px;
          background: linear-gradient(135deg, var(--accent), var(--accent-2));
          color: #06111f;
          border: 0;
          font-weight: 800;
        }

        .container {
          animation: dashboardIn .7s ease both;
        }

        .stat, .toolbar > *, .table-wrap {
          animation: fadeUp .55s ease both;
        }

        .stat:nth-child(1) { animation-delay: .05s; }
        .stat:nth-child(2) { animation-delay: .1s; }
        .stat:nth-child(3) { animation-delay: .15s; }
        .stat:nth-child(4) { animation-delay: .2s; }
        .stat:nth-child(5) { animation-delay: .25s; }

        tbody tr {
          animation: rowIn .25s ease both;
        }

        @keyframes introUp {
          from { opacity: 0; transform: translateY(24px) scale(.98); }
          to { opacity: 1; transform: translateY(0) scale(1); }
        }

        @keyframes dashboardIn {
          from { opacity: 0; transform: translateY(14px); }
          to { opacity: 1; transform: translateY(0); }
        }

        @keyframes fadeUp {
          from { opacity: 0; transform: translateY(12px); }
          to { opacity: 1; transform: translateY(0); }
        }

        @keyframes rowIn {
          from { opacity: 0; transform: translateY(4px); }
          to { opacity: 1; transform: translateY(0); }
        }

        @keyframes floatOrb {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-10px); }
        }

        @keyframes shine {
          0% { transform: translateX(-100%); }
          55%, 100% { transform: translateX(100%); }
        }

        .quality-badge {
          display: inline-flex;
          align-items: center;
          gap: 6px;
          padding: 5px 9px;
          border-radius: 999px;
          font-size: 12px;
          border: 1px solid var(--border);
        }

        .quality-badge.strong {
          color: var(--accent-2);
          background: rgba(126,231,135,.1);
        }

        .quality-badge.good {
          color: var(--accent);
          background: rgba(110,168,254,.1);
        }

        .quality-badge.test {
          color: var(--warn);
          background: rgba(255,209,102,.1);
        }

        .quality-badge.risky {
          color: var(--danger);
          background: rgba(255,107,107,.1);
        }
      `;

      document.head.appendChild(style);
      document.body.appendChild(intro);

      const closeIntro = () => {
        intro.classList.add("hidden");
        setTimeout(() => intro.remove(), 550);
      };

      document.getElementById("enterDashboard").addEventListener("click", closeIntro);
      setTimeout(closeIntro, 1800);
    }

    function renderHeaders() {
      els.headerRow.innerHTML = "";

      columns.forEach((col, index) => {
        const th = document.createElement("th");
        th.textContent = col;
        th.title = "Click to sort";
        th.addEventListener("click", () => sortBy(index));
        els.headerRow.appendChild(th);
      });
    }

    function populateFilters() {
      fillSelect(els.categoryFilter, uniqueValues(2));
      fillSelect(els.platformFilter, uniqueValues(3));
      fillSelect(els.businessTypeFilter, uniqueValues(9));
      fillSelect(els.verdictFilter, uniqueValues(41));
    }

    function uniqueValues(index) {
      return [...new Set(data.map(row => row[index]).filter(Boolean))]
        .sort((a, b) => String(a).localeCompare(String(b)));
    }

    function fillSelect(select, values) {
      values.forEach(value => {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = value;
        select.appendChild(option);
      });
    }

    function bindEvents() {
      els.searchInput.addEventListener("input", applyFilters);
      els.categoryFilter.addEventListener("change", applyFilters);
      els.platformFilter.addEventListener("change", applyFilters);
      els.businessTypeFilter.addEventListener("change", applyFilters);
      els.verdictFilter.addEventListener("change", applyFilters);

      els.resetFilters.addEventListener("click", () => {
        els.searchInput.value = "";
        els.categoryFilter.value = "";
        els.platformFilter.value = "";
        els.businessTypeFilter.value = "";
        els.verdictFilter.value = "";
        state.sortIndex = null;
        state.sortDir = "asc";
        applyFilters();
      });

      els.exportCsv.addEventListener("click", exportCsv);

      els.themeToggle.addEventListener("click", () => {
        document.body.classList.toggle("light");
        state.theme = document.body.classList.contains("light") ? "light" : "dark";
        localStorage.setItem("theme", state.theme);
      });
    }

    function applyFilters() {
      const q = els.searchInput.value.trim().toLowerCase();
      const category = els.categoryFilter.value;
      const platform = els.platformFilter.value;
      const businessType = els.businessTypeFilter.value;
      const verdict = els.verdictFilter.value;

      state.filtered = data.filter(row => {
        const matchesSearch = !q || row.some(cell =>
          String(cell ?? "").toLowerCase().includes(q)
        );

        return (
          matchesSearch &&
          (!category || row[2] === category) &&
          (!platform || row[3] === platform) &&
          (!businessType || row[9] === businessType) &&
          (!verdict || row[41] === verdict)
        );
      });

      if (state.sortIndex !== null) {
        sortRowsOnly();
      }

      renderTable();
      updateStats();
    }

    function sortBy(index) {
      if (state.sortIndex === index) {
        state.sortDir = state.sortDir === "asc" ? "desc" : "asc";
      } else {
        state.sortIndex = index;
        state.sortDir = "asc";
      }

      sortRowsOnly();
      renderTable();
    }

    function sortRowsOnly() {
      const index = state.sortIndex;
      const dir = state.sortDir === "asc" ? 1 : -1;

      state.filtered.sort((a, b) => {
        const av = a[index];
        const bv = b[index];

        const an = Number(av);
        const bn = Number(bv);

        if (!Number.isNaN(an) && !Number.isNaN(bn)) {
          return (an - bn) * dir;
        }

        return String(av ?? "").localeCompare(String(bv ?? "")) * dir;
      });
    }

    function renderTable() {
      els.tableBody.innerHTML = "";

      if (!state.filtered.length) {
        const tr = document.createElement("tr");
        const td = document.createElement("td");
        td.colSpan = columns.length;
        td.style.textAlign = "center";
        td.style.padding = "40px";
        td.innerHTML = `
          <strong>No ideas found.</strong>
          <div class="small">Try clearing filters or changing the search query.</div>
        `;
        tr.appendChild(td);
        els.tableBody.appendChild(tr);
        return;
      }

      const frag = document.createDocumentFragment();

      state.filtered.forEach((row, rowIndex) => {
        const tr = document.createElement("tr");
        tr.style.animationDelay = `${Math.min(rowIndex * 0.015, 0.35)}s`;

        row.forEach((cell, index) => {
          const td = document.createElement("td");

          if (index === 40) {
            const score = Number(cell);
            const cls = score >= 78 ? "high" : score >= 70 ? "mid" : "low";
            td.innerHTML = `<span class="score ${cls}">${escapeHtml(cell)}</span>`;
          } else if (index === 41) {
            td.innerHTML = renderVerdict(cell);
          } else if ([2, 3, 9, 11, 13, 14].includes(index)) {
            td.innerHTML = `<span class="tag">${escapeHtml(cell)}</span>`;
          } else if ([5, 6, 7, 8, 42, 43, 44, 45, 46].includes(index)) {
            td.innerHTML = `<div style="max-width:340px">${escapeHtml(cell)}</div>`;
          } else {
            td.textContent = cell;
          }

          tr.appendChild(td);
        });

        frag.appendChild(tr);
      });

      els.tableBody.appendChild(frag);
    }

    function renderVerdict(value) {
      const v = String(value || "");
      const lower = v.toLowerCase();

      let cls = "test";

      if (
        lower.includes("strong") ||
        lower.includes("build first") ||
        lower.includes("good micro") ||
        lower.includes("good funded")
      ) {
        cls = "strong";
      } else if (
        lower.includes("good") ||
        lower.includes("candidate")
      ) {
        cls = "good";
      } else if (
        lower.includes("operational") ||
        lower.includes("needs platform") ||
        lower.includes("risky")
      ) {
        cls = "risky";
      }

      return `<span class="quality-badge ${cls}">${escapeHtml(v)}</span>`;
    }

    function updateStats() {
      const rows = state.filtered;
      const count = rows.length;

      els.visibleCount.textContent = count;

      const scores = rows
        .map(row => Number(row[40]))
        .filter(num => !Number.isNaN(num));

      const avg = scores.length
        ? scores.reduce((a, b) => a + b, 0) / scores.length
        : 0;

      els.avgScore.textContent = avg ? avg.toFixed(1) : "0";

      els.topCategory.textContent = mostCommon(rows, 2);
      els.topVerdict.textContent = shortText(mostCommon(rows, 41), 22);
      els.topPlatform.textContent = mostCommon(rows, 3);
    }

    function mostCommon(rows, index) {
      if (!rows.length) return "—";

      const map = new Map();

      rows.forEach(row => {
        const key = row[index] || "—";
        map.set(key, (map.get(key) || 0) + 1);
      });

      return [...map.entries()].sort((a, b) => b[1] - a[1])[0][0];
    }

    function shortText(text, limit = 18) {
      text = String(text || "—");
      return text.length > limit ? text.slice(0, limit) + "…" : text;
    }

    function exportCsv() {
      const rows = [columns, ...state.filtered];

      const csv = rows.map(row =>
        row.map(cell => {
          const value = String(cell ?? "").replaceAll('"', '""');
          return `"${value}"`;
        }).join(",")
      ).join("\n");

      const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
      const url = URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = "rubika-baleh-opportunity-table.csv";
      document.body.appendChild(a);
      a.click();
      a.remove();

      URL.revokeObjectURL(url);
    }

    function escapeHtml(value) {
      return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
    }

    init();
  </script>
</body>
</html>
