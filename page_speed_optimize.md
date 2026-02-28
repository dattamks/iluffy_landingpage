# iluffy.in — PageSpeed Insights Optimization Report

**Audit Date:** February 28, 2026
**Stack:** Django + PostgreSQL + Railway.app
**App:** Resume AI with Luffy (iluffy.in)

---

## 1. Audit Scores at a Glance

> No CrUX field data — Google hasn't collected enough real-user traffic yet. This is expected for a newly launched site. All scores below are Lighthouse lab data.

### 1.1 Desktop Scores

| Performance | Accessibility | Best Practices | SEO |
|:-----------:|:-------------:|:--------------:|:---:|
| 🟠 **84** | 🟢 **92** | 🟢 **100** | 🟢 **91** |

### 1.2 Mobile Scores

| Performance | Accessibility | Best Practices | SEO |
|:-----------:|:-------------:|:--------------:|:---:|
| 🟠 **78** | 🟢 **94** | 🟢 **100** | 🟢 **91** |

---

## 2. Core Web Vitals — Detailed Metrics

### 2.1 Desktop

| Metric | Value | Status | Threshold |
|--------|-------|--------|-----------|
| First Contentful Paint (FCP) | **0.7s** | 🟢 Good | < 1.8s |
| Largest Contentful Paint (LCP) | **0.7s** | 🟢 Good | < 2.5s |
| Total Blocking Time (TBT) | **350ms** | 🔴 Poor | < 200ms |
| Cumulative Layout Shift (CLS) | **0** | 🟢 Good | < 0.1 |
| Speed Index | **1.1s** | 🟢 Good | < 3.4s |

**Desktop verdict:** FCP and LCP are excellent. Speed Index is good. CLS is perfect. The only red flag is TBT at 350ms — heavy JavaScript is blocking the main thread.

### 2.2 Mobile

| Metric | Value | Status | Threshold |
|--------|-------|--------|-----------|
| First Contentful Paint (FCP) | **2.9s** | 🟠 Needs Improvement | < 1.8s |
| Largest Contentful Paint (LCP) | **2.9s** | 🟠 Needs Improvement | < 2.5s |
| Total Blocking Time (TBT) | **350ms** | 🟠 Needs Improvement | < 200ms |
| Cumulative Layout Shift (CLS) | **0** | 🟢 Good | < 0.1 |
| Speed Index | **5.0s** | 🟠 Needs Improvement | < 3.4s |

**Mobile verdict:** FCP and LCP at 2.9s sit in the Needs Improvement band. Speed Index of 5.0s is orange. TBT is the same as desktop, confirming render-blocking JS is the root cause.

> ⚠️ **The 4x gap between desktop (0.7s LCP) and mobile (2.9s LCP) is classic render-blocking resource behaviour.** On mobile's slower simulated connection (Slow 4G), render-blocking CSS/JS delays the first paint dramatically. This is your #1 priority to fix.

---

## 3. Complete Issue Registry

### 3.1 Performance Issues

| Severity | Issue | Savings / Impact | Affected Metric |
|----------|-------|-----------------|-----------------|
| 🔴 Critical | Render-blocking requests | Desktop −490ms \| Mobile −1,510ms | FCP, LCP, TBT |
| 🔴 Critical | Reduce JavaScript execution time | Mobile: 1.5s execution time | TBT, FCP |
| 🔴 Critical | Minimize main-thread work | Mobile: 3.7s total | TBT, Speed Index |
| 🔴 Critical | LCP breakdown (mobile) | LCP at 2.9s vs 2.5s threshold | LCP |
| 🟠 High | Network dependency tree | Long waterfall chain detected | FCP, LCP |
| 🟠 High | Reduce unused JavaScript | Est. savings of 37 KiB | TBT, Speed Index |
| 🟡 Medium | Use efficient cache lifetimes | Est. savings of 10 KiB | Repeat visits |
| 🔵 Low | Avoid long main-thread tasks | Desktop: 3 tasks \| Mobile: 6 tasks | TBT |
| 🔵 Low | Avoid non-composited animations | 2 animated elements | CLS, Jank |
| 🔵 Low | Optimize DOM size | DOM may be too large | Speed Index |
| 🔵 Low | 3rd parties | External scripts present | FCP, TBT |

