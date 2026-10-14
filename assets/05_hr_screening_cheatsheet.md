# Khung Tiêu Chí Phỏng Vấn Nhanh Dành Cho HR (HR Screening Cheat-Sheet)

- **Biên soạn theo tài liệu**: `flutter_dev_source.txt`
- **Mục đích**: Bảng câu hỏi sàng lọc và bộ từ khóa cốt lõi giúp chuyên viên tuyển dụng (HR / Talent Acquisition) đánh giá ứng viên Flutter trong vòng 10-15 phút phỏng vấn sơ loại (Screening Call).

---

## 🎯 MA TRẬN ĐÁNH GIÁ ỨNG VIÊN THEO CẤP BẬC

### 1. CẤP BẬC: INTERN / FRESHER / JUNIOR
#### Từ khóa & Chủ đề cần kiểm tra:
* **Ngôn ngữ Dart căn bản**:
  - `final` vs `const`: Cả hai đều không thể gán lại giá trị, nhưng `const` là hằng số lúc biên dịch (compile-time), `final` là hằng số lúc chạy (runtime).
  - `var` vs `dynamic`: `var` suy luận kiểu cố định khi gán; `dynamic` cho phép đổi kiểu tự do khi chạy.
  - `Null Safety`: Cơ chế ngăn chặn null, ý nghĩa của dấu `?` (nullable) và `!` (null assertion).
* **Flutter Core & Widget**:
  - `StatelessWidget` vs `StatefulWidget`: StatelessWidget không đổi trạng thái; StatefulWidget có State thay đổi được và rebuild qua `setState()`.
  - `Hot Reload` vs `Hot Restart`: Hot Reload tiêm code mới mà không mất state; Hot Restart reset toàn bộ ứng dụng và xóa sạch state.
  - Vòng đời cơ bản: `initState()` (khởi tạo), `build()` (vẽ UI), `dispose()` (giải phóng tài nguyên).
  - Bố cục UI: `Row`, `Column`, `ListView`, `Expanded`, `Flexible`, `Stack`.

---

### 2. CẤP BẬC: MIDDLE DEVELOPER
#### Từ khóa & Chủ đề cần kiểm tra:
* **Quản lý trạng thái (State Management)**:
  - Hiểu sâu một trong các thư viện: Provider, Riverpod, BLoC hoặc GetX.
  - Biết giải thích lý do khi nào nên dùng loại nào và các nhược điểm đi kèm.
* **Lập trình bất đồng bộ (Asynchronous)**:
  - Khái niệm `Future`, `Stream`, `async`, `await`.
  - Thành thạo widget `FutureBuilder` và `StreamBuilder`.
* **Quản lý tài nguyên & Bộ nhớ**:
  - Biết cách phòng tránh Memory Leak bằng cách `dispose()` các `TextEditingController`, `StreamSubscription`, `AnimationController`.
* **Kết nối mạng & Lưu trữ**:
  - Xử lý RESTful API qua `http` hoặc `dio` (Interceptors, Token refresh).
  - Parse JSON data, lưu trữ local qua SQLite (`sqflite`), `Hive` hoặc `SharedPreferences`.
* **Giao diện nâng cao**:
  - `CustomPaint`, `Hero` animation, `AnimationController`.

---

### 3. CẤP BẬC: SENIOR / TECH LEAD
#### Từ khóa & Chủ đề cần kiểm tra:
* **Kiến trúc ứng dụng**:
  - Clean Architecture, MVVM, SOLID Principles.
  - Dependency Injection (`get_it`, `injectable`).
* **Tối ưu hiệu năng (Performance Optimization)**:
  - Kỹ thuật giảm thiểu rebuild thừa: dùng `const`, `Selector`, `buildWhen`.
  - Sử dụng Flutter DevTools để phân tích CPU, Memory, phát hiện UI frame drop.
* **Xử lý đa luồng & Concurrency**:
  - Bản chất Single-threaded Event Loop, Microtask Queue.
  - Sử dụng `Isolate` hoặc hàm `compute()` để đưa tác vụ tính toán nặng (parse JSON lớn, giải mã ảnh) ra ngoài Main thread.
* **Tích hợp Native (Platform Channels)**:
  - Viết `MethodChannel` để giao tiếp với Android (Kotlin/Java) và iOS (Swift/Obj-C).
* **Kiểm thử & CI/CD**:
  - Viết Unit Test, Widget Test, Integration Test.
  - Thiết lập pipeline tự động hóa build/deploy với Fastlane, GitHub Actions.
