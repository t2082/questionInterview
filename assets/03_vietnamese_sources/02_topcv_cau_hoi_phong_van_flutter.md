# TopCV - Bộ Câu Hỏi Phỏng Vấn Flutter Phổ Biến Nhất & Đáp Án Chuẩn

- **Original Reference**: [https://blog.topcv.vn/cau-hoi-phong-van-flutter/](https://blog.topcv.vn/cau-hoi-phong-van-flutter/)
- **Crawl & Compilation Date**: 2026-10-13 09:48:24
- **Mục tiêu**: Tuyển tập các câu hỏi phỏng vấn kinh điển, hay gặp nhất trong tất cả các đợt tuyển dụng nhân sự Mobile Developer tại Việt Nam.

---

## MỤC LỤC
1. [Bộ câu hỏi về Ngôn ngữ Dart](#1-bo-cau-hoi-ve-ngon-ngu-dart)
2. [Bộ câu hỏi về Flutter UI & Widget](#2-bo-cau-hoi-ve-flutter-ui--widget)
3. [Bộ câu hỏi về Quản lý trạng thái (State Management)](#3-bo-cau-hoi-ve-quan-ly-trang-thai)
4. [Bộ câu hỏi về Mạng, Caching & Lưu trữ dữ liệu](#4-bo-cau-hoi-ve-mang-caching--luu-tru)
5. [Bộ câu hỏi về Native Integration & Triển khai ứng dụng](#5-bo-cau-hoi-ve-native-integration--trien-khai)

---

### 1. BỘ CÂU HỎI VỀ NGÔN NGỮ DART

#### Q1: Vì sao Flutter lại lựa chọn Dart làm ngôn ngữ phát triển thay vì JavaScript hay C#?
* **Đáp án**:
  1. **Dual Compilation**: Dart hỗ trợ cả **JIT (Just-in-Time)** để phục vụ tính năng Hot Reload siêu tốc khi lập trình, và **AOT (Ahead-of-Time)** để biên dịch thẳng ra mã máy tối ưu hóa cao khi phát hành.
  2. **Single-threaded Event Loop**: Mô hình hướng sự kiện đơn luồng hạn chế triệt để lỗi xung đột tài nguyên luồng (race condition, deadlock).
  3. **Generational Garbage Collection**: Tối ưu thu gom bộ nhớ cho các đối tượng ngắn hạn (short-lived objects), rất phù hợp với việc tạo và hủy Widget liên tục trong Flutter.
  4. **Không cần cầu nối (No JavaScript Bridge)**: Dart biên dịch thẳng ra mã máy native, vẽ UI trực tiếp qua Skia/Impeller engine, đem lại độ mượt 60fps / 120fps.

#### Q2: Phân biệt `var`, `dynamic`, `Object?`, `final` và `const`?
* **Đáp án**:
  - `var`: Trình biên dịch tự suy luận kiểu tại thời điểm khởi tạo; sau khi gán, kiểu đó không được đổi.
  - `dynamic`: Tắt kiểm tra kiểu tĩnh lúc biên dịch, cho phép thay đổi bất kỳ kiểu nào tại runtime (dễ gây lỗi NoSuchMethodError).
  - `Object?`: Lớp cha của mọi đối tượng trong Dart; có kiểm tra kiểu, phải ép kiểu (cast/is) trước khi gọi method cụ thể.
  - `final`: Hằng số runtime, chỉ được gán giá trị một lần duy nhất khi chạy chương trình.
  - `const`: Hằng số compile-time, giá trị phải được biết trước lúc build, được lưu vào bộ nhớ dùng chung (canonicalized).

#### Q3: Sound Null Safety trong Dart là gì?
* **Đáp án**:
  Cơ chế bảo đảm an toàn kiểu dữ liệu lúc biên dịch. Mặc định mọi biến trong Dart là non-nullable (không thể mang giá trị `null`). Nếu muốn cho phép `null`, lập trình viên phải thêm `?` (ví dụ: `String? name`).
  - Toán tử `!`: Báo cho compiler biến chắc chắn không null (Null Assertion).
  - Toán tử `?.`: Truy cập an toàn (nếu null thì trả về null thay vì crash).
  - Toán tử `??`: Gán giá trị mặc định nếu biểu thức bên trái là null (Elvis operator).
  - Từ khóa `late`: Khai báo biến non-nullable nhưng khởi tạo muộn sau đó.

---

### 2. BỘ CÂU HỎI VỀ FLUTTER UI & WIDGET

#### Q4: Vòng đời của một `StatefulWidget` gồm các bước nào?
* **Đáp án**:
  1. `createState()`: Tạo State object gắn với widget.
  2. `initState()`: Được gọi đúng 1 lần khi State object được chèn vào cây. Dùng để khởi tạo controller, đăng ký listener, gọi API khởi đầu.
  3. `didChangeDependencies()`: Được gọi ngay sau `initState()` hoặc khi một `InheritedWidget` cha mà widget này phụ thuộc có sự thay đổi.
  4. `build()`: Vẽ và trả về cây widget con. Hàm này được gọi nhiều lần mỗi khi gọi `setState()`.
  5. `didUpdateWidget()`: Được gọi khi widget cha rebuild và cấu hình lại widget này với các tham số mới cùng `runtimeType` và `key`.
  6. `deactivate()`: State object tạm thời bị gỡ khỏi cây (ví dụ chuyển route).
  7. `dispose()`: State object bị hủy vĩnh viễn khỏi cây. Nơi bắt buộc phải giải phóng bộ nhớ (hủy stream, controller, listener).

#### Q5: Sự khác nhau giữa `Row`/`Column` với `ListView` là gì?
* **Đáp án**:
  - `Row`/`Column`: Render tất cả các phần tử con cùng một lúc vào bộ nhớ, không hỗ trợ cuộn tự động. Nếu nội dung vượt quá kích thước màn hình sẽ gây lỗi Overflow (vàng đen sọc).
  - `ListView.builder`: Có cơ chế ảo hóa (Virtualization / Lazy loading), chỉ tạo và render các phần tử đang hiển thị trên màn hình (viewport), giúp tiết kiệm bộ nhớ và cuộn mượt mà đối với danh sách hàng nghìn phần tử.

#### Q6: Khi nào nên sử dụng `GlobalKey`?
* **Đáp án**:
  - Khi cần truy cập trạng thái (`State`) hoặc phương thức của một widget con từ một nơi khác ngoài cây phân cấp (ví dụ: `FormState` để gọi `formKey.currentState.validate()`).
  - Khi cần di chuyển một widget từ nhánh cây này sang nhánh cây khác mà không làm mất trạng thái của nó.
  - *Lưu ý*: `GlobalKey` rất tốn tài nguyên vì nó phải đăng ký trên toàn bộ ứng dụng, không nên lạm dụng.

---

### 3. BỘ CÂU HỎI VỀ QUẢN LÝ TRẠNG THÁI (STATE MANAGEMENT)

#### Q7: So sánh các thư viện State Management: BLoC, Provider, Riverpod và GetX?
* **Đáp án**:
  - **BLoC (Business Logic Component)**:
    - *Ưu điểm*: Tách bạch 100% logic khỏi UI; kiến trúc phân lớp chuẩn mực; kiểm thử (Unit test) rất dễ; chuẩn enterprise.
    - *Nhược điểm*: Nhiều boilerplate code (phải viết Event, State, Bloc).
  - **Provider**:
    - *Ưu điểm*: Được Google khuyến nghị chính thức; bám sát `InheritedWidget`; cú pháp đơn giản, dễ tiếp cận.
    - *Nhược điểm*: Phụ thuộc vào `BuildContext`, khó sử dụng ở các tầng ngoài UI.
  - **Riverpod**:
    - *Ưu điểm*: Thế hệ kế tiếp của Provider; hoàn toàn compile-safe; không phụ thuộc `BuildContext`; hỗ trợ caching và provider kết hợp cực mạnh.
    - *Nhược điểm*: Khái niệm mới (ConsumerWidget, Ref) cần thời gian làm quen.
  - **GetX**:
    - *Ưu điểm*: Rất ít boilerplate; tốc độ phát triển nhanh; tích hợp trọn gói (State, Navigation, DI).
    - *Nhược điểm*: Đi chệch khỏi triết lý Flutter nguyên bản; quản lý context ngầm có thể gây memory leak và khó scale ở các dự án lớn.

---

### 4. BỘ CÂU HỎI VỀ MẠNG & LƯU TRỮ (NETWORKING & CACHING)

#### Q8: Trong Flutter, bạn xử lý HTTP Request và Interceptor như thế nào?
* **Đáp án**:
  Thường dùng package `dio` thay vì thư viện `http` cơ bản vì `dio` hỗ trợ:
  - **Interceptors**: Tự động đính kèm `Bearer Token` vào header; tự động bắt mã lỗi `401 Unauthorized` để gọi API Refresh Token và thử lại request cũ (Retry).
  - **Global Error Handling**: Bắt lỗi kết nối mạng (Timeout, No Internet) tại một nơi tập trung.
  - **Cancellation Token**: Hủy bỏ request đang chạy nếu người dùng thoát khỏi màn hình.

#### Q9: So sánh các giải pháp lưu trữ dữ liệu cục bộ (Local Storage): SharedPreferences, Hive, Isar và SQLite (sqflite)?
* **Đáp án**:
  - `SharedPreferences`: Key-value lưu kiểu dữ liệu đơn giản (token, settings, boolean flag). Tốc độ chậm với lượng dữ liệu lớn.
  - `Hive` / `Isar`: NoSQL database thuần Dart, lưu trữ dạng nhị phân, tốc độ đọc ghi cực nhanh, thích hợp làm offline cache.
  - `SQLite (sqflite)`: Cơ sở dữ liệu quan hệ (SQL), hỗ trợ quan hệ bảng phức tạp, index, query điều kiện nặng.

---

### 5. BỘ CÂU HỎI VỀ NATIVE & PERFORMANCE

#### Q10: Platform Channel là gì? Phân biệt MethodChannel và EventChannel?
* **Đáp án**:
  Cơ chế cho phép Flutter giao tiếp bất đồng bộ với mã nguồn Native (Kotlin/Java trên Android, Swift/Objective-C trên iOS):
  - `MethodChannel`: Giao tiếp 2 chiều dạng gọi hàm (Request - Response). Dùng khi Flutter gọi Native lấy mức pin, mở camera, gọi SDK bên thứ 3.
  - `EventChannel`: Giao tiếp 1 chiều dạng luồng (Stream) từ Native gửi dữ liệu liên tục về Flutter. Dùng cho cảm biến gia tốc, định vị GPS, la bàn.

#### Q11: Làm thế nào để giảm dung lượng file APK/IPA khi build ứng dụng Flutter?
* **Đáp án**:
  1. Sử dụng split APK theo kiến trúc CPU: `flutter build apk --split-per-abi` (chia ra arm64-v8a, armeabi-v7a).
  2. Bật cờ tối ưu mã nguồn và làm sạch tài nguyên: `minifyEnabled true`, `shrinkResources true` trong file build.gradle.
  3. Bật nén ảnh, sử dụng định dạng WebP hoặc SVG thay vì PNG/JPEG kích thước lớn.
  4. Sử dụng font chữ tùy chỉnh chỉ chứa glyph cần thiết (`--tree-shake-icons`).