### 3.2 Accessibility Issues

| Severity | Issue | Category |
|----------|-------|----------|
| 🟠 High | Background & foreground colors have insufficient contrast ratio | Contrast |
| 🟠 High | Heading elements not in sequentially-descending order | Navigation |
| 🟡 Medium | Document does not have a main landmark | Best Practices (Desktop) |
| 🟡 Medium | Uses links with no compatible elements (empty/icon links) | Best Practices (Desktop) |

### 3.3 SEO Issues

| Severity | Issue | Category |
|----------|-------|----------|
| 🔴 Critical | robots.txt is not valid — 1 error found | Crawling & Indexing |

---

## 4. Fix-by-Fix Implementation Guide

> **Target after all fixes:** Desktop Performance 95+, Mobile Performance 90+, SEO 100, Accessibility 98+

---

### FIX 1 — Eliminate Render-Blocking Resources
**Severity: 🔴 Critical | Mobile savings: −1,510ms | Affects: FCP, LCP, TBT**

This is your single biggest win. Render-blocking resources are CSS/JS files loaded in `<head>` that prevent the browser from painting anything until they are fully downloaded and parsed. On mobile's Slow 4G simulation, this costs 1.5 full seconds before anything appears.

#### Fix 1a — Defer / Async all non-critical JavaScript

In your Django base template, change all script tags from:

```html
<script src="{% static 'js/bootstrap.bundle.min.js' %}"></script>
```

To:

```html
<script src="{% static 'js/bootstrap.bundle.min.js' %}" defer></script>
```

Use `defer` for scripts that need DOM access, `async` for independent third-party scripts. Never place scripts in `<head>` without `defer` or `async`.

#### Fix 1b — Load non-critical CSS non-blocking

```html
<link rel="preload" href="{% static 'css/style.css' %}" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="{% static 'css/style.css' %}"></noscript>
```

#### Fix 1c — Google Fonts: add display=swap and preconnect

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=YourFont&display=swap" rel="stylesheet">
```

`display=swap` tells the browser to show fallback text immediately, so users see content instead of invisible text during font download (FOIT).

#### Fix 1d — Inline critical CSS

Extract CSS rules needed for above-the-fold content (navbar, hero section, primary button) and inline them in `<head>`:

```html
<head>
  <style>
    /* Paste critical above-the-fold CSS here */
    body { margin: 0; font-family: 'YourFont', sans-serif; }
    .navbar { ... }
    .hero { ... }
    .btn-primary { ... }
  </style>
  <!-- All other CSS loaded non-blocking below -->
</head>
```

Tools like [critical](https://github.com/addyosmani/critical) or [criticalcss.com](https://criticalcss.com) can extract this automatically.

> ✅ **Expected result:** Mobile FCP should drop from 2.9s to ~1.2–1.6s. This alone will likely push mobile Performance from **78 → 88+**.

---

### FIX 2 — Reduce JavaScript Execution Time
**Severity: 🔴 Critical | Mobile JS execution: 1.5s | Main-thread: 3.7s**

#### Fix 2a — Use Bootstrap CSS-only on the landing page

If your landing page uses Bootstrap mainly for layout and styling (no dropdowns or modals), remove `bootstrap.bundle.min.js` entirely from the landing page. Only include it on pages that actually need JS components.

#### Fix 2b — Split your custom JavaScript

```html
<!-- Inline ONLY the above-the-fold critical JS -->
<script>
  // Mobile menu toggle only
  document.getElementById('navToggle').addEventListener('click', function() {
    document.getElementById('navMenu').classList.toggle('open');
  });
</script>

