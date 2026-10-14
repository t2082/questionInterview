# 🚀 Flutter Interview Pro • Nền Tảng Ôn Tập Phỏng Vấn Flutter Toàn Diện

> **Bộ tài nguyên và ứng dụng Web tĩnh ôn luyện phỏng vấn Flutter Developer toàn diện nhất với 730+ câu hỏi chuẩn hóa từ các nguồn uy tín toàn cầu.**

![Flutter Interview Suite](https://img.shields.io/badge/Flutter-Interview%20Pro-02569B?logo=flutter&logoColor=white)
![Questions](https://img.shields.io/badge/Questions-736%20Curated-success)
![Storage](https://img.shields.io/badge/Local%20Database-IndexedDB%20v1.0-blueviolet)
![Responsive](https://img.shields.io/badge/Design-Mobile%20Optimized-orange)

---

## 🌟 Tính Năng Nổi Bật

### 1. 🗂️ Thẻ Ghi Nhớ Tương Tác (3D Interactive Flashcards)
- Hiệu ứng lật thẻ 3D mượt mà (chạm hoặc bấm `Space`).
- **Phân loại thông minh**:
  - `❌ Chưa thuộc` (Phím `1`): Đưa câu hỏi vào danh sách cần cải thiện.
  - `✅ Đã thuộc` (Phím `2`): Tự động loại khỏi danh sách backlog chưa thuộc và đưa vào danh sách đã thành thạo.
- **Deck Switcher**: Cho phép chọn lọc học theo danh mục `📚 Tất Cả`, `❌ Chưa Thuộc`, `✅ Đã Thuộc`, hoặc `★ Yêu Thích`.
- **Thao tác cử chỉ di động**: Hỗ trợ vuốt ngang cảm ứng (Swipe Left/Right) trên điện thoại để chuyển thẻ kế tiếp / thẻ trước đó.

### 2. 📋 1-Click Copy Prompt Hỏi AI
- Tích hợp nút **Copy Prompt AI** ngay trên thẻ Flashcard và từng câu hỏi trong Ngân hàng câu hỏi.
- Sao chép văn bản chuẩn hóa để gửi ngay cho ChatGPT / Claude / Gemini:
  ```text
  Giải thích và giúp tôi hiểu được đáp án của câu này: <Nội dung câu hỏi>
  ```

### 3. 💾 Local Database (IndexedDB) & Backup JSON
- Toàn bộ trạng thái câu hỏi (Đã thuộc, Chưa thuộc, Bookmark, Phiên ôn luyện, Lịch sử Quiz) được lưu trữ trực tiếp trong trình duyệt qua **IndexedDB API** (`FlutterInterviewDB`).
- Cơ chế **Dual-Sync** song song với `localStorage` đảm bảo không bao giờ thất lạc dữ liệu.
- **Quản lý CSDL (Modal 💾)**:
  - 📥 **Xuất bản sao lưu (Export JSON)**: Tải tệp backup về máy tính cá nhân.
  - 📤 **Phục hồi dữ liệu (Import JSON)**: Khôi phục lại tiến trình học tập chỉ trong 1 giây.
  - 🗑️ **Đặt lại CSDL**: Khởi động lại lộ trình ôn tập khi cần.

### 4. 🔍 Ngân Hàng Câu Hỏi & Tra Cứu Đa Chiều (Question Bank)
- 736 câu hỏi được phân loại theo 10 chủ đề cốt lõi:
  - Dart Fundamentals
  - Widgets & UI Core
  - State Management (BLoC, Riverpod, Provider, GetX, Signals)
  - Kiến Trúc & Clean Code (MVVM, Clean Arch, SOLID)
  - Tối Ưu Hiệu Năng & Render Tree
  - Bất Đồng Bộ, Streams & Isolates
  - Mạng & Lưu Trữ (Dio, Retrofit, Hive, SQLite)
  - Native Integration (MethodChannel, FFI, Platform Views)
  - Kiểm Thử & DevOps (Unit, Widget, Integration test, CI/CD)
  - HR & Phỏng Vấn Sàng Lọc
- Bộ lọc theo: Trạng thái (Đã thuộc / Chưa thuộc), Trình độ (Junior, Middle, Senior), Ngôn ngữ (Vi / En), Từ khóa tìm kiếm tức thì.

### 5. ⏱️ Giả Lập Phỏng Vấn (Quiz Simulator)
- Tùy chỉnh số lượng câu hỏi (5, 10, 20 câu) theo từng chủ đề hoặc độ khó.
- Chế độ tự chấm điểm (0% - 50% - 100%) và tổng kết xếp loại năng lực.

### 6. 📱 Tối Ưu Hóa Điện Thoại 100% (Mobile Responsive)
- Thanh điều hướng thông minh dính đáy (Bottom Navigation Bar) chuẩn UX ứng dụng di động.
- Touch Pill trượt ngang mềm mại, cỡ chữ và khoảng đệm tối ưu cho một tay thao tác.

---

## 📂 Cấu Trúc Dự Án

```
├── assets/                          # Dữ liệu nguồn gốc crawl từ 27+ nền tảng công nghệ
│   ├── 01_github_repositories/      # 14 repos GitHub nổi tiếng (Power19942, Debasmita, ...)
│   ├── 02_global_platforms/         # GeeksforGeeks, DevInterview, Edureka, Simplilearn, ...
│   ├── 03_vietnamese_sources/       # TopCV, Viblo
│   ├── 04_official_standards/       # Dart FAQ & trọn bộ 170+ tài liệu Flutter Wiki chính thức
│   └── 05_hr_screening_cheatsheet.md# Khung sàng lọc ứng viên 15 phút dành cho HR
├── css/
│   └── style.css                    # Design system Vanilla CSS (Obsidian & Flutter Sky Blue theme)
├── data/
│   ├── questions.json               # Bộ dữ liệu 736 câu hỏi định dạng JSON
│   └── questions.js                 # Export window.FLUTTER_QUESTIONS (chạy offline zero-CORS)
├── js/
│   ├── db.js                        # Module IndexedDB Local Database & Backup/Restore
│   └── app.js                       # Logic ứng dụng, Flashcard, Quiz, Audio FX, Filters
├── crawl_all.py                     # Script Python tự động hóa thu thập dữ liệu
├── generate_questions_dataset.py    # Pipeline chuẩn hóa, trích xuất & làm sạch câu hỏi
├── flutter_dev_source.txt           # Danh mục 27+ đường link nguồn
├── index.html                       # Ứng dụng Web tĩnh chính
└── README.md
```

---

## 💻 Hướng Dẫn Sử Dụng

### Cách 1: Khởi chạy trực tiếp bằng Local Server
```bash
# Sử dụng Python built-in HTTP server:
python3 -m http.server 4567

# Hoặc bằng Node.js npx serve:
npx serve -l 4567
```
👉 Mở trình duyệt và truy cập: **`http://localhost:4567`**

### Cách 2: Mở trực tiếp không cần Server
Nhấp đúp chuột trực tiếp vào file **`index.html`** trong trình duyệt bất kỳ (Chrome, Safari, Edge, Firefox). Hệ thống được thiết kế với cơ chế Zero-CORS tương thích hoàn toàn khi mở qua giao thức `file:///`.

---

## ⌨️ Phím Tắt Tiện Dụng

| Phím tắt | Chức năng |
| :---: | :--- |
| `Space` | Lật thẻ Flashcard (Xem câu hỏi / Xem đáp án) |
| `→` hoặc `Enter` | Chuyển sang thẻ câu hỏi tiếp theo |
| `←` | Quay lại thẻ câu hỏi trước đó |
| `1` | Đánh dấu **❌ Chưa thuộc** |
| `2` | Đánh dấu **✅ Đã thuộc** |
| `C` | **Sao chép Prompt AI** để hỏi ChatGPT/Gemini |
| `B` | Lưu / Bỏ lưu câu hỏi vào danh sách **★ Yêu thích** |

---

## 📜 Bản Quyền & Nguồn Tham Khảo
Dữ liệu câu hỏi được tổng hợp và xử lý từ các dự án mã nguồn mở và nền tảng cộng đồng (xem danh mục chi tiết tại [`assets/README.md`](assets/README.md)). Bản quyền nội dung gốc thuộc về các tác giả và tổ chức đóng góp mở.
