#!/usr/bin/env python3
"""
浠ｇ爜楠屾敹 鈥?杩愯娴嬭瘯濂椾欢 + lint 妫€鏌ャ€?浜у嚭 code-uat-report.json
"""
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime


def run_code_uat(project_dir):
    project = Path(project_dir)
    results_dir = project / ".harness"
    results_dir.mkdir(parents=True, exist_ok=True)

    report = {
        "mode": "code",
        "timestamp": datetime.now().isoformat(),
        "tests": {"passed": False, "details": ""},
        "lint": {"passed": False, "details": ""},
        "overall": False,
    }

    # 娴嬭瘯
    test_files = list(project.rglob("test_*.py")) + list(project.rglob("*_test.py"))
    if test_files:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", str(project), "-v", "--tb=short"],
                capture_output=True, text=True, timeout=120, cwd=str(project)
            )
            report["tests"]["passed"] = result.returncode == 0
            report["tests"]["details"] = (result.stdout + result.stderr)[-2000:]
            print(f"  娴嬭瘯: {'PASS' if result.returncode == 0 else 'FAIL'} ({result.returncode})")
        except Exception as e:
            report["tests"]["details"] = str(e)
            print(f"  娴嬭瘯: 鎵ц寮傚父 鈥?{e}")
    else:
        report["tests"]["details"] = "鏃犳祴璇曟枃浠?
        print("  鈿?鏃犳祴璇曟枃浠?)

    # Lint
    try:
        flake8_result = subprocess.run(
            [sys.executable, "-m", "flake8", str(project), "--max-line-length=120", "--count"],
            capture_output=True, text=True, timeout=60, cwd=str(project)
        )
        report["lint"]["passed"] = flake8_result.returncode == 0
        report["lint"]["details"] = (flake8_result.stdout + flake8_result.stderr)[-2000:]
        print(f"  Lint: {'PASS' if flake8_result.returncode == 0 else 'FAIL'}")
    except Exception as e:
        report["lint"]["details"] = str(e)
        print(f"  Lint: 鎵ц寮傚父 鈥?{e}")

    report["overall"] = report["tests"]["passed"] and report["lint"]["passed"]

    (results_dir / "code-uat-report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    if report["overall"]:
        print("PASS 鈥?浠ｇ爜楠屾敹閫氳繃")
    else:
        print("FAIL 鈥?浠ｇ爜楠屾敹涓嶉€氳繃")
    return report["overall"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("鐢ㄦ硶: code_uat.py <椤圭洰鐩綍>")
        sys.exit(1)
    ok = run_code_uat(sys.argv[1])
    sys.exit(0 if ok else 1)
