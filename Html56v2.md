---
fable_schema: "5.1.0"
urn: "urn:tgn:blueprint:dashboard_app:761f20c6-84e9-4da6-8dc4-f2e7faf3b4f4"
title: "Domestic Opportunity Matrix Interactive Dashboard v2"
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
    - "tailwindcss>=3.0.0"
    - "vanilla-js"
  internal_urns:
    - "urn:tgn:blueprint:dashboard_app:b2b528ef-91ce-4de5-98df-ba8346e7b7d3"
    - "urn:tgn:blueprint:market_inventory:2dccf812-2d1b-425a-80b6-0504ec1e1009"
breaking_changes_detected: []
verification_checksum: "72838d47b97387b71d73e99e154a53c6165bd5789fbdf835f529397552aa41dc"
---
حتماً. این یک فایل `index.html` کامل، مستقل، بدون وابستگی خارجی، responsive، RTL، production-ready و شامل این قابلیت‌هاست:

- Intro/Hero متحرک
- کارت‌های داشبورد
- Top Opportunities
- Heatmap امتیازات
- تغییر نما بین جدول و کارت
- فیلتر، جستجو، مرتب‌سازی
- رنگ‌بندی دسته‌بندی‌ها
- Modal جزئیات ایده
- Dark/Light Theme
- Export CSV
- UI موبایل بهتر
- تعاملات نرم و بدون کتابخانه خارجی

> فقط فایل را با نام `index.html` ذخیره کن و مستقیم در مرورگر باز کن.

