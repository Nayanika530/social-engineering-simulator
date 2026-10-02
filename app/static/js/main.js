/**
 * AUTHKIT-INSPIRED JAVASCRIPT ENGINE FOR SOCIAL ENGINEERING SIMULATOR
 * Powers ambient stardust canvas, 3D card tilt & stage switching,
 * theme toggle, live attack simulation, threat classification, and interactive widgets.
 */

document.addEventListener('DOMContentLoaded', () => {
  initAmbientCanvases();
  initHeroCardSwitcher();
  initThemeSwitch();
  initFeatureTimeline();
  initCodeTabs();
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
    const count = Math.min(Math.floor((width * height) / 9000), 120);

    for (let i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        radius: Math.random() * 1.2 + 0.3,
        alpha: Math.random() * 0.55 + 0.15,
        speedX: (Math.random() - 0.5) * 0.25,
        speedY: (Math.random() - 0.5) * 0.25
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
    card.addEventListener('click', (e) => {
      // If user clicked inside an input, button, or textarea, don't swap card
      if (['INPUT', 'TEXTAREA', 'BUTTON', 'A'].includes(e.target.tagName)) return;

      if (card.classList.contains('card-center')) return;

      const currentCenter = stage.querySelector('.card-center');
      const clickedLeft = card.classList.contains('card-left');

      if (clickedLeft) {
        currentCenter.classList.replace('card-center', 'card-right');
        currentCenter.classList.remove('auth-card-animated');
        card.classList.replace('card-left', 'card-center');
        card.classList.add('auth-card-animated');

        const remaining = stage.querySelector('.card-right:not([data-active])');
        const otherRight = cards.find(c => c !== currentCenter && c.classList.contains('card-right'));
        if (otherRight) {
          otherRight.classList.replace('card-right', 'card-left');
        }
      } else {
        currentCenter.classList.replace('card-center', 'card-left');
        currentCenter.classList.remove('auth-card-animated');
        card.classList.replace('card-right', 'card-center');
        card.classList.add('auth-card-animated');

        const otherLeft = cards.find(c => c !== currentCenter && c.classList.contains('card-left'));
        if (otherLeft) {
          otherLeft.classList.replace('card-left', 'card-right');
        }
      }
    });

    // 3D Perspective Tilt on Hover for center card
    card.addEventListener('mousemove', (e) => {
      if (!card.classList.contains('card-center')) return;
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;

      const tiltX = (y / (rect.height / 2)) * -6;
      const tiltY = (x / (rect.width / 2)) * 6;

      card.style.transform = `perspective(1000px) rotateX(${tiltX}deg) rotateY(${tiltY}deg) translateZ(10px)`;
    });

    card.addEventListener('mouseleave', () => {
      if (card.classList.contains('card-center')) {
        card.style.transform = 'translateX(0) scale(1) translateZ(0)';
      }
    });
  });
}

/* ==========================================================================
   3. LIGHT / DARK THEME TOGGLE
   ========================================================================== */
function initThemeSwitch() {
  const switcher = document.getElementById('themeSwitch');
  if (!switcher) return;

  const savedTheme = localStorage.getItem('seng-theme');
  if (savedTheme === 'light') {
    document.body.classList.add('light-theme');
    switcher.classList.add('active-light');
  }

  switcher.addEventListener('click', () => {
    const isLight = document.body.classList.toggle('light-theme');
    switcher.classList.toggle('active-light', isLight);
    localStorage.setItem('seng-theme', isLight ? 'light' : 'dark');
  });
}

/* ==========================================================================
   4. FEATURES TIMELINE STEPPER
   ========================================================================== */
