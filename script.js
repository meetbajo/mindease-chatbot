/* ============================================================
   MindEase — Mental Health Chatbot PoC Script
   ============================================================ */

'use strict';

// ── Navigation ────────────────────────────────────────────────
const navItems = document.querySelectorAll('.nav-item');
const tabPanels = document.querySelectorAll('.tab-panel');

function switchTab(tabId) {
  navItems.forEach(n => n.classList.toggle('active', n.dataset.tab === tabId));
  tabPanels.forEach(p => p.classList.toggle('active', p.id === `tab-${tabId}`));
}

navItems.forEach(item => {
  item.addEventListener('click', () => switchTab(item.dataset.tab));
});

document.getElementById('go-to-chat').addEventListener('click', () => switchTab('chat'));

// ── Mood Quick Picker ──────────────────────────────────────────
const moodBtns = document.querySelectorAll('.mood-emoji');
let todayMood = null;

moodBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    moodBtns.forEach(b => b.classList.remove('selected'));
    btn.classList.add('selected');
    todayMood = parseInt(btn.dataset.mood);
    logMood(todayMood);
    // Acknowledge in chat
    const moodLabel = ['', 'very sad', 'a bit sad', 'okay', 'good', 'great'][todayMood];
    addBotMessage(`I see you're feeling ${moodLabel} today 💜 That's completely valid. I'm here if you want to talk about it.`);
    switchTab('chat');
  });
});

// ── Chat ──────────────────────────────────────────────────────
const chatMessages = document.getElementById('chat-messages');
const chatInput    = document.getElementById('chat-input');
const sendBtn      = document.getElementById('send-btn');
const typingIndicator = document.getElementById('typing-indicator');

