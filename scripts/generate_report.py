#!/usr/bin/env python3
"""
generate_report.py
根据采集到的硬件数据和打分结果，生成一份可视化 HTML 报告，
并保存到指定路径（默认 ./hardware_report.html）。

用法:
    python3 generate_report.py --scores '{"cpu":72,"memory":88,"storage":85,"gpu":55,"display":82,"resale":61}' \
        --spec '{"cpu":"Intel Core i9-9980HK","memory":"32 GB DDR4 2667MHz","storage":"1TB NVMe SSD","gpu":"AMD Radeon Pro 5300M 4GB","display":"16\" 3072x1920 Retina"}' \
        --output ./hardware_report.html
"""

import argparse
import json
import sys
from datetime import datetime


def build_html(scores: dict, spec: dict, output_path: str) -> None:
    total = round(sum(scores.values()) / len(scores))
    label_map = {
        "cpu": "CPU",
        "memory": "内存",
        "storage": "存储",
        "gpu": "显卡",
        "display": "屏幕",
        "resale": "保值度",
    }
    color_map = {
        "cpu": "#4f8ef7",
        "memory": "#36c78b",
        "storage": "#f7a73a",
        "gpu": "#e55c6c",
        "display": "#a76bdb",
        "resale": "#4ec4c4",
    }
    spec_map = {
        "cpu": "⚡ CPU",
        "memory": "💾 内存",
        "storage": "💿 存储",
        "gpu": "🎮 显卡",
        "display": "🖥 屏幕",
        "resale": "💎 保值",
    }

    rows = ""
    for key, score in scores.items():
        label = label_map.get(key, key)
        detail = spec.get(key, "N/A")
        bar_color = color_map.get(key, "#888")
        emoji_label = spec_map.get(key, label)
        rows += f"""
        <tr>
          <td>{emoji_label}</td>
          <td class="spec-cell">{detail}</td>
          <td>
            <div class="bar-bg">
              <div class="bar-fill" style="width:{score}%;background:{bar_color};"></div>
            </div>
          </td>
          <td class="score-num" style="color:{bar_color};">{score}</td>
        </tr>
"""

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    grade = (
        "优秀" if total >= 90 else
        "良好" if total >= 75 else
        "一般" if total >= 60 else
        "偏低"
    )
    grade_color = (
        "#36c78b" if total >= 90 else
        "#4f8ef7" if total >= 75 else
        "#f7a73a" if total >= 60 else
        "#e55c6c"
    )

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>硬件配置评分报告</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
         background: #0f1117; color: #e0e0e0; min-height: 100vh; padding: 40px 20px; }}
  .container {{ max-width: 760px; margin: 0 auto; }}
  h1 {{ font-size: 1.6rem; font-weight: 700; color: #fff; margin-bottom: 4px; }}
  .subtitle {{ font-size: 0.85rem; color: #666; margin-bottom: 30px; }}
  .total-card {{
    background: #1a1d27; border-radius: 16px; padding: 28px 32px;
    display: flex; align-items: center; gap: 32px; margin-bottom: 28px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
  }}
  .total-score {{ font-size: 5rem; font-weight: 800; color: {grade_color}; line-height: 1; }}
  .total-info h2 {{ font-size: 1.2rem; color: #fff; }}
  .total-info p {{ font-size: 0.9rem; color: #999; margin-top: 6px; line-height: 1.6; }}
  .grade-badge {{
    display: inline-block; padding: 3px 12px; border-radius: 20px;
    font-size: 0.8rem; font-weight: 600;
    background: {grade_color}22; color: {grade_color};
    border: 1px solid {grade_color}55; margin-bottom: 8px;
  }}
  table {{ width: 100%; border-collapse: collapse; background: #1a1d27;
           border-radius: 16px; overflow: hidden;
           box-shadow: 0 4px 24px rgba(0,0,0,0.4); }}
  th {{ background: #242736; padding: 14px 18px; font-size: 0.78rem;
        font-weight: 600; color: #888; text-align: left; text-transform: uppercase; letter-spacing: .06em; }}
  td {{ padding: 14px 18px; border-top: 1px solid #22253a; font-size: 0.88rem; vertical-align: middle; }}
  .spec-cell {{ color: #aaa; font-size: 0.82rem; max-width: 200px; }}
  .bar-bg {{ background: #22253a; border-radius: 8px; height: 8px; width: 100%; min-width: 120px; }}
  .bar-fill {{ height: 8px; border-radius: 8px; transition: width .6s ease; }}
  .score-num {{ font-weight: 700; font-size: 1rem; text-align: right; min-width: 40px; }}
  footer {{ text-align: center; color: #444; font-size: 0.75rem; margin-top: 28px; }}
</style>
</head>
<body>
<div class="container">
  <h1>🖥 硬件配置评分报告</h1>
  <p class="subtitle">生成时间：{now} &nbsp;·&nbsp; 满分 100 分</p>

  <div class="total-card">
    <div class="total-score">{total}</div>
    <div class="total-info">
      <div class="grade-badge">{grade}</div>
      <h2>综合得分</h2>
      <p>基于 CPU / 内存 / 存储 / 显卡 / 屏幕 / 保值度<br>
         对照 2026 年主流硬件市场行情综合评定</p>
    </div>
  </div>

  <table>
    <thead>
      <tr>
        <th>组件</th>
        <th>配置</th>
        <th>评分进度</th>
        <th style="text-align:right">分数</th>
      </tr>
    </thead>
    <tbody>
      {rows}
    </tbody>
  </table>

  <footer>由 hardware-master-skill 自动生成 · WorkBuddy</footer>
</div>
</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] 报告已生成: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="生成硬件评分 HTML 报告")
    parser.add_argument("--scores", required=True, help="JSON 字符串，各组件评分")
    parser.add_argument("--spec", required=True, help="JSON 字符串，各组件规格描述")
    parser.add_argument("--output", default="./hardware_report.html", help="输出路径")
    args = parser.parse_args()

    try:
        scores = json.loads(args.scores)
        spec = json.loads(args.spec)
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON 解析失败: {e}", file=sys.stderr)
        sys.exit(1)

    build_html(scores, spec, args.output)


if __name__ == "__main__":
    main()
