#!/usr/bin/env python3
"""
Playwright 娴忚鍣ㄨ嚜鍔ㄥ寲楠屾敹銆?
鍔熻兘:
1. 鍚姩 headless 娴忚鍣?2. 閫愰〉鎴浘锛堚墺3 椤碉級
3. 娣辨祬涓婚鍒囨崲鎴浘
4. 375px 绉诲姩绔埅鍥?5. 浜у嚭 uat-report.json
"""
import sys
import json
import time
from pathlib import Path
from datetime import datetime


def run_browser_uat(project_dir, url, min_pages=3):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("FAIL 鈥?闇€瑕佸畨瑁?playwright: pip install playwright && playwright install chromium")
        return False

    project = Path(project_dir)
    screenshots_dir = project / ".harness" / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    report = {
        "mode": "browser",
        "url": url,
        "timestamp": datetime.now().isoformat(),
        "pages": [],
        "themes": {"light": [], "dark": []},
        "mobile": [],
        "passed": False,
    }

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": 1280, "height": 800})

            print(f"鍚姩娴忚鍣ㄩ獙鏀? {url}")

            # 涓婚〉闈㈡埅鍥?            page = context.new_page()
            page.goto(url, timeout=10000)
            page.wait_for_load_state("networkidle", timeout=5000)
            time.sleep(1)

            main_path = screenshots_dir / "page-main.png"
            page.screenshot(path=str(main_path), full_page=True)
            report["pages"].append({"name": "main", "path": str(main_path), "width": 1280})
            print(f"  鉁?涓婚〉闈㈡埅鍥? {main_path}")

            # 娴呰壊涓婚
            page.evaluate("document.documentElement.setAttribute('data-theme', 'light')")
            time.sleep(0.3)
            light_path = screenshots_dir / "theme-light.png"
            page.screenshot(path=str(light_path))
            report["themes"]["light"].append(str(light_path))
            print(f"  鉁?娴呰壊涓婚: {light_path}")

            # 娣辫壊涓婚
            page.evaluate("document.documentElement.setAttribute('data-theme', 'dark')")
            time.sleep(0.3)
            dark_path = screenshots_dir / "theme-dark.png"
            page.screenshot(path=str(dark_path))
            report["themes"]["dark"].append(str(dark_path))
            print(f"  鉁?娣辫壊涓婚: {dark_path}")

            # 绉诲姩绔?375px
            page.set_viewport_size({"width": 375, "height": 812})
            time.sleep(0.3)
            mobile_path = screenshots_dir / "mobile-375.png"
            page.screenshot(path=str(mobile_path))
            report["mobile"].append({"path": str(mobile_path), "width": 375})
            print(f"  鉁?绉诲姩绔?375px: {mobile_path}")

            # 灏濊瘯鐐瑰嚮瀵艰埅閾炬帴鎴洿澶氶〉
            nav_links = page.query_selector_all("nav a, .nav a, [class*=nav] a, [class*=menu] a")
            for i, link in enumerate(nav_links[:min_pages - 1]):
                try:
                    href = link.get_attribute("href")
                    if href and not href.startswith("http") and not href.startswith("#"):
                        page.goto(f"{url.rstrip('/')}/{href.lstrip('/')}", timeout=5000)
                        time.sleep(0.5)
                        extra_path = screenshots_dir / f"page-{i + 1}.png"
                        page.screenshot(path=str(extra_path), full_page=True)
                        report["pages"].append({"name": f"page-{i + 1}", "path": str(extra_path)})
                        print(f"  鉁?瀛愰〉闈? {extra_path}")
                except Exception:
                    pass

            browser.close()

        total_screenshots = len(report["pages"]) + len(report["themes"]["light"]) + len(report["themes"]["dark"]) + len(report["mobile"])
        report["total_screenshots"] = total_screenshots

        if len(report["pages"]) >= min_pages and report["themes"]["light"] and report["themes"]["dark"] and report["mobile"]:
            report["passed"] = True
        else:
            issues = []
            if len(report["pages"]) < min_pages:
                issues.append(f"椤甸潰鎴浘鏁?{len(report['pages'])} < {min_pages}")
            if not report["themes"]["light"]:
                issues.append("缂哄皯娴呰壊涓婚鎴浘")
            if not report["themes"]["dark"]:
                issues.append("缂哄皯娣辫壊涓婚鎴浘")
            if not report["mobile"]:
                issues.append("缂哄皯绉诲姩绔埅鍥?)
            report["issues"] = issues

        report_path = screenshots_dir / "uat-report.json"
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

        if report["passed"]:
            print(f"\nPASS 鈥?娴忚鍣ㄩ獙鏀堕€氳繃 ({total_screenshots} 寮犳埅鍥?")
        else:
            print(f"\nFAIL 鈥?娴忚鍣ㄩ獙鏀朵笉閫氳繃")
            for i in report.get("issues", []):
                print(f"  鈫?{i}")
        return report["passed"]

    except Exception as e:
        print(f"FAIL 鈥?娴忚鍣ㄩ獙鏀跺紓甯? {e}")
        report["error"] = str(e)
        (screenshots_dir / "uat-report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("鐢ㄦ硶: browser_uat.py <椤圭洰鐩綍> <URL> [鏈€灏戦〉鏁癩")
        sys.exit(1)
    proj = sys.argv[1]
    u = sys.argv[2]
    mp = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    ok = run_browser_uat(proj, u, mp)
    sys.exit(0 if ok else 1)
