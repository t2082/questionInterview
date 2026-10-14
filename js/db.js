/**
 * FlutterInterviewDB - Client-side Local Database Manager using IndexedDB
 * Handles persistent storage for question mastery states, bookmarks, quiz logs, and user settings.
 */
(function (root) {
  'use strict';

  const DB_NAME = 'FlutterInterviewDB';
  const DB_VERSION = 1;

  class LocalDatabase {
    constructor() {
      this.db = null;
      this.isReady = false;
      this.readyPromise = null;
    }

    /**
     * Initialize IndexedDB database and setup object stores
     */
    init() {
      if (this.readyPromise) return this.readyPromise;

      this.readyPromise = new Promise((resolve, reject) => {
        if (!('indexedDB' in window)) {
          console.warn('[LocalDB] IndexedDB not supported by browser. Falling back to localStorage.');
          this.isReady = false;
          resolve(false);
          return;
        }

        const request = window.indexedDB.open(DB_NAME, DB_VERSION);

        request.onupgradeneeded = (event) => {
          const db = event.target.result;

          // 1. Store: question_status (id, status, updatedAt, reviewCount)
          if (!db.objectStoreNames.contains('question_status')) {
            const statusStore = db.createObjectStore('question_status', { keyPath: 'id' });
            statusStore.createIndex('status', 'status', { unique: false });
            statusStore.createIndex('updatedAt', 'updatedAt', { unique: false });
          }

          // 2. Store: bookmarks (id, createdAt)
          if (!db.objectStoreNames.contains('bookmarks')) {
            db.createObjectStore('bookmarks', { keyPath: 'id' });
          }

          // 3. Store: app_settings (key, value, updatedAt)
          if (!db.objectStoreNames.contains('app_settings')) {
            db.createObjectStore('app_settings', { keyPath: 'key' });
          }

          // 4. Store: quiz_history (id, date, score, total, percentage, answers)
          if (!db.objectStoreNames.contains('quiz_history')) {
            const quizStore = db.createObjectStore('quiz_history', { keyPath: 'id', autoIncrement: true });
            quizStore.createIndex('timestamp', 'timestamp', { unique: false });
          }
        };

        request.onsuccess = async (event) => {
          this.db = event.target.result;
          this.isReady = true;

          // Handle database unexpected close
          this.db.onclose = () => {
            this.isReady = false;
          };

          // Migrate existing localStorage data into IndexedDB on first load
          try {
            await this.migrateFromLocalStorage();
          } catch (e) {
            console.warn('[LocalDB] Error during initial migration:', e);
          }

          resolve(true);
        };

        request.onerror = (event) => {
          console.error('[LocalDB] Failed to open IndexedDB:', event.target.error);
          this.isReady = false;
          resolve(false);
        };
      });

      return this.readyPromise;
    }

    /**
     * Migrate existing items from localStorage to IndexedDB
     */
    async migrateFromLocalStorage() {
      if (!this.db) return;

      const mastered = JSON.parse(localStorage.getItem('flutter_mastered') || '[]');
      const hard = JSON.parse(localStorage.getItem('flutter_hard') || '[]');
      const bookmarks = JSON.parse(localStorage.getItem('flutter_bookmarks') || '[]');

      // If we have items in localStorage, populate IndexedDB if empty
      const existingStatusCount = await this.count('question_status');
      if (existingStatusCount === 0 && (mastered.length > 0 || hard.length > 0)) {
        const tx = this.db.transaction(['question_status'], 'readwrite');
        const store = tx.objectStore('question_status');
        const now = Date.now();

        mastered.forEach(id => {
          store.put({ id, status: 'mastered', updatedAt: now, reviewCount: 1 });
        });
        hard.forEach(id => {
          store.put({ id, status: 'hard', updatedAt: now, reviewCount: 1 });
        });
      }

      const existingBmCount = await this.count('bookmarks');
      if (existingBmCount === 0 && bookmarks.length > 0) {
        const tx = this.db.transaction(['bookmarks'], 'readwrite');
        const store = tx.objectStore('bookmarks');
        const now = Date.now();
        bookmarks.forEach(id => {
          store.put({ id, createdAt: now });
        });
      }
    }

    count(storeName) {
      return new Promise((resolve) => {
        if (!this.db) return resolve(0);
        try {
          const tx = this.db.transaction([storeName], 'readonly');
          const store = tx.objectStore(storeName);
          const req = store.count();
          req.onsuccess = () => resolve(req.result || 0);
          req.onerror = () => resolve(0);
        } catch (e) {
          resolve(0);
        }
      });
    }

    /**
     * Save or update question status ('mastered' | 'hard' | 'unlearned')
     */
    async saveQuestionStatus(id, status) {
      if (!this.db) return false;
      return new Promise((resolve) => {
        try {
          const tx = this.db.transaction(['question_status'], 'readwrite');
          const store = tx.objectStore('question_status');
          const getReq = store.get(id);

          getReq.onsuccess = () => {
            const existing = getReq.result;
            const record = {
              id: id,
              status: status,
              updatedAt: Date.now(),
              reviewCount: (existing ? existing.reviewCount || 0 : 0) + 1
            };
            store.put(record);
          };

          tx.oncomplete = () => resolve(true);
          tx.onerror = () => resolve(false);
        } catch (e) {
          resolve(false);
        }
      });
    }

    /**
     * Get all question statuses
     */
    async getAllQuestionStatuses() {
      if (!this.db) return [];
      return new Promise((resolve) => {
        try {
          const tx = this.db.transaction(['question_status'], 'readonly');
          const store = tx.objectStore('question_status');
          const req = store.getAll();
          req.onsuccess = () => resolve(req.result || []);
          req.onerror = () => resolve([]);
        } catch (e) {
          resolve([]);
        }
      });
    }

    /**
     * Save bookmark status
     */
    async saveBookmark(id, isBookmarked) {
      if (!this.db) return false;
      return new Promise((resolve) => {
        try {
          const tx = this.db.transaction(['bookmarks'], 'readwrite');
          const store = tx.objectStore('bookmarks');
          if (isBookmarked) {
            store.put({ id: id, createdAt: Date.now() });
          } else {
            store.delete(id);
          }
          tx.oncomplete = () => resolve(true);
          tx.onerror = () => resolve(false);
        } catch (e) {
          resolve(false);
        }
      });
    }

    /**
     * Get all bookmarked IDs
     */
    async getAllBookmarks() {
      if (!this.db) return [];
      return new Promise((resolve) => {
        try {
          const tx = this.db.transaction(['bookmarks'], 'readonly');
          const store = tx.objectStore('bookmarks');
          const req = store.getAll();
          req.onsuccess = () => resolve(req.result ? req.result.map(item => item.id) : []);
          req.onerror = () => resolve([]);
        } catch (e) {
          resolve([]);
        }
      });
    }

    /**
     * Save application settings or session state
     */
    async saveSetting(key, value) {
      if (!this.db) return false;
      return new Promise((resolve) => {
        try {
          const tx = this.db.transaction(['app_settings'], 'readwrite');
          const store = tx.objectStore('app_settings');
          store.put({ key: key, value: value, updatedAt: Date.now() });
          tx.oncomplete = () => resolve(true);
          tx.onerror = () => resolve(false);
        } catch (e) {
          resolve(false);
        }
      });
    }

    /**
     * Get setting by key
     */
    async getSetting(key) {
      if (!this.db) return null;
      return new Promise((resolve) => {
        try {
          const tx = this.db.transaction(['app_settings'], 'readonly');
          const store = tx.objectStore('app_settings');
          const req = store.get(key);
          req.onsuccess = () => resolve(req.result ? req.result.value : null);
          req.onerror = () => resolve(null);
        } catch (e) {
          resolve(null);
        }
      });
    }

    /**
     * Save quiz attempt
     */
    async saveQuizResult(quizData) {
      if (!this.db) return false;
      return new Promise((resolve) => {
        try {
          const tx = this.db.transaction(['quiz_history'], 'readwrite');
          const store = tx.objectStore('quiz_history');
          store.add({
            timestamp: Date.now(),
            date: new Date().toISOString(),
            score: quizData.score,
            total: quizData.total,
            percentage: Math.round((quizData.score / quizData.total) * 100),
            answers: quizData.answers || []
          });
          tx.oncomplete = () => resolve(true);
          tx.onerror = () => resolve(false);
        } catch (e) {
          resolve(false);
        }
      });
    }

    /**
     * Get quiz history
     */
    async getQuizHistory() {
      if (!this.db) return [];
      return new Promise((resolve) => {
        try {
          const tx = this.db.transaction(['quiz_history'], 'readonly');
          const store = tx.objectStore('quiz_history');
          const req = store.getAll();
          req.onsuccess = () => resolve(req.result || []);
          req.onerror = () => resolve([]);
        } catch (e) {
          resolve([]);
        }
      });
    }

    /**
     * Export entire database as JSON backup
     */
    async exportDatabase() {
      const statuses = await this.getAllQuestionStatuses();
      const bookmarks = await this.getAllBookmarks();
      const quizzes = await this.getQuizHistory();

      return {
        database: DB_NAME,
        version: DB_VERSION,
        exportedAt: new Date().toISOString(),
        timestamp: Date.now(),
        statistics: {
          masteredCount: statuses.filter(s => s.status === 'mastered').length,
          hardCount: statuses.filter(s => s.status === 'hard').length,
          bookmarksCount: bookmarks.length,
          quizzesCount: quizzes.length
        },
        data: {
          question_status: statuses,
          bookmarks: bookmarks,
          quiz_history: quizzes
        }
      };
    }

    /**
     * Import JSON backup into IndexedDB
     */
    async importDatabase(jsonData) {
      if (!this.db || !jsonData || !jsonData.data) {
        throw new Error('Dữ liệu không hợp lệ hoặc CSDL chưa sẵn sàng');
      }

      const tx = this.db.transaction(['question_status', 'bookmarks', 'quiz_history'], 'readwrite');
      const statusStore = tx.objectStore('question_status');
      const bmStore = tx.objectStore('bookmarks');
      const quizStore = tx.objectStore('quiz_history');

      // Clear existing records first
      await new Promise((resolve, reject) => {
        statusStore.clear().onsuccess = () => {
          bmStore.clear().onsuccess = () => {
            quizStore.clear().onsuccess = () => resolve();
          };
        };
      });

      // Restore question_status
      if (Array.isArray(jsonData.data.question_status)) {
        jsonData.data.question_status.forEach(record => {
          statusStore.put(record);
        });
      }

      // Restore bookmarks
      if (Array.isArray(jsonData.data.bookmarks)) {
        jsonData.data.bookmarks.forEach(id => {
          bmStore.put({ id: id, createdAt: Date.now() });
        });
      }

      // Restore quiz_history
      if (Array.isArray(jsonData.data.quiz_history)) {
        jsonData.data.quiz_history.forEach(item => {
          quizStore.add(item);
        });
      }

      return new Promise((resolve, reject) => {
        tx.oncomplete = () => resolve(true);
        tx.onerror = (e) => reject(e);
      });
    }

    /**
     * Clear all records in local database
     */
    async resetDatabase() {
      if (!this.db) return false;
      return new Promise((resolve, reject) => {
        try {
          const tx = this.db.transaction(['question_status', 'bookmarks', 'quiz_history', 'app_settings'], 'readwrite');
          tx.objectStore('question_status').clear();
          tx.objectStore('bookmarks').clear();
          tx.objectStore('quiz_history').clear();
          tx.objectStore('app_settings').clear();
          tx.oncomplete = () => resolve(true);
          tx.onerror = () => resolve(false);
        } catch (e) {
          resolve(false);
        }
      });
    }
  }

  // Export singleton to global window
  root.LocalDatabase = LocalDatabase;
  root.appDB = new LocalDatabase();

})(window);