function getTime() {
  return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function addMessage(text, role) {
  const msgDiv = document.createElement('div');
  msgDiv.className = `message ${role}`;

  const avatar = document.createElement('div');
  avatar.className = 'msg-avatar';
  avatar.textContent = role === 'bot' ? '🤍' : 'U';

  const bubble = document.createElement('div');
  bubble.className = 'msg-bubble';
  bubble.innerHTML = text.replace(/\n/g, '<br>');

  const time = document.createElement('div');
  time.className = 'msg-time';
  time.textContent = getTime();

  const wrap = document.createElement('div');
  wrap.style.display = 'flex';
  wrap.style.flexDirection = 'column';
  wrap.appendChild(bubble);
  wrap.appendChild(time);

  if (role === 'bot') {
    msgDiv.appendChild(avatar);
    msgDiv.appendChild(wrap);
  } else {
    msgDiv.appendChild(wrap);
    msgDiv.appendChild(avatar);
  }

  chatMessages.appendChild(msgDiv);
  chatMessages.scrollTo({ top: chatMessages.scrollHeight, behavior: 'smooth' });
}

function addBotMessage(text) {
  typingIndicator.classList.remove('hidden');
  chatMessages.scrollTo({ top: chatMessages.scrollHeight, behavior: 'smooth' });
  setTimeout(() => {
    typingIndicator.classList.add('hidden');
    addMessage(text, 'bot');
  }, 1200 + Math.random() * 800);
}

function sendMessage() {
  const text = chatInput.value.trim();
  if (!text) return;
  addMessage(text, 'user');
  chatInput.value = '';
  chatInput.style.height = 'auto';
  const reply = getBotReply(text.toLowerCase());
  addBotMessage(reply);
}

sendBtn.addEventListener('click', sendMessage);

chatInput.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

chatInput.addEventListener('input', () => {
  chatInput.style.height = 'auto';
  chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + 'px';
});

// Quick prompts
document.querySelectorAll('.quick-prompt').forEach(btn => {
  btn.addEventListener('click', () => {
    chatInput.value = btn.dataset.prompt;
    sendMessage();
  });
});

// Clear chat
document.getElementById('clear-chat-btn').addEventListener('click', () => {
  chatMessages.innerHTML = '';
  setTimeout(() => {
    addMessage("Hi again! 💜 I'm Elara, your mental wellness companion. What's on your mind today?", 'bot');
  }, 300);
});

// ── Chatbot Responses ─────────────────────────────────────────
const responses = [
  {
    patterns: ['hello', 'hi ', 'hey', 'greet', 'good morning', 'good evening', 'good afternoon'],
    replies: [
      "Hello! 💜 I'm Elara, your mental wellness companion. How are you feeling today? Remember, this is a safe space to share anything.",
      "Hi there! 😊 I'm so glad you're here. What's on your heart today?",
      "Hey! 🌟 Welcome to MindEase. I'm here to listen and support you. How are you doing right now?"
    ]
  },
  {
    patterns: ['anxious', 'anxiety', 'worry', 'worried', 'nervous', 'panic', 'panic attack', 'overthink'],
    replies: [
      "I hear you — anxiety can feel really overwhelming. 💜\n\nLet's try something together right now:\n\n🫁 **Box Breathing** — inhale for 4 counts → hold for 4 → exhale for 4 → hold for 4. Repeat 3–4 times.\n\nThis activates your parasympathetic nervous system and calms the stress response within minutes. Do you want to try it?",
      "Anxiety is incredibly common and you are not alone in feeling this. 🤝\n\nOne thing that really helps is the **5-4-3-2-1 grounding technique**: name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste. This brings your mind back to the present moment.\n\nWould you like to tell me more about what's making you feel anxious?",
      "I understand the weight of anxiety. 💫 Your feelings are completely valid.\n\nSome science-backed strategies:\n• 🧘 Deep diaphragmatic breathing\n• ✍️ Writing down your worries (journaling)\n• 🚶 A brisk 10-minute walk\n• 📵 Digital detox for 30 minutes\n\nWhat feels most do-able for you right now?"
    ]
  },
  {
    patterns: ['stress', 'stressed', 'overwhelm', 'overwhelmed', 'pressure', 'burnout', 'exhausted'],
    replies: [
      "It sounds like you're carrying a really heavy load right now. 💜 Stress and overwhelm are signals that your mind and body need care.\n\nHere's a simple reset:\n1. **Stop** — pause everything for 2 minutes\n2. **Breathe** — slow, deep breaths\n3. **List** — write the top 3 priorities only\n4. **Release** — let go of everything else for now\n\nYou don't have to do everything at once. What's the single most stressful thing right now?",
      "Feeling overwhelmed is so hard. 🌊 Let's break it down together.\n\n**The STOP technique:**\n• S — Stop what you're doing\n• T — Take a deep breath\n• O — Observe your thoughts without judgment\n• P — Proceed with intention\n\nRemember: you can only do one thing at a time, and that's okay. 💪"
    ]
  },
  {
    patterns: ['depress', 'sad', 'unhappy', 'hopeless', 'empty', 'numb', 'meaningless', 'worthless'],
    replies: [
      "Thank you for trusting me with something so personal. 💜 Depression and deep sadness are real and valid. You're not weak for feeling this way.\n\nSome gentle steps that can help:\n• 🌅 Morning sunlight (even 5 minutes)\n• 🚶 A short walk — movement releases endorphins\n• 📞 Reaching out to one person you trust\n• ✅ Completing one small task to build momentum\n\nPlease know that you don't have to face this alone. Are there any professional mental health services available to you?",
      "I'm really glad you shared that with me. 🤍 Feeling this way is not a personal failure — it's something many people experience and it can get better.\n\nRight now, try one tiny act of self-care:\n• Make yourself a warm drink 🍵\n• Step outside for fresh air 🌿\n• Text someone you trust 💬\n\nI'm also here to listen whenever you need. Would you like to talk more about what's been happening?"
    ]
  },
  {
    patterns: ['sleep', 'insomnia', 'can\'t sleep', "can't sleep", 'sleep problem', 'tired', 'fatigue'],
    replies: [
      "Poor sleep can really worsen mental health. 😴 Here's proven sleep hygiene advice:\n\n🌙 **Wind-Down Routine:**\n• Stop screens 60 minutes before bed\n• Keep room cool and dark\n• Try the 4-7-8 breathing method\n• Write a short 'worry dump' in a journal\n\n⏰ **Consistency is key** — wake at the same time daily, even weekends.\n\nIs your sleep issue falling asleep, staying asleep, or waking too early?",
      "Sleep difficulties are very connected to mental health. 💤\n\n**Try this tonight:**\nThe Military Sleep Method — relax your face muscles, drop your shoulders, breathe out slowly, clear your mind for 10 seconds. Most people fall asleep within 2 minutes with practice.\n\nWhat do you think is keeping you awake?"
    ]
  },
  {
    patterns: ['lonely', 'alone', 'no friends', 'isolated', 'no one cares', 'nobody'],
    replies: [
      "Loneliness is one of the most painful feelings there is. 💔 Please know that your feelings matter deeply — even if it doesn't feel that way right now.\n\nYou reached out here, and that takes courage. 🌟\n\nSmall steps to connection:\n• 📱 Send one text to an old friend today\n• 🌐 Join an online community around an interest\n• 🤝 Volunteer locally — shared purpose builds bonds\n• 📖 A library, café, or class puts you around others gently\n\nI'm also here to listen. What's your life like right now — what's a typical day?",
      "I hear you. 💜 Feeling alone is incredibly hard, and your longing for connection is so human and valid.\n\nWould you like to talk about what's been going on? Sometimes just being heard helps. I'm not going anywhere. 🕊️"
    ]
  },
  {
    patterns: ['breath', 'breathing', 'calm down', 'calm me', 'relax', 'relaxation', 'meditat'],
    replies: [
      "Let's do a breathing exercise together right now. 🫁\n\n**4-7-8 Technique:**\n1. Inhale quietly through your nose for **4 seconds**\n2. Hold your breath for **7 seconds**\n3. Exhale completely through your mouth for **8 seconds**\n4. Repeat 4 cycles\n\nThis is like a natural tranquilizer for your nervous system. Begin now — I'll be here when you're done. 🕊️\n\nAlternatively, head to the **Resources** tab to use our interactive breathing guide!",
      "Here's the **Box Breathing** technique used by Navy SEALs to stay calm under pressure:\n\n⬜ Inhale 4 → Hold 4 → Exhale 4 → Hold 4\n\nVisualize tracing the four sides of a box as you breathe. Do 4 rounds and let me know how you feel. 💜"
    ]
  },
  {
    patterns: ['crisis', 'emergency', 'suicid', 'self-harm', 'hurt myself', 'end it', 'give up', 'no reason to live'],
    replies: [
      "⚠️ I'm really concerned about you right now and I want you to be safe.\n\n**Please reach out immediately:**\n🇮🇳 iCall (India): 9152987821\n📞 Vandrevala Foundation: 1860-266-2345\n🌍 International: befrienders.org\n\nYou deserve support from a trained professional right now. Please go to the **Crisis Help** tab or call one of these numbers. 💜\n\nYour life has value. I care about you."
    ]
  },
  {
    patterns: ['thank', 'thanks', 'helpful', 'better', 'good job', 'appreciate'],
    replies: [
      "You're so welcome! 💜 I'm really glad I could help even a little. Remember, taking care of your mental health is one of the most important things you can do. 🌟\n\nIs there anything else on your mind?",
      "It means a lot to hear that! Keep going — you're doing something brave by taking care of your mental health. 🌿\n\nI'm always here whenever you need to talk.",
      "Aww, thank you! 🤍 You're doing great by reaching out and being self-aware. That's the first step to healing. Take care of yourself today! 💜"
    ]
  },
  {
    patterns: ['tip', 'advice', 'help me', 'what should i do', 'what can i do', 'suggest'],
    replies: [
      "Here are some evidence-based mental wellness tips for today: 💡\n\n🏃 **Move** — 20 min of exercise reduces anxiety by 48%\n📓 **Journal** — 3 minutes of gratitude journaling rewires your brain\n📵 **Unplug** — Social media detox for 1 hour improves mood\n💤 **Sleep** — 7-8 hours is non-negotiable for mental health\n🌿 **Nature** — 15 minutes outside lowers cortisol levels\n🤝 **Connect** — One meaningful conversation per day\n\nWhat area would you like to focus on most?",
      "I'd love to help! Here are personalized tips depending on what you need:\n\n• Feeling anxious → Try the 5-4-3-2-1 grounding method\n• Feeling sad → Behavioral activation: do one enjoyable thing\n• Feeling stressed → Break tasks into 10-minute chunks\n• Feeling lonely → Reach out to one person today\n• Feeling tired → Prioritize sleep and light movement\n\nWhich of these resonates with you?"
    ]
  }
];

function getBotReply(input) {
  for (const r of responses) {
    if (r.patterns.some(p => input.includes(p))) {
      return r.replies[Math.floor(Math.random() * r.replies.length)];
    }
  }
  // Default empathetic replies
  const defaults = [
    "Thank you for sharing that with me. 💜 It takes courage to talk about how you're feeling. Can you tell me a bit more about what you're going through?",
    "I hear you. 🤍 Your feelings are completely valid. Let's explore this together — what would feel most helpful right now?",
    "I'm here and I'm listening. 💫 You don't have to figure this out alone. Would you like some coping strategies, or do you just want to talk?",
    "That sounds really tough. 💙 I want to make sure you get the right support. Is this something that's been going on for a while, or did something happen recently?",
    "Thank you for opening up. 🌸 Mental health is just as important as physical health. What's weighing on your mind most right now?"
  ];
  return defaults[Math.floor(Math.random() * defaults.length)];
}

// ── Initial Welcome Message ────────────────────────────────────
window.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    addMessage(
      "Hello! I'm <strong>Elara</strong> 💜 — your AI mental wellness companion.\n\nThis is a safe, confidential space for you to share what's on your mind. I'm here to listen, provide guidance, and connect you with resources.\n\n<em>How are you feeling today?</em> You can also use the quick buttons below or tap an emoji in the sidebar.",
      'bot'
    );
    initMoodChart();
    initMoodLog();
    initBreathing();
    initJournal();
    initMindfulness();
  }, 400);
});