const timelineData = [
  {
    title: "1. Persona & Scenario Config",
    desc: "Attack parameters configured dynamically: attacker impersonates trusted departmental entities (e.g. IT, HR, Finance) and tailors target role context."
  },
  {
    title: "2. GPT-2 Language Generator",
    desc: "Fine-tuned on 5,594 real phishing emails to craft convincing, contextually accurate spearphishing messages matching attacker psychological levers."
  },
  {
    title: "3. TF-IDF N-Gram Vectorizer",
    desc: "Extracts sub-word lexical patterns and n-gram vectors across 17,537 training vocabulary items to map subtle semantic markers."
  },
  {
    title: "4. Logistic Regression Classifier",
    desc: "Evaluates transformed sparse vector weights with 97.75% held-out test accuracy, balancing high precision against deceptive linguistic tactics."
  },
  {
    title: "5. Real-Time Threat Score",
    desc: "Produces calibrated threat probability (<200ms latency), categorizing the email as High-Risk Phishing or Legitimate Communication with confidence rating."
  }
];

function initFeatureTimeline() {
  const items = document.querySelectorAll('.feature-slider-item');
  const descBox = document.getElementById('timelineDesc');

  items.forEach((item, index) => {
    item.addEventListener('click', () => {
      items.forEach(i => i.classList.remove('active'));
      item.classList.add('active');
      if (descBox && timelineData[index]) {
        descBox.innerHTML = `<strong>${timelineData[index].title}</strong> — ${timelineData[index].desc}`;
      }
    });
  });
}

/* ==========================================================================
   5. CODE INTEGRATION TABS
   ========================================================================== */
const codeSnippets = {
  python: `import requests

# Simulate social engineering attack payload
response = requests.post("http://localhost:5000/generate_attack", json={
    "scenario": "IT password reset",
    "target_role": "Finance Manager",
    "company": "Acme Corp"
})

result = response.json()
print("Threat Level:", result["threat_level"])
print("Confidence:", result["confidence"], "%")
print("Generated Payload:\\n", result["generated_email"])`,

  curl: `curl -X POST https://social-engineering-simulator-opt1.onrender.com/generate_attack \\
  -H "Content-Type: application/json" \\
  -d '{
    "scenario": "Urgent Wire Transfer",
    "target_role": "Finance Director",
    "company": "Global Retail Inc"
  }'`,

  javascript: `// Test live classification in browser or Node.js
const res = await fetch('/generate_attack', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    scenario: 'Cloud SSO Access Revocation',
    target_role: 'DevOps Lead',
    company: 'FinTech Dynamics'
  })
});

const data = await res.json();
console.log(\`[\${data.threat_level}] \${data.confidence}%\`);`,

  sklearn: `# Underlying Scikit-Learn Model Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

vectorizer = joblib.load("models/classifier_vectorizer.pkl")
classifier = joblib.load("models/classifier_model.pkl")

email_vec = vectorizer.transform([email_text])
prediction = classifier.predict(email_vec)[0]  # 1 = Phishing, 0 = Safe
proba = classifier.predict_proba(email_vec)[0]`
};

function initCodeTabs() {
  const tabs = document.querySelectorAll('.code-tab');
  const codePre = document.getElementById('codeDisplay');
  const copyBtn = document.getElementById('copyCodeBtn');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const lang = tab.getAttribute('data-lang');
      if (codePre && codeSnippets[lang]) {
        codePre.textContent = codeSnippets[lang];
      }
    });
  });

  if (copyBtn && codePre) {
    copyBtn.addEventListener('click', () => {
      navigator.clipboard.writeText(codePre.textContent).then(() => {
        copyBtn.innerHTML = `<span>Copied!</span>`;
        setTimeout(() => {
          copyBtn.innerHTML = `
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
            <span>Copy Code</span>`;
        }, 2000);
      });
    });
  }
}

/* ==========================================================================
   6. ATTACK SIMULATION & CLASSIFIER LOGIC
   ========================================================================== */
function applyPreset(scenario, role, company) {
  const scenarioInput = document.getElementById("scenario");
  const roleInput = document.getElementById("target_role");
  const companyInput = document.getElementById("company");

  if (scenarioInput) scenarioInput.value = scenario;
  if (roleInput) roleInput.value = role;
  if (companyInput) companyInput.value = company;

  // Ensure center card is active
  const centerCard = document.querySelector('.card-center');
  const simCard = document.getElementById('simCard');
  if (simCard && !simCard.classList.contains('card-center')) {
    simCard.click();
  }

  generateAttack();
}

