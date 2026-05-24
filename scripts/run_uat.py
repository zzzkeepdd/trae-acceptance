#!/usr/bin/env python3
"""
缁熶竴楠屾敹鍏ュ彛 鈥?璺敱鍒?browser / code / visual 涓夌妯″紡銆?"""
import sys
import argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description="Trae Acceptance Runner")
    sub = parser.add_subparsers(dest="mode")

    p_browser = sub.add_parser("browser", help="Playwright 娴忚鍣ㄨ嚜鍔ㄥ寲楠屾敹")
    p_browser.add_argument("--project", required=True, help="椤圭洰鐩綍")
    p_browser.add_argument("--url", default="http://localhost:3000", help="鍓嶇 URL")
    p_browser.add_argument("--pages", type=int, default=3, help="鏈€灏戞埅鍥鹃〉鏁?)

    p_code = sub.add_parser("code", help="浠ｇ爜楠屾敹")
    p_code.add_argument("--project", required=True, help="椤圭洰鐩綍")

    p_visual = sub.add_parser("visual", help="瑙嗚楠屾敹")
    p_visual.add_argument("--project", required=True, help="椤圭洰鐩綍")

    args = parser.parse_args()

    if args.mode == "browser":
        from browser_uat import run_browser_uat
        ok = run_browser_uat(args.project, args.url, args.pages)
    elif args.mode == "code":
        from code_uat import run_code_uat
        ok = run_code_uat(args.project)
    elif args.mode == "visual":
        from visual_uat import run_visual_uat
        ok = run_visual_uat(args.project)
    else:
        parser.print_help()
        sys.exit(1)

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