// ── Mood Chart (Canvas) ───────────────────────────────────────
const moodData = [
  { day: 'Mon', score: 2 },
  { day: 'Tue', score: 3 },
  { day: 'Wed', score: 4 },
  { day: 'Thu', score: 5 },
  { day: 'Fri', score: 3 },
  { day: 'Sat', score: 4 },
  { day: 'Sun', score: 3.5 }
];

function initMoodChart() {
  const canvas = document.getElementById('mood-chart');
  const ctx = canvas.getContext('2d');

  const W = canvas.offsetWidth || 600;
  const H = 200;
  canvas.width = W;
  canvas.height = H;

  const pad = { top: 20, bottom: 40, left: 30, right: 20 };
  const pw = W - pad.left - pad.right;
  const ph = H - pad.top - pad.bottom;

  // Background grid
  ctx.strokeStyle = 'rgba(255,255,255,0.06)';
  ctx.lineWidth = 1;
  for (let i = 0; i <= 5; i++) {
    const y = pad.top + ph - (i / 5) * ph;
    ctx.beginPath();
    ctx.moveTo(pad.left, y);
    ctx.lineTo(W - pad.right, y);
    ctx.stroke();
  }

  // Gradient fill under curve
  const grad = ctx.createLinearGradient(0, pad.top, 0, H - pad.bottom);
  grad.addColorStop(0, 'rgba(124, 106, 247, 0.35)');
  grad.addColorStop(1, 'rgba(124, 106, 247, 0.01)');

  const pts = moodData.map((d, i) => ({
    x: pad.left + (i / (moodData.length - 1)) * pw,
    y: pad.top + ph - ((d.score - 1) / 4) * ph
  }));

  // Draw fill
  ctx.beginPath();
  ctx.moveTo(pts[0].x, H - pad.bottom);
  pts.forEach(p => ctx.lineTo(p.x, p.y));
  ctx.lineTo(pts[pts.length - 1].x, H - pad.bottom);
  ctx.closePath();
  ctx.fillStyle = grad;
  ctx.fill();

  // Draw curve
  ctx.beginPath();
  ctx.moveTo(pts[0].x, pts[0].y);
  for (let i = 1; i < pts.length; i++) {
    const cp1x = (pts[i - 1].x + pts[i].x) / 2;
    const cp1y = pts[i - 1].y;
    const cp2x = (pts[i - 1].x + pts[i].x) / 2;
    const cp2y = pts[i].y;
    ctx.bezierCurveTo(cp1x, cp1y, cp2x, cp2y, pts[i].x, pts[i].y);
  }
  ctx.strokeStyle = '#7c6af7';
  ctx.lineWidth = 2.5;
  ctx.stroke();

  // Points + labels
  pts.forEach((p, i) => {
    ctx.beginPath();
    ctx.arc(p.x, p.y, 5, 0, Math.PI * 2);
    ctx.fillStyle = '#a89cf8';
    ctx.fill();
    ctx.strokeStyle = '#0d0d1a';
    ctx.lineWidth = 2;
    ctx.stroke();

    ctx.fillStyle = 'rgba(240,238,255,0.6)';
    ctx.font = '11px Inter';
    ctx.textAlign = 'center';
    ctx.fillText(moodData[i].day, p.x, H - pad.bottom + 15);

    const emojis = ['', '😢', '😕', '😐', '🙂', '😄'];
    ctx.font = '13px serif';
    ctx.fillText(emojis[Math.round(moodData[i].score)] || '😐', p.x, p.y - 10);
  });
}