<!-- Everything else deferred -->
<script src="{% static 'js/animations.js' %}" defer></script>
<script src="{% static 'js/analytics.js' %}" defer></script>
```

#### Fix 2c — Reduce unused JavaScript (37 KiB flagged)

- **Option A (Quick):** Remove Bootstrap JS entirely if unused
- **Option B (Better):** Import only Bootstrap JS components you use via ES modules:

```javascript
// Instead of the full bundle, import only what you need
import { Modal } from 'bootstrap';
import { Tooltip } from 'bootstrap';
```

- **Option C (Best long-term):** Bundle with Webpack or Vite — tree-shakes unused code automatically

#### Fix 2d — Avoid large inline JS from Django context

Move large Django-injected data to a JSON endpoint and fetch it lazily instead of embedding it in `<script>` tags:

```python
# views.py — create a lightweight JSON endpoint
def page_data(request):
    return JsonResponse({'plans': [...], 'features': [...]})
```

```javascript
// Fetch lazily in your JS
fetch('/api/page-data/').then(r => r.json()).then(data => {
  // render dynamic content
});
```

---

### FIX 3 — Fix robots.txt Syntax Error
**Severity: 🔴 Critical | Affect: SEO 91 → 100**

One broken line in your `robots.txt` prevents Googlebot from parsing it correctly, which can cause unpredictable crawling behaviour.

#### Step 1 — Find the error

Open `https://iluffy.in/robots.txt` in a browser and look for:
- Missing blank line between User-agent blocks
- Comments (`#`) on the same line as a directive
- Incorrect capitalisation (`disallow` instead of `Disallow`)
- Sitemap URL pointing to a non-existent file

#### Step 2 — A correct robots.txt for iluffy.in

```
User-agent: *
Disallow: /admin/
Disallow: /accounts/
Allow: /

Sitemap: https://iluffy.in/sitemap.xml
```

#### Step 3 — Serve it cleanly from Django

```python
# urls.py
from django.views.generic import TemplateView

urlpatterns = [
    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt',
        content_type='text/plain'
    )),
]
```

Create `templates/robots.txt` with the valid content above. After deploying, validate at:
**https://search.google.com/search-console/robots-testing-tool**

> ✅ **Expected result:** SEO score jumps from **91 → 100**.

---

### FIX 4 — Configure Cache-Control Headers via WhiteNoise
**Severity: 🟠 High | Saves: 10 KiB + improves all repeat visits**

Since iluffy.in runs on Railway.app (a managed PaaS), you have no direct Nginx access. Cache-Control headers, Gzip compression, and static file serving are all handled at the Django level using **WhiteNoise**. This is the correct and recommended approach for Railway-deployed Django apps.

#### Step 1 — Install WhiteNoise

```bash
pip install whitenoise
```

Add to `requirements.txt`:

```
whitenoise[brotli]
```

The `[brotli]` extra enables Brotli compression (better than Gzip, supported by all modern browsers).

#### Step 2 — Configure settings.py

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Must be second, immediately after SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ... rest of your middleware
]

# Serve static files with WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Cache static files for 1 year (safe because filenames are fingerprinted)
WHITENOISE_MAX_AGE = 31536000

