# Viblo - Kinh Nghiệm Phỏng Vấn Mobile/Flutter Thực Tế (Intern/Fresher)

- **Source URL**: [https://viblo.asia/p/kinh-nghiem-phong-van-internfresher-mobile-nhung-dieu-minh-da-hoc-duoc-MkNLr5WwJgA](https://viblo.asia/p/kinh-nghiem-phong-van-internfresher-mobile-nhung-dieu-minh-da-hoc-duoc-MkNLr5WwJgA)
- **Crawl Date**: 2026-10-13 09:48:23
- **Tác giả / Nền tảng**: Viblo Asia Community
- **Mô tả**: Trải nghiệm phỏng vấn thực chiến, các câu hỏi về OOP, SOLID, asynchronous, và mẹo trả lời câu hỏi chuyên môn dành cho ứng viên và nhà tuyển dụng.

---

__

  * __Report
  * __Add to my series

## Mở Bài

Có một lần mình đi phỏng vấn, mặc dù đã ôn rất kỹ, nhưng chỉ cần bị hỏi một câu mà mình không biết, thì các kiến thức khác cũng "bay màu" luôn. 😵‍💫 Vậy nên mình viết bài này để chia sẻ kinh nghiệm cho các bạn đang chuẩn bị phỏng vấn Intern/Fresher Mobile. Hy vọng nó giúp bạn tự tin hơn khi đối mặt với interviewer!

* * *

## Nội Dung Chính

### Lập Trình Hướng Đối Tượng (OOP)

#### 🔹 4 tính chất OOP

  * **Encapsulation (Đóng gói):** Giữ dữ liệu an toàn bằng cách sử dụng `private`, `protected`.
  * **Abstraction (Trừu tượng):** Chỉ hiển thị thông tin cần thiết, giấu bớt chi tiết.
  * **Inheritance (Kế thừa):** Tái sử dụng code bằng cách kế thừa từ class cha.
  * **Polymorphism (Đa hình):** Một phương thức có thể hoạt động khác nhau tùy vào context.

#### 🔹 Câu hỏi phỏng vấn mình thường gặp

  * Nêu rõ 4 tính chất của OOP: Định nghĩa, ví dụ.
  * Phân biệt overriding và overloading.
  * So sánh kế thừa và đa hình?
  * Live coding: Implement 2-3 class, trong đó có 1-2 class có danh sách, và các phương thức CRUD cũng như tính toán theo yêu cầu của Interviewer.

* * *

### Nguyên Tắc SOLID

  * **S** ingle Responsibility: Mỗi class chỉ có một trách nhiệm.
  * **O** pen/Closed: Class mở rộng được nhưng không chỉnh sửa trực tiếp.
  * **L** iskov Substitution: Class con có thể thay thế class cha.
  * **I** nterface Segregation: Không ép class implement interface không cần thiết.
  * **D** ependency Inversion: Phụ thuộc vào abstraction, không phải implementation.

👉 _Tip:_ Hãy đưa ví dụ thực tế trong code để chứng minh bạn hiểu SOLID.

#### 🔹 Câu hỏi phỏng vấn mình thường gặp

  * Tại sao lại cần áp dụng nguyên tắc này, nó có ích gì?

* * *

### Kiến thức về Mobile Development

#### 🔹 Các câu hỏi mà mình không biết trả lời sao khi lần đầu gặp

  * Làm sao bảo mật key khi lưu ở local?
  * Cách xử lý để bảo mật ứng dụng khi hacker root máy?
  * License khi tích hợp SDK bên thứ ba?
  * Một SDK mà mình đã struggle trong việc tích hợp và hướng giải quyết như thế nào?
  * Hiểu biết về các chuẩn format code.

* * *

### Flutter

#### 🔹 Câu hỏi thường gặp

  * Stateless vs Stateful Widget?
  * Future khác gì với kiểu dữ liệu thông thường?
  * Singleton vs Factory trong Dependency Injection?
  * Cách tối ưu hiệu suất widget tree?
  * Phân biệt async và sync.
  * Giải thích về method build, initState,...
  * Nói về Clean Architecture trong Flutter.

* * *

### Design Pattern & Unit test

#### 🔹 Câu hỏi mình đã gặp

  * Giải thích về MVVM? Tại sao lại apply MVVM trong các project trong CV thay vì MVC?
  * Một số câu hỏi về Interface và Strategy Design Pattern?
  * Unit test là gì? Có mấy loại Unit test?

* * *

### CI/CD & Quy Trình Phát Triển

  * **CI/CD:** Dùng GitHub Actions, Codemagic để tự động hóa build.
  * **Scrum, Agile:** Biết cách quản lý task trên Jira, GitHub Project.

* * *

### Cấu Trúc Dữ Liệu & Giải Thuật (DSA)

#### 🔹 Một số bài coding mình đã gặp

  * **Tìm người thắng Tic-Tac-Toe**
  * **Đếm số ngày đã qua trong năm**
  * **Xác định chuỗi có "good" hay không (đóng mở dấu ngoặc đúng không?)**

👉 _Tip:_ Đọc kỹ constraints trước khi code, nếu bí thì xin hint từ interviewer!

* * *

### Kỹ Năng Làm Việc Nhóm

  * Xử lý khi deadline cận kề.
  * Làm gì khi đồng đội delay task?
  * Cách phối hợp với designer, backend?

* * *

### Tiếng Anh Trong Phỏng Vấn

  * Không yêu cầu cao như thi IELTS (phải đúng ngữ pháp, phát âm phải "wow"), chỉ cần giao tiếp bình thường là được!
  * Nếu không biết từ nào? → "I don’t know what it’s called in English, but it means..."
  * Nghe không rõ? → "Excuse me, can you repeat that?"
  * Không hiểu câu hỏi? → "Can you explain more, please?"
  * Confirm lại đề bài → "To ensure that I understand the problem correctly, let me restate it in my own words."

* * *

## Ngoài Lề

  * Nếu nhận email fail, đừng buồn, hãy xin feedback để cải thiện.
  * Mỗi lần fail là một lần học hỏi, rồi bạn sẽ có job thôi!
  * Lúc post blog này mình cũng đang tích cực rải CV. 😆

Hy vọng bài viết này giúp ích cho bạn. Nếu bạn có câu hỏi hoặc muốn chia sẻ trải nghiệm của mình, hãy để lại comment nhé! 🚀

[ Fresher/New Dev ](/tags/freshernew-dev)[ Coding Interview ](/tags/coding-interview)[ Flutter ](/tags/flutter)[ Kinh nghiệm phỏng vấn ](/tags/kinh-nghiem-phong-van)[ mobile developer ](/tags/mobile-developer)

  

All Rights Reserved 

____

__

  * __Report
  * __Add to my series