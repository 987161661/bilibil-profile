#!/usr/bin/env python3
"""Create an evidence-layered Markdown profile from normalized Bilibili JSON."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


CATEGORIES = {
    "AI、编程与开发工具": r"AI|模型|GPT|Claude|Codex|Gemini|DeepSeek|Qwen|GLM|Agent|MCP|编程|代码|程序员|开源|大模型|提示词|LLM|Python|软件",
    "历史、政治与国际议题": r"历史|古代|王朝|战争|军事|政治|国家|美国|中国|日本|苏联|国际|外交|经济|财经|社会制度|帝国",
    "数码、空间改造与动手创造": r"数码|电脑|Mac|桌搭|电竞房|装修|家装|收纳|打印机|3D打印|DIY|硬件|主机|显示器|华强北|UE5|设计|材料|改造",
    "科学、工程与知识科普": r"科学|科普|物理|化学|数学|宇宙|生物|医学|材料|原理|实验|博士|为什么|机制|工程",
    "游戏与游戏文化": r"游戏|玩家|电竞|Steam|任天堂|主机|街霸|原神|英雄联盟|王者|塞尔达|游戏开发",
    "社会观察、心理与生活选择": r"社会|年轻人|男性|女性|婚姻|恋爱|工作|职场|人生|心理|生活|消费|普通人|赚钱|副业|情绪|教育",
    "影视、动漫与叙事娱乐": r"电影|影视|动漫|动画|番剧|解说|剧情|演员|导演|名著|小说|故事|娱乐|综艺",
    "运动、健身与格斗": r"健身|肌肉|减脂|训练|拳|格斗|武术|跑步|运动|体脂|力量",
    "音乐与乐器": r"音乐|吉他|钢琴|歌曲|唱|乐器|编曲|和弦",
}


def load(path: Path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def topic_counts(items, text):
    counts = Counter()
    for item in items:
        value = text(item)
        for name, pattern in CATEGORIES.items():
            if re.search(pattern, value, re.I):
                counts[name] += 1
    return counts


def percent(value: int, total: int) -> str:
    return f"{100 * value / total:.1f}%" if total else "0.0%"


def table(counts: Counter, total: int) -> str:
    rows = ["| 主题 | 命中数 | 占比 |", "|---|---:|---:|"]
    rows += [
        f"| {name} | {count} | {percent(count, total)} |"
        for name, count in counts.most_common()
    ]
    return "\n".join(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    follows = load(args.input / "following.json", {"items": []}).get("items", [])
    history_data = load(args.input / "history.json", {"items": []})
    history = history_data.get("items", [])
    favorite_data = load(args.input / "favorites.json", {"folders": []})
    favorites = [
        {**item, "folder": folder.get("title", "")}
        for folder in favorite_data.get("folders", [])
        for item in folder.get("items", [])
    ]
    watch_later = load(args.input / "watch-later.json", {"items": []}).get("items", [])
    feed = load(args.input / "feed.json", {"items": []}).get("items", [])

    creators = Counter(x.get("author", "") for x in history if x.get("author"))
    unique_creators = len(creators)
    top10 = sum(count for _, count in creators.most_common(10))
    same_creator = sum(
        1
        for left, right in zip(history, history[1:])
        if left.get("author") and left.get("author") == right.get("author")
    )
    days = Counter(x.get("viewed_at", "")[:10] for x in history if x.get("viewed_at"))
    history_topics = topic_counts(history, lambda x: f"{x.get('title', '')} {x.get('author', '')}")
    favorite_topics = topic_counts(
        favorites,
        lambda x: f"{x.get('title', '')} {(x.get('upper') or {}).get('name', '')} {x.get('folder', '')}",
    )

    first = history[0].get("viewed_at", "") if history else ""
    last = history[-1].get("viewed_at", "") if history else ""
    top_authors = "\n".join(
        f"{index}. {name}（{count}条）"
        for index, (name, count) in enumerate(creators.most_common(20), 1)
    )
    day_rows = "\n".join(f"- {day}：{days[day]}条" for day in sorted(days))
    folder_rows = "\n".join(
        f"- {folder.get('title', '未命名')}：账面{folder.get('media_count', 0)}条，导出{folder.get('exported', len(folder.get('items', [])))}条"
        for folder in favorite_data.get("folders", [])
    )

    report = f"""# B站兴趣画像

## 数据范围

- 关注：{len(follows)}个。
- 观看历史：{len(history)}条，覆盖 {last or '未知'} 至 {first or '未知'}；边界：{history_data.get('boundary') or '未记录'}。
- 收藏：{len(favorites)}条可见唯一内容。
- 稍后再看：{len(watch_later)}条。
- 动态样本：{len(feed)}条，仅作订阅供给背景。

证据权重：命名收藏夹与重复收藏 > 跨日重复观看 > 关注结构 > 单日观看簇 > 动态流。

## 近期观看主题

同一视频可命中多个主题，因此比例不要求相加为100%。

{table(history_topics, len(history))}

## 长期兴趣证据：收藏

{table(favorite_topics, len(favorites))}

收藏夹完整度：

{folder_rows or '- 无收藏夹数据'}

## 探索方式

- {len(history)}条历史来自{unique_creators}位创作者。
- 前10位创作者占{percent(top10, len(history))}。
- 相邻同创作者跳转占{percent(same_creator, max(1, len(history) - 1))}。

若创作者集中度低、主题分布广，优先判断为“主题驱动型探索”，而非对少数创作者的稳定追随。结合跨日数据和收藏验证，不要仅凭一天的密集观看下结论。

## 近期观看最多的创作者

{top_authors or '无数据'}

## 每日活动

{day_rows or '- 无数据'}

## 分析边界

- 点开不等于喜欢；数据通常缺乏可靠的实际观看时长。
- 历史记录是B站当前保留窗口，不是终身历史。
- 关键词分类是方向性统计，不是心理诊断。
- 推荐系统解释必须标记为基于行为数据的推断。
"""
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

