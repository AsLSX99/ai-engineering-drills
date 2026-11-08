#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""特训队列与间隔重复记账（纯标准库，Python >= 3.9）。

用法：
  python drill.py add <id> [<id> ...]        # 入队（今天到期）
  python drill.py next                       # 取下一题（到期优先，easy→medium→hard）
  python drill.py log <id> --result pass|fail [--hints N|exceeded] [--minutes M]
  python drill.py status                     # 连击/到期/毕业总览
  python drill.py list                       # 队列明细

数据文件：./drill-progress.json
排期阶梯：pass +1/+3/+7/+14/+30 天 → 第 6 次毕业；
          hints 3-4 → 间隔减半；hints exceeded → +2 天重考；fail → +1 天。
"""
import argparse
import json
import pathlib
import sys
from datetime import date, datetime, timedelta

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

DATA_FILE = pathlib.Path("drill-progress.json")
LADDER = [1, 3, 7, 14, 30]          # 第 1..5 次 pass 的间隔天数
DIFFICULTY_RANK = {"easy": 0, "medium": 1, "hard": 2}


def today():
    return date.today().isoformat()


def load():
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            sys.exit("进度文件损坏：%s（修复或删除 %s 后重试）" % (e, DATA_FILE))
        data.setdefault("drills", {})
        data.setdefault("records", [])
        return data
    return {"drills": {}, "records": []}


def save(data):
    DATA_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def find_practice_dir():
    """向上查找 <dir>/practice/_harness/practice_check.py。"""
    p = pathlib.Path.cwd().resolve()
    for _ in range(5):
        cand = p / "practice"
        if (cand / "_harness" / "practice_check.py").exists():
            return cand
        if p.parent == p:
            break
        p = p.parent
    return None


def read_meta(practice_dir, drill_id):
    meta = practice_dir / drill_id / "meta.json"
    if meta.exists():
        try:
            return json.loads(meta.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def cmd_add(args):
    data = load()
    practice = find_practice_dir()
    added = []
    for drill_id in args.ids:
        if drill_id in data["drills"] and data["drills"][drill_id]["status"] != "graduated":
            print("已在队列：%s（跳过）" % drill_id)
            continue
        entry = {
            "due": today(),
            "level": 0,
            "status": "active",
            "difficulty": "medium",
            "minutes": None,
            "fails": 0,
            "added": today(),
        }
        if practice:
            meta = read_meta(practice, drill_id)
            if meta:
                entry["difficulty"] = meta.get("difficulty", "medium")
                entry["minutes"] = meta.get("minutes")
            else:
                print("警告：practice/ 里找不到 %r（仍入队，仅缺元数据）" % drill_id)
        else:
            print("提示：未找到课程仓库的 practice/ 目录，%s 按中等难度入队" % drill_id)
        data["drills"][drill_id] = entry
        added.append(drill_id)
    save(data)
    if added:
        print("已入队：%s" % "、".join(added))


def sort_key(item):
    drill_id, e = item
    rank = DIFFICULTY_RANK.get(e.get("difficulty", "medium"), 1)
    return (e["due"], rank, e.get("added", ""), drill_id)


def cmd_next(_args):
    data = load()
    active = {k: v for k, v in data["drills"].items() if v["status"] == "active"}
    if not active:
        print("队列是空的。先：python drill.py add <题id>")
        return
    due = {k: v for k, v in active.items() if v["due"] <= today()}
    if due:
        drill_id, e = sorted(due.items(), key=sort_key)[0]
        print("今日到期：%s（%s · 预计 %s 分钟 · 第 %s 次复习）" % (
            drill_id, e.get("difficulty", "?"),
            e.get("minutes") or "?", e["level"] + 1))
        practice = find_practice_dir()
        if practice:
            print("题面：%s" % (practice / drill_id / "problem.md"))
        print("判分：python %s/scripts/practice/run.py %s <你的代码.py>"
              % (practice.parent if practice else "<课程仓库>", drill_id))
        return
    nxt = sorted(active.items(), key=sort_key)[0]
    print("今天没有到期的题。最近到期：%s → %s（%s）" % (
        nxt[1]["due"], nxt[0], nxt[1].get("difficulty", "?")))
    print("想提前练就直接：python drill.py log %s --result ..." % nxt[0])


def cmd_log(args):
    if args.result not in ("pass", "fail"):
        sys.exit("--result 只能是 pass 或 fail")
    data = load()
    drill_id = args.id
    if drill_id not in data["drills"]:
        sys.exit("%s 不在队列里，先：python drill.py add %s" % (drill_id, drill_id))
    e = data["drills"][drill_id]
    hints = str(args.hints or "")
    record = {
        "ts": datetime.now().isoformat(timespec="seconds"),
        "id": drill_id,
        "result": args.result,
        "hints": hints,
        "minutes": args.minutes,
    }
    data["records"].append(record)

    if args.result == "fail":
        e["fails"] = e.get("fails", 0) + 1
        e["due"] = (date.today() + timedelta(days=1)).isoformat()
        msg = "%s 记 fail，明天到期" % drill_id
        if e["fails"] >= 2:
            msg += "；连续 2 次 fail → 按协议降一档难度换题"
            e["fails"] = 0
        print(msg)
    else:
        e["fails"] = 0
        if hints == "exceeded":
            e["due"] = (date.today() + timedelta(days=2)).isoformat()
            print("%s 通关但 hints 超限 → 2 天后强制重考（遮住参考解重写）" % drill_id)
        else:
            n = e["level"] + 1
            if n > len(LADDER):
                e["status"] = "graduated"
                e["due"] = "9999-12-31"
                print("%s 毕业（6 次通关），不再入队" % drill_id)
            else:
                days = LADDER[n - 1]
                try:
                    h = int(hints)
                    if h >= 3:
                        days = max(1, days // 2)   # 学得不牢，更快复习
                except (TypeError, ValueError):
                    pass
                e["level"] = n
                e["due"] = (date.today() + timedelta(days=days)).isoformat()
                print("%s 第 %d 次通关，下次复习：%s（+%d 天）" % (
                    drill_id, n, e["due"], days))
    save(data)


def streak_days(records):
    days = sorted({r["ts"][:10] for r in records})
    if not days:
        return 0
    streak, cur = 0, date.today()
    if days[-1] != cur.isoformat():
        cur -= timedelta(days=1)          # 今天还没练，允许从昨天起算
    for d in reversed(days):
        if d == cur.isoformat():
            streak += 1
            cur -= timedelta(days=1)
        else:
            break
    return streak


def cmd_status(_args):
    data = load()
    drills, records = data["drills"], data["records"]
    if not drills and not records:
        print("还没有训练记录。先：python drill.py add <题id>")
        return
    active = [v for v in drills.values() if v["status"] == "active"]
    due = [v for v in active if v["due"] <= today()]
    graduated = [k for k, v in drills.items() if v["status"] == "graduated"]
    passes = [r for r in records if r["result"] == "pass"]
    fails = [r for r in records if r["result"] == "fail"]

    print("记录 %d 条 · 通关 %d · 失败 %d · 连击 %d 天" % (
        len(records), len(passes), len(fails), streak_days(records)))
    print("队列：进行中 %d · 今日到期 %d · 已毕业 %d" % (
        len(active), len(due), len(graduated)))
    print("-" * 52)
    for drill_id, e in sorted(
            ((k, v) for k, v in drills.items() if v["status"] == "active"),
            key=sort_key):
        mark = "DUE" if e["due"] <= today() else "   "
        print("%s %-32s %-6s level=%d due=%s" % (
            mark, drill_id, e.get("difficulty", "?"), e["level"], e["due"]))
    if graduated:
        print("-" * 52)
        print("毕业：%s" % "、".join(sorted(graduated)))
    if records:
        last = records[-1]
        print("-" * 52)
        print("最近：%s · %s · %s（%s）" % (
            last["ts"], last["id"], last["result"], last.get("hints") or "-"))


def cmd_list(_args):
    data = load()
    if not data["drills"]:
        print("队列是空的。")
        return
    for drill_id, e in sorted(data["drills"].items(), key=sort_key):
        print("%-32s %-6s level=%d due=%s status=%s" % (
            drill_id, e.get("difficulty", "?"), e["level"], e["due"], e["status"]))


def main():
    ap = argparse.ArgumentParser(description="特训队列与间隔重复记账")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("add", help="题目入队")
    p.add_argument("ids", nargs="+")
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("next", help="取下一题")
    p.set_defaults(func=cmd_next)

    p = sub.add_parser("log", help="记录一次结果并排期")
    p.add_argument("id")
    p.add_argument("--result", required=True, choices=["pass", "fail"])
    p.add_argument("--hints", default="")
    p.add_argument("--minutes", type=int, default=None)
    p.set_defaults(func=cmd_log)

    p = sub.add_parser("status", help="总览")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("list", help="队列明细")
    p.set_defaults(func=cmd_list)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