# Optional: serve index.html for unknown URLs (useful for SPAs, skip if not needed)
# WHITENOISE_ROOT = BASE_DIR / 'staticfiles'
```

`CompressedManifestStaticFilesStorage` appends a content hash to filenames (e.g. `main.abc123.css`), enabling safe 1-year caching because the URL changes whenever content changes. WhiteNoise also automatically serves Brotli-compressed versions where supported.

#### Step 3 — Collect static files on deploy

Ensure your Railway deploy command runs `collectstatic`:

```bash
# In railway.toml or your start command
python manage.py collectstatic --noinput && gunicorn myproject.wsgi
```

Or in `railway.toml`:

```toml
[deploy]
startCommand = "python manage.py collectstatic --noinput && gunicorn myproject.wsgi:application"
```

#### Step 4 — Verify headers are working

After deploying, open Chrome DevTools → Network tab → click any `.css` or `.js` file → check Response Headers for:

```
Cache-Control: public, max-age=31536000, immutable
Content-Encoding: br   ← Brotli compression active
```

---

### FIX 5 — Fix Colour Contrast Ratio
**Severity: 🟠 High | Affects: Accessibility 92/94 → 97+**

Some text/background colour combinations don't meet WCAG 2.1 AA (minimum 4.5:1 for normal text, 3:1 for large text).

#### How to find offending elements

Open Chrome DevTools → Elements tab → select any text element → Accessibility panel on the right shows the contrast ratio. Common culprits:

- Light gray text on white backgrounds (subtitles, labels)
- White text on light-coloured backgrounds (badges, tags)
- Placeholder text in input fields

#### Fix in your CSS

```css
/* BEFORE — insufficient contrast (~2.85:1) */
.subtitle    { color: #999999; }
.helper-text { color: #AAAAAA; }

/* AFTER — WCAG AA compliant */
.subtitle    { color: #595959; }  /* 7.0:1 ratio on white */
.helper-text { color: #767676; }  /* 4.54:1 ratio on white */
```

Validate your colour pairs at: **https://webaim.org/resources/contrastchecker**

---

### FIX 6 — Fix Heading Hierarchy
**Severity: 🟠 High | Affects: Accessibility + SEO**

Your headings skip levels (e.g. `h1` → `h3`, missing `h2`). Screen readers depend on heading structure for navigation, and Google uses it to understand content hierarchy.

#### Correct structure for a landing page

```html
<!-- ONE h1 per page — the primary page topic -->
<h1>Your Resume, Perfected by AI Intelligence</h1>

<h2>How It Works</h2>
  <h3>Upload Your Resume</h3>
  <h3>Get Your ATS Score</h3>
  <h3>Download Optimized Resume</h3>

<h2>Pricing</h2>
  <h3>Free Plan</h3>
  <h3>Pro Plan — ₹499/month</h3>

<h2>Why iluffy.in?</h2>
```

**Common mistakes to check in your templates:**
- Using `h3` directly after `h1` (skipping `h2`)
- Using heading tags for visual styling — use a CSS class instead (`<p class="section-title">`)
- Multiple `h1` tags on the page
- Hero subheading styled as `h1` when it should be a `<p>` with large styling

---

### FIX 7 — Add ARIA Landmark Roles
**Severity: 🟡 Medium | Affects: Accessibility**

The desktop report flags no `<main>` landmark. Screen readers cannot jump directly to main content without it.

```html
<!-- base.html or landing.html -->
<body>
  <header role="banner">
    <nav role="navigation" aria-label="Main navigation">
      <!-- navbar -->
    </nav>
  </header>

  <main role="main">          <!-- ← This was missing -->
    {% block content %}{% endblock %}
  </main>

  <footer role="contentinfo">
    <!-- footer -->
  </footer>
</body>
```

---

### FIX 8 — Fix Empty / Icon-Only Links
**Severity: 🟡 Medium | Affects: Accessibility**

Links with no text content and no `aria-label` are inaccessible to screen readers. Typically social media icons or SVG-only buttons in your navbar/footer.

```html
<!-- BAD — screen reader announces "link" with no context -->
<a href="https://linkedin.com/...">
  <i class="fab fa-linkedin"></i>
</a>

<!-- GOOD — screen reader announces "LinkedIn Profile" -->
<a href="https://linkedin.com/..." aria-label="LinkedIn Profile">
  <i class="fab fa-linkedin" aria-hidden="true"></i>
</a>
```

`aria-hidden="true"` on the icon tells screen readers to ignore it, since the link's `aria-label` already describes the action.

---

### FIX 9 — Fix Non-Composited Animations
**Severity: 🔵 Low | Affects: Jank on budget Android phones**

Two animated elements use CSS properties that trigger layout/paint recalculation on every frame. This causes visible jank on budget Android phones common in the Indian market.

```css
/* BAD — triggers layout recalculation every frame */
@keyframes slideIn {
  from { left: -100px; }
  to   { left: 0; }
}

/* GOOD — GPU composited, zero layout cost */
@keyframes slideIn {
  from { transform: translateX(-100px); }
  to   { transform: translateX(0); }
}

.animated-element {
  animation: slideIn 0.5s ease;
  will-change: transform;  /* hints browser to promote to GPU layer */
}
```

**Rule:** Only animate `transform` and `opacity`. Never animate `top`, `left`, `width`, `height`, `margin`, or `padding`.

---

### FIX 10 — Optimize DOM Size
**Severity: 🔵 Low | Affects: Memory & Speed Index**

A large DOM costs more memory and layout time — especially on low-end Android devices. Target under 1,500 DOM nodes for a landing page.

**Common causes in Django/Bootstrap templates:**
- Deeply nested Bootstrap grid (`col > row > col > row`)
- Repeating `{% include %}` partials that each add many nodes
- Hidden `display:none` sections still rendered in the DOM
- Font Awesome adding extra elements

**Fixes:**
- Use Chrome DevTools → Elements → Ctrl+F to count nodes
- Replace nested Bootstrap grids with native CSS Flexbox/Grid where possible
- Move modal content to `{% include %}` loaded on demand rather than always in the DOM

---

## 5. Additional Recommendations

### 5.1 Add sitemap.xml (Required for SEO 100)

```python
# settings.py
INSTALLED_APPS += ['django.contrib.sitemaps']
```

```python
# sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'weekly'

    def items(self):
        return ['landing', 'pricing', 'about']

    def location(self, item):
        return reverse(item)
```

```python
# urls.py
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap

urlpatterns += [
    path('sitemap.xml', sitemap, {'sitemaps': {'static': StaticViewSitemap}}),
]
```

### 5.2 HTTP/2 — Already Enabled on Railway

Railway's edge proxy automatically serves all traffic over HTTP/2. You don't need to configure anything for this. Putting Cloudflare in front (see 5.3) also ensures HTTP/2 and HTTP/3 (QUIC) at the CDN edge.

### 5.3 Set Up Cloudflare (Free) — Critical for Indian Users on Railway

Your Railway app is deployed in a US/EU region. For Indian users, every request to load static files adds significant transcontinental latency. Cloudflare's free plan sits in front of Railway as a CDN proxy with edge nodes in Mumbai and Chennai.

**What Cloudflare gives you on Railway:**
- CDN edge nodes in Mumbai and Chennai (closest to your Indian users)
- Automatic CSS/JS/HTML minification
- Browser Cache TTL override (even if Railway changes headers)
- Free DDoS protection
- SSL/TLS management at the edge

**Setup (30 minutes):**

1. Create a free Cloudflare account at cloudflare.com
2. Add your domain `iluffy.in` to Cloudflare
3. Change your domain registrar's nameservers to Cloudflare's (e.g. `asha.ns.cloudflare.com`)
4. In Cloudflare dashboard → SSL/TLS → set mode to **Full (strict)**
5. In Speed → Optimization → enable **Auto Minify** (JS, CSS, HTML)
6. In Caching → Configuration → set Browser Cache TTL to **1 year**

Railway's custom domain continues to work — Cloudflare simply proxies requests to your Railway-assigned URL.

> ✅ **Cloudflare alone typically adds +10–15pts to mobile Performance** for Indian users by eliminating transcontinental latency.

### 5.4 Preload the LCP Image

Identify which element is the LCP on mobile (the hero image or product mockup visible in the Lighthouse filmstrip). Preload it:

```html
<link rel="preload" as="image"
      href="{% static 'img/hero-mockup.webp' %}"
      fetchpriority="high">
```

### 5.5 Serve Images in WebP Format

WebP is 25–35% smaller than JPEG at equivalent quality — meaningful for Indian users on limited mobile data.

```python
# Convert existing images
from PIL import Image

img = Image.open('hero.png')
img.save('hero.webp', 'WEBP', quality=85)
```

```html
<!-- Use <picture> for progressive enhancement -->
<picture>
  <source srcset="{% static 'img/hero.webp' %}" type="image/webp">
  <img src="{% static 'img/hero.png' %}" alt="Resume AI Demo" width="600" height="400">
</picture>
```

Always include `width` and `height` on `<img>` tags — this prevents layout shift and contributes to your CLS of 0.

### 5.6 Add Security Headers via Django (Railway has no Nginx access)

Since Railway is a managed PaaS, security headers must be set at the Django application level, not Nginx. Django's built-in security settings and middleware handle this cleanly.

#### Built-in Django security settings (settings.py)

```python
# settings.py

# HSTS — tells browsers to always use HTTPS
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True  # Submit to browser HSTS preload lists

# Prevent clickjacking
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Prevent MIME type sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True

# XSS protection (older browsers)
SECURE_BROWSER_XSS_FILTER = True

# Redirect HTTP to HTTPS (Railway handles SSL, but this adds safety)
SECURE_SSL_REDIRECT = True  # Set False if Railway already enforces this

# Secure cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

#### Content Security Policy — install django-csp

```bash
pip install django-csp
```

```python
# settings.py
MIDDLEWARE += ['csp.middleware.CSPMiddleware']

CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC  = ("'self'", "https://fonts.googleapis.com")
CSP_STYLE_SRC   = ("'self'", "'unsafe-inline'", "https://fonts.googleapis.com")
CSP_FONT_SRC    = ("'self'", "https://fonts.gstatic.com")
CSP_IMG_SRC     = ("'self'", "data:")
```

#### Verify headers are active

After deploying, check at: **https://securityheaders.com/?q=iluffy.in**

---

## 6. Prioritized Action Plan

| # | Action | Est. Time | Score Impact | Priority |
|---|--------|-----------|-------------|----------|
| 1 | Add `defer` to all JS, fix Google Fonts with `display=swap`, inline critical CSS | 1–2 hrs | 🟢 Mobile +8–12pts | **This Week** |
| 2 | Fix `robots.txt` syntax error — validate in Search Console | 30 mins | 🟢 SEO 91→100 | **This Week** |
| 3 | Configure WhiteNoise (Cache-Control + Brotli compression) in settings.py | 1 hr | 🟢 +3–5pts both | **This Week** |
| 4 | Fix heading hierarchy (h1→h2→h3) + add `<main>` landmark | 1 hr | 🟢 Acc. 92→97+ | This Week |
| 5 | Fix colour contrast ratios — update low-contrast text | 1–2 hrs | 🟢 Acc. +3–5pts | Next Sprint |
| 6 | Add `aria-label` to all icon-only links | 30 mins | 🟢 Acc. +1–2pts | Next Sprint |
| 7 | Convert images to WebP + preload LCP image + add sitemap.xml | 2–3 hrs | 🟢 LCP + SEO | Next Sprint |
| 8 | Set up Cloudflare (free) — CDN with Indian edge nodes | 30–60 mins | 🟢 +10–15pts mobile | After Launch |

---

## 7. Expected Scores After All Fixes

### Desktop (After All Fixes)

| Performance | Accessibility | Best Practices | SEO |
|:-----------:|:-------------:|:--------------:|:---:|
| 🟢 **95+** | 🟢 **98+** | 🟢 **100** | 🟢 **100** |

### Mobile (After All Fixes)

| Performance | Accessibility | Best Practices | SEO |
|:-----------:|:-------------:|:--------------:|:---:|
| 🟢 **90+** | 🟢 **98+** | 🟢 **100** | 🟢 **100** |

### Expected Mobile Core Web Vitals (After Fixes)

| FCP | LCP | TBT | CLS | Speed Index |
|-----|-----|-----|-----|-------------|
| 🟢 < 1.5s | 🟢 < 2.0s | 🟢 < 200ms | 🟢 0 | 🟢 < 2.5s |

> All targets are estimates based on this issue profile. Re-run PageSpeed Insights after each fix to track progress. Results depend on hosting environment, third-party scripts, and content.

---

## 8. What Is Already Working Well

- **CLS = 0 on both mobile and desktop** — Perfect. No layout shift at all. Your images have proper dimensions set and no dynamic content is inserting above the fold.
- **Best Practices = 100 on both** — HTTPS properly configured, no browser console errors, no deprecated APIs.
- **Desktop LCP = 0.7s** — Outstanding server response time and well-optimised above-the-fold content for desktop.
- **No JavaScript console errors** — Clean codebase with no runtime errors.
- **Accessibility 92/94** — Good foundation. The issues are surface-level CSS/HTML patterns, not deep structural problems.
- **CLS = 0** — All images have `width` and `height` attributes set, which is the most common cause of layout shift.

The core performance issue is entirely the **render-blocking resources pattern** — the most common and well-understood performance problem in Bootstrap-based Django sites. Once fixed, iluffy.in will be technically competitive with well-optimised commercial resume tools.

---

*iluffy.in — PageSpeed Optimization Report — February 2026 — Deployed on Railway.app*