// Generate Attack API Call
async function generateAttack() {
  const scenario = document.getElementById("scenario").value.trim() || "IT password reset";
  const target_role = document.getElementById("target_role").value.trim() || "Finance Manager";
  const company = document.getElementById("company").value.trim() || "Acme Corp";

  const btn = document.getElementById("btnGenerate");
  const spinner = document.getElementById("simSpinner");
  if (btn) btn.disabled = true;
  if (spinner) spinner.style.display = "inline-block";

  try {
    const response = await fetch("/generate_attack", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ scenario, target_role, company })
    });

    if (!response.ok) {
      throw new Error("Server returned status " + response.status);
    }

    const data = await response.json();
    renderResults(data, scenario, target_role, company);
  } catch (err) {
    alert("Error simulating attack: " + err.message + "\nIf backend is starting up, please allow a moment.");
  } finally {
    if (btn) btn.disabled = false;
    if (spinner) spinner.style.display = "none";
  }
}

// Classify Custom Text API Call
async function classifyCustomText() {
  const emailText = document.getElementById("customEmailText").value.trim();
  if (!emailText) {
    alert("Please paste email text to classify.");
    return;
  }

  const btn = document.getElementById("btnClassify");
  const spinner = document.getElementById("classifySpinner");
  if (btn) btn.disabled = true;
  if (spinner) spinner.style.display = "inline-block";

  try {
    const response = await fetch("/classify_text", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email_text: emailText })
    });

    if (!response.ok) {
      throw new Error("Server returned status " + response.status);
    }

    const data = await response.json();
    renderResults(data, "Raw Custom Payload Analysis", "Direct Recipient", "Enterprise Gateway");
  } catch (err) {
    alert("Error classifying email: " + err.message);
  } finally {
    if (btn) btn.disabled = false;
    if (spinner) spinner.style.display = "none";
  }
}

// Render Results Modal / Card
function renderResults(data, scenario, target_role, company) {
  const resultSection = document.getElementById("resultSection");
  const statusBadge = document.getElementById("statusBadge");
  const threatStatusText = document.getElementById("threatStatusText");
  const confidenceBar = document.getElementById("confidenceBar");
  const confidenceVal = document.getElementById("confidenceVal");
  const emailContent = document.getElementById("emailContent");
  const metaRecipient = document.getElementById("metaRecipient");
  const metaSubject = document.getElementById("metaSubject");
  const vectorName = document.getElementById("vectorName");
  const profileRole = document.getElementById("profileRole");
  const profileCompany = document.getElementById("profileCompany");

  const isPhishing = data.threat_level === "Phishing";

  if (isPhishing) {
    statusBadge.className = "report-status-badge badge-phishing";
    threatStatusText.textContent = "High-Risk Spearphishing Threat";
    confidenceBar.style.backgroundColor = "#ef4444";
  } else {
    statusBadge.className = "report-status-badge badge-safe";
    threatStatusText.textContent = "Legitimate / Safe Communication";
    confidenceBar.style.backgroundColor = "#10b981";
  }

  const conf = data.confidence || 95.0;
  confidenceBar.style.width = conf + "%";
  confidenceVal.textContent = conf + "%";

  metaRecipient.textContent = `${target_role} <${target_role.toLowerCase().replace(/\s+/g, '.')}@${company.toLowerCase().replace(/\s+/g, '')}.com>`;
  metaSubject.textContent = `Urgent Notice: ${scenario} - ${company}`;
  emailContent.textContent = data.generated_email;

  vectorName.textContent = scenario;
  profileRole.textContent = target_role;
  profileCompany.textContent = company;

  resultSection.style.display = "block";
  resultSection.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

// Copy Email Content
function copyEmailContent() {
  const text = document.getElementById("emailContent").textContent;
  navigator.clipboard.writeText(text).then(() => {
    const btnText = document.getElementById("copyBtnText");
    btnText.textContent = "Copied!";
    setTimeout(() => { btnText.textContent = "Copy Email"; }, 2000);
  });
}

// Dismiss Results
function dismissResult() {
  document.getElementById("resultSection").style.display = "none";
}