function initMoodLog() {
  const logList = document.getElementById('mood-log-list');
  const emojis = ['', '😢', '😕', '😐', '🙂', '😄'];
  const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

  moodData.forEach((d, i) => {
    const entry = document.createElement('div');
    entry.className = 'mood-log-entry';
    const pct = ((d.score - 1) / 4) * 100;
    entry.innerHTML = `
      <span class="log-day">${days[i]}</span>
      <div class="log-bar-wrap"><div class="log-bar" style="width:${pct}%"></div></div>
      <span class="log-emoji">${emojis[Math.round(d.score)]}</span>
    `;
    logList.appendChild(entry);
  });
}

// ── Mood Local Storage ────────────────────────────────────────
function logMood(score) {
  const logs = JSON.parse(localStorage.getItem('moodLogs') || '[]');
  logs.push({ date: new Date().toISOString(), score });
  localStorage.setItem('moodLogs', JSON.stringify(logs.slice(-30)));
}

// ── Breathing Exercise ─────────────────────────────────────────
function initBreathing() {
  const circle = document.getElementById('breath-circle');
  const phase  = document.getElementById('breath-phase');
  let running  = false;
  let timeout  = null;

  const sequence = [
    { label: 'Inhale…',   duration: 4000, action: 'expand' },
    { label: 'Hold…',     duration: 4000, action: null     },
    { label: 'Exhale…',   duration: 4000, action: 'contract' },
    { label: 'Hold…',     duration: 4000, action: null     }
  ];

  let step = 0;

  function runStep() {
    if (!running) return;
    const s = sequence[step % sequence.length];
    phase.textContent = s.label;
    circle.textContent = s.label;
    circle.className = 'breath-circle';
    if (s.action) {
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          circle.classList.add(s.action);
        });
      });
    }
    step++;
    timeout = setTimeout(runStep, s.duration);
  }

  circle.addEventListener('click', () => {
    running = !running;
    if (running) {
      step = 0;
      runStep();
    } else {
      clearTimeout(timeout);
      circle.textContent = 'Tap to Start';
      circle.className = 'breath-circle';
      phase.textContent = '';
    }
  });
}

