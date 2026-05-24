#!/usr/bin/env python3
"""
瑙嗚楠屾敹 鈥?妫€鏌ヨ棰?璁捐椤圭洰鐨勭敾闈骇鍑恒€?浜у嚭 visual-uat-report.json
"""
import sys
import json
from pathlib import Path
from datetime import datetime


def run_visual_uat(project_dir):
    project = Path(project_dir)
    results_dir = project / ".harness"
    results_dir.mkdir(parents=True, exist_ok=True)

    report = {
        "mode": "visual",
        "timestamp": datetime.now().isoformat(),
        "checks": {},
        "overall": False,
    }

    # 妫€鏌ュ垎闀滄枃浠?    storyboard = project / "storyboard.json"
    design_brief = project / "design-brief.json"
    frame_dirs = [project / "frames", project / "screenshots", project / "output"]

    has_frames = False
    for d in frame_dirs:
        if d.exists() and any(d.iterdir()):
            frames = list(d.glob("*.png")) + list(d.glob("*.jpg")) + list(d.glob("*.webp"))
            report["checks"]["frames"] = {
                "passed": len(frames) >= 3,
                "count": len(frames),
                "dir": str(d),
            }
            has_frames = True
            print(f"  鐢婚潰鏂囦欢: {len(frames)} 涓?)
            break

    if not has_frames:
        report["checks"]["frames"] = {
            "passed": False,
            "count": 0,
            "detail": "鏃犵敾闈㈡枃浠剁洰褰?,
        }
        print("  鈿?鏃犵敾闈㈡枃浠?)

    # 妫€鏌ュ垎闀滆剼鏈?    if storyboard.exists():
        try:
            sb = json.loads(storyboard.read_text(encoding="utf-8"))
            scenes = sb.get("scenes", [])
            report["checks"]["storyboard"] = {
                "passed": len(scenes) >= 3,
                "scenes": len(scenes),
            }
            print(f"  鍒嗛暅鍦烘櫙: {len(scenes)} 涓?)
        except Exception:
            report["checks"]["storyboard"] = {"passed": False, "detail": "JSON 瑙ｆ瀽澶辫触"}
    elif design_brief.exists():
        try:
            db = json.loads(design_brief.read_text(encoding="utf-8"))
            elements = db.get("elements", [])
            report["checks"]["design_brief"] = {
                "passed": len(elements) >= 1,
                "elements": len(elements),
            }
            print(f"  璁捐鍏冪礌: {len(elements)} 涓?)
        except Exception:
            report["checks"]["design_brief"] = {"passed": False, "detail": "JSON 瑙ｆ瀽澶辫触"}
    else:
        report["checks"]["storyboard"] = {"passed": False, "detail": "缂哄皯 storyboard.json 鎴?design-brief.json"}

    all_checks = report["checks"]
    report["overall"] = all(c.get("passed", False) for c in all_checks.values())

    (results_dir / "visual-uat-report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    if report["overall"]:
        print("PASS 鈥?瑙嗚楠屾敹閫氳繃")
    else:
        print("FAIL 鈥?瑙嗚楠屾敹涓嶉€氳繃")
        for k, v in all_checks.items():
            if not v.get("passed"):
                print(f"  鈫?{k}: {v.get('detail', v)}")
    return report["overall"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("鐢ㄦ硶: visual_uat.py <椤圭洰鐩綍>")
        sys.exit(1)
    ok = run_visual_uat(sys.argv[1])
    sys.exit(0 if ok else 1)
