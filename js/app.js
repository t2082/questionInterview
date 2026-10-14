/**
 * FLUTTER INTERVIEW PRO - MASTER APPLICATION SCRIPT
 * Full-featured study platform with Flashcards, Search Explorer, Quiz & HR Tools
 */

(function () {
  'use strict';

  // --- AUDIO SYNTHESIS ENGINE (Web Audio API) ---
  class SoundFX {
    constructor() {
      this.enabled = true;
      this.ctx = null;
    }
    init() {
      if (!this.ctx) {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (AudioCtx) this.ctx = new AudioCtx();
      }
    }
    playTone(freq, type = 'sine', duration = 0.12, volume = 0.08) {
      if (!this.enabled) return;
      try {
        this.init();
        if (!this.ctx) return;
        if (this.ctx.state === 'suspended') this.ctx.resume();
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
        gain.gain.setValueAtTime(volume, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + duration);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start();
        osc.stop(this.ctx.currentTime + duration);
      } catch (e) {
        // Audio muted or not allowed
      }
    }
    flip() { this.playTone(320, 'sine', 0.08, 0.04); }
    correct() {
      this.playTone(523.25, 'triangle', 0.1, 0.06);
      setTimeout(() => this.playTone(659.25, 'triangle', 0.15, 0.06), 80);
    }
    hard() { this.playTone(220, 'sawtooth', 0.15, 0.04); }
    complete() {
      [523.25, 659.25, 783.99, 1046.5].forEach((freq, i) => {
        setTimeout(() => this.playTone(freq, 'triangle', 0.2, 0.08), i * 110);
      });
    }
  }

  // --- LIGHTWEIGHT EMBEDDED MARKDOWN RENDERER ---
  function renderMarkdown(md) {
    if (!md) return '';
    let html = md;

    // Normalize Windows line breaks
    html = html.replace(/\r\n/g, '\n');

    // Code Blocks: ```lang ... ```
    html = html.replace(/```([a-zA-Z0-9_-]*)\n([\s\S]*?)```/g, function (match, lang, code) {
      const escaped = code.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
      return `<pre><code class="language-${lang || 'dart'}">${escaped}</code></pre>`;
    });

    // Inline Code: `...`
    html = html.replace(/`([^`]+)`/g, function (match, code) {
      const escaped = code.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
      return `<code>${escaped}</code>`;
    });

    // Headers
    html = html.replace(/^#### (.*$)/gim, '<h4>$1</h4>');
    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');

    // Bold & Italic
    html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/__([^_]+)__/g, '<strong>$1</strong>');
    html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    html = html.replace(/_([^_]+)_/g, '<em>$1</em>');

    // Blockquotes
    html = html.replace(/^\> (.*$)/gim, '<blockquote>$1</blockquote>');

    // Links [text](url)
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');

    // Unordered lists
    html = html.replace(/^\s*[\*\-]\s+(.*$)/gim, '<ul><li>$1</li></ul>');
    html = html.replace(/<\/ul>\s*<ul>/g, '');

    // Ordered lists
    html = html.replace(/^\s*\d+\.\s+(.*$)/gim, '<ol><li>$1</li></ol>');
    html = html.replace(/<\/ol>\s*<ol>/g, '');

    // Paragraphs & double line breaks
    const blocks = html.split(/\n{2,}/);
    html = blocks.map(b => {
      b = b.trim();
      if (!b) return '';
      if (/^<(h[1-6]|pre|ul|ol|blockquote)/.test(b)) return b;
      return `<p>${b.replace(/\n/g, '<br>')}</p>`;
    }).join('\n');

    return html;
  }

  // --- APP STATE ---
  const state = {
    allQuestions: [],
    flashcardList: [],
    currentCardIndex: 0,
    isFlipped: false,
    currentDeck: 'all', // 'all', 'hard', 'mastered', 'bookmarked'

    // Persistence
    bookmarkedIds: new Set(JSON.parse(localStorage.getItem('flutter_bookmarks') || '[]')),
    masteredIds: new Set(JSON.parse(localStorage.getItem('flutter_mastered') || '[]')),
    hardIds: new Set(JSON.parse(localStorage.getItem('flutter_hard') || '[]')),
    theme: localStorage.getItem('flutter_theme') || 'dark',

    // Explorer Filter State
    filters: {
      search: '',
      category: 'all',
      level: 'all',
      lang: 'all',
      status: 'all'
    },

    // Quiz State
    quiz: {
      questions: [],
      currentIndex: 0,
      score: 0,
      total: 10,
      timerSec: 0,
      timerInterval: null,
      isAnswerShown: false
    }
  };

  const sound = new SoundFX();

  // --- TOAST NOTIFICATION HELPER ---
  let toastTimer = null;
  function showToast(msg) {
    const el = document.getElementById('toast-notification');
    if (!el) return;
    el.textContent = msg;
    el.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      el.classList.remove('show');
    }, 2200);
  }

  // --- LOCAL STORAGE & LOCAL DATABASE (IndexedDB) HELPERS ---
  function saveState(actionPayload) {
    // 1. Dual-Sync: Synchronous LocalStorage Cache
    localStorage.setItem('flutter_bookmarks', JSON.stringify([...state.bookmarkedIds]));
    localStorage.setItem('flutter_mastered', JSON.stringify([...state.masteredIds]));
    localStorage.setItem('flutter_hard', JSON.stringify([...state.hardIds]));
    updateStatsCounter();

    // 2. Dual-Sync: Persistent Local Database (IndexedDB)
    if (window.appDB && window.appDB.isReady) {
      if (actionPayload) {
        if (actionPayload.type === 'status' && actionPayload.id) {
          window.appDB.saveQuestionStatus(actionPayload.id, actionPayload.status);
        } else if (actionPayload.type === 'bookmark' && actionPayload.id) {
          window.appDB.saveBookmark(actionPayload.id, actionPayload.isBookmarked);
        }
      }
      window.appDB.saveSetting('app_state', {
        theme: state.theme,
        currentDeck: state.currentDeck,
        currentCardIndex: state.currentCardIndex
      });
    }
  }

  function updateStatsCounter() {
    const total = state.allQuestions.length;
    const mastered = state.masteredIds.size;
    const hard = state.hardIds.size;
    const bookmarked = state.bookmarkedIds.size;

    // Header badge
    const el = document.getElementById('stat-mastery-text');
    if (el) el.textContent = `✅ ${mastered} • ❌ ${hard}`;

    // Deck Tab Counts
    const cAll = document.getElementById('count-deck-all');
    if (cAll) cAll.textContent = total;

    const cHard = document.getElementById('count-deck-hard');
    if (cHard) cHard.textContent = hard;

    const cMastered = document.getElementById('count-deck-mastered');
    if (cMastered) cMastered.textContent = mastered;

    const cBookmarked = document.getElementById('count-deck-bookmarked');
    if (cBookmarked) cBookmarked.textContent = bookmarked;

    // Modal stats
    const mMastered = document.getElementById('db-stat-mastered');
    if (mMastered) mMastered.textContent = mastered;

    const mHard = document.getElementById('db-stat-hard');
    if (mHard) mHard.textContent = hard;

    const mBookmarks = document.getElementById('db-stat-bookmarks');
    if (mBookmarks) mBookmarks.textContent = bookmarked;
  }

  // --- INITIALIZATION ---
  window.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Theme
    document.documentElement.setAttribute('data-theme', state.theme);
    updateThemeIcon();

    // 2. Load Questions Dataset
    if (window.FLUTTER_QUESTIONS && window.FLUTTER_QUESTIONS.length > 0) {
      state.allQuestions = window.FLUTTER_QUESTIONS;
      initApp();
    } else {
      // Fallback: Fetch questions.json
      fetch('data/questions.json')
        .then(res => res.json())
        .then(data => {
          state.allQuestions = data;
          initApp();
        })
        .catch(err => {
          console.error('Error loading questions:', err);
          document.getElementById('card-q-title').textContent = 'Lỗi tải dữ liệu. Hãy đảm bảo tệp data/questions.js tồn tại.';
        });
    }
  });

  async function initApp() {
    state.flashcardList = [...state.allQuestions];

    // Connect & Sync with IndexedDB Local Database
    if (window.appDB) {
      try {
        await window.appDB.init();
        const statuses = await window.appDB.getAllQuestionStatuses();
        statuses.forEach(s => {
          if (s.status === 'mastered') {
            state.masteredIds.add(s.id);
            state.hardIds.delete(s.id);
          } else if (s.status === 'hard') {
            state.hardIds.add(s.id);
            state.masteredIds.delete(s.id);
          }
        });
        const bms = await window.appDB.getAllBookmarks();
        bms.forEach(id => state.bookmarkedIds.add(id));
      } catch (err) {
        console.warn('[App] LocalDB initial sync warning:', err);
      }
    }

    setupEventListeners();
    setupCategoryPills();
    updateStatsCounter();
    renderFlashcard();
    renderExplorer();
    renderHRTools();
  }

  // --- THEME TOGGLE ---
  function updateThemeIcon() {
    const icon = document.getElementById('theme-toggle-icon');
    if (icon) {
      icon.textContent = state.theme === 'dark' ? '🌙' : '☀️';
    }
  }

  function toggleTheme() {
    state.theme = state.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', state.theme);
    localStorage.setItem('flutter_theme', state.theme);
    updateThemeIcon();
  }

  // --- EVENT LISTENERS ---
  function setupEventListeners() {
    // Mode Switcher Tabs
    document.querySelectorAll('.nav-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        const mode = tab.dataset.mode;
        switchMode(mode);
      });
    });

    // Theme Toggle
    const themeBtn = document.getElementById('btn-toggle-theme');
    if (themeBtn) themeBtn.addEventListener('click', toggleTheme);

    // Audio Toggle
    const audioBtn = document.getElementById('btn-toggle-audio');
    if (audioBtn) {
      audioBtn.addEventListener('click', () => {
        sound.enabled = !sound.enabled;
        audioBtn.classList.toggle('active', sound.enabled);
        audioBtn.title = sound.enabled ? 'Tắt âm thanh' : 'Bật âm thanh';
        audioBtn.textContent = sound.enabled ? '🔊' : '🔇';
      });
    }

    // Flashcard Interactions with Touch Swipe for Mobile
    const flipCard = document.getElementById('flip-card-wrapper');
    if (flipCard) {
      let touchStartX = 0;
      let touchStartY = 0;
      let touchStartTime = 0;
      let didSwipe = false;

      flipCard.addEventListener('touchstart', (e) => {
        if (e.touches.length === 1) {
          touchStartX = e.touches[0].clientX;
          touchStartY = e.touches[0].clientY;
          touchStartTime = Date.now();
          didSwipe = false;
        }
      }, { passive: true });

      flipCard.addEventListener('touchend', (e) => {
        if (e.changedTouches.length === 1) {
          const deltaX = e.changedTouches[0].clientX - touchStartX;
          const deltaY = e.changedTouches[0].clientY - touchStartY;
          const deltaTime = Date.now() - touchStartTime;

          // If horizontal swipe (> 45px distance, primarily horizontal, under 500ms)
          if (Math.abs(deltaX) > 45 && Math.abs(deltaX) > Math.abs(deltaY) * 1.3 && deltaTime < 500) {
            didSwipe = true;
            if (deltaX < 0) {
              // Swipe Left -> Next Card
              nextCard();
            } else {
              // Swipe Right -> Prev Card
              prevCard();
            }
          }
        }
      }, { passive: true });

      flipCard.addEventListener('click', (e) => {
        // If it was a swipe gesture, ignore the click
        if (didSwipe) {
          didSwipe = false;
          return;
        }
        // Prevent flipping if clicked on links, buttons, or scrollbars
        if (e.target.closest('a') || e.target.closest('button')) return;
        toggleFlipCard();
      });
    }

    document.getElementById('btn-prev-card')?.addEventListener('click', prevCard);
    document.getElementById('btn-next-card')?.addEventListener('click', nextCard);
    document.getElementById('btn-flip-card')?.addEventListener('click', toggleFlipCard);
    document.getElementById('btn-shuffle-cards')?.addEventListener('click', shuffleCards);

    // Deck Tab Switcher Listeners
    document.querySelectorAll('.deck-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        setDeck(tab.dataset.deck);
      });
    });

    // Clicking header stats badge opens flashcards
    document.getElementById('stat-mastery-text')?.parentElement?.addEventListener('click', () => {
      switchMode('flashcards');
    });

    document.getElementById('btn-card-hard')?.addEventListener('click', () => {
      sound.hard();
      const q = getCurrentCard();
      if (q) {
        state.hardIds.add(q.id);
        state.masteredIds.delete(q.id);
        saveState({ type: 'status', id: q.id, status: 'hard' });
        showToast(`❌ Đã thêm vào danh sách Chưa thuộc (${state.hardIds.size} câu)`);

        // If currently studying 'mastered' deck, remove from current deck list
        if (state.currentDeck === 'mastered') {
          state.flashcardList = state.flashcardList.filter(item => item.id !== q.id);
          if (state.currentCardIndex >= state.flashcardList.length) {
            state.currentCardIndex = Math.max(0, state.flashcardList.length - 1);
          }
          state.isFlipped = false;
          renderFlashcard();
        } else {
          nextCard();
        }
      }
    });

    document.getElementById('btn-card-easy')?.addEventListener('click', () => {
      sound.correct();
      const q = getCurrentCard();
      if (q) {
        state.masteredIds.add(q.id);
        state.hardIds.delete(q.id);
        saveState({ type: 'status', id: q.id, status: 'mastered' });
        showToast(`✅ Đã thêm vào danh sách Đã thuộc (${state.masteredIds.size} câu)`);

        // If currently studying 'hard' deck, remove from current deck list so backlog clears!
        if (state.currentDeck === 'hard') {
          state.flashcardList = state.flashcardList.filter(item => item.id !== q.id);
          if (state.currentCardIndex >= state.flashcardList.length) {
            state.currentCardIndex = Math.max(0, state.flashcardList.length - 1);
          }
          state.isFlipped = false;
          renderFlashcard();
        } else {
          nextCard();
        }
      }
    });

    document.getElementById('btn-card-bookmark')?.addEventListener('click', (e) => {
      e.stopPropagation();
      toggleCardBookmark();
    });

    // Copy Prompt Buttons on Flashcards
    document.getElementById('btn-card-copy-front')?.addEventListener('click', (e) => {
      e.stopPropagation();
      copyPromptForCurrentCard();
    });
    document.getElementById('btn-card-copy-back')?.addEventListener('click', (e) => {
      e.stopPropagation();
      copyPromptForCurrentCard();
    });

    // Local Database Modal Listeners
    const dbModal = document.getElementById('modal-db-manager');
    document.getElementById('btn-open-db-modal')?.addEventListener('click', openDatabaseModal);
    document.getElementById('btn-close-db-modal')?.addEventListener('click', closeDatabaseModal);
    if (dbModal) {
      dbModal.addEventListener('click', (e) => {
        if (e.target === dbModal) closeDatabaseModal();
      });
    }
    document.getElementById('btn-db-export')?.addEventListener('click', exportDatabaseBackup);
    document.getElementById('input-db-import-file')?.addEventListener('change', importDatabaseBackup);
    document.getElementById('btn-db-reset')?.addEventListener('click', resetLocalDatabase);

    // Card Jump Input
    const jumpInput = document.getElementById('card-jump-input');
    if (jumpInput) {
      jumpInput.addEventListener('change', () => {
        let val = parseInt(jumpInput.value, 10);
        if (isNaN(val)) val = 1;
        val = Math.max(1, Math.min(val, state.flashcardList.length));
        state.currentCardIndex = val - 1;
        state.isFlipped = false;
        renderFlashcard();
      });
    }

    // Explorer Filter Listeners
    const searchInput = document.getElementById('explorer-search-input');
    if (searchInput) {
      let debounceTimer = null;
      searchInput.addEventListener('input', () => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
          state.filters.search = searchInput.value.trim().toLowerCase();
          renderExplorer();
        }, 180);
      });
    }

    document.getElementById('filter-level')?.addEventListener('change', (e) => {
      state.filters.level = e.target.value;
      renderExplorer();
    });

    document.getElementById('filter-lang')?.addEventListener('change', (e) => {
      state.filters.lang = e.target.value;
      renderExplorer();
    });

    document.getElementById('filter-status')?.addEventListener('change', (e) => {
      state.filters.status = e.target.value;
      renderExplorer();
    });

    document.getElementById('btn-expand-all')?.addEventListener('click', () => {
      document.querySelectorAll('.question-accordion-card').forEach(c => c.classList.add('open'));
    });

    document.getElementById('btn-collapse-all')?.addEventListener('click', () => {
      document.querySelectorAll('.question-accordion-card').forEach(c => c.classList.remove('open'));
    });

    // Quiz Mode Listeners
    document.getElementById('btn-start-quiz')?.addEventListener('click', startQuiz);
    document.getElementById('btn-quiz-show-answer')?.addEventListener('click', toggleQuizAnswer);
    document.getElementById('btn-quiz-next')?.addEventListener('click', nextQuizQuestion);

    document.getElementById('btn-rate-0')?.addEventListener('click', () => recordQuizAnswer(0));
    document.getElementById('btn-rate-50')?.addEventListener('click', () => recordQuizAnswer(50));
    document.getElementById('btn-rate-100')?.addEventListener('click', () => recordQuizAnswer(100));
    document.getElementById('btn-quiz-restart')?.addEventListener('click', restartQuiz);

    // Global Keyboard Shortcuts
    document.addEventListener('keydown', (e) => {
      const activeSection = document.querySelector('.view-section.active');
      if (activeSection && activeSection.id === 'section-flashcards') {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

        if (e.code === 'Space') {
          e.preventDefault();
          toggleFlipCard();
        } else if (e.code === 'ArrowRight' || e.code === 'Enter') {
          e.preventDefault();
          nextCard();
        } else if (e.code === 'ArrowLeft') {
          e.preventDefault();
          prevCard();
        } else if (e.key === '1') {
          document.getElementById('btn-card-hard')?.click();
        } else if (e.key === '2') {
          document.getElementById('btn-card-easy')?.click();
        } else if (e.key === 'b' || e.key === 'B') {
          toggleCardBookmark();
        } else if (e.key === 'c' || e.key === 'C') {
          copyPromptForCurrentCard();
        }
      }
    });
  }

  // --- NAVIGATION MODE SWITCHING ---
  function switchMode(mode) {
    document.querySelectorAll('.nav-tab').forEach(t => {
      t.classList.toggle('active', t.dataset.mode === mode);
    });
    document.querySelectorAll('.view-section').forEach(sec => {
      sec.classList.toggle('active', sec.id === `section-${mode}`);
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });

    if (mode === 'explorer') {
      renderExplorer();
    }
  }

  // --- FLASHCARD ENGINE ---
  function getCurrentCard() {
    if (state.flashcardList.length === 0) return null;
    return state.flashcardList[state.currentCardIndex];
  }

  function toggleFlipCard() {
    state.isFlipped = !state.isFlipped;
    sound.flip();
    const inner = document.getElementById('flip-card-inner');
    if (inner) inner.classList.toggle('is-flipped', state.isFlipped);
  }

  function nextCard() {
    if (state.flashcardList.length === 0) return;
    state.currentCardIndex = (state.currentCardIndex + 1) % state.flashcardList.length;
    state.isFlipped = false;
    sound.flip();
    renderFlashcard();
  }

  function prevCard() {
    if (state.flashcardList.length === 0) return;
    state.currentCardIndex = (state.currentCardIndex - 1 + state.flashcardList.length) % state.flashcardList.length;
    state.isFlipped = false;
    sound.flip();
    renderFlashcard();
  }

  function shuffleCards() {
    sound.flip();
    for (let i = state.flashcardList.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [state.flashcardList[i], state.flashcardList[j]] = [state.flashcardList[j], state.flashcardList[i]];
    }
    state.currentCardIndex = 0;
    state.isFlipped = false;
    renderFlashcard();
  }

  function toggleCardBookmark() {
    const q = getCurrentCard();
    if (!q) return;
    const isNowBookmarked = !state.bookmarkedIds.has(q.id);
    if (isNowBookmarked) {
      state.bookmarkedIds.add(q.id);
    } else {
      state.bookmarkedIds.delete(q.id);
    }
    saveState({ type: 'bookmark', id: q.id, isBookmarked: isNowBookmarked });
    renderBookmarkIcon();
  }

  function renderBookmarkIcon() {
    const q = getCurrentCard();
    const btn = document.getElementById('btn-card-bookmark');
    if (!q || !btn) return;
    const isBookmarked = state.bookmarkedIds.has(q.id);
    btn.classList.toggle('bookmarked', isBookmarked);
    btn.textContent = isBookmarked ? '★' : '☆';
    btn.title = isBookmarked ? 'Bỏ lưu câu hỏi' : 'Lưu câu hỏi yêu thích';
  }

  function setDeck(deckName) {
    state.currentDeck = deckName;
    document.querySelectorAll('.deck-tab').forEach(tab => {
      tab.classList.toggle('active', tab.dataset.deck === deckName);
    });

    if (deckName === 'hard') {
      state.flashcardList = state.allQuestions.filter(q => state.hardIds.has(q.id));
    } else if (deckName === 'mastered') {
      state.flashcardList = state.allQuestions.filter(q => state.masteredIds.has(q.id));
    } else if (deckName === 'bookmarked') {
      state.flashcardList = state.allQuestions.filter(q => state.bookmarkedIds.has(q.id));
    } else {
      state.flashcardList = [...state.allQuestions];
    }

    state.currentCardIndex = 0;
    state.isFlipped = false;
    renderFlashcard();
  }

  function renderFlashcard() {
    const total = state.flashcardList.length;
    const currentNum = total > 0 ? state.currentCardIndex + 1 : 0;
    const q = getCurrentCard();

    // Progress
    const pct = total > 0 ? (currentNum / total) * 100 : 0;
    const fill = document.getElementById('card-progress-fill');
    if (fill) fill.style.width = `${pct}%`;

    const progText = document.getElementById('card-progress-text');
    if (progText) {
      const deckLabel = state.currentDeck === 'hard' ? ' (Chưa thuộc)' :
                        state.currentDeck === 'mastered' ? ' (Đã thuộc)' :
                        state.currentDeck === 'bookmarked' ? ' (Yêu thích)' : '';
      progText.textContent = `Thẻ ${currentNum} / ${total}${deckLabel}`;
    }

    const jump = document.getElementById('card-jump-input');
    if (jump) {
      jump.value = currentNum;
      jump.max = total;
    }

    const inner = document.getElementById('flip-card-inner');
    if (inner) inner.classList.toggle('is-flipped', state.isFlipped);

    if (!q) {
      let emptyTitle = 'Không có câu hỏi nào trong danh sách này.';
      let emptySub = 'Hãy bắt đầu bằng cách ôn tập danh sách đầy đủ.';
      if (state.currentDeck === 'hard') {
        emptyTitle = '🎉 Tuyệt vời! Danh sách "Chưa thuộc" đang trống!';
        emptySub = 'Bạn không có câu hỏi nào bị đánh dấu chưa thuộc lúc này. Hãy tiếp tục ôn tập danh sách tất cả các câu!';
      } else if (state.currentDeck === 'mastered') {
        emptyTitle = 'Bạn chưa đánh dấu câu hỏi nào là "Đã thuộc".';
        emptySub = 'Khi gặp câu hỏi đã nắm vững, nhấn nút [✅ Đã thuộc] để đưa vào danh sách này nhé!';
      } else if (state.currentDeck === 'bookmarked') {
        emptyTitle = 'Chưa có câu hỏi nào trong danh sách "Yêu thích".';
        emptySub = 'Nhấn vào ngôi sao ☆ trên góc thẻ để lưu các câu hỏi quan trọng!';
      }

      document.getElementById('card-q-title').innerHTML = `
        <div style="text-align: center; padding: 24px 0;">
          <div style="font-size: 2.4rem; margin-bottom: 12px;">🌟</div>
          <div style="font-size: 1.25rem; font-weight: 800; color: var(--text-main); margin-bottom: 8px;">${emptyTitle}</div>
          <p style="font-size: 0.9rem; color: var(--text-muted); max-width: 460px; margin: 0 auto 20px;">${emptySub}</p>
          <button class="btn-eval btn-eval-easy" style="margin: 0 auto; display: inline-flex;" onclick="window.switchDeck('all')">
            📚 Xem tất cả ${state.allQuestions.length} câu hỏi
          </button>
        </div>
      `;
      document.getElementById('card-ans-body').innerHTML = '';
      return;
    }

    // Status Badge
    const statusBadge = document.getElementById('card-status-badge');
    if (statusBadge) {
      if (state.masteredIds.has(q.id)) {
        statusBadge.className = 'badge badge-status-mastered';
        statusBadge.textContent = '✅ Đã thuộc';
      } else if (state.hardIds.has(q.id)) {
        statusBadge.className = 'badge badge-status-hard';
        statusBadge.textContent = '❌ Chưa thuộc';
      } else {
        statusBadge.className = 'badge badge-status-unlearned';
        statusBadge.textContent = '⏳ Chưa ôn';
      }
    }

    // Meta badges
    document.getElementById('card-level-badge').textContent = q.level;
    document.getElementById('card-level-badge').className = `badge badge-level-${q.level.toLowerCase()}`;
    document.getElementById('card-category-badge').textContent = q.category;
    document.getElementById('card-lang-badge').textContent = q.lang === 'vi' ? 'Tiếng Việt' : 'English';
    document.getElementById('card-index-tag').textContent = `Câu #${currentNum} • ${q.id}`;

    // Question & Answer
    document.getElementById('card-q-title').textContent = q.title;
    document.getElementById('card-ans-body').innerHTML = renderMarkdown(q.answer);

    // Source link
    const sourceEl = document.getElementById('card-source-text');
    if (sourceEl) {
      if (q.source_url) {
        sourceEl.innerHTML = `Nguồn: <a href="${q.source_url}" target="_blank" class="card-source-link">${q.source} ↗</a>`;
      } else {
        sourceEl.textContent = `Nguồn: ${q.source}`;
      }
    }

    renderBookmarkIcon();
  }

  // --- QUESTION BANK & EXPLORER ---
  function setupCategoryPills() {
    const container = document.getElementById('category-pills-container');
    if (!container) return;

    const categories = [
      'Tất cả',
      'Dart Fundamentals',
      'Widgets & UI Core',
      'State Management',
      'Kiến Trúc & Clean Code',
      'Tối Ưu Hiệu Năng',
      'Bất Đồng Bộ & Isolates',
      'Mạng & Lưu Trữ',
      'Native Integration',
      'Kiểm Thử & DevOps',
      'HR & Tuyển Dụng'
    ];

    container.innerHTML = '';
    categories.forEach(cat => {
      const pill = document.createElement('button');
      pill.className = `cat-pill ${cat === 'Tất cả' ? 'active' : ''}`;
      pill.textContent = cat;
      pill.addEventListener('click', () => {
        document.querySelectorAll('.cat-pill').forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        state.filters.category = cat === 'Tất cả' ? 'all' : cat;
        renderExplorer();
      });
      container.appendChild(pill);
    });
  }

  function filterQuestions() {
    return state.allQuestions.filter(q => {
      // Search
      if (state.filters.search) {
        const text = (q.title + ' ' + q.answer + ' ' + q.category + ' ' + q.source).toLowerCase();
        if (!text.includes(state.filters.search)) return false;
      }
      // Category
      if (state.filters.category !== 'all' && q.category !== state.filters.category) {
        return false;
      }
      // Level
      if (state.filters.level !== 'all' && q.level.toLowerCase() !== state.filters.level.toLowerCase()) {
        return false;
      }
      // Language
      if (state.filters.lang !== 'all' && q.lang !== state.filters.lang) {
        return false;
      }
      // Status
      if (state.filters.status === 'mastered' && !state.masteredIds.has(q.id)) return false;
      if (state.filters.status === 'hard' && !state.hardIds.has(q.id)) return false;
      if (state.filters.status === 'bookmarked' && !state.bookmarkedIds.has(q.id)) return false;

      return true;
    });
  }

  function renderExplorer() {
    const container = document.getElementById('explorer-questions-list');
    if (!container) return;

    const filtered = filterQuestions();
    const countEl = document.getElementById('explorer-results-count');
    if (countEl) countEl.textContent = `Hiển thị ${filtered.length} / ${state.allQuestions.length} câu hỏi`;

    if (filtered.length === 0) {
      container.innerHTML = `
        <div style="text-align: center; padding: 48px 20px; color: var(--text-muted);">
          <div style="font-size: 2.5rem; margin-bottom: 12px;">🔍</div>
          <div style="font-size: 1.15rem; font-weight: 700; color: var(--text-main);">Không tìm thấy câu hỏi phù hợp</div>
          <p style="margin-top: 6px;">Hãy thử từ khóa khác hoặc điều chỉnh lại bộ lọc trên thanh tìm kiếm.</p>
        </div>
      `;
      return;
    }

    // Render cards with virtual / slice limit of 80 to keep DOM super snappy
    const slice = filtered.slice(0, 100);
    container.innerHTML = slice.map((q, idx) => {
      const isBookmarked = state.bookmarkedIds.has(q.id);
      const isMastered = state.masteredIds.has(q.id);
      const isHard = state.hardIds.has(q.id);
      return `
        <div class="question-accordion-card" id="acc-${q.id}">
          <div class="accordion-header" onclick="window.toggleAccordion('${q.id}')">
            <div class="accordion-title-col">
              <div class="meta-badges">
                <span class="badge badge-level-${q.level.toLowerCase()}">${q.level}</span>
                <span class="badge badge-category">${q.category}</span>
                ${isMastered ? '<span class="badge badge-status-mastered">✅ Đã thuộc</span>' :
                  isHard ? '<span class="badge badge-status-hard">❌ Chưa thuộc</span>' :
                  '<span class="badge badge-status-unlearned">⏳ Chưa ôn</span>'}
                ${isBookmarked ? '<span style="color: var(--color-amber);">★</span>' : ''}
              </div>
              <div class="accordion-q-title">${idx + 1}. ${q.title}</div>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
              <button class="btn-copy-header" title="Copy prompt: 'Giải thích và giúp tôi hiểu được đáp án của câu này...'" onclick="window.copyPromptForQuestion(window.getQuestionTitleById('${q.id}'), event)">
                📋
              </button>
              <div class="accordion-expand-icon">▼</div>
            </div>
          </div>
          <div class="accordion-body">
            <div class="markdown-body">
              ${renderMarkdown(q.answer)}
            </div>
            <div class="card-source-footer">
              <span>Nguồn: <strong>${q.source}</strong></span>
              <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                <button class="btn-text" style="color: var(--color-primary-light); font-weight: 600;" onclick="window.copyPromptForQuestion(window.getQuestionTitleById('${q.id}'), event)">
                  📋 Copy Prompt AI
                </button>
                <button class="btn-text" style="color: #fb7185;" onclick="window.markCardHard('${q.id}', event)">❌ Chưa thuộc</button>
                <button class="btn-text" style="color: #34d399;" onclick="window.markCardMastered('${q.id}', event)">✅ Đã thuộc</button>
                <button class="btn-text" onclick="window.studySingleQuestion('${q.id}')">🗂️ Ôn dạng Flashcard</button>
                <button class="btn-text" onclick="window.copyQuestion('${q.id}')">📄 Sao chép câu & giải thích</button>
              </div>
            </div>
          </div>
        </div>
      `;
    }).join('');

    if (filtered.length > 100) {
      container.innerHTML += `
        <div style="text-align: center; padding: 18px; color: var(--text-subtle); font-size: 0.9rem;">
          Đang hiển thị 100 câu đầu tiên trong tổng số ${filtered.length} câu tìm được. Hãy thu hẹp bộ lọc để tra cứu chính xác hơn.
        </div>
      `;
    }
  }

  window.getQuestionTitleById = function(qid) {
    const q = state.allQuestions.find(item => item.id === qid);
    return q ? q.title : '';
  };

  window.toggleAccordion = function (qid) {
    const card = document.getElementById(`acc-${qid}`);
    if (card) card.classList.toggle('open');
  };

  window.markCardHard = function (qid, e) {
    if (e) e.stopPropagation();
    state.hardIds.add(qid);
    state.masteredIds.delete(qid);
    saveState({ type: 'status', id: qid, status: 'hard' });
    sound.hard();
    showToast(`❌ Đã đưa vào danh sách Chưa thuộc (${state.hardIds.size} câu)`);
    renderExplorer();
  };

  window.markCardMastered = function (qid, e) {
    if (e) e.stopPropagation();
    state.masteredIds.add(qid);
    state.hardIds.delete(qid);
    saveState({ type: 'status', id: qid, status: 'mastered' });
    sound.correct();
    showToast(`✅ Đã đưa vào danh sách Đã thuộc (${state.masteredIds.size} câu)`);
    renderExplorer();
  };

  window.switchDeck = function (deckName) {
    setDeck(deckName);
  };

  // --- COPY PROMPT AI LOGIC ---
  function copyPromptForQuestion(title) {
    if (!title) return;
    const promptText = `Giải thích và giúp tôi hiểu được đáp án của câu này: ${title}`;

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(promptText).then(() => {
        sound.flip();
        showToast(`📋 Đã copy: "Giải thích và giúp tôi hiểu được đáp án của câu này: ${title.slice(0, 32)}..."`);
      }).catch(() => fallbackCopyPrompt(promptText, title));
    } else {
      fallbackCopyPrompt(promptText, title);
    }
  }

  function fallbackCopyPrompt(promptText, title) {
    const ta = document.createElement('textarea');
    ta.value = promptText;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try {
      document.execCommand('copy');
      sound.flip();
      showToast(`📋 Đã copy: "Giải thích và giúp tôi hiểu được đáp án của câu này: ${title.slice(0, 32)}..."`);
    } catch (e) {
      showToast('❌ Không thể truy cập clipboard của trình duyệt.');
    }
    document.body.removeChild(ta);
  }

  function copyPromptForCurrentCard() {
    const q = getCurrentCard();
    if (q) {
      copyPromptForQuestion(q.title);
    }
  }

  window.copyPromptForQuestion = function(title, e) {
    if (e) e.stopPropagation();
    copyPromptForQuestion(title);
  };

  window.copyQuestion = function (qid) {
    const q = state.allQuestions.find(item => item.id === qid);
    if (!q) return;
    const text = `${q.title}\n\n${q.answer}\n\nNguồn: ${q.source}`;
    navigator.clipboard.writeText(text).then(() => {
      showToast('📋 Đã sao chép câu hỏi và đáp án!');
    });
  };

  // --- LOCAL DATABASE MODAL CONTROLS ---
  function openDatabaseModal() {
    const modal = document.getElementById('modal-db-manager');
    if (!modal) return;
    updateStatsCounter();
    const connEl = document.getElementById('db-stat-conn-status');
    if (connEl) {
      connEl.textContent = (window.appDB && window.appDB.isReady) ? '🟢 Sẵn sàng (IndexedDB API)' : '🟠 Sử dụng bộ nhớ đệm (LocalStorage)';
    }
    modal.classList.add('show');
  }

  function closeDatabaseModal() {
    const modal = document.getElementById('modal-db-manager');
    if (modal) modal.classList.remove('show');
  }

  async function exportDatabaseBackup() {
    try {
      if (!window.appDB) return;
      const data = await window.appDB.exportDatabase();
      const jsonStr = JSON.stringify(data, null, 2);
      const blob = new Blob([jsonStr], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `flutter_interview_backup_${new Date().toISOString().slice(0, 10)}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      showToast('📥 Đã xuất file sao lưu CSDL thành công!');
    } catch (e) {
      console.error(e);
      showToast('❌ Lỗi khi xuất bản sao lưu!');
    }
  }

  async function importDatabaseBackup(e) {
    const file = e.target.files && e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async (event) => {
      try {
        const json = JSON.parse(event.target.result);
        if (!json.data) throw new Error('Cấu trúc file không đúng chuẩn');

        await window.appDB.importDatabase(json);

        // Refresh state sets
        state.masteredIds.clear();
        state.hardIds.clear();
        state.bookmarkedIds.clear();

        if (Array.isArray(json.data.question_status)) {
          json.data.question_status.forEach(item => {
            if (item.status === 'mastered') state.masteredIds.add(item.id);
            if (item.status === 'hard') state.hardIds.add(item.id);
          });
        }
        if (Array.isArray(json.data.bookmarks)) {
          json.data.bookmarks.forEach(id => state.bookmarkedIds.add(id));
        }

        // Sync local storage
        saveState();
        setDeck(state.currentDeck);
        renderExplorer();
        closeDatabaseModal();
        showToast('📤 Phục hồi dữ liệu CSDL thành công!');
      } catch (err) {
        console.error(err);
        showToast('❌ Tệp sao lưu không hợp lệ!');
      }
    };
    reader.readAsText(file);
    e.target.value = ''; // Reset input
  }

  async function resetLocalDatabase() {
    const ok = confirm('⚠️ Bạn có chắc chắn muốn đặt lại toàn bộ CSDL ôn tập? Thao tác này sẽ xóa tất cả danh sách Đã thuộc và Chưa thuộc.');
    if (!ok) return;

    if (window.appDB) {
      await window.appDB.resetDatabase();
    }
    state.masteredIds.clear();
    state.hardIds.clear();
    state.bookmarkedIds.clear();
    localStorage.removeItem('flutter_mastered');
    localStorage.removeItem('flutter_hard');
    localStorage.removeItem('flutter_bookmarks');

    saveState();
    setDeck('all');
    renderExplorer();
    closeDatabaseModal();
    showToast('🗑️ Đã đặt lại CSDL về trạng thái ban đầu!');
  }

  window.studySingleQuestion = function (qid) {
    const idx = state.allQuestions.findIndex(item => item.id === qid);
    if (idx !== -1) {
      state.flashcardList = [...state.allQuestions];
      state.currentCardIndex = idx;
      state.isFlipped = false;
      switchMode('flashcards');
      renderFlashcard();
    }
  };

  // --- QUIZ & PRACTICE MODE ---
  function startQuiz() {
    const countSelect = document.getElementById('quiz-select-count');
    const catSelect = document.getElementById('quiz-select-category');
    const lvlSelect = document.getElementById('quiz-select-level');

    const count = parseInt(countSelect.value, 10) || 10;
    const cat = catSelect.value;
    const lvl = lvlSelect.value;

    let pool = state.allQuestions.filter(q => {
      if (cat !== 'all' && q.category !== cat) return false;
      if (lvl !== 'all' && q.level.toLowerCase() !== lvl.toLowerCase()) return false;
      return true;
    });

    if (pool.length === 0) {
      alert('Không có câu hỏi nào khớp với điều kiện đã chọn.');
      return;
    }

    // Shuffle pool and take slice
    pool = pool.sort(() => 0.5 - Math.random()).slice(0, count);

    state.quiz = {
      questions: pool,
      currentIndex: 0,
      score: 0,
      total: pool.length,
      timerSec: 0,
      timerInterval: null,
      isAnswerShown: false
    };

    document.getElementById('quiz-setup-card').style.display = 'none';
    document.getElementById('quiz-active-card').style.display = 'flex';
    document.getElementById('quiz-summary-card').style.display = 'none';

    renderQuizQuestion();
  }

  function renderQuizQuestion() {
    const q = state.quiz.questions[state.quiz.currentIndex];
    const currentNum = state.quiz.currentIndex + 1;
    const total = state.quiz.total;

    // Progress
    const fill = document.getElementById('quiz-progress-fill');
    if (fill) fill.style.width = `${(currentNum / total) * 100}%`;

    document.getElementById('quiz-q-counter').textContent = `Câu hỏi ${currentNum} / ${total}`;
    document.getElementById('quiz-level-badge').textContent = q.level;
    document.getElementById('quiz-level-badge').className = `badge badge-level-${q.level.toLowerCase()}`;
    document.getElementById('quiz-category-badge').textContent = q.category;

    document.getElementById('quiz-q-title').textContent = q.title;
    document.getElementById('quiz-ans-body').innerHTML = renderMarkdown(q.answer);

    // Hide answer by default
    state.quiz.isAnswerShown = false;
    document.getElementById('quiz-answer-box').classList.remove('visible');
    document.getElementById('btn-quiz-show-answer').textContent = '👁️ Hiện đáp án tham khảo';
    document.getElementById('quiz-rating-row').style.display = 'none';
  }

  function toggleQuizAnswer() {
    state.quiz.isAnswerShown = !state.quiz.isAnswerShown;
    const box = document.getElementById('quiz-answer-box');
    const btn = document.getElementById('btn-quiz-show-answer');
    if (state.quiz.isAnswerShown) {
      box.classList.add('visible');
      btn.textContent = '🙈 Ẩn đáp án';
      document.getElementById('quiz-rating-row').style.display = 'flex';
      sound.flip();
    } else {
      box.classList.remove('visible');
      btn.textContent = '👁️ Hiện đáp án tham khảo';
      document.getElementById('quiz-rating-row').style.display = 'none';
    }
  }

  function recordQuizAnswer(points) {
    if (points === 100) {
      state.quiz.score += 100;
      sound.correct();
    } else if (points === 50) {
      state.quiz.score += 50;
      sound.flip();
    } else {
      sound.hard();
    }

    if (state.quiz.currentIndex < state.quiz.total - 1) {
      state.quiz.currentIndex++;
      renderQuizQuestion();
    } else {
      finishQuiz();
    }
  }

  function finishQuiz() {
    sound.complete();
    document.getElementById('quiz-active-card').style.display = 'none';
    const summaryCard = document.getElementById('quiz-summary-card');
    summaryCard.style.display = 'flex';

    const maxScore = state.quiz.total * 100;
    const percentage = Math.round((state.quiz.score / maxScore) * 100);

    document.getElementById('quiz-final-score').textContent = `${percentage}%`;
    document.getElementById('quiz-final-msg').textContent =
      percentage >= 80 ? '🎉 Xuất sắc! Bạn đã nắm rất vững kiến thức Flutter!' :
      percentage >= 60 ? '👍 Khá tốt! Cần củng cố thêm một số chủ đề nâng cao.' :
      '💪 Hãy tiếp tục luyện tập thêm với chế độ Flashcards!';
  }

  function restartQuiz() {
    document.getElementById('quiz-setup-card').style.display = 'flex';
    document.getElementById('quiz-active-card').style.display = 'none';
    document.getElementById('quiz-summary-card').style.display = 'none';
  }

  // --- HR & EVALUATION TOOLS ---
  function renderHRTools() {
    // Calculator auto computation
    const calcInputs = document.querySelectorAll('.hr-calc-slider');
    calcInputs.forEach(input => {
      input.addEventListener('input', computeHRScore);
    });
    computeHRScore();
  }

  function computeHRScore() {
    const dart = parseInt(document.getElementById('hr-val-dart')?.value || 3, 10);
    const widget = parseInt(document.getElementById('hr-val-widget')?.value || 3, 10);
    const stateVal = parseInt(document.getElementById('hr-val-state')?.value || 3, 10);
    const perf = parseInt(document.getElementById('hr-val-perf')?.value || 3, 10);
    const soft = parseInt(document.getElementById('hr-val-soft')?.value || 3, 10);

    const total = dart + widget + stateVal + perf + soft;
    const max = 25;
    const pct = Math.round((total / max) * 100);

    const scoreDisplay = document.getElementById('hr-total-score-display');
    if (scoreDisplay) scoreDisplay.textContent = `${total} / 25 (${pct}%)`;

    const recDisplay = document.getElementById('hr-rec-verdict');
    if (recDisplay) {
      if (pct >= 80) {
        recDisplay.textContent = '✅ ĐẠT - ĐỀ XUẤT TUYỂN DỤNG (STRONG HIRE)';
        recDisplay.style.color = '#34d399';
      } else if (pct >= 60) {
        recDisplay.textContent = '⚠️ CÂN NHẮC - CẦN PHỎNG VẤN KỸ THUẬT VÒNG 2';
        recDisplay.style.color = '#fbbf24';
      } else {
        recDisplay.textContent = '❌ CHƯA ĐẠT YÊU CẦU CHO VỊ TRÍ';
        recDisplay.style.color = '#fb7185';
      }
    }
  }

})();
