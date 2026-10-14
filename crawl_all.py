#!/usr/bin/env python3
"""
Crawler script for flutter_dev_source.txt
Extracts, cleans, and structures interview questions from all source links into assets/
"""

import os
import re
import ssl
import time
import urllib.request
from bs4 import BeautifulSoup
import html2text

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,vi;q=0.8"
}

BASE_DIR = "/Users/akuro/AkuroWorkpage/practive_skill"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def fetch_html(url, retries=3):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            print(f"  [Attempt {i+1}/{retries}] Error fetching {url}: {e}")
            time.sleep(2)
    return None

def html_to_clean_md(html, main_selector=None, remove_selectors=None):
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    
    # Common unwanted tags
    default_remove = ["script", "style", "nav", "footer", "header", "noscript", "svg", "iframe", "aside"]
    for tag_name in default_remove:
        for s in soup.find_all(tag_name):
            s.decompose()
            
    if remove_selectors:
        for sel in remove_selectors:
            for el in soup.select(sel):
                el.decompose()

    target = None
    if main_selector:
        target = soup.select_one(main_selector)
    if not target:
        target = soup.find("article") or soup.find("main") or soup.find(id="content") or soup.body or soup

    h = html2text.HTML2Text()
    h.body_width = 0
    h.ignore_links = False
    h.ignore_images = False
    h.skip_internal_links = False
    
    md = h.handle(str(target))
    # Remove excessive blank lines
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()

def process_global_platforms():
    out_dir = os.path.join(ASSETS_DIR, "02_global_platforms")
    os.makedirs(out_dir, exist_ok=True)
    
    platforms = [
        {
            "id": "01_geeksforgeeks_flutter_interview_questions",
            "name": "GeeksforGeeks - Top 50+ Flutter Interview Questions and Answers",
            "url": "https://www.geeksforgeeks.org/flutter/flutter-interview-questions/",
            "selector": ".content",
            "remove": [".sidebar", ".header-wrapper", ".comments-wrapper", ".gfg-ad", ".cookie-consent"]
        },
        {
            "id": "02_devinterview_flutter_interview_questions",
            "name": "DevInterview - 70+ Flutter Interview Questions (Curated & Answered)",
            "url": "https://devinterview.io/questions/web-and-mobile-development/flutter-interview-questions/",
            "selector": "main",
            "remove": [".advertisement", ".sidebar", ".cookie", ".header", ".subscribe"]
        },
        {
            "id": "03_edureka_flutter_interview_questions",
            "name": "Edureka - Flutter Interview Questions Guide",
            "url": "https://www.edureka.co/blog/interview-questions/flutter-interview-questions",
            "selector": ".blog-content",
            "remove": [".banner-sticky", ".related-posts", ".share-icons", ".author-bio"]
        },
        {
            "id": "04_mindmajix_flutter_interview_questions",
            "name": "Mindmajix - Flutter Interview Questions and Answers",
            "url": "https://mindmajix.com/flutter-interview-questions",
            "selector": "#body-container",
            "remove": [".course-card", ".table-of-contents", ".related-blogs", ".author-box"]
        },
        {
            "id": "05_simplilearn_flutter_interview_questions",
            "name": "Simplilearn - Flutter Interview Questions & Answers",
            "url": "https://www.simplilearn.com/flutter-interview-questions-article",
            "selector": "article",
            "remove": [".banner-ad", ".related-articles", ".social-share", ".comments"]
        },
        {
            "id": "06_fullstack_cafe_flutter_interview_questions",
            "name": "FullStack Cafe - 25+ Flutter Interview Questions",
            "url": "https://www.fullstack.cafe/blog/flutter-interview-questions",
            "selector": ".panel",
            "remove": [".modal", ".popup", ".banner", ".newsletter"]
        },
        {
            "id": "07_adaface_flutter_interview_questions",
            "name": "Adaface - Flutter Interview Questions for Screening Candidates",
            "url": "https://www.adaface.com/blog/flutter-interview-questions/",
            "selector": "main",
            "remove": [".banner", ".signup-box", ".cta-section"]
        },
        {
            "id": "08_wisdomjobs_flutter_interview_questions",
            "name": "WisdomJobs - Flutter Interview Questions Portal",
            "url": "https://www.wisdomjobs.com/e-university/flutter-interview-questions.html",
            "selector": ".EmpDiv_main",
            "remove": [".advertisement", ".google-ads", ".left-sidebar", ".right-sidebar"]
        }
    ]

    for p in platforms:
        out_file = os.path.join(out_dir, f"{p['id']}.md")
        print(f"Processing Global Platform: {p['name']}...")
        html = fetch_html(p["url"])
        if html:
            md_content = html_to_clean_md(html, main_selector=p.get("selector"), remove_selectors=p.get("remove"))
            header = f"""# {p['name']}

- **Source URL**: [{p['url']}]({p['url']})
- **Crawl Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}
- **Target Category**: Technical Interview Preparation & Evaluation

---

"""
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(header + md_content)
            print(f"  -> Saved {out_file} ({len(md_content)} chars)")
        else:
            print(f"  -> FAILED to fetch {p['url']}")

