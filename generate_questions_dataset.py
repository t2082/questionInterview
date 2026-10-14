#!/usr/bin/env python3
"""
generate_questions_dataset.py
Parses and normalizes questions from assets/ into a structured database.
Outputs:
  - data/questions.js (for offline file:// compatibility)
  - data/questions.json
"""

import os
import re
import glob
import json

BASE_DIR = "/Users/akuro/AkuroWorkpage/practive_skill"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

questions = []
seen_titles = set()

def normalize_title(title):
    t = title.strip()
    t = re.sub(r"^[\*\#\-\d\.\:\s\(\)]+", "", t)
    t = re.sub(r"\\([\.])", r"\1", t)
    t = t.strip()
    t = re.sub(r"^[Qq]\d+[\.\:\s]+", "", t)
    t = t.strip(" *`_:")
    return t

def categorize_question(title, content):
    tc = (title + " " + content[:300]).lower()
    if any(k in tc for k in ["hr screening", "lương", "văn hóa", "ứng viên", "tuyển dụng", "soft skill", "rubric", "red flag", "green flag", "kinh nghiệm phỏng vấn"]):
        return "HR & Tuyển Dụng"
    if any(k in tc for k in ["dart", "null safety", "var vs", "final vs const", "mixin", "extension method", "fat arrow", "cascading"]):
        return "Dart Fundamentals"
    if any(k in tc for k in ["bloc", "provider", "riverpod", "getx", "redux", "state management", "cubit"]):
        return "State Management"
    if any(k in tc for k in ["widget", "stateless", "stateful", "buildcontext", "keys", "element", "renderobject", "lifecycle", "row", "column", "scaffold", "listview"]):
        return "Widgets & UI Core"
    if any(k in tc for k in ["clean architecture", "mvvm", "mvc", "solid", "dependency injection", "get_it", "design pattern", "repository"]):
        return "Kiến Trúc & Clean Code"
    if any(k in tc for k in ["performance", "memory leak", "jank", "fps", "repaintboundary", "tree shaking", "shader", "impeller", "skia", "profiler", "devtools"]):
        return "Tối Ưu Hiệu Năng"
    if any(k in tc for k in ["isolate", "future", "stream", "async", "await", "event loop", "microtask", "concurrency"]):
        return "Bất Đồng Bộ & Isolates"
    if any(k in tc for k in ["platform channel", "methodchannel", "eventchannel", "swift", "kotlin", "native", "pigeon"]):
        return "Native Integration"
    if any(k in tc for k in ["dio", "http", "api", "sqlite", "sqflite", "hive", "sharedpreferences", "caching", "json"]):
        return "Mạng & Lưu Trữ"
    if any(k in tc for k in ["unit test", "widget test", "integration test", "golden test", "ci/cd", "fastlane", "github actions"]):
        return "Kiểm Thử & DevOps"
    return "Flutter Core"

def infer_level(title, content, default="Junior"):
    tc = (title + " " + content[:200]).lower()
    if any(k in tc for k in ["isolate", "renderobject", "clean architecture", "memory leak", "event loop", "profiling", "shader", "impeller", "custom painter", "platform channel", "senior", "lead", "expert"]):
        return "Senior"
    if any(k in tc for k in ["bloc", "riverpod", "inheritedwidget", "dio", "sqflite", "hive", "interceptor", "mounted", "key", "builder", "middle", "intermediate"]):
        return "Middle"
    if any(k in tc for k in ["fresher", "intern", "what is flutter", "stateless", "hot reload", "hot restart", "final vs const", "basic", "easy"]):
        return "Fresher"
    return default

def add_question(title, answer, source, lang="en", level=None, category=None, source_url=""):
    clean_t = normalize_title(title)
    if len(clean_t) < 8 or len(clean_t) > 250:
        return
    norm_key = re.sub(r"[^a-zA-Z0-9\u00C0-\u1EF9]", "", clean_t.lower())
    if len(norm_key) < 5 or norm_key in seen_titles:
        return
    seen_titles.add(norm_key)
    
    clean_ans = answer.strip()
    if len(clean_ans) < 20:
        return
    # Truncate overly massive answers if over 8000 chars
    if len(clean_ans) > 8000:
        clean_ans = clean_ans[:8000] + "\n\n*(Xem thêm chi tiết trong mã nguồn gốc...)*"
        
    inferred_cat = category or categorize_question(clean_t, clean_ans)
    inferred_lvl = level or infer_level(clean_t, clean_ans)
    
    q_id = f"flutter-q-{len(questions) + 1:04d}"
    questions.append({
        "id": q_id,
        "title": clean_t,
        "answer": clean_ans,
        "category": inferred_cat,
        "level": inferred_lvl,
        "source": source,
        "source_url": source_url,
        "lang": lang
    })

# 1. Parse Vietnamese Sources (TopCV, Viblo, Cheatsheet)
def parse_vietnamese():
    # TopCV 1
    p1 = os.path.join(ASSETS_DIR, "03_vietnamese_sources/01_topcv_cau_hoi_phong_van_flutter_developer.md")
    if os.path.exists(p1):
        with open(p1, "r", encoding="utf-8") as f:
            content = f.read()
        # Parse questions starting with * **Câu
        matches = re.split(r"\n(?=\*\s+\*\*Câu)", content)
        for m in matches[1:]:
            tm = re.search(r"\*\s+\*\*Câu[^\*]+\*\*:\s*\*([^\*]+)\*", m)
            if tm:
                title = tm.group(1).strip()
                ans = m[tm.end():].strip()
                add_question(title, ans, "TopCV - Tuyển Dụng & HR Flutter", "vi", source_url="https://blog.topcv.vn/cau-hoi-phong-van-flutter-developer/")

    # TopCV 2
    p2 = os.path.join(ASSETS_DIR, "03_vietnamese_sources/02_topcv_cau_hoi_phong_van_flutter.md")
    if os.path.exists(p2):
        with open(p2, "r", encoding="utf-8") as f:
            content = f.read()
        matches = re.split(r"\n(?=####\s+Q\d+:)", content)
        for m in matches[1:]:
            tm = re.search(r"####\s+Q\d+:\s*([^\n]+)", m)
            if tm:
                title = tm.group(1).strip()
                ans = m[tm.end():].strip()
                add_question(title, ans, "TopCV - Bộ Câu Hỏi Kinh Điển", "vi", source_url="https://blog.topcv.vn/cau-hoi-phong-van-flutter/")

    # Viblo 1
    v1 = os.path.join(ASSETS_DIR, "03_vietnamese_sources/03_viblo_kinh_nghiem_phong_van_intern_fresher_mobile.md")
    if os.path.exists(v1):
        with open(v1, "r", encoding="utf-8") as f:
            v_content = f.read()
        # Extract headings or sections
        for chunk in re.split(r"\n(?=###?\s+)", v_content):
            hm = re.match(r"###?\s+([^\n]+)", chunk)
            if hm and len(hm.group(1)) > 15:
                title = hm.group(1).strip()
                ans = chunk[hm.end():].strip()
                add_question(title, ans, "Viblo - Kinh Nghiệm Thực Chiến Intern/Fresher", "vi", "Fresher", source_url="https://viblo.asia/p/kinh-nghiem-phong-van-internfresher-mobile-nhung-dieu-minh-da-hoc-duoc-MkNLr5WwJgA")

    # HR Cheatsheet
    cs = os.path.join(ASSETS_DIR, "05_hr_screening_cheatsheet.md")
    if os.path.exists(cs):
        with open(cs, "r", encoding="utf-8") as f:
            cs_content = f.read()
        # Extract bullet question points
        for bp in re.findall(r"\*\s+`([^`]+)`(?:\s+vs\s+`([^`]+)`)?:\s*([^\n]+)", cs_content):
            title = f"Phân biệt `{bp[0]}` và `{bp[1]}` trong lập trình Flutter/Dart" if bp[1] else f"Khái niệm `{bp[0]}` trong Flutter"
            ans = bp[2]
            add_question(title, ans, "HR Screening Cheat-Sheet", "vi")

# 2. Parse debasmitasarkar Guide 2026
def parse_debasmitasarkar():
    guide_files = glob.glob(os.path.join(ASSETS_DIR, "01_github_repositories/03_debasmitasarkar_flutter_interview_guide_2026/**/*.md"), recursive=True)
    for gf in guide_files:
        if "README.md" not in gf: continue
        lvl = "Junior" if "junior" in gf else "Middle" if "mid-level" in gf else "Senior" if "senior" in gf else "Expert" if "expert" in gf else "General"
        with open(gf, "r", encoding="utf-8", errors="replace") as f:
            chunks = re.split(r"\n(?=###?\s+\d+[\.\)])", f.read())
        for c in chunks[1:]:
            hm = re.match(r"###?\s+\d+[\.\)]\s*(.+)", c)
            if hm:
                title = hm.group(1).strip()
                ans = c[hm.end():].strip()
                add_question(title, ans, "debasmitasarkar / flutter_interview_guide_2026", "en", lvl, source_url="https://github.com/debasmitasarkar/flutter_interview_guide_2026")

# 3. Parse justsandip Questions
def parse_justsandip():
    path = os.path.join(ASSETS_DIR, "01_github_repositories/04_justsandip_flutter-interview-questions/README.md")
    if not os.path.exists(path): return
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        chunks = re.split(r"\n(?=###\s+)", f.read())
    for c in chunks[1:]:
        hm = re.match(r"###\s+(.+)", c)
        if hm:
            title = hm.group(1).strip()
            if len(title) > 10 and not title.startswith("Table of Contents"):
                ans = c[hm.end():].strip()
                ans = re.sub(r"\[\s*Back to top\s*\].+", "", ans, flags=re.I).strip()
                add_question(title, ans, "justsandip / flutter-interview-questions", "en", source_url="https://github.com/justsandip/flutter-interview-questions")

# 4. Parse power19942 Questions
def parse_power19942():
    path = os.path.join(ASSETS_DIR, "01_github_repositories/01_power19942_flutter-interview-questions/README.md")
    if not os.path.exists(path): return
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        chunks = re.split(r"\n(?=\d+[\.\)]\s*)", f.read())
    for c in chunks[1:]:
        hm = re.match(r"(\d+)[\.\)]\s*(.+)", c)
        if hm:
            title = hm.group(2).strip()
            ans = c[hm.end():].strip()
            add_question(title, ans, "power19942 / flutter-interview-questions", "en", source_url="https://github.com/power19942/flutter-interview-questions")

# 5. Parse Mahmood Hamdi Repository
def parse_mahmoodhamdi():
    base = os.path.join(ASSETS_DIR, "01_github_repositories/05_mahmoodhamdi_Flutter-Developer-Interview-Questions")
    ans_files = glob.glob(f"{base}/**/answers.md", recursive=True)
    for af in ans_files:
        cat_folder = os.path.basename(os.path.dirname(af))
        with open(af, "r", encoding="utf-8", errors="replace") as f:
            chunks = re.split(r"\n(?=###?\s+)", f.read())
        for c in chunks[1:]:
            hm = re.match(r"###?\s+([^\n]+)", c)
            if hm:
                title = hm.group(1).strip()
                ans = c[hm.end():].strip()
                add_question(title, ans, f"mahmoodhamdi / {cat_folder}", "en", source_url="https://github.com/mahmoodhamdi/Flutter-Developer-Interview-Questions")

# 6. Parse Global Platforms
def parse_global_platforms():
    # DevInterview
    dev_path = os.path.join(ASSETS_DIR, "02_global_platforms/02_devinterview_flutter_interview_questions.md")
    if os.path.exists(dev_path):
        with open(dev_path, "r", encoding="utf-8", errors="replace") as f:
            chunks = re.split(r"\n(?=###\s+)", f.read())
        for c in chunks[1:]:
            hm = re.match(r"###\s+([^\n]+)", c)
            if hm:
                title = hm.group(1).strip()
                ans = c[hm.end():].strip()
                # Clean prefix Question / Answer
                ans = re.sub(r"^Question\s+Answer:\s*", "", ans, flags=re.I).strip()
                add_question(title, ans, "DevInterview.io - 100 Must-Know Questions", "en", source_url="https://devinterview.io/questions/web-and-mobile-development/flutter-interview-questions/")

    # GeeksforGeeks
    gfg_path = os.path.join(ASSETS_DIR, "02_global_platforms/01_geeksforgeeks_flutter_interview_questions.md")
    if os.path.exists(gfg_path):
        with open(gfg_path, "r", encoding="utf-8", errors="replace") as f:
            chunks = re.split(r"\n(?=###\s+\d+\\\.\s+)", f.read())
        for c in chunks[1:]:
            hm = re.match(r"###\s+\d+\\\.\s+([^\n]+)", c)
            if hm:
                title = hm.group(1).strip()
                ans = c[hm.end():].strip()
                add_question(title, ans, "GeeksforGeeks - Top 50+ Flutter Interview Questions", "en", source_url="https://www.geeksforgeeks.org/flutter/flutter-interview-questions/")

    # FullStack Cafe
    fc_path = os.path.join(ASSETS_DIR, "02_global_platforms/06_fullstack_cafe_flutter_interview_questions.md")
    if os.path.exists(fc_path):
        with open(fc_path, "r", encoding="utf-8", errors="replace") as f:
            chunks = re.split(r"\n(?=##\s+_?Q\d+_?\s*:)", f.read())
        for c in chunks[1:]:
            lines = c.strip().split("\n")
            title = lines[0]
            if len(lines) > 1 and len(title) < 25:
                # First line might just be Q1, next line is question
                title = lines[1].strip("# *`_")
                ans = "\n".join(lines[2:]).strip()
            else:
                ans = "\n".join(lines[1:]).strip()
            add_question(title, ans, "FullStack Cafe - Technical Screening", "en", source_url="https://www.fullstack.cafe/blog/flutter-interview-questions")

    # Edureka
    edu_path = os.path.join(ASSETS_DIR, "02_global_platforms/03_edureka_flutter_interview_questions.md")
    if os.path.exists(edu_path):
        with open(edu_path, "r", encoding="utf-8", errors="replace") as f:
            chunks = re.split(r"\n(?=\*\*\d+\\\.\s+)", f.read())
        for c in chunks[1:]:
            hm = re.match(r"\*\*\d+\\\.\s+([^\*]+)\*\*", c)
            if hm:
                title = hm.group(1).strip()
                ans = c[hm.end():].strip()
                add_question(title, ans, "Edureka - Flutter Interview Guide", "en", source_url="https://www.edureka.co/blog/interview-questions/flutter-interview-questions")

    # Mindmajix
    mm_path = os.path.join(ASSETS_DIR, "02_global_platforms/04_mindmajix_flutter_interview_questions.md")
    if os.path.exists(mm_path):
        with open(mm_path, "r", encoding="utf-8", errors="replace") as f:
            chunks = re.split(r"\n(?=###\s+\d+\\\.\s+)", f.read())
        for c in chunks[1:]:
            hm = re.match(r"###\s+\d+\\\.\s+([^\n]+)", c)
            if hm:
                title = hm.group(1).strip()
                ans = c[hm.end():].strip()
                add_question(title, ans, "Mindmajix - Flutter Real-World Questions", "en", source_url="https://mindmajix.com/flutter-interview-questions")

    # Simplilearn
    sl_path = os.path.join(ASSETS_DIR, "02_global_platforms/05_simplilearn_flutter_interview_questions.md")
    if os.path.exists(sl_path):
        with open(sl_path, "r", encoding="utf-8", errors="replace") as f:
            chunks = re.split(r"\n(?=###\s+\d+\.?\s+)", f.read())
        for c in chunks[1:]:
            hm = re.match(r"###\s+\d+\.?\s+([^\n]+)", c)
            if hm:
                title = hm.group(1).strip()
                ans = c[hm.end():].strip()
                add_question(title, ans, "Simplilearn - Mobile Dev Screening", "en", source_url="https://www.simplilearn.com/flutter-interview-questions-article")

    # Adaface
    ada_path = os.path.join(ASSETS_DIR, "02_global_platforms/07_adaface_flutter_interview_questions.md")
    if os.path.exists(ada_path):
        with open(ada_path, "r", encoding="utf-8", errors="replace") as f:
            chunks = re.split(r"\n(?=###?\s+\d+[\.\)]\s*)", f.read())
        for c in chunks[1:]:
            hm = re.match(r"###?\s+\d+[\.\)]\s*([^\n]+)", c)
            if hm:
                title = hm.group(1).strip()
                ans = c[hm.end():].strip()
                add_question(title, ans, "Adaface - Candidate Screening Guide", "en", source_url="https://www.adaface.com/blog/flutter-interview-questions/")

# 7. Parse Dart FAQ
def parse_dart_faq():
    df_path = os.path.join(ASSETS_DIR, "04_official_standards/01_dart_faq.md")
    if not os.path.exists(df_path): return
    with open(df_path, "r", encoding="utf-8", errors="replace") as f:
        chunks = re.split(r"\n(?=##\s+)", f.read())
    for c in chunks[1:]:
        hm = re.match(r"##\s+([^\n]+)", c)
        if hm and "?" in hm.group(1):
            title = hm.group(1).strip()
            ans = c[hm.end():].strip()
            add_question(title, ans, "Google Dart Official Team (Dart FAQ)", "en", "Senior", "Dart Fundamentals", source_url="https://dart.dev/faq")

if __name__ == "__main__":
    print("Extracting questions from all assets...")
    parse_vietnamese()
    parse_debasmitasarkar()
    parse_justsandip()
    parse_power19942()
    parse_mahmoodhamdi()
    parse_global_platforms()
    parse_dart_faq()
    
    print(f"Total deduplicated, curated questions extracted: {len(questions)}")
    
    # Save as JSON
    json_path = os.path.join(DATA_DIR, "questions.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    print(f"Saved: {json_path}")
    
    # Save as JS for direct offline file:// load without CORS issues
    js_path = os.path.join(DATA_DIR, "questions.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write("// Auto-generated Flutter & Dart Interview Question Dataset\n")
        f.write("window.FLUTTER_QUESTIONS = ")
        json.dump(questions, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    print(f"Saved: {js_path}")
