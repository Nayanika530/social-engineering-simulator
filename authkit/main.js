/**
 * AUTHKIT BY WORKOS - JAVASCRIPT INTERACTIONS & ENGINE
 * Provides interactive starfield canvases, 3D card perspective tilt,
 * theme toggle, brand customizer controls, and dynamic security simulations.
 */

document.addEventListener('DOMContentLoaded', () => {
  initAmbientCanvases();
  initHeroCardSwitcher();
  initThemeSwitch();
  initBrandCustomizer();
  initFeatureTimeline();
  initSecuritySimulations();
});

/* ==========================================================================
   1. AMBIENT STARFIELD & STARDUST CANVAS ANIMATION
   ========================================================================== */
function initAmbientCanvases() {
  const canvases = document.querySelectorAll('.ambient-canvas');
  canvases.forEach(canvas => {
    const ctx = canvas.getContext('2d');
    let width = canvas.width = canvas.parentElement.offsetWidth;
    let height = canvas.height = canvas.parentElement.offsetHeight;

    window.addEventListener('resize', () => {
      width = canvas.width = canvas.parentElement.offsetWidth;
      height = canvas.height = canvas.parentElement.offsetHeight;
    });

    const particles = [];
    const count = Math.floor((width * height) / 8000);

    for (let i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        radius: Math.random() * 1.2 + 0.3,
        alpha: Math.random() * 0.6 + 0.15,
        speedX: (Math.random() - 0.5) * 0.2,
        speedY: (Math.random() - 0.5) * 0.2
      });
    }

    function render() {
      ctx.clearRect(0, 0, width, height);

      particles.forEach(p => {
        p.x += p.speedX;
        p.y += p.speedY;

        if (p.x < 0) p.x = width;
        if (p.x > width) p.x = 0;
        if (p.y < 0) p.y = height;
        if (p.y > height) p.y = 0;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(186, 215, 247, ${p.alpha})`;
        ctx.fill();
      });

      requestAnimationFrame(render);
    }
    render();
  });
}

/* ==========================================================================
   2. HERO 3D CARD SHOWCASE & TILT
   ========================================================================== */
function initHeroCardSwitcher() {
  const stage = document.querySelector('.hero-cards-stage');
  if (!stage) return;

  const cards = Array.from(stage.querySelectorAll('.auth-card'));

  cards.forEach(card => {
    card.addEventListener('click', () => {
      if (card.classList.contains('card-center')) return;

      const currentCenter = stage.querySelector('.card-center');
      const clickedPos = card.classList.contains('card-left') ? 'left' : 'right';

      if (clickedPos === 'left') {
        currentCenter.classList.replace('card-center', 'card-right');
        card.classList.replace('card-left', 'card-center');
        const remaining = stage.querySelector('.card-right:not([data-prev-center])');
        if (remaining && remaining !== currentCenter) {
          remaining.classList.replace('card-right', 'card-left');
        }
      } else {
        currentCenter.classList.replace('card-center', 'card-left');
        card.classList.replace('card-right', 'card-center');
        const remaining = stage.querySelector('.card-left:not([data-prev-center])');
        if (remaining && remaining !== currentCenter) {
          remaining.classList.replace('card-left', 'card-right');
        }
      }

      cards.forEach(c => {
        c.classList.remove('auth-card-animated');
      });
      card.classList.add('auth-card-animated');
    });
  });

  // Dynamic 3D mouse tracking on center card
  stage.addEventListener('mousemove', (e) => {
    const centerCard = stage.querySelector('.card-center');
    if (!centerCard) return;

    const rect = centerCard.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;

    const rotateX = -(y / rect.height) * 12;
    const rotateY = (x / rect.width) * 12;

    centerCard.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
  });

  stage.addEventListener('mouseleave', () => {
    const centerCard = stage.querySelector('.card-center');
    if (!centerCard) return;
    centerCard.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale(1)';
  });
}

/* ==========================================================================
   3. LIGHT / DARK THEME TOGGLE SWITCH
   ========================================================================== */
function initThemeSwitch() {
  const switchBtn = document.getElementById('themeSwitch');
  const cardsStage = document.querySelector('.hero-cards-stage');
  if (!switchBtn || !cardsStage) return;

  switchBtn.addEventListener('click', () => {
    const isLight = switchBtn.classList.toggle('active-light');
    if (isLight) {
      cardsStage.classList.add('cards-light-mode');
    } else {
      cardsStage.classList.remove('cards-light-mode');
    }
  });
}

/* ==========================================================================
   4. INTERACTIVE BRAND CUSTOMIZER ("SHINE BRIGHT")
   ========================================================================== */
function initBrandCustomizer() {
  const previewCard = document.getElementById('customizerPreviewCard');
  if (!previewCard) return;

  // 1. Color Picker
  const swatches = document.querySelectorAll('.color-swatch');
  swatches.forEach(swatch => {
    swatch.addEventListener('click', () => {
      swatches.forEach(s => s.classList.remove('active'));
      swatch.classList.add('active');

      const color = swatch.dataset.color;
      previewCard.style.setProperty('--brand-color', color);
      const btn = previewCard.querySelector('.btn-primary');
      if (btn) btn.style.backgroundColor = color;
    });
  });

  // 2. Logo Picker
  const logoChoices = document.querySelectorAll('.logo-choice');
  const previewLogoContainer = document.getElementById('previewCardLogo');
  logoChoices.forEach(choice => {
    choice.addEventListener('click', () => {
      logoChoices.forEach(c => c.classList.remove('active'));
      choice.classList.add('active');

      if (previewLogoContainer) {
        previewLogoContainer.innerHTML = choice.innerHTML;
      }
    });
  });

  // 3. Radius Picker
  const radiusBtns = document.querySelectorAll('.radius-btn');
  radiusBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      radiusBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const radius = btn.dataset.radius;
      previewCard.style.setProperty('--brand-radius', radius);
      
      const inputs = previewCard.querySelectorAll('.form-input, .btn-primary, .btn-outline');
      inputs.forEach(el => el.style.borderRadius = radius);
    });
  });

  // 4. Appearance Mode (System, Light, Dark)
  const appearancePills = document.querySelectorAll('.appearance-pill');
  appearancePills.forEach(pill => {
    pill.addEventListener('click', () => {
      appearancePills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');

      const mode = pill.dataset.mode;
      if (mode === 'light') {
        previewCard.style.backgroundColor = '#ffffff';
        previewCard.style.color = '#05060f';
        previewCard.querySelectorAll('.form-label').forEach(l => l.style.color = '#334155');
        previewCard.querySelectorAll('.form-input').forEach(i => {
          i.style.backgroundColor = '#f8fafc';
          i.style.borderColor = '#e2e8f0';
          i.style.color = '#0f172a';
        });
        const outlineBtn = previewCard.querySelector('.btn-outline');
        if (outlineBtn) {
          outlineBtn.style.backgroundColor = '#f8fafc';
          outlineBtn.style.borderColor = '#e2e8f0';
          outlineBtn.style.color = '#1e293b';
        }
      } else {
        previewCard.style.backgroundColor = 'rgba(5, 6, 15, 0.95)';
        previewCard.style.color = '#ffffff';
        previewCard.querySelectorAll('.form-label').forEach(l => l.style.color = 'var(--body-loud)');
        previewCard.querySelectorAll('.form-input').forEach(i => {
          i.style.backgroundColor = 'rgba(199, 211, 234, 0.06)';
          i.style.borderColor = 'rgba(186, 215, 247, 0.15)';
          i.style.color = '#fff';
        });
        const outlineBtn = previewCard.querySelector('.btn-outline');
        if (outlineBtn) {
          outlineBtn.style.backgroundColor = 'rgba(186, 214, 247, 0.04)';
          outlineBtn.style.borderColor = 'rgba(186, 215, 247, 0.15)';
          outlineBtn.style.color = '#d1e4fa';
        }
      }
    });
  });
}

/* ==========================================================================
   5. FEATURE TIMELINE STEPPER
   ========================================================================== */
function initFeatureTimeline() {
  const items = document.querySelectorAll('.feature-slider-item');
  if (!items.length) return;

  let current = 0;
  setInterval(() => {
    items.forEach(it => it.classList.remove('active'));
    items[current].classList.add('active');
    
    const sep = items[current].querySelector('.feature-separator');
    if (sep) {
      sep.classList.add('pulse');
      setTimeout(() => sep.classList.remove('pulse'), 1800);
    }

    current = (current + 1) % items.length;
  }, 2200);
}

/* ==========================================================================
   6. SECURITY SIMULATIONS (PASSWORD STRENGTH, OTP, SCANNER)
   ========================================================================== */
function initSecuritySimulations() {
  // Animated Password strength ticker
  const pwdText = document.getElementById('simPwdText');
  const bars = document.querySelectorAll('.strength-bar');

  if (pwdText && bars.length) {
    const passwords = [
      { text: '123456', level: 1, color: '#ef4444' },
      { text: 'correcthorse', level: 2, color: '#f59e0b' },
      { text: '9#XmK!99_vLz', level: 4, color: '#10b981' }
    ];
    let idx = 0;

    setInterval(() => {
      const current = passwords[idx];
      pwdText.textContent = current.text;

      bars.forEach((bar, i) => {
        if (i < current.level) {
          bar.style.backgroundColor = current.color;
          bar.style.boxShadow = `0 0 8px ${current.color}`;
        } else {
          bar.style.backgroundColor = 'rgba(186, 215, 247, 0.15)';
          bar.style.boxShadow = 'none';
        }
      });

      idx = (idx + 1) % passwords.length;
    }, 2500);
  }

  // MFA Dots sequence animation
  const mfaDots = document.querySelectorAll('.mfa-dot');
  if (mfaDots.length) {
    let filled = 0;
    setInterval(() => {
      filled = (filled + 1) % (mfaDots.length + 2);
      mfaDots.forEach((dot, i) => {
        if (i < filled && filled <= mfaDots.length) {
          dot.style.opacity = '1';
          dot.style.transform = 'scale(1.3)';
        } else {
          dot.style.opacity = '0.2';
          dot.style.transform = 'scale(1)';
        }
      });
    }, 600);
  }
}