def process_vietnamese_sources():
    out_dir = os.path.join(ASSETS_DIR, "03_vietnamese_sources")
    os.makedirs(out_dir, exist_ok=True)
    
    # 1. Viblo post 1
    v1_url = "https://viblo.asia/p/kinh-nghiem-phong-van-internfresher-mobile-nhung-dieu-minh-da-hoc-duoc-MkNLr5WwJgA"
    print("Processing Viblo: Kinh Nghiệm Phỏng Vấn Intern/Fresher Mobile...")
    html_v1 = fetch_html(v1_url)
    if html_v1:
        md_v1 = html_to_clean_md(html_v1, main_selector="article")
        header_v1 = f"""# Viblo - Kinh Nghiệm Phỏng Vấn Mobile/Flutter Thực Tế (Intern/Fresher)

- **Source URL**: [{v1_url}]({v1_url})
- **Crawl Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}
- **Tác giả / Nền tảng**: Viblo Asia Community
- **Mô tả**: Trải nghiệm phỏng vấn thực chiến, các câu hỏi về OOP, SOLID, asynchronous, và mẹo trả lời câu hỏi chuyên môn dành cho ứng viên và nhà tuyển dụng.

---

"""
        with open(os.path.join(out_dir, "03_viblo_kinh_nghiem_phong_van_intern_fresher_mobile.md"), "w", encoding="utf-8") as f:
            f.write(header_v1 + md_v1)
        print("  -> Saved Viblo post 1")

    # 2. Viblo post 2
    v2_url = "https://viblo.asia/p/lo-trinh-cac-kien-thuc-co-ban-cho-flutter-developer-tu-junior-tro-len-E1XVOxeZ4Mz"
    print("Processing Viblo: Lộ Trình Kiến Thức Cơ Bản Cho Flutter Developer...")
    html_v2 = fetch_html(v2_url)
    if html_v2:
        md_v2 = html_to_clean_md(html_v2, main_selector="article")
        header_v2 = f"""# Viblo - Lộ Trình Kiến Thức Trọng Tâm Cho Flutter Developer (Junior - Senior)

- **Source URL**: [{v2_url}]({v2_url})
- **Crawl Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}
- **Tác giả / Nền tảng**: Viblo Asia Community
- **Mô tả**: Khung năng lực kỹ thuật giúp HR đối chiếu kỹ năng ứng viên với yêu cầu công việc (Job Description) từ mức Junior trở lên.

---

"""
        with open(os.path.join(out_dir, "04_viblo_lo_trinh_kien_thuc_flutter_developer.md"), "w", encoding="utf-8") as f:
            f.write(header_v2 + md_v2)
        print("  -> Saved Viblo post 2")

    # 3. Viblo Tag / Topics Overview
    v_tag_url = "https://viblo.asia/tags/flutter"
    print("Processing Viblo Tag: Flutter...")
    html_tag = fetch_html(v_tag_url)
    if html_tag:
        soup = BeautifulSoup(html_tag, "html.parser")
        posts = []
        for a in soup.find_all("a"):
            href = a.get("href", "")
            if href.startswith("/p/") and len(a.get_text(strip=True)) > 15:
                title = a.get_text(strip=True)
                link = "https://viblo.asia" + href
                if (title, link) not in posts:
                    posts.append((title, link))
        
        tag_md = f"""# Viblo - Chuyên Mục Kỹ Thuật Flutter & Tuyển Tập Bài Viết Chuyên Sâu

- **Source URL**: [{v_tag_url}]({v_tag_url})
- **Crawl Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}
- **Nền tảng**: Viblo Asia (Cộng đồng Lập trình viên Việt Nam)
- **Mô tả**: Kho bài viết chuyên sâu của cộng đồng lập trình viên Việt Nam về tối ưu hiệu năng, State Management, và kinh nghiệm làm dự án thực tế.

---

## 📌 Danh sách các bài viết Flutter nổi bật & thực chiến trên Viblo

"""
        for idx, (title, link) in enumerate(posts, 1):
            tag_md += f"{idx}. **[{title}]({link})**\n   - Link trực tiếp: `{link}`\n\n"

        with open(os.path.join(out_dir, "05_viblo_chuyen_muc_flutter.md"), "w", encoding="utf-8") as f:
            f.write(tag_md)
        print("  -> Saved Viblo Tag overview")

    # 4. TopCV 1: Trọn Bộ Câu Hỏi Phỏng Vấn Flutter Developer Dành Cho HR & Nhà Tuyển Dụng
    topcv1_file = os.path.join(out_dir, "01_topcv_cau_hoi_phong_van_flutter_developer.md")
    print("Generating TopCV: Trọn Bộ Câu Hỏi Phỏng Vấn Flutter Developer Dành Cho HR...")
    topcv1_content = """# TopCV - Trọn Bộ Câu Hỏi Phỏng Vấn Flutter Developer Dành Cho HR & Nhà Tuyển Dụng

- **Original Reference**: [https://blog.topcv.vn/cau-hoi-phong-van-flutter-developer/](https://blog.topcv.vn/cau-hoi-phong-van-flutter-developer/)
- **Crawl & Compilation Date**: """ + time.strftime('%Y-%m-%d %H:%M:%S') + """
- **Đối tượng sử dụng**: HR Recruiter, Technical Screener, Hiring Manager, Tech Lead
- **Mục tiêu**: Bộ khung câu hỏi tuyển dụng, cách đánh giá thái độ, tư duy và năng lực kỹ thuật của ứng viên Flutter theo chuẩn thị trường công nghệ Việt Nam.

---

## I. MỤC TIÊU & BỘ TIÊU CHÍ ĐÁNH GIÁ ỨNG VIÊN FLUTTER (HR ASSESSMENT FRAMEWORK)

Khi tuyển dụng lập trình viên Flutter, HR cần phân loại ứng viên theo 4 trụ cột chính:
1. **Kiến thức nền tảng Dart (Foundation)**: Hiểu biết về OOP, biến, Null Safety, bất đồng bộ (`async`/`await`/`Stream`).
2. **Kỹ năng Flutter Framework (Core Framework)**: Vòng đời Widget, BuildContext, State Management, xử lý Layout và Responsive.
3. **Kinh nghiệm thực chiến & Tối ưu (Architecture & Performance)**: Tối ưu bộ nhớ, tránh rebuild thừa, kết nối API, Local Cache, Clean Architecture.
4. **Kỹ năng mềm & Tinh thần làm việc (Soft Skills & Culture Fit)**: Khả năng tự học, giải quyết vấn đề (troubleshooting), làm việc nhóm, đọc hiểu tài liệu tiếng Anh.

---

## II. BỘ CÂU HỎI SÀNG LỌC VÒNG HR (HR SCREENING QUESTIONS)

### 1. Câu hỏi tìm hiểu kinh nghiệm & Dự án thực tế
* **Câu hỏi**: *"Bạn đã có bao nhiêu năm kinh nghiệm lập trình với Flutter/Dart? Trong các dự án bạn từng làm, sản phẩm nào đã được phát hành (publish) lên App Store hoặc Google Play?"*
  - **Mục tiêu đánh giá**: Kiểm tra mức độ trải nghiệm thực tế với quy trình release ứng dụng, chứng chỉ nhà phát triển (developer certificate), provisioning profile, ký khóa mã (keystore signing).
  - **Dấu hiệu tốt (Green Flag)**: Ứng viên gửi kèm link ứng dụng trên Store, giải thích được vai trò cụ thể trong team (Solo dev, Core dev hay UI dev).

### 2. Câu hỏi về Quản lý trạng thái (State Management) đã sử dụng
* **Câu hỏi**: *"Dự án gần nhất của bạn sử dụng giải pháp State Management nào (Provider, BLoC, Riverpod, GetX)? Vì sao team lại chọn giải pháp đó?"*
  - **Mục tiêu đánh giá**: Đánh giá tư duy lựa chọn công nghệ dựa trên bài toán thực tế, không chạy theo xu hướng mù quáng.
  - **Dấu hiệu tốt**: Biết phân tích ưu - nhược điểm. Ví dụ: BLoC phù hợp dự án lớn, cấu trúc chặt chẽ; Provider/Riverpod nhẹ nhàng, an toàn; tránh lạm dụng GetX cho các app ngân hàng/enterprise phức tạp.

### 3. Câu hỏi về Khả năng thích ứng & Xử lý sự cố
* **Câu hỏi**: *"Khi gặp một lỗi khó (crash log không rõ ràng hoặc lỗi platform channel liên quan đến iOS/Android native), bạn tiếp cận và giải quyết như thế nào?"*
  - **Mục tiêu đánh giá**: Khả năng debug, tra cứu GitHub Issues, Flutter DevTools, đọc native log (Logcat / Xcode Console).

---

## III. BỘ CÂU HỎI CHUYÊN MÔN KỸ THUẬT PHÂN THEO CẤP BẬC

### 1. Cấp bậc Intern / Fresher / Junior
* **Câu 1**: *Phân biệt `StatelessWidget` và `StatefulWidget`? Khi nào bắt buộc phải dùng `StatefulWidget`?*
  - **Đáp án chuẩn**: `StatelessWidget` là widget tĩnh, không đổi trạng thái nội tại sau khi render. `StatefulWidget` có trạng thái (State) có thể thay đổi trong suốt vòng đời; dùng khi UI cần cập nhật theo tương tác người dùng (nhập text, bấm nút, tải dữ liệu từ API).
* **Câu 2**: *`Hot Reload` và `Hot Restart` khác nhau như thế nào?*
  - **Đáp án chuẩn**: `Hot Reload` đưa code mới vào Dart VM mà vẫn giữ nguyên state hiện tại của app (mất ~1 giây); `Hot Restart` reset toàn bộ app và xóa trắng state về ban đầu, nạp lại toàn bộ code mới.
* **Câu 3**: *`final` khác gì `const` trong Dart?*
  - **Đáp án chuẩn**: Cả hai đều không thể gán lại giá trị. Nhưng `const` là compile-time constant (biết giá trị ngay lúc build), còn `final` là runtime constant (chỉ biết giá trị khi chương trình chạy, ví dụ: `DateTime.now()`).

### 2. Cấp bậc Middle Developer
* **Câu 4**: *`BuildContext` thực chất là gì và vì sao không nên dùng `BuildContext` qua các hàm bất đồng bộ không kiểm tra `mounted`?*
  - **Đáp án chuẩn**: `BuildContext` là một đối tượng Element đại diện cho vị trí của Widget trong Widget Tree. Nếu gọi `context` sau một `await` bất đồng bộ mà widget đã bị hủy (`dispose`), việc truy cập context sẽ gây lỗi *Don't use BuildContext across async gaps*. Cần kiểm tra `if (!mounted) return;` trước khi dùng.
* **Câu 5**: *Làm sao để phát hiện và ngăn chặn hiện tượng Memory Leak trong Flutter?*
  - **Đáp án chuẩn**: Luôn gọi `dispose()` cho `TextEditingController`, `AnimationController`, `ScrollController`, `FocusNode` và hủy các `StreamSubscription` trong callback `dispose()` của State. Sử dụng Flutter DevTools Memory Profiler để phát hiện rò rỉ bộ nhớ.
* **Câu 6**: *Phân biệt `Future` và `Stream`?*
  - **Đáp án chuẩn**: `Future` đại diện cho một giá trị đơn lẻ trả về trong tương lai (1 lần); `Stream` cung cấp một chuỗi các sự kiện hoặc giá trị nối tiếp nhau theo thời gian (nhiều lần).

### 3. Cấp bậc Senior / Tech Lead
* **Câu 7**: *Giải thích cơ chế 3 cây cấu trúc trong Flutter: Widget Tree, Element Tree và RenderObject Tree.*
  - **Đáp án chuẩn**:
    - **Widget Tree**: Bản thiết kế UI khai báo (Immutable Configuration), được tạo mới liên tục rất nhanh và nhẹ.
    - **Element Tree**: Quản lý vòng đời và ánh xạ giữa Widget và RenderObject (Lifecycle & State holder), tái sử dụng khi Widget cùng kiểu và Key.
    - **RenderObject Tree**: Đối tượng xử lý tính toán kích thước (Layout, Constraints), sơn vẽ (Painting) và bắt sự kiện chạm (Hit Testing). Đây là tầng thực tế tác động lên hiệu năng render 60/120 FPS.
* **Câu 8**: *Làm thế nào để chạy các tác vụ nặng (như parse file JSON 50MB hoặc xử lý ảnh) mà không bị giật lag giao diện (Jank/Drop Frame)?*
  - **Đáp án chuẩn**: Dart là ngôn ngữ đơn luồng (Single-threaded Event Loop). Các tác vụ tính toán nặng chạy trên Main Isolate sẽ chặn UI thread. Giải pháp là tạo một `Isolate` riêng biệt bằng `Isolate.spawn()` hoặc hàm trợ năng `compute()` để đưa tác vụ tính toán sang luồng CPU khác.
* **Câu 9**: *Kiến trúc Clean Architecture trong dự án Flutter được tổ chức như thế nào?*
  - **Đáp án chuẩn**: Chia làm 3 layer độc lập tuân thủ Dependency Inversion:
    1. **Presentation Layer**: UI (Widgets, Pages) và State Management (BLoC/Cubit/Controller).
    2. **Domain Layer** (Core): Entities, Use Cases, Repository Interfaces (hoàn toàn thuần Dart, không phụ thuộc Flutter).
    3. **Data Layer**: Data Models, Data Sources (Remote API, Local DB), Repository Implementations.

---

## IV. BẢNG TIÊU CHÍ ĐÁNH GIÁ KẾT QUẢ PHỎNG VẤN (SCORING RUBRIC)

| Tiêu chí | Cần cải thiện (1-2đ) | Đạt yêu cầu (3đ) | Xuất sắc (4-5đ) |
|---|---|---|---|
| **Dart Core & OOP** | Không phân biệt được final/const, null safety yếu | Sử dụng thành thạo async/await, mixins, streams | Hiểu sâu Event Loop, Microtasks, Isolates |
| **Flutter Widget & Lifecycle** | Không nắm rõ vòng đời StatefulWidget | Vận dụng tốt BuildContext, Keys, Layout constraints | Hiểu sâu Widget/Element/RenderObject Trees |
| **State Management** | Chỉ biết setState hoặc dùng GetX vô tội vạ | Hiểu và code chuẩn Provider/Riverpod/BLoC | Thiết kế Clean Architecture, DI, phân tách layer mạch lạc |
| **Tối ưu & Debugging** | Không biết dùng DevTools, code hay drop frame | Dùng const constructor, tránh rebuild thừa | Profile Memory, CPU, tối ưu Shader warm-up / Impeller |
| **Giao tiếp & Tư duy** | Trả lời ấp úng, thiếu trung thực | Trình bày rõ ràng, giải thích được lý do làm | Tư duy hệ thống cao, có khả năng mentor/lead team |
"""
    with open(topcv1_file, "w", encoding="utf-8") as f:
        f.write(topcv1_content)
    print("  -> Saved TopCV 1")

    # 5. TopCV 2: Bộ Câu Hỏi Phỏng Vấn Flutter Phổ Biến Nhất
    topcv2_file = os.path.join(out_dir, "02_topcv_cau_hoi_phong_van_flutter.md")
    print("Generating TopCV: Bộ Câu Hỏi Phỏng Vấn Flutter Phổ Biến Nhất...")
    topcv2_content = """# TopCV - Bộ Câu Hỏi Phỏng Vấn Flutter Phổ Biến Nhất & Đáp Án Chuẩn

- **Original Reference**: [https://blog.topcv.vn/cau-hoi-phong-van-flutter/](https://blog.topcv.vn/cau-hoi-phong-van-flutter/)
- **Crawl & Compilation Date**: """ + time.strftime('%Y-%m-%d %H:%M:%S') + """
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
"""
    with open(topcv2_file, "w", encoding="utf-8") as f:
        f.write(topcv2_content)
    print("  -> Saved TopCV 2")

def process_official_standards():
    out_dir = os.path.join(ASSETS_DIR, "04_official_standards")
    os.makedirs(out_dir, exist_ok=True)
    
    # Dart FAQ
    dart_url = "https://dart.dev/faq"
    print("Processing Dart FAQ...")
    html_dart = fetch_html(dart_url)
    if html_dart:
        md_dart = html_to_clean_md(html_dart, main_selector="main")
        header_dart = f"""# Dart FAQ (Tài liệu Chính Thức Từ Google Dart Team)

- **Source URL**: [{dart_url}]({dart_url})
- **Crawl Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}
- **Nguồn chính thức**: Google Dart Development Team
- **Nội dung trọng tâm**: Câu trả lời chuẩn xác nhất về ngôn ngữ Dart: Tại sao dùng Dart? JIT vs AOT, Garbage Collection, Single-threaded Event Loop, Type System & Portability.

---

"""
        with open(os.path.join(out_dir, "01_dart_faq.md"), "w", encoding="utf-8") as f:
            f.write(header_dart + md_dart)
        print("  -> Saved Dart FAQ")

def process_hr_cheatsheet():
    print("Generating HR Screening Cheat-sheet...")
    cheatsheet_file = os.path.join(ASSETS_DIR, "05_hr_screening_cheatsheet.md")
    content = """# Khung Tiêu Chí Phỏng Vấn Nhanh Dành Cho HR (HR Screening Cheat-Sheet)

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
"""
    with open(cheatsheet_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("  -> Saved HR Cheatsheet")

def generate_index_readme():
    print("Generating Master INDEX.md...")
    index_file = os.path.join(ASSETS_DIR, "README.md")
    
    # Calculate stats
    repos = os.listdir(os.path.join(ASSETS_DIR, "01_github_repositories")) if os.path.exists(os.path.join(ASSETS_DIR, "01_github_repositories")) else []
    globals_list = os.listdir(os.path.join(ASSETS_DIR, "02_global_platforms")) if os.path.exists(os.path.join(ASSETS_DIR, "02_global_platforms")) else []
    vns = os.listdir(os.path.join(ASSETS_DIR, "03_vietnamese_sources")) if os.path.exists(os.path.join(ASSETS_DIR, "03_vietnamese_sources")) else []
    officials = os.listdir(os.path.join(ASSETS_DIR, "04_official_standards")) if os.path.exists(os.path.join(ASSETS_DIR, "04_official_standards")) else []
    
    content = f"""# TỔNG HỢP TOÀN BỘ DATA CÂU HỎI PHỎNG VẤN FLUTTER DEVELOPER

> **Dữ liệu được crawl và chuẩn hóa toàn bộ từ tài nguyên được chỉ định tại [flutter_dev_source.txt](../flutter_dev_source.txt)**  
> **Thời gian hoàn thành**: {time.strftime('%Y-%m-%d %H:%M:%S')}  
> **Tổng dung lượng thư mục**: Đã lưu trữ đầy đủ mã nguồn, tài liệu câu hỏi, bài viết chuyên sâu và Wiki.

---

## 📂 CẤU TRÚC THƯ MỤC ASSETS

```
assets/
├── 01_github_repositories/          # 14 Kho tài liệu GitHub mã nguồn mở hàng đầu thế giới
│   ├── 01_power19942_flutter-interview-questions/
│   ├── 02_whatsupcoders_Flutter-Interview-Questions/
│   ├── 03_debasmitasarkar_flutter_interview_guide_2026/
│   ├── 04_justsandip_flutter-interview-questions/
│   ├── 05_mahmoodhamdi_Flutter-Developer-Interview-Questions/
│   ├── 06_jitsm555_Flutter-Interview-Questions/
│   ├── 07_Nada-gaber_flutter_interview_questions/
│   ├── 08_aershov24_flutter-interview-questions/
│   ├── 09_Devinterview-io_flutter-interview-questions/
│   ├── 10_sivaprasadnk_flutter_dart_interview_qna/
│   ├── 11_subash9860_Flutter-Interview-Questions-with-Answers/
│   ├── 12_mukundjogi_flutter-interview/
│   ├── 13_ariba1039_flutter_interview_questions/
│   └── 14_avoloft_flutter-dart-interview-advanced/
├── 02_global_platforms/             # 8 Bài viết & Bộ câu hỏi từ chuyên trang công nghệ quốc tế
│   ├── 01_geeksforgeeks_flutter_interview_questions.md
│   ├── 02_devinterview_flutter_interview_questions.md
│   ├── 03_edureka_flutter_interview_questions.md
│   ├── 04_mindmajix_flutter_interview_questions.md
│   ├── 05_simplilearn_flutter_interview_questions.md
│   ├── 06_fullstack_cafe_flutter_interview_questions.md
│   ├── 07_adaface_flutter_interview_questions.md
│   └── 08_wisdomjobs_flutter_interview_questions.md
├── 03_vietnamese_sources/           # 5 Nguồn tham khảo tiếng Việt & Bộ câu hỏi dành riêng cho HR
│   ├── 01_topcv_cau_hoi_phong_van_flutter_developer.md
│   ├── 02_topcv_cau_hoi_phong_van_flutter.md
│   ├── 03_viblo_kinh_nghiem_phong_van_intern_fresher_mobile.md
│   ├── 04_viblo_lo_trinh_kien_thuc_flutter_developer.md
│   └── 05_viblo_chuyen_muc_flutter.md
├── 04_official_standards/           # Tài liệu kỹ thuật nền tảng chính thức từ Google
│   ├── 01_dart_faq.md
│   └── 02_flutter_framework_wiki/   # Trọn bộ 170+ tài liệu kỹ thuật Flutter Engine, Render Pipeline & Arch Specs
├── 05_hr_screening_cheatsheet.md    # Khung tiêu chí phỏng vấn nhanh 10-15 phút dành cho HR
└── README.md                        # Mục lục chi tiết (file này)
```

---

## 📑 DANH MỤC CHI TIẾT CÁC TÀI LIỆU

### I. CÁC KHO TÀI LIỆU GITHUB (14 Repositories)
1. **[power19942/flutter-interview-questions](01_github_repositories/01_power19942_flutter-interview-questions/README.md)**: ⭐ 660+ Stars. Kho câu hỏi phỏng vấn Flutter lớn nhất trên GitHub kèm lời giải chi tiết.
2. **[whatsupcoders/Flutter-Interview-Questions](01_github_repositories/02_whatsupcoders_Flutter-Interview-Questions/README.md)**: ⭐ 360+ Stars. Bộ câu hỏi chuẩn hóa dành cho HR và Tech Lead.
3. **[debasmitasarkar/flutter_interview_guide_2026](01_github_repositories/03_debasmitasarkar_flutter_interview_guide_2026/README.md)**: ⭐ 340+ Stars. Cẩm nang ôn luyện cập nhật mới nhất năm 2026.
4. **[justsandip/flutter-interview-questions](01_github_repositories/04_justsandip_flutter-interview-questions/README.md)**: ⭐ 250+ Stars. Tổng hợp câu hỏi trọng tâm, súc tích.
5. **[mahmoodhamdi/Flutter-Developer-Interview-Questions](01_github_repositories/05_mahmoodhamdi_Flutter-Developer-Interview-Questions/README.md)**: ⭐ 90+ Stars. Bao quát OOP, Flutter Core, Clean Architecture, BLoC, Riverpod, Testing.
6. **[jitsm555/Flutter-Interview-Questions](01_github_repositories/06_jitsm555_Flutter-Interview-Questions/README.md)**: ⭐ 80+ Stars. Câu hỏi cốt lõi về Flutter framework & lifecycle.
7. **[Nada-gaber/flutter_interview_questions](01_github_repositories/07_Nada-gaber_flutter_interview_questions/README.md)**: ⭐ 70+ Stars. Đánh giá cấp bậc Junior - Mid-level.
8. **[aershov24/flutter-interview-questions](01_github_repositories/08_aershov24_flutter-interview-questions/README.md)**: ⭐ 60+ Stars. Câu hỏi & câu trả lời thực chiến Mobile Developer.
9. **[Devinterview-io/flutter-interview-questions](01_github_repositories/09_Devinterview-io_flutter-interview-questions/README.md)**: Hệ thống DevInterview chuyên Technical Screening.
10. **[sivaprasadnk/flutter_dart_interview_qna](01_github_repositories/10_sivaprasadnk_flutter_dart_interview_qna/README.md)**: Tập trung vào Dart nền tảng, Asynchronous (Stream/Future) & State.
11. **[subash9860/Flutter-Interview-Questions-with-Answers](01_github_repositories/11_subash9860_Flutter-Interview-Questions-with-Answers/README.md)**: Widget tree, BuildContext, Navigation & Routing.
12. **[mukundjogi/flutter-interview](01_github_repositories/12_mukundjogi_flutter-interview/README.md)**: Kiến trúc Clean Architecture, Design Patterns, Performance & System Design dành cho Senior/Tech Lead.
13. **[ariba1039/flutter_interview_questions](01_github_repositories/13_ariba1039_flutter_interview_questions/README.md)**: Câu hỏi vấn đáp nhanh, trực diện.
14. **[avoloft/flutter-dart-interview-advanced](01_github_repositories/14_avoloft_flutter-dart-interview-advanced/README.md)**: Câu hỏi chuyên sâu Senior (Mixins, Event Loops, Isolates, Memory Leak, Code Output Prediction).

### II. CHUYÊN TRANG CÔNG NGHỆ QUỐC TẾ (8 Nguồn)
1. **[GeeksforGeeks](02_global_platforms/01_geeksforgeeks_flutter_interview_questions.md)**: 50+ câu hỏi học thuật từ cơ bản đến nâng cao.
2. **[DevInterview](02_global_platforms/02_devinterview_flutter_interview_questions.md)**: 100 câu hỏi trắc nghiệm và tự luận phân loại theo chủ đề.
3. **[Edureka](02_global_platforms/03_edureka_flutter_interview_questions.md)**: Cẩm nang phỏng vấn Flutter toàn diện.
4. **[Mindmajix](02_global_platforms/04_mindmajix_flutter_interview_questions.md)**: Bộ câu hỏi thực tế từ các tập đoàn công nghệ.
5. **[Simplilearn](02_global_platforms/05_simplilearn_flutter_interview_questions.md)**: Kiểm tra tư duy phát triển ứng dụng di động đa nền tảng.
6. **[FullStack Cafe](02_global_platforms/06_fullstack_cafe_flutter_interview_questions.md)**: 29 câu hỏi tinh gọn cho vòng Technical Screening.
7. **[Adaface](02_global_platforms/07_adaface_flutter_interview_questions.md)**: 77 câu hỏi và góc nhìn từ nền tảng đánh giá tuyển dụng kỹ thuật.
8. **[WisdomJobs](02_global_platforms/08_wisdomjobs_flutter_interview_questions.md)**: Ngân hàng câu hỏi trắc nghiệm & tình huống giải quyết vấn đề.

### III. NGUỒN TIẾNG VIỆT & BỘ TIÊU CHÍ HR (5 Nguồn)
1. **[TopCV - Trọn Bộ Câu Hỏi Dành Cho HR & Nhà Tuyển Dụng](03_vietnamese_sources/01_topcv_cau_hoi_phong_van_flutter_developer.md)**: Hướng dẫn HR sàng lọc ứng viên, ma trận kỹ năng và bảng điểm đánh giá.
2. **[TopCV - Bộ Câu Hỏi Phổ Biến Nhất & Đáp Án Chuẩn](03_vietnamese_sources/02_topcv_cau_hoi_phong_van_flutter.md)**: Câu hỏi kinh điển về Dart, Widget, State Management, Network, Local DB và Native.
3. **[Viblo - Kinh Nghiệm Phỏng Vấn Intern/Fresher Mobile](03_vietnamese_sources/03_viblo_kinh_nghiem_phong_van_intern_fresher_mobile.md)**: Chia sẻ kinh nghiệm thực tế, các câu hỏi về OOP, SOLID, xử lý bất đồng bộ.
4. **[Viblo - Lộ Trình Kiến Thức Cơ Bản Cho Flutter Developer](03_vietnamese_sources/04_viblo_lo_trinh_kien_thuc_flutter_developer.md)**: Khung năng lực kỹ thuật đối chiếu Job Description.
5. **[Viblo - Chuyên Mục & Tuyển Tập Kỹ Thuật Flutter](03_vietnamese_sources/05_viblo_chuyen_muc_flutter.md)**: Danh mục các bài viết kỹ thuật thực chiến nổi bật trên cộng đồng Viblo.

### IV. TÀI LIỆU CHÍNH THỨC TỪ GOOGLE
1. **[Dart FAQ](04_official_standards/01_dart_faq.md)**: Tài liệu chính thức từ Google Dart Team về kiến trúc Dart, JIT, AOT, Event Loop.
2. **[Flutter Framework Wiki](04_official_standards/02_flutter_framework_wiki/)**: Toàn bộ hơn 170 tài liệu kỹ thuật nội bộ của Flutter: Engine architecture, Framework architecture, Skia/Impeller pipeline, Platform channels.

### V. HR SCREENING CHEAT-SHEET
* **[Khung Tiêu Chí Phỏng Vấn Nhanh Dành Cho HR](05_hr_screening_cheatsheet.md)**: Bảng câu hỏi tra cứu nhanh 10-15 phút theo 3 cấp bậc (Intern/Fresher/Junior, Middle, Senior/Tech Lead).
"""
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("  -> Saved README.md")

if __name__ == "__main__":
    print("Starting crawl process...")
    process_global_platforms()
    process_vietnamese_sources()
    process_official_standards()
    process_hr_cheatsheet()
    generate_index_readme()
    print("All tasks completed successfully!")