// ── Journal Prompts ────────────────────────────────────────────
const journalPrompts = [
  "What is one thing you are grateful for today, no matter how small?",
  "Describe a moment this week when you felt genuinely at peace.",
  "What emotion are you carrying right now, and where do you feel it in your body?",
  "What is one thing you would tell your younger self about getting through hard times?",
  "List three personal strengths that have helped you overcome challenges.",
  "What does your ideal day for mental wellbeing look like?",
  "Write about a time you were proud of yourself for being resilient.",
  "What boundaries do you need to set to protect your mental energy?",
  "If your anxiety could speak, what would it say? What would you say back?",
  "What brings you joy that you haven't done in a while? Can you do it today?",
  "Describe someone in your life who makes you feel safe and valued.",
  "What negative thought pattern do you want to release this week?"
];

let promptIndex = Math.floor(Math.random() * journalPrompts.length);

function initJournal() {
  const promptEl = document.getElementById('journal-prompt');
  promptEl.textContent = `"${journalPrompts[promptIndex]}"`;

  document.getElementById('new-prompt-btn').addEventListener('click', () => {
    promptIndex = (promptIndex + 1) % journalPrompts.length;
    promptEl.style.opacity = '0';
    promptEl.style.transform = 'translateY(5px)';
    setTimeout(() => {
      promptEl.textContent = `"${journalPrompts[promptIndex]}"`;
      promptEl.style.transition = 'opacity 0.4s, transform 0.4s';
      promptEl.style.opacity = '1';
      promptEl.style.transform = 'translateY(0)';
    }, 300);
  });
}

// ── Mindfulness Technique Tabs ─────────────────────────────────
const techniques = {
  '54321': {
    btn: document.getElementById('tech-54321'),
    content: `<strong>The 5-4-3-2-1 Grounding Technique</strong><br/><br/>This pulls your mind out of rumination and into the present moment:<br/>
    🟣 Name <strong>5</strong> things you can see right now<br/>
    🔵 Name <strong>4</strong> things you can physically feel<br/>
    🟢 Name <strong>3</strong> things you can hear<br/>
    🟡 Name <strong>2</strong> things you can smell<br/>
    🔴 Name <strong>1</strong> thing you can taste<br/><br/>Repeat whenever you feel overwhelmed.`
  },
  'bodyscan': {
    btn: document.getElementById('tech-bodyscan'),
    content: `<strong>Body Scan Meditation</strong><br/><br/>Lie or sit comfortably. Close your eyes.<br/><br/>
    Starting at the top of your head, slowly scan your body downward — notice any tension, tightness, or discomfort without judgment.<br/><br/>
    Breathe into each area and consciously relax it before moving on. 
    Take 10–15 minutes for a full scan.<br/><br/>This connects mind and body and reduces chronic stress.`
  },
  'visualize': {
    btn: document.getElementById('tech-visualize'),
    content: `<strong>Safe Place Visualization</strong><br/><br/>Close your eyes and imagine a place where you feel completely safe and at peace — a beach, forest, childhood bedroom, or anywhere real or imagined.<br/><br/>
    Engage all your senses: What do you see? Hear? Smell? Feel?<br/><br/>
    Spend 5 minutes here. This calms the amygdala (your brain's threat center) and activates the rest-and-digest system.`
  }
};

function initMindfulness() {
  const contentEl = document.getElementById('technique-content');
  Object.entries(techniques).forEach(([key, tech]) => {
    tech.btn.addEventListener('click', () => {
      Object.values(techniques).forEach(t => t.btn.classList.remove('active'));
      tech.btn.classList.add('active');
      contentEl.style.opacity = '0';
      setTimeout(() => {
        contentEl.innerHTML = tech.content;
        contentEl.style.transition = 'opacity 0.3s';
        contentEl.style.opacity = '1';
      }, 250);
    });
  });

  // Set initial
  contentEl.innerHTML = techniques['54321'].content;
}