```html
<!doctype html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>داشبورد ارزیابی ایده‌ها</title>
  <meta name="description" content="داشبورد مستقل برای تحلیل، رتبه‌بندی و بررسی فرصت‌های ایده‌ها" />

  <style>
    :root {
      --bg: #f6f8fc;
      --surface: rgba(255, 255, 255, 0.82);
      --surface-solid: #ffffff;
      --text: #172033;
      --muted: #667085;
      --border: rgba(20, 30, 55, 0.1);
      --primary: #2563eb;
      --primary-2: #7c3aed;
      --good: #16a34a;
      --warn: #f59e0b;
      --bad: #ef4444;
      --shadow: 0 20px 50px rgba(15, 23, 42, 0.08);
      --shadow-soft: 0 10px 30px rgba(15, 23, 42, 0.06);
      --radius-lg: 24px;
      --radius-md: 18px;
      --radius-sm: 12px;
      --blur: blur(18px);
      --transition: 220ms ease;
    }

    [data-theme="dark"] {
      --bg: #070b14;
      --surface: rgba(17, 24, 39, 0.78);
      --surface-solid: #111827;
      --text: #f8fafc;
      --muted: #9ca3af;
      --border: rgba(255, 255, 255, 0.1);
      --primary: #60a5fa;
      --primary-2: #a78bfa;
      --shadow: 0 20px 50px rgba(0, 0, 0, 0.35);
      --shadow-soft: 0 10px 30px rgba(0, 0, 0, 0.24);
    }

    * {
      box-sizing: border-box;
    }

    html {
      scroll-behavior: smooth;
    }

    body {
      margin: 0;
      font-family:
        Vazirmatn,
        IRANSans,
        system-ui,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
      background:
        radial-gradient(circle at top right, rgba(37, 99, 235, 0.18), transparent 32rem),
        radial-gradient(circle at top left, rgba(124, 58, 237, 0.16), transparent 30rem),
        var(--bg);
      color: var(--text);
      min-height: 100vh;
      overflow-x: hidden;
    }

    button,
    input,
    select {
      font: inherit;
    }

    button {
      cursor: pointer;
    }

    .app {
      width: min(1440px, calc(100% - 32px));
      margin: 0 auto;
      padding: 24px 0 56px;
    }

    .hero {
      position: relative;
      overflow: hidden;
      min-height: 420px;
      border: 1px solid var(--border);
      border-radius: 32px;
      background:
        linear-gradient(135deg, rgba(37, 99, 235, 0.14), rgba(124, 58, 237, 0.1)),
        var(--surface);
      backdrop-filter: var(--blur);
      box-shadow: var(--shadow);
      padding: 36px;
      display: grid;
      grid-template-columns: 1.1fr 0.9fr;
      gap: 28px;
      align-items: center;
    }

    .hero::before,
    .hero::after {
      content: "";
      position: absolute;
      border-radius: 999px;
      filter: blur(8px);
      opacity: 0.75;
      animation: float 9s ease-in-out infinite;
      pointer-events: none;
    }

    .hero::before {
      width: 260px;
      height: 260px;
      background: rgba(37, 99, 235, 0.24);
      left: -70px;
      top: -70px;
    }

    .hero::after {
      width: 320px;
      height: 320px;
      background: rgba(124, 58, 237, 0.2);
      right: -90px;
      bottom: -120px;
      animation-delay: -3s;
    }

    @keyframes float {
      0%, 100% {
        transform: translate3d(0, 0, 0) scale(1);
      }
      50% {
        transform: translate3d(18px, -20px, 0) scale(1.06);
      }
    }

    .hero-content,
    .hero-visual {
      position: relative;
      z-index: 1;
    }

    .eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      border-radius: 999px;
      color: var(--primary);
      border: 1px solid rgba(37, 99, 235, 0.22);
      background: rgba(37, 99, 235, 0.08);
      font-size: 13px;
      font-weight: 700;
      margin-bottom: 18px;
    }

    .pulse-dot {
      width: 8px;
      height: 8px;
      border-radius: 999px;
      background: var(--good);
      box-shadow: 0 0 0 0 rgba(22, 163, 74, 0.5);
      animation: pulse 1.6s infinite;
    }

    @keyframes pulse {
      70% {
        box-shadow: 0 0 0 12px rgba(22, 163, 74, 0);
      }
      100% {
        box-shadow: 0 0 0 0 rgba(22, 163, 74, 0);
      }
    }

    h1 {
      margin: 0;
      font-size: clamp(32px, 5vw, 62px);
      line-height: 1.1;
      letter-spacing: -1.2px;
    }

    .gradient-text {
      background: linear-gradient(135deg, var(--primary), var(--primary-2));
      -webkit-background-clip: text;
      background-clip: text;
      color: transparent;
    }

    .hero p {
      color: var(--muted);
      line-height: 1.9;
      max-width: 720px;
      margin: 18px 0 0;
      font-size: 16px;
    }

    .hero-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 26px;
    }

    .btn {
      border: 0;
      border-radius: 14px;
      padding: 12px 16px;
      font-weight: 800;
      transition:
        transform var(--transition),
        box-shadow var(--transition),
        background var(--transition),
        border-color var(--transition);
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      min-height: 44px;
      color: var(--text);
      background: var(--surface-solid);
      border: 1px solid var(--border);
    }

    .btn:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-soft);
    }

    .btn-primary {
      color: #fff;
      background: linear-gradient(135deg, #2563eb, #7c3aed);
      border-color: transparent;
    }

    [data-theme="dark"] .btn-primary {
      color: #fff;
    }

    .btn-ghost {
      background: rgba(255, 255, 255, 0.52);
    }

    [data-theme="dark"] .btn-ghost {
      background: rgba(17, 24, 39, 0.6);
    }

    .hero-visual {
      min-height: 300px;
      display: grid;
      place-items: center;
    }

    .orbital {
      position: relative;
      width: min(360px, 82vw);
      aspect-ratio: 1;
      border-radius: 50%;
      background:
        radial-gradient(circle, rgba(255,255,255,0.35), transparent 45%),
        conic-gradient(from 180deg, rgba(37,99,235,0.1), rgba(124,58,237,0.35), rgba(22,163,74,0.25), rgba(37,99,235,0.1));
      border: 1px solid var(--border);
      box-shadow: inset 0 0 60px rgba(255, 255, 255, 0.16), var(--shadow);
      animation: rotateSlow 18s linear infinite;
    }

    @keyframes rotateSlow {
      to {
        transform: rotate(360deg);
      }
    }

    .orbital-card {
      position: absolute;
      width: 150px;
      padding: 14px;
      border-radius: 18px;
      background: var(--surface);
      border: 1px solid var(--border);
      backdrop-filter: var(--blur);
      box-shadow: var(--shadow-soft);
      animation: counterRotate 18s linear infinite;
    }

    @keyframes counterRotate {
      to {
        transform: rotate(-360deg);
      }
    }

    .orbital-card strong {
      display: block;
      font-size: 24px;
      margin-bottom: 4px;
    }

    .orbital-card span {
      color: var(--muted);
      font-size: 12px;
    }

    .oc-1 {
      top: 6%;
      right: -24px;
    }

    .oc-2 {
      bottom: 8%;
      left: -18px;
    }

    .oc-3 {
      top: 48%;
      right: 35%;
      transform-origin: center;
    }

    .section {
      margin-top: 26px;
    }

    .section-title {
      display: flex;
      justify-content: space-between;
      align-items: end;
      gap: 16px;
      margin-bottom: 14px;
    }

    .section-title h2 {
      margin: 0;
      font-size: 22px;
    }

    .section-title p {
      margin: 6px 0 0;
      color: var(--muted);
      font-size: 14px;
    }

    .stats-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px;
    }

    .stat-card,
    .panel,
    .idea-card {
      border: 1px solid var(--border);
      background: var(--surface);
      backdrop-filter: var(--blur);
      box-shadow: var(--shadow-soft);
      border-radius: var(--radius-lg);
    }

    .stat-card {
      padding: 18px;
      position: relative;
      overflow: hidden;
    }

    .stat-card::after {
      content: "";
      position: absolute;
      inset-inline-start: -24px;
      bottom: -32px;
      width: 120px;
      height: 120px;
      border-radius: 50%;
      background: var(--accent, rgba(37,99,235,0.18));
    }

    .stat-label {
      color: var(--muted);
      font-size: 13px;
      font-weight: 700;
    }

    .stat-value {
      font-size: 32px;
      font-weight: 900;
      margin-top: 8px;
      letter-spacing: -0.5px;
    }

    .stat-note {
      margin-top: 8px;
      color: var(--muted);
      font-size: 13px;
    }

    .toolbar {
      display: grid;
      grid-template-columns: 1.4fr repeat(3, minmax(150px, 0.5fr)) auto;
      gap: 10px;
      padding: 14px;
      border-radius: var(--radius-lg);
      background: var(--surface);
      border: 1px solid var(--border);
      backdrop-filter: var(--blur);
      box-shadow: var(--shadow-soft);
    }

    .field {
      width: 100%;
      border: 1px solid var(--border);
      background: var(--surface-solid);
      color: var(--text);
      border-radius: 14px;
      min-height: 44px;
      padding: 0 12px;
      outline: none;
      transition: border-color var(--transition), box-shadow var(--transition);
    }

    .field:focus {
      border-color: rgba(37, 99, 235, 0.55);
      box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.12);
    }

    .view-toggle {
      display: flex;
      gap: 6px;
      padding: 4px;
      border: 1px solid var(--border);
      background: var(--surface-solid);
      border-radius: 14px;
    }

    .toggle-btn {
      border: 0;
      background: transparent;
      color: var(--muted);
      padding: 8px 12px;
      border-radius: 10px;
      font-weight: 900;
    }

    .toggle-btn.active {
      background: linear-gradient(135deg, rgba(37,99,235,0.16), rgba(124,58,237,0.14));
      color: var(--primary);
    }

    .layout {
      display: grid;
      grid-template-columns: 1.45fr 0.55fr;
      gap: 16px;
      align-items: start;
    }

    .panel {
      padding: 16px;
    }

    .top-list {
      display: grid;
      gap: 10px;
    }

    .top-item {
      display: grid;
      grid-template-columns: auto 1fr auto;
      gap: 10px;
      align-items: center;
      padding: 12px;
      border: 1px solid var(--border);
      background: var(--surface-solid);
      border-radius: 16px;
      transition: transform var(--transition), border-color var(--transition);
    }

    .top-item:hover {
      transform: translateY(-2px);
      border-color: rgba(37, 99, 235, 0.35);
    }

    .rank {
      width: 34px;
      height: 34px;
      border-radius: 12px;
      display: grid;
      place-items: center;
      font-weight: 900;
      color: #fff;
      background: linear-gradient(135deg, #2563eb, #7c3aed);
    }

    .top-title {
      font-weight: 900;
      margin-bottom: 3px;
    }

    .top-meta {
      color: var(--muted);
      font-size: 12px;
    }

    .score-badge {
      min-width: 54px;
      text-align: center;
      border-radius: 999px;
      padding: 7px 10px;
      font-weight: 900;
      color: #fff;
      background: var(--good);
    }

    .heatmap {
      display: grid;
      grid-template-columns: repeat(10, 1fr);
      gap: 8px;
    }

    .heat-cell {
      aspect-ratio: 1;
      border: 0;
      color: #fff;
      border-radius: 10px;
      font-size: 12px;
      font-weight: 900;
      display: grid;
      place-items: center;
      transition: transform var(--transition), box-shadow var(--transition);
    }

    .heat-cell:hover {
      transform: scale(1.08);
      box-shadow: var(--shadow-soft);
    }

    .cards-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 14px;
    }

    .idea-card {
      padding: 16px;
      transition:
        transform var(--transition),
        box-shadow var(--transition),
        border-color var(--transition);
      position: relative;
      overflow: hidden;
    }

    .idea-card:hover {
      transform: translateY(-4px);
      border-color: rgba(37, 99, 235, 0.35);
      box-shadow: var(--shadow);
    }

    .idea-card::before {
      content: "";
      position: absolute;
      inset: 0;
      height: 4px;
      background: var(--cat-color, var(--primary));
    }

    .idea-head {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: start;
      margin-top: 4px;
    }

    .idea-title {
      margin: 0;
      font-size: 16px;
      line-height: 1.55;
    }

    .category {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      margin-top: 10px;
      border-radius: 999px;
      padding: 6px 10px;
      font-size: 12px;
      font-weight: 900;
      color: var(--cat-color);
      background: color-mix(in srgb, var(--cat-color) 13%, transparent);
      border: 1px solid color-mix(in srgb, var(--cat-color) 28%, transparent);
    }

    .dot {
      width: 8px;
      height: 8px;
      background: var(--cat-color);
      border-radius: 999px;
    }

    .desc {
      color: var(--muted);
      margin: 12px 0 14px;
      line-height: 1.8;
      font-size: 13px;
      min-height: 48px;
    }

    .metrics {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
      margin-bottom: 14px;
    }

    .metric {
      background: var(--surface-solid);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 10px;
      text-align: center;
    }

    .metric strong {
      display: block;
      font-size: 18px;
    }

    .metric span {
      color: var(--muted);
      font-size: 11px;
      font-weight: 700;
    }

    .progress {
      width: 100%;
      height: 9px;
      background: rgba(148, 163, 184, 0.18);
      border-radius: 999px;
      overflow: hidden;
      margin: 10px 0 12px;
    }

    .progress > i {
      display: block;
      height: 100%;
      width: var(--w);
      background: linear-gradient(90deg, var(--cat-color), var(--primary-2));
      border-radius: inherit;
    }

    .card-actions {
      display: flex;
      justify-content: space-between;
      gap: 8px;
      align-items: center;
    }

    .small-btn {
      border: 1px solid var(--border);
      background: var(--surface-solid);
      color: var(--text);
      border-radius: 12px;
      padding: 9px 12px;
      font-weight: 900;
      transition: transform var(--transition), background var(--transition);
    }

    .small-btn:hover {
      transform: translateY(-2px);
      background: rgba(37, 99, 235, 0.08);
    }

    .table-wrap {
      overflow: auto;
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      background: var(--surface);
      box-shadow: var(--shadow-soft);
      backdrop-filter: var(--blur);
    }

    table {
      width: 100%;
      border-collapse: collapse;
      min-width: 920px;
    }

    th,
    td {
      padding: 14px;
      text-align: right;
      border-bottom: 1px solid var(--border);
      vertical-align: middle;
    }

    th {
      color: var(--muted);
      font-size: 12px;
      background: rgba(148, 163, 184, 0.08);
      position: sticky;
      top: 0;
      z-index: 1;
    }

    tr {
      transition: background var(--transition);
    }

    tr:hover td {
      background: rgba(37, 99, 235, 0.05);
    }

    .table-title {
      font-weight: 900;
    }

    .empty {
      padding: 34px;
      text-align: center;
      color: var(--muted);
      border: 1px dashed var(--border);
      border-radius: var(--radius-lg);
      background: var(--surface);
    }

    .modal-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(2, 6, 23, 0.62);
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
      z-index: 100;
    }

    .modal-backdrop.open {
      display: flex;
      animation: fadeIn 160ms ease;
    }

    @keyframes fadeIn {
      from {
        opacity: 0;
      }
    }

    .modal {
      width: min(820px, 100%);
      max-height: min(760px, calc(100vh - 40px));
      overflow: auto;
      border-radius: 28px;
      background: var(--surface-solid);
      color: var(--text);
      border: 1px solid var(--border);
      box-shadow: 0 35px 80px rgba(0, 0, 0, 0.32);
      animation: modalIn 220ms ease;
    }

    @keyframes modalIn {
      from {
        transform: translateY(14px) scale(0.98);
        opacity: 0;
      }
    }

    .modal-header {
      padding: 22px;
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: start;
      position: sticky;
      top: 0;
      background: var(--surface-solid);
      z-index: 2;
    }

    .modal-header h3 {
      margin: 0;
      font-size: 22px;
      line-height: 1.5;
    }

    .close-btn {
      width: 42px;
      height: 42px;
      border-radius: 14px;
      border: 1px solid var(--border);
      background: var(--surface);
      color: var(--text);
      font-size: 24px;
      line-height: 1;
    }

    .modal-body {
      padding: 22px;
    }

    .detail-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      margin: 16px 0;
    }

    .detail-box {
      padding: 14px;
      border: 1px solid var(--border);
      border-radius: 16px;
      background: var(--surface);
      text-align: center;
    }

    .detail-box strong {
      display: block;
      font-size: 24px;
    }

    .detail-box span {
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
    }

    .detail-section {
      margin-top: 18px;
    }

    .detail-section h4 {
      margin: 0 0 8px;
    }

    .detail-section p,
    .detail-section li {
      color: var(--muted);
      line-height: 1.9;
    }

    .chips {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 10px;
    }

    .chip {
      border: 1px solid var(--border);
      border-radius: 999px;
      padding: 7px 10px;
      background: var(--surface);
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
    }

    .toast {
      position: fixed;
      left: 20px;
      bottom: 20px;
      background: #111827;
      color: #fff;
      padding: 12px 16px;
      border-radius: 14px;
      box-shadow: var(--shadow);
      transform: translateY(20px);
      opacity: 0;
      pointer-events: none;
      transition: 200ms ease;
      z-index: 200;
      font-weight: 800;
    }

    .toast.show {
      opacity: 1;
      transform: translateY(0);
    }

    .hidden {
      display: none !important;
    }

    @media (max-width: 1100px) {
      .hero,
      .layout {
        grid-template-columns: 1fr;
      }

      .stats-grid {
        grid-template-columns: repeat(2, 1fr);
      }

      .cards-grid {
        grid-template-columns: repeat(2, 1fr);
      }

      .toolbar {
        grid-template-columns: 1fr 1fr;
      }

      .toolbar .view-toggle {
        grid-column: span 2;
      }
    }

    @media (max-width: 720px) {
      .app {
        width: min(100% - 20px, 1440px);
        padding-top: 10px;
      }

      .hero {
        padding: 22px;
        border-radius: 24px;
        min-height: auto;
      }

      .hero-visual {
        min-height: 230px;
      }

      .orbital {
        width: min(250px, 78vw);
      }

      .orbital-card {
        width: 124px;
        padding: 11px;
      }

      .oc-1 {
        right: -8px;
      }

      .oc-2 {
        left: -10px;
      }

      .stats-grid,
      .cards-grid,
      .toolbar,
      .detail-grid {
        grid-template-columns: 1fr;
      }

      .toolbar .view-toggle {
        grid-column: auto;
      }

      .section-title {
        align-items: start;
        flex-direction: column;
      }

      .heatmap {
        grid-template-columns: repeat(6, 1fr);
      }

      .modal-header,
      .modal-body {
        padding: 16px;
      }

      .btn,
      .field {
        width: 100%;
      }

      .hero-actions {
        flex-direction: column;
      }

      .card-actions {
        flex-direction: column;
        align-items: stretch;
      }
    }

    @media (prefers-reduced-motion: reduce) {
      *,
      *::before,
      *::after {
        animation: none !important;
        scroll-behavior: auto !important;
        transition: none !important;
      }
    }
  </style>
</head>

<body>
  <main class="app">
    <section class="hero">
      <div class="hero-content">
        <div class="eyebrow">
          <span class="pulse-dot"></span>
          داشبورد زنده تحلیل ایده‌ها
        </div>

        <h1>
          ارزیابی، رتبه‌بندی و کشف
          <span class="gradient-text">فرصت‌های برتر</span>
        </h1>

        <p>
          این داشبورد برای بررسی سریع ایده‌ها، مقایسه امتیازها، مشاهده نقشه حرارتی،
          تحلیل فرصت‌های برتر و باز کردن جزئیات هر ایده طراحی شده است.
          همه‌چیز داخل همین فایل HTML قرار دارد و نیازی به اینترنت یا کتابخانه خارجی ندارد.
        </p>

        <div class="hero-actions">
          <button class="btn btn-primary" id="scrollToDashboard">شروع تحلیل</button>
          <button class="btn btn-ghost" id="themeToggle">تغییر تم</button>
          <button class="btn btn-ghost" id="exportCsv">خروجی CSV</button>
        </div>
      </div>

      <div class="hero-visual" aria-hidden="true">
        <div class="orbital">
          <div class="orbital-card oc-1">
            <strong id="heroTotal">0</strong>
            <span>ایده ثبت‌شده</span>
          </div>
          <div class="orbital-card oc-2">
            <strong id="heroBest">0</strong>
            <span>بهترین امتیاز</span>
          </div>
          <div class="orbital-card oc-3">
            <strong id="heroAvg">0</strong>
            <span>میانگین کل</span>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="dashboard">
      <div class="section-title">
        <div>
          <h2>نمای کلی داشبورد</h2>
          <p>خلاصه وضعیت ایده‌ها بر اساس امتیاز، ریسک، بازار و اجراپذیری</p>
        </div>
      </div>

      <div class="stats-grid">
        <article class="stat-card" style="--accent: rgba(37,99,235,.16)">
          <div class="stat-label">تعداد ایده‌ها</div>
          <div class="stat-value" id="totalIdeas">0</div>
          <div class="stat-note">کل موارد موجود در دیتاست</div>
        </article>

        <article class="stat-card" style="--accent: rgba(22,163,74,.16)">
          <div class="stat-label">میانگین امتیاز</div>
          <div class="stat-value" id="avgScore">0</div>
          <div class="stat-note">از 100</div>
        </article>

        <article class="stat-card" style="--accent: rgba(124,58,237,.16)">
          <div class="stat-label">بالاترین فرصت</div>
          <div class="stat-value" id="bestScore">0</div>
          <div class="stat-note" id="bestTitle">-</div>
        </article>

        <article class="stat-card" style="--accent: rgba(245,158,11,.16)">
          <div class="stat-label">دسته‌بندی‌ها</div>
          <div class="stat-value" id="categoryCount">0</div>
          <div class="stat-note">گروه‌های موضوعی فعال</div>
        </article>
      </div>
    </section>

    <section class="section">
      <div class="toolbar">
        <input class="field" id="searchInput" type="search" placeholder="جستجو در عنوان، توضیح یا دسته‌بندی..." />

        <select class="field" id="categoryFilter">
          <option value="all">همه دسته‌بندی‌ها</option>
        </select>

        <select class="field" id="sortBy">
          <option value="score-desc">امتیاز: زیاد به کم</option>
          <option value="score-asc">امتیاز: کم به زیاد</option>
          <option value="market-desc">بازار: زیاد به کم</option>
          <option value="feasibility-desc">اجراپذیری: زیاد به کم</option>
          <option value="risk-asc">ریسک: کم به زیاد</option>
          <option value="title-asc">عنوان: الفبا</option>
        </select>

        <select class="field" id="scoreFilter">
          <option value="all">همه امتیازها</option>
          <option value="80">امتیاز 80+</option>
          <option value="70">امتیاز 70+</option>
          <option value="60">امتیاز 60+</option>
        </select>

        <div class="view-toggle" role="group" aria-label="تغییر نما">
          <button class="toggle-btn active" id="cardsViewBtn" type="button">کارت</button>
          <button class="toggle-btn" id="tableViewBtn" type="button">جدول</button>
        </div>
      </div>
    </section>

    <section class="section layout">
      <div>
        <div class="section-title">
          <div>
            <h2>ایده‌ها</h2>
            <p id="resultCount">در حال بارگذاری...</p>
          </div>
        </div>

        <div id="cardsView" class="cards-grid"></div>

        <div id="tableView" class="table-wrap hidden">
          <table>
            <thead>
              <tr>
                <th>عنوان</th>
                <th>دسته‌بندی</th>
                <th>امتیاز</th>
                <th>بازار</th>
                <th>اجرا</th>
                <th>ریسک</th>
                <th>جزئیات</th>
              </tr>
            </thead>
            <tbody id="ideasTableBody"></tbody>
          </table>
        </div>

        <div id="emptyState" class="empty hidden">
          نتیجه‌ای پیدا نشد. فیلترها یا عبارت جستجو را تغییر بده.
        </div>
      </div>

      <aside>
        <div class="panel">
          <div class="section-title">
            <div>
              <h2>فرصت‌های برتر</h2>
              <p>پنج ایده با بالاترین امتیاز</p>
            </div>
          </div>
          <div class="top-list" id="topList"></div>
        </div>

        <div class="panel section">
          <div class="section-title">
            <div>
              <h2>Heatmap امتیاز</h2>
              <p>شدت رنگ بر اساس امتیاز کل</p>
            </div>
          </div>
          <div class="heatmap" id="heatmap"></div>
        </div>
      </aside>
    </section>
  </main>

  <div class="modal-backdrop" id="modalBackdrop" aria-hidden="true">
    <section class="modal" role="dialog" aria-modal="true" aria-labelledby="modalTitle">
      <header class="modal-header">
        <div>
          <h3 id="modalTitle">جزئیات ایده</h3>
          <div id="modalCategory"></div>
        </div>
        <button class="close-btn" id="closeModal" type="button" aria-label="بستن">×</button>
      </header>
      <div class="modal-body" id="modalBody"></div>
    </section>
  </div>

  <div class="toast" id="toast">انجام شد</div>

  <script>
    "use strict";

    const ideas = [
      {
        id: 1,
        title: "پلتفرم داوری فرصت‌های آربیتراژ",
        category: "FinTech",
        description: "سیستمی برای شناسایی و اولویت‌بندی فرصت‌های اختلاف قیمت و تصمیم‌گیری سریع.",
        score: 91,
        market: 88,
        feasibility: 82,
        risk: 42,
        impact: 90,
        effort: 68,
        tags: ["Arbitrage", "Dashboard", "Automation"],
        details: "تمرکز اصلی روی سرعت پردازش، شفافیت داده و کاهش خطای انسانی در تصمیم‌گیری است.",
        nextSteps: ["طراحی مدل امتیازدهی", "ساخت MVP بدون وابستگی خارجی", "تعریف معیارهای هشدار"]
      },
      {
        id: 2,
        title: "داشبورد مدیریت جریان نقدی",
        category: "Finance",
        description: "ابزاری برای پایش ورودی و خروجی نقدینگی، پیش‌بینی کمبود نقدی و سناریوسازی.",
        score: 87,
        market: 84,
        feasibility: 86,
        risk: 38,
        impact: 88,
        effort: 61,
        tags: ["Cashflow", "Forecasting", "SME"],
        details: "برای کسب‌وکارهای کوچک و متوسط مناسب است و می‌تواند با فایل‌های CSV کار کند.",
        nextSteps: ["تعریف قالب CSV", "ساخت گزارش ماهانه", "اضافه کردن هشدار کسری نقدینگی"]
      },
      {
        id: 3,
        title: "سیستم رزومه‌ساز هوشمند",
        category: "Productivity",
        description: "ساخت رزومه‌های هدفمند بر اساس موقعیت شغلی، مهارت‌ها و تجربه کاربر.",
        score: 79,
        market: 81,
        feasibility: 90,
        risk: 35,
        impact: 74,
        effort: 52,
        tags: ["CV", "Career", "Template"],
        details: "قابل پیاده‌سازی به صورت کاملاً آفلاین با قالب‌های HTML و خروجی PDF مرورگر.",
        nextSteps: ["طراحی قالب‌ها", "ساخت فرم اطلاعات", "افزودن خروجی چاپ"]
      },
      {
        id: 4,
        title: "پایگاه داده نقش‌های بازی مافیا",
        category: "Game",
        description: "بانک اطلاعاتی نقش‌ها، سناریوها و قوانین برای مدیریت بازی مافیا.",
        score: 76,
        market: 65,
        feasibility: 91,
        risk: 28,
        impact: 70,
        effort: 45,
        tags: ["Mafia", "Database", "Game Design"],
        details: "مناسب برای تولید محتوا، اپلیکیشن مدیریت بازی یا مرجع سناریوها.",
        nextSteps: ["ساخت دیتای استاندارد", "طراحی فیلتر نقش‌ها", "افزودن سناریوساز"]
      },
      {
        id: 5,
        title: "ابزار تحلیل ایده‌های تحقیق و توسعه",
        category: "R&D",
        description: "سامانه‌ای برای امتیازدهی به ایده‌های R&D بر اساس نوآوری، هزینه و امکان اجرا.",
        score: 84,
        market: 73,
        feasibility: 78,
        risk: 49,
        impact: 92,
        effort: 72,
        tags: ["Innovation", "Scoring", "R&D"],
        details: "برای تیم‌هایی که چندین ایده پژوهشی دارند و نیاز به اولویت‌بندی دارند کاربردی است.",
        nextSteps: ["تعریف شاخص‌های R&D", "ساخت فرم ارزیابی", "خروجی مقایسه‌ای"]
      },
      {
        id: 6,
        title: "سیستم تحلیل شغل و مهارت",
        category: "HRTech",
        description: "تحلیل فاصله مهارتی بین رزومه فرد و نیازمندی‌های شغلی.",
        score: 82,
        market: 86,
        feasibility: 74,
        risk: 46,
        impact: 83,
        effort: 69,
        tags: ["Skills", "Jobs", "Matching"],
        details: "می‌تواند به صورت rule-based شروع شود و بعداً با مدل‌های هوشمندتر توسعه پیدا کند.",
        nextSteps: ["استخراج مهارت‌ها", "تعریف ماتریس تطبیق", "ساخت گزارش شکاف مهارتی"]
      },
      {
        id: 7,
        title: "کنترل پنل فرصت‌های صادراتی",
        category: "Business",
        description: "داشبوردی برای رتبه‌بندی بازارهای صادراتی بر اساس تقاضا، ریسک و حاشیه سود.",
        score: 80,
        market: 89,
        feasibility: 63,
        risk: 57,
        impact: 86,
        effort: 75,
        tags: ["Export", "Market", "Risk"],
        details: "مناسب کسب‌وکارهایی است که نیاز به تصمیم‌گیری سریع درباره بازار هدف دارند.",
        nextSteps: ["تعریف شاخص کشورها", "ورود دیتای اولیه", "طراحی مدل اولویت‌بندی"]
      },
      {
        id: 8,
        title: "داشبورد آموزشی برای تحلیل مالی",
        category: "Education",
        description: "محیطی برای آموزش مفاهیم مالی با نمودار، مثال و تمرین‌های مرحله‌ای.",
        score: 73,
        market: 77,
        feasibility: 88,
        risk: 33,
        impact: 69,
        effort: 55,
        tags: ["Learning", "Finance", "Interactive"],
        details: "بدون نیاز به بک‌اند می‌تواند به شکل فایل HTML مستقل برای آموزش استفاده شود.",
        nextSteps: ["ساخت درس‌های کوتاه", "افزودن مثال تعاملی", "طراحی آزمون ساده"]
      },
      {
        id: 9,
        title: "سیستم ثبت و تحلیل پروژه‌های کوچک",
        category: "SaaS",
        description: "ابزاری سبک برای مدیریت ایده، وضعیت، هزینه و خروجی پروژه‌های کوچک.",
        score: 78,
        market: 75,
        feasibility: 87,
        risk: 37,
        impact: 76,
        effort: 58,
        tags: ["Project", "SaaS", "Tracking"],
        details: "قابل اجرا به صورت لوکال یا روی هاست ساده با ذخیره‌سازی فایل/LocalStorage.",
        nextSteps: ["تعریف وضعیت‌ها", "ساخت کارت پروژه", "افزودن خروجی CSV"]
      },
      {
        id: 10,
        title: "تحلیلگر سناریوهای سرمایه‌گذاری",
        category: "Investment",
        description: "مقایسه سناریوهای مختلف سرمایه‌گذاری با امتیازدهی ریسک و بازده.",
        score: 85,
        market: 82,
        feasibility: 72,
        risk: 52,
        impact: 89,
        effort: 70,
        tags: ["Scenario", "ROI", "Risk"],
        details: "تمرکز روی تصمیم‌سازی، نه توصیه مالی مستقیم. خروجی باید شفاف و قابل توضیح باشد.",
        nextSteps: ["تعریف فرمول امتیازدهی", "ساخت جدول سناریو", "افزودن مقایسه بصری"]
      },
      {
        id: 11,
        title: "کتابخانه کامپوننت UI آفلاین",
        category: "Developer Tool",
        description: "مجموعه‌ای از کامپوننت‌های HTML/CSS/JS بدون وابستگی برای ساخت سریع داشبوردها.",
        score: 81,
        market: 70,
        feasibility: 93,
        risk: 31,
        impact: 78,
        effort: 50,
        tags: ["UI", "Offline", "Components"],
        details: "برای شرایطی که نصب پکیج خارجی سخت است، یک کتابخانه سبک داخلی ارزش زیادی دارد.",
        nextSteps: ["تعریف توکن‌های طراحی", "ساخت کامپوننت‌ها", "مستندسازی نمونه‌ها"]
      },
      {
        id: 12,
        title: "ابزار بررسی کیفیت پرامپت‌ها",
        category: "AI Tooling",
        description: "رتبه‌بندی و بهبود پرامپت‌ها بر اساس وضوح، محدودیت‌ها و خروجی مورد انتظار.",
        score: 83,
        market: 79,
        feasibility: 80,
        risk: 41,
        impact: 84,
        effort: 64,
        tags: ["Prompt", "Quality", "AI"],
        details: "می‌تواند با چک‌لیست‌های ثابت شروع شود و بعداً به موتور تحلیل پیشرفته‌تر تبدیل شود.",
        nextSteps: ["تعریف معیارهای پرامپت", "ساخت امتیازدهی", "پیشنهاد نسخه بهبود‌یافته"]
      }
    ];

    const categoryColors = {
      FinTech: "#2563eb",
      Finance: "#16a34a",
      Productivity: "#7c3aed",
      Game: "#f97316",
      "R&D": "#0891b2",
      HRTech: "#db2777",
      Business: "#ca8a04",
      Education: "#0d9488",
      SaaS: "#4f46e5",
      Investment: "#dc2626",
      "Developer Tool": "#9333ea",
      "AI Tooling": "#0284c7"
    };

    const state = {
      view: localStorage.getItem("ideas_view") || "cards",
      theme: localStorage.getItem("ideas_theme") || "light",
      query: "",
      category: "all",
      sort: "score-desc",
      minScore: "all"
    };

    const $ = selector => document.querySelector(selector);

    const els = {
      totalIdeas: $("#totalIdeas"),
      avgScore: $("#avgScore"),
      bestScore: $("#bestScore"),
      bestTitle: $("#bestTitle"),
      categoryCount: $("#categoryCount"),
      heroTotal: $("#heroTotal"),
      heroBest: $("#heroBest"),
      heroAvg: $("#heroAvg"),
      searchInput: $("#searchInput"),
      categoryFilter: $("#categoryFilter"),
      sortBy: $("#sortBy"),
      scoreFilter: $("#scoreFilter"),
      cardsView: $("#cardsView"),
      tableView: $("#tableView"),
      tableBody: $("#ideasTableBody"),
      resultCount: $("#resultCount"),
      emptyState: $("#emptyState"),
      topList: $("#topList"),
      heatmap: $("#heatmap"),
      cardsViewBtn: $("#cardsViewBtn"),
      tableViewBtn: $("#tableViewBtn"),
      modalBackdrop: $("#modalBackdrop"),
      closeModal: $("#closeModal"),
      modalTitle: $("#modalTitle"),
      modalCategory: $("#modalCategory"),
      modalBody: $("#modalBody"),
      toast: $("#toast")
    };

    function formatNumber(value) {
      return new Intl.NumberFormat("fa-IR").format(value);
    }

    function getScoreColor(score) {
      if (score >= 85) return "#16a34a";
      if (score >= 75) return "#2563eb";
      if (score >= 65) return "#f59e0b";
      return "#ef4444";
    }

    function getRiskLabel(risk) {
      if (risk <= 35) return "کم";
      if (risk <= 55) return "متوسط";
      return "زیاد";
    }

    function getCategoryColor(category) {
      return categoryColors[category] || "#64748b";
    }

    function escapeHtml(value) {
      return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
    }

    function setTheme(theme) {
      state.theme = theme;
      document.documentElement.dataset.theme = theme;
      localStorage.setItem("ideas_theme", theme);
    }

    function showToast(message) {
      els.toast.textContent = message;
      els.toast.classList.add("show");
      window.clearTimeout(showToast.timer);
      showToast.timer = window.setTimeout(() => {
        els.toast.classList.remove("show");
      }, 2200);
    }

    function populateCategories() {
      const categories = [...new Set(ideas.map(item => item.category))].sort();
      const options = categories
        .map(category => `<option value="${escapeHtml(category)}">${escapeHtml(category)}</option>`)
        .join("");

      els.categoryFilter.insertAdjacentHTML("beforeend", options);
    }

    function computeStats() {
      const total = ideas.length;
      const avg = Math.round(ideas.reduce((sum, item) => sum + item.score, 0) / total);
      const best = [...ideas].sort((a, b) => b.score - a.score)[0];
      const categoryCount = new Set(ideas.map(item => item.category)).size;

      els.totalIdeas.textContent = formatNumber(total);
      els.avgScore.textContent = formatNumber(avg);
      els.bestScore.textContent = formatNumber(best.score);
      els.bestTitle.textContent = best.title;
      els.categoryCount.textContent = formatNumber(categoryCount);

      els.heroTotal.textContent = formatNumber(total);
      els.heroBest.textContent = formatNumber(best.score);
      els.heroAvg.textContent = formatNumber(avg);
    }

    function getFilteredIdeas() {
      const query = state.query.trim().toLowerCase();

      let list = ideas.filter(item => {
        const matchesQuery =
          !query ||
          item.title.toLowerCase().includes(query) ||
          item.description.toLowerCase().includes(query) ||
          item.category.toLowerCase().includes(query) ||
          item.tags.some(tag => tag.toLowerCase().includes(query));

        const matchesCategory = state.category === "all" || item.category === state.category;
        const matchesScore = state.minScore === "all" || item.score >= Number(state.minScore);

        return matchesQuery && matchesCategory && matchesScore;
      });

      list.sort((a, b) => {
        switch (state.sort) {
          case "score-asc":
            return a.score - b.score;
          case "market-desc":
            return b.market - a.market;
          case "feasibility-desc":
            return b.feasibility - a.feasibility;
          case "risk-asc":
            return a.risk - b.risk;
          case "title-asc":
            return a.title.localeCompare(b.title, "fa");
          case "score-desc":
          default:
            return b.score - a.score;
        }
      });

      return list;
    }

    function renderCards(list) {
      els.cardsView.innerHTML = list.map(item => {
        const color = getCategoryColor(item.category);

        return `
          <article class="idea-card" style="--cat-color:${color}">
            <div class="idea-head">
              <h3 class="idea-title">${escapeHtml(item.title)}</h3>
              <span class="score-badge" style="background:${getScoreColor(item.score)}">${formatNumber(item.score)}</span>
            </div>

            <div class="category">
              <span class="dot"></span>
              ${escapeHtml(item.category)}
            </div>

            <p class="desc">${escapeHtml(item.description)}</p>

            <div class="metrics">
              <div class="metric">
                <strong>${formatNumber(item.market)}</strong>
                <span>بازار</span>
              </div>
              <div class="metric">
                <strong>${formatNumber(item.feasibility)}</strong>
                <span>اجرا</span>
              </div>
              <div class="metric">
                <strong>${escapeHtml(getRiskLabel(item.risk))}</strong>
                <span>ریسک</span>
              </div>
            </div>

            <div class="progress" aria-label="امتیاز">
              <i style="--w:${item.score}%"></i>
            </div>

            <div class="card-actions">
              <div class="chips">
                ${item.tags.slice(0, 2).map(tag => `<span class="chip">${escapeHtml(tag)}</span>`).join("")}
              </div>
              <button class="small-btn" type="button" data-open="${item.id}">جزئیات</button>
            </div>
          </article>
        `;
      }).join("");
    }

    function renderTable(list) {
      els.tableBody.innerHTML = list.map(item => {
        const color = getCategoryColor(item.category);

        return `
          <tr>
            <td class="table-title">${escapeHtml(item.title)}</td>
            <td>
              <span class="category" style="--cat-color:${color}; margin-top:0">
                <span class="dot"></span>
                ${escapeHtml(item.category)}
              </span>
            </td>
            <td>
              <span class="score-badge" style="background:${getScoreColor(item.score)}">
                ${formatNumber(item.score)}
              </span>
            </td>
            <td>${formatNumber(item.market)}</td>
            <td>${formatNumber(item.feasibility)}</td>
            <td>${escapeHtml(getRiskLabel(item.risk))} / ${formatNumber(item.risk)}</td>
            <td>
              <button class="small-btn" type="button" data-open="${item.id}">مشاهده</button>
            </td>
          </tr>
        `;
      }).join("");
    }

    function renderTopOpportunities() {
      const top = [...ideas].sort((a, b) => b.score - a.score).slice(0, 5);

      els.topList.innerHTML = top.map((item, index) => `
        <button class="top-item" type="button" data-open="${item.id}">
          <span class="rank">${formatNumber(index + 1)}</span>
          <span>
            <span class="top-title">${escapeHtml(item.title)}</span>
            <span class="top-meta">${escapeHtml(item.category)} · بازار ${formatNumber(item.market)}</span>
          </span>
          <span class="score-badge" style="background:${getScoreColor(item.score)}">${formatNumber(item.score)}</span>
        </button>
      `).join("");
    }

    function renderHeatmap() {
      const sorted = [...ideas].sort((a, b) => b.score - a.score);

      els.heatmap.innerHTML = sorted.map(item => {
        const alpha = Math.max(0.32, item.score / 100);
        const color = getScoreColor(item.score);

        return `
          <button
            class="heat-cell"
            type="button"
            data-open="${item.id}"
            title="${escapeHtml(item.title)} - ${item.score}"
            style="background: color-mix(in srgb, ${color} ${Math.round(alpha * 100)}%, #111827)"
          >
            ${formatNumber(item.score)}
          </button>
        `;
      }).join("");
    }

    function renderView() {
      const list = getFilteredIdeas();
      const hasResults = list.length > 0;

      els.resultCount.textContent = `${formatNumber(list.length)} نتیجه از ${formatNumber(ideas.length)} ایده`;
      els.emptyState.classList.toggle("hidden", hasResults);

      renderCards(list);
      renderTable(list);

      els.cardsView.classList.toggle("hidden", state.view !== "cards" || !hasResults);
      els.tableView.classList.toggle("hidden", state.view !== "table" || !hasResults);

      els.cardsViewBtn.classList.toggle("active", state.view === "cards");
      els.tableViewBtn.classList.toggle("active", state.view === "table");
    }

    function openModal(id) {
      const item = ideas.find(idea => idea.id === Number(id));
      if (!item) return;

      const color = getCategoryColor(item.category);

      els.modalTitle.textContent = item.title;
      els.modalCategory.innerHTML = `
        <span class="category" style="--cat-color:${color}">
          <span class="dot"></span>
          ${escapeHtml(item.category)}
        </span>
      `;

      els.modalBody.innerHTML = `
        <p style="color:var(--muted); line-height:1.9; margin-top:0">
          ${escapeHtml(item.description)}
        </p>

        <div class="detail-grid">
          <div class="detail-box">
            <strong>${formatNumber(item.score)}</strong>
            <span>امتیاز کل</span>
          </div>
          <div class="detail-box">
            <strong>${formatNumber(item.market)}</strong>
            <span>بازار</span>
          </div>
          <div class="detail-box">
            <strong>${formatNumber(item.feasibility)}</strong>
            <span>اجراپذیری</span>
          </div>
          <div class="detail-box">
            <strong>${formatNumber(item.risk)}</strong>
            <span>ریسک</span>
          </div>
        </div>

        <div class="detail-grid">
          <div class="detail-box">
            <strong>${formatNumber(item.impact)}</strong>
            <span>اثرگذاری</span>
          </div>
          <div class="detail-box">
            <strong>${formatNumber(item.effort)}</strong>
            <span>هزینه/تلاش</span>
          </div>
          <div class="detail-box">
            <strong>${escapeHtml(getRiskLabel(item.risk))}</strong>
            <span>سطح ریسک</span>
          </div>
          <div class="detail-box">
            <strong>${item.score >= 80 ? "بالا" : item.score >= 70 ? "متوسط" : "نیازمند بررسی"}</strong>
            <span>اولویت</span>
          </div>
        </div>

        <div class="detail-section">
          <h4>تحلیل کوتاه</h4>
          <p>${escapeHtml(item.details)}</p>
        </div>

        <div class="detail-section">
          <h4>اقدام‌های پیشنهادی</h4>
          <ul>
            ${item.nextSteps.map(step => `<li>${escapeHtml(step)}</li>`).join("")}
          </ul>
        </div>

        <div class="detail-section">
          <h4>برچسب‌ها</h4>
          <div class="chips">
            ${item.tags.map(tag => `<span class="chip">${escapeHtml(tag)}</span>`).join("")}
          </div>
        </div>
      `;

      els.modalBackdrop.classList.add("open");
      els.modalBackdrop.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";
    }

    function closeModal() {
      els.modalBackdrop.classList.remove("open");
      els.modalBackdrop.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
    }

    function setView(view) {
      state.view = view;
      localStorage.setItem("ideas_view", view);
      renderView();
    }

    function exportCsv() {
      const rows = getFilteredIdeas();
      const headers = [
        "id",
        "title",
        "category",
        "score",
        "market",
        "feasibility",
        "risk",
        "impact",
        "effort",
        "tags",
        "description"
      ];

      const csv = [
        headers.join(","),
        ...rows.map(item => headers.map(key => {
          const value = Array.isArray(item[key]) ? item[key].join("|") : item[key];
          return `"${String(value ?? "").replaceAll('"', '""')}"`;
        }).join(","))
      ].join("\n");

      const blob = new Blob(["\ufeff" + csv], { type: "text/csv;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");

      a.href = url;
      a.download = "ideas-dashboard.csv";
      document.body.appendChild(a);
      a.click();
      a.remove();

      URL.revokeObjectURL(url);
      showToast("فایل CSV ساخته شد");
    }

    function bindEvents() {
      els.searchInput.addEventListener("input", event => {
        state.query = event.target.value;
        renderView();
      });

      els.categoryFilter.addEventListener("change", event => {
        state.category = event.target.value;
        renderView();
      });

      els.sortBy.addEventListener("change", event => {
        state.sort = event.target.value;
        renderView();
      });

      els.scoreFilter.addEventListener("change", event => {
        state.minScore = event.target.value;
        renderView();
      });

      els.cardsViewBtn.addEventListener("click", () => setView("cards"));
      els.tableViewBtn.addEventListener("click", () => setView("table"));

      document.addEventListener("click", event => {
        const opener = event.target.closest("[data-open]");
        if (opener) {
          openModal(opener.dataset.open);
        }
      });

      els.closeModal.addEventListener("click", closeModal);

      els.modalBackdrop.addEventListener("click", event => {
        if (event.target === els.modalBackdrop) closeModal();
      });

      document.addEventListener("keydown", event => {
        if (event.key === "Escape") closeModal();
      });

      $("#themeToggle").addEventListener("click", () => {
        setTheme(state.theme === "dark" ? "light" : "dark");
      });

      $("#exportCsv").addEventListener("click", exportCsv);

      $("#scrollToDashboard").addEventListener("click", () => {
        $("#dashboard").scrollIntoView({ behavior: "smooth", block: "start" });
      });
    }

    function init() {
      setTheme(state.theme);
      populateCategories();
      computeStats();
      renderTopOpportunities();
      renderHeatmap();
      bindEvents();
      setView(state.view);
    }

    init();
  </script>
</body>
</html>
```

نکته مهم: دیتای داخل آرایه `ideas` فعلاً داخل همین فایل است. اگر بخواهی، در پیام بعدی می‌توانم همین نسخه را دقیقاً با دیتای کامل ۵۶ ایده‌ای خودت پر کنم و ساختار امتیازدهی را هم استانداردتر کنم.