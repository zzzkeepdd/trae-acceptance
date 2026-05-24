#!/usr/bin/env python3
"""
鍙岃建澶嶇洏 鈥?娴佺▼鍚堣 + 浜у搧鍙敤涓ら亾璇勫垎銆?璇诲彇椤圭洰鐩綍涓嬬殑 uat-report.json / code-uat-report.json / visual-uat-report.json
浜у嚭 review-report.json
"""
import sys
import json
from pathlib import Path
from datetime import datetime


def run_review(project_dir):
    project = Path(project_dir)
    results_dir = project / ".harness"
    results_dir.mkdir(parents=True, exist_ok=True)

    report = {
        "timestamp": datetime.now().isoformat(),
        "process_track": {"score": 0, "items": []},
        "product_track": {"score": 0, "items": []},
        "overall_verdict": "FAIL",
        "improvement_actions": [],
    }

    # 娴佺▼杞細妫€鏌ラ棬绂佷骇鍑烘槸鍚﹀瓨鍦?    gate_files = {
        "debate-output.json": "杈╄浜у嚭",
        "spec.md": "闇€姹傝鏍?,
        "execution-manifest.json": "鎵ц娓呭崟",
        ".handover-complete": "浜ゆ帴瀹屾垚",
    }

    for fname, label in gate_files.items():
        exists = (project / fname).exists()
        report["process_track"]["items"].append({
            "item": label,
            "file": fname,
            "passed": exists,
        })

    process_passed = sum(1 for i in report["process_track"]["items"] if i["passed"])
    process_total = len(report["process_track"]["items"])
    report["process_track"]["score"] = round(process_passed / process_total * 100, 1) if process_total > 0 else 0

    # 浜у搧杞細妫€鏌ラ獙鏀舵姤鍛?    uat_files = ["uat-report.json", "code-uat-report.json", "visual-uat-report.json"]
    uat_found = False
    for fname in uat_files:
        p = results_dir / fname
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                passed = data.get("passed", data.get("overall", False))
                report["product_track"]["items"].append({
                    "item": fname,
                    "passed": passed,
                    "mode": data.get("mode", "unknown"),
                })
                uat_found = True
            except Exception:
                report["product_track"]["items"].append({
                    "item": fname,
                    "passed": False,
                    "error": "JSON 瑙ｆ瀽澶辫触",
                })

    if not uat_found:
        report["product_track"]["items"].append({"item": "no-uat-report", "passed": False, "error": "鏃犻獙鏀舵姤鍛?})

    product_passed = sum(1 for i in report["product_track"]["items"] if i["passed"])
    product_total = len(report["product_track"]["items"])
    report["product_track"]["score"] = round(product_passed / product_total * 100, 1) if product_total > 0 else 0

    # 缁煎悎鍒ゅ畾
    p_s = report["process_track"]["score"]
    r_s = report["product_track"]["score"]
    if p_s >= 100 and r_s >= 60:
        report["overall_verdict"] = "PASS"
    elif p_s >= 75:
        report["overall_verdict"] = "CONDITIONAL_PASS"

    # 鏀硅繘寤鸿
    for item in report["process_track"]["items"]:
        if not item["passed"]:
            report["improvement_actions"].append({
                "priority": "high",
                "track": "process",
                "action": f"琛ュ厖缂哄け鏂囦欢: {item['item']} ({item['file']})",
            })

    for item in report["product_track"]["items"]:
        if not item["passed"]:
            report["improvement_actions"].append({
                "priority": "medium",
                "track": "product",
                "action": f"淇楠屾敹闂: {item['item']}",
            })

    (results_dir / "review-report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"娴佺▼鍚堣: {p_s}%")
    print(f"浜у搧鍙敤: {r_s}%")
    print(f"缁煎悎鍒ゅ畾: {report['overall_verdict']}")
    if report["improvement_actions"]:
        print("\n鏀硅繘寤鸿:")
        for a in report["improvement_actions"][:5]:
            print(f"  [{a['priority']}] {a['action']}")

    return report["overall_verdict"] in ("PASS", "CONDITIONAL_PASS")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="鍙岃建澶嶇洏")
    parser.add_argument("--project", required=True, help="椤圭洰鐩綍")
    args = parser.parse_args()
    ok = run_review(args.project)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
