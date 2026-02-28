(function () {
  'use strict'

  /* ── Logo renderer ─────────────────────────────────────────────── */
  function renderLogo(container, size) {
    const r = size / 112
    container.innerHTML = `
      <div style="display:inline-flex;align-items:stretch;height:${size}px;border:${Math.max(1,2*r)}px solid #312e81;box-shadow:inset 0 0 ${40*r}px rgba(49,46,129,.15),0 0 0 ${Math.max(1,3*r)}px #c7d2fe,0 0 0 ${Math.max(2,5*r)}px #312e81;background:#eef2ff;position:relative;overflow:hidden;flex-shrink:0;">
        <div style="position:absolute;inset:0;opacity:.5;pointer-events:none;z-index:3;background-image:url(&quot;data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)' opacity='0.07'/%3E%3C/svg%3E&quot;)"></div>
        <div style="position:absolute;inset:0;background:radial-gradient(ellipse at center,transparent 30%,rgba(30,27,75,.15) 100%);pointer-events:none;z-index:3;"></div>
        <div style="width:${90*r}px;background:linear-gradient(160deg,#4f46e5 0%,#3730a3 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative;z-index:1;flex-shrink:0;border-right:${Math.max(1,2*r)}px solid #3730a3;">
          <div style="position:absolute;inset:0;background:repeating-linear-gradient(-45deg,transparent 0px,transparent 6px,rgba(0,0,0,.07) 6px,rgba(0,0,0,.07) 12px);"></div>
          <div style="width:${54*r}px;height:${54*r}px;border-radius:50%;border:${Math.max(1,2*r)}px dashed rgba(199,210,254,.5);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:${4*r}px;position:relative;z-index:1;">
            <div style="width:${13*r}px;height:${13*r}px;border-radius:50%;background:#c7d2fe;box-shadow:0 0 ${6*r}px rgba(199,210,254,.6);"></div>
            <div style="width:${10*r}px;height:${22*r}px;background:#c7d2fe;border-radius:${2*r}px;box-shadow:0 0 ${6*r}px rgba(199,210,254,.6);"></div>
          </div>
        </div>
        <div style="display:flex;flex-direction:column;align-items:flex-start;justify-content:center;padding:${10*r}px ${24*r}px ${10*r}px ${18*r}px;gap:0;position:relative;z-index:1;">
          <div style="display:flex;align-items:center;gap:${8*r}px;margin-bottom:${1*r}px;">
            <span style="font-family:'Oswald',sans-serif;font-size:${8*r}px;font-weight:700;letter-spacing:${4*r}px;color:#4338ca;text-transform:uppercase;white-space:nowrap;">Resume Analyzer</span>
            <div style="width:${32*r}px;height:${Math.max(1,r)}px;background:rgba(67,56,202,.4);"></div>
          </div>
          <div style="font-family:'Pirata One',serif;font-size:${66*r}px;color:#1e1b4b;line-height:.9;letter-spacing:${1*r}px;text-shadow:${1*r}px ${1*r}px 0 rgba(49,46,129,.18);white-space:nowrap;">iLuffy</div>
        </div>
      </div>`
  }

  // Render logos
  renderLogo(document.getElementById('nav-logo'), 48)
  renderLogo(document.getElementById('footer-logo'), 36)

  /* ── Dark mode toggle ──────────────────────────────────────────── */
  const html = document.documentElement
  const themeBtn = document.getElementById('theme-btn')
  const sunIcon = document.getElementById('icon-sun')
  const moonIcon = document.getElementById('icon-moon')
  const reportCard = document.getElementById('report-card')

  function setDark(on) {
    html.classList.toggle('dark', on)
    sunIcon.classList.toggle('hidden', !on)
    moonIcon.classList.toggle('hidden', on)
    // Update report card outer border colors
    if (reportCard) {
      reportCard.style.background = on ? '#1f2937' : '#d4d4da'
      reportCard.style.borderColor = on ? '#374151' : '#808088'
    }
    localStorage.setItem('theme', on ? 'dark' : 'light')
  }

  // Init from localStorage or system preference
  const stored = localStorage.getItem('theme')
  if (stored === 'dark' || (!stored && window.matchMedia('(prefers-color-scheme:dark)').matches)) {
    setDark(true)
  }

  themeBtn.addEventListener('click', () => setDark(!html.classList.contains('dark')))

  /* ── Scroll handler: navbar shrink + back-to-top + scrollspy + parallax ── */
  const nav = document.getElementById('main-nav')
  const heroOrb = document.getElementById('hero-orb')
  const backToTop = document.getElementById('back-to-top')
  const navLinks = document.querySelectorAll('.nav-link')
  let activeSection = ''

  function onScroll() {
    const y = window.scrollY
    // Nav shrink
    nav.style.height = y > 20 ? '56px' : '72px'

    // Navbar logo resize
    const navLogo = document.getElementById('nav-logo')
    if (navLogo && navLogo.firstElementChild) {
      const newSize = y > 20 ? 38 : 48
      renderLogo(navLogo, newSize)
    }

    // Back-to-top
    backToTop.classList.toggle('hidden', y <= 600)

    // Parallax
    if (heroOrb) heroOrb.style.transform = `translate(-50%, ${y * 0.25}px)`

    // Scrollspy
    const ids = ['faq', 'pricing', 'intelligence', 'process']
    let found = ''
    for (const id of ids) {
      const el = document.getElementById(id)
      if (el && el.getBoundingClientRect().top <= 140) { found = id; break }
    }
    if (found !== activeSection) {
      activeSection = found
      navLinks.forEach((link) => {
        const isActive = link.dataset.section === activeSection
        link.classList.toggle('text-indigo-600', isActive)
        link.classList.toggle('dark:text-indigo-400', isActive)
        link.classList.toggle('text-gray-600', !isActive)
        link.classList.toggle('dark:text-gray-400', !isActive)
      })
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true })
  backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }))

  /* ── Mobile menu ───────────────────────────────────────────────── */
  const hamburgerBtn = document.getElementById('hamburger-btn')
  const hamburgerOpen = document.getElementById('hamburger-open')
  const hamburgerClose = document.getElementById('hamburger-close')
  const mobileMenu = document.getElementById('mobile-menu')

  hamburgerBtn.addEventListener('click', () => {
    const isOpen = !mobileMenu.classList.contains('hidden')
    mobileMenu.classList.toggle('hidden', isOpen)
    hamburgerOpen.classList.toggle('hidden', !isOpen)
    hamburgerClose.classList.toggle('hidden', isOpen)
    hamburgerBtn.setAttribute('aria-expanded', String(!isOpen))
  })

  // Close mobile menu on link click
  document.querySelectorAll('.mobile-link').forEach((link) => {
    link.addEventListener('click', () => {
      mobileMenu.classList.add('hidden')
      hamburgerOpen.classList.remove('hidden')
      hamburgerClose.classList.add('hidden')
    })
  })

  // Close on resize
  window.addEventListener('resize', () => {
    mobileMenu.classList.add('hidden')
    hamburgerOpen.classList.remove('hidden')
    hamburgerClose.classList.add('hidden')
  })

  /* ── Report card mouse tilt ────────────────────────────────────── */
  if (reportCard) {
    reportCard.addEventListener('mousemove', (e) => {
      const rect = reportCard.getBoundingClientRect()
      const x = (e.clientX - rect.left) / rect.width - 0.5
      const y = (e.clientY - rect.top) / rect.height - 0.5
      reportCard.style.transition = 'none'
      reportCard.style.transform = `perspective(1000px) rotateY(${x * 8}deg) rotateX(${-y * 8}deg)`
    })
    reportCard.addEventListener('mouseleave', () => {
      reportCard.style.transition = 'transform 0.5s ease-out'
      reportCard.style.transform = 'perspective(1000px) rotateY(0deg) rotateX(0deg)'
    })
  }

  /* ── Trend chart ───────────────────────────────────────────────── */
  const trend = [45, 52, 61, 58, 72, 78, 85, 82, 88, 92]
  const chart = document.getElementById('trend-chart')
  if (chart) {
    trend.forEach((v) => {
      const col = document.createElement('div')
      col.className = 'flex-1 flex flex-col items-center justify-end h-full'
      const label = document.createElement('span')
      label.className = 'text-[10px] text-gray-400 dark:text-gray-500 mb-1'
      label.textContent = v
      const bar = document.createElement('div')
      const color = v >= 75 ? 'bg-green-500' : v >= 50 ? 'bg-amber-500' : 'bg-red-400'
      bar.className = `w-full rounded-t transition-all ${color}`
      bar.style.height = `${v}%`
      col.appendChild(label)
      col.appendChild(bar)
      chart.appendChild(col)
    })
  }

  /* ── FAQ accordion ─────────────────────────────────────────────── */
  const FAQS = [
    { q: 'HOW DOES THE AI SIMULATE ATS SCORING?', a: 'Our engine utilizes Large Language Models trained on parsing logic from Workday, Greenhouse, and Lever. It evaluates keyword density, semantic relevance, and formatting compatibility simultaneously.' },
    { q: 'WHAT IS THE IMPACT REWRITING ENGINE?', a: "It's an AI-driven text optimizer that identifies passive job descriptions and converts them into quantified achievements using recruiter-preferred action verbs and metrics." },
    { q: 'HOW IS MY PERSONAL DATA PROTECTED?', a: 'We use industry-standard encryption for all data handling. Your resume is processed in an isolated sandbox and is never used to train public models. Your data remains private and you can delete it at any time.' },
    { q: 'DOES IT WORK FOR ALL INDUSTRIES?', a: 'Yes. From Tech and Finance to Creative and Healthcare, our AI adapts its scoring parameters based on the industry-specific job description you provide.' },
    { q: 'WHAT FILE FORMATS DO YOU SUPPORT?', a: 'Currently we support PDF resumes. PDF is the most widely accepted format by ATS systems and preserves your formatting consistently across platforms.' },
    { q: 'CAN I ANALYZE AGAINST MULTIPLE JOBS?', a: 'Yes! Save job descriptions in your Jobs library and run unlimited analyses against any combination of resumes and positions. The Compare feature lets you view results side-by-side.' },
  ]

  const faqList = document.getElementById('faq-list')
  let openFaq = null

  if (faqList) {
    FAQS.forEach((faq, i) => {
      const wrapper = document.createElement('div')
      wrapper.className = 'border rounded-xl overflow-hidden transition-all bg-cream border-gray-100 dark:bg-graphite dark:border-slate-700/60'

      const btn = document.createElement('button')
      btn.className = 'w-full flex items-center justify-between px-5 py-4 text-left hover:bg-mist-50 dark:hover:bg-charcoal/50 transition-colors group'
      btn.innerHTML = `
        <span class="text-sm font-semibold text-gray-900 dark:text-white pr-4">${faq.q}</span>
        <span class="faq-icon text-gray-400 flex-shrink-0 transition-transform duration-300">
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" /></svg>
        </span>`

      const content = document.createElement('div')
      content.className = 'overflow-hidden transition-all duration-300 ease-in-out'
      content.style.maxHeight = '0px'
      content.style.opacity = '0'
      content.innerHTML = `<p class="px-5 sm:px-6 pb-5 sm:pb-6 pt-4 text-sm leading-relaxed border-t text-gray-600 border-mist-200 dark:text-gray-400 dark:border-gray-800">${faq.a}</p>`

      btn.addEventListener('click', () => {
        const isOpen = openFaq === i
        // Close all
        faqList.querySelectorAll('.faq-content').forEach((c) => { c.style.maxHeight = '0px'; c.style.opacity = '0' })
        faqList.querySelectorAll('.faq-icon').forEach((ic) => ic.style.transform = '')
        if (!isOpen) {
          content.style.maxHeight = '300px'
          content.style.opacity = '1'
          btn.querySelector('.faq-icon').style.transform = 'rotate(45deg)'
          openFaq = i
        } else {
          openFaq = null
        }
      })

      content.classList.add('faq-content')
      wrapper.appendChild(btn)
      wrapper.appendChild(content)
      faqList.appendChild(wrapper)
    })
  }

  /* ── Contact form (demo — shows alert) ─────────────────────────── */
  const contactForm = document.getElementById('contact-form')
  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault()
      const name = e.target.name.value.trim()
      const email = e.target.email.value.trim()
      const subject = e.target.subject.value.trim()
      const message = e.target.message.value.trim()
      if (!name || !email || !subject || !message) {
        alert('Please fill in all fields.')
        return
      }
      alert("Message sent! We'll get back to you shortly.")
      e.target.reset()
    })
  }

  /* ── Billing toggle (Monthly / Annual) ─────────────────────────── */
  const btnMonthly = document.getElementById('billing-monthly')
  const btnAnnual  = document.getElementById('billing-annual')

  if (btnMonthly && btnAnnual) {
    const monthlyPrices = document.querySelectorAll('.price-monthly')
    const annualPrices  = document.querySelectorAll('.price-annual')

    const activeClasses   = ['bg-indigo-600', 'text-white', 'shadow-md']
    const inactiveClasses = ['text-gray-500', 'dark:text-gray-400', 'bg-transparent']

    function resetBtn(btn) {
      activeClasses.forEach(c => btn.classList.remove(c))
      inactiveClasses.forEach(c => btn.classList.remove(c))
    }

    function showMonthly() {
      resetBtn(btnMonthly); resetBtn(btnAnnual)
      activeClasses.forEach(c => btnMonthly.classList.add(c))
      inactiveClasses.forEach(c => btnAnnual.classList.add(c))
      monthlyPrices.forEach(el => el.classList.remove('hidden'))
      annualPrices.forEach(el => el.classList.add('hidden'))
    }

    function showAnnual() {
      resetBtn(btnMonthly); resetBtn(btnAnnual)
      activeClasses.forEach(c => btnAnnual.classList.add(c))
      inactiveClasses.forEach(c => btnMonthly.classList.add(c))
      annualPrices.forEach(el => el.classList.remove('hidden'))
      monthlyPrices.forEach(el => el.classList.add('hidden'))
    }

    btnMonthly.addEventListener('click', showMonthly)
    btnAnnual.addEventListener('click', showAnnual)

    // Default state: monthly visible
    showMonthly()
  }

})()
