"""Read the canonical static-site case list without executing its site build."""
import ast
import hashlib
import json
from pathlib import Path

PROTOTYPE = Path(__file__).resolve().parents[1]
WORKSPACE = PROTOTYPE.parents[1]
source = WORKSPACE / "build_site.py"
text = source.read_text()
tree = ast.parse(text)
node = next(n for n in tree.body if isinstance(n, ast.Assign) and any(
    isinstance(t, ast.Name) and t.id == "CASE_LIBRARY_ITEMS" for t in n.targets))
items = ast.literal_eval(node.value)
catalog = []
for i, item in enumerate(items):
    href = item.get("href")
    if href:
        assert (WORKSPACE / href).is_file(), href
    catalog.append({
        "id": item.get("id", "reference-" + str(i)),
        "title": item["title"], "description": item["description"],
        "type": item["kicker"], "tags": item["tags"],
        "search": item.get("search_text", ""),
        "source": href or item.get("source_href"),
        "status": item.get("status_label", ""),
    })
(PROTOTYPE / "src/case-catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
index = ["# 官网案例检索入口", "", "来源：`build_site.py` 中的 `CASE_LIBRARY_ITEMS`。",
         "更新：运行 `python3 output/homepage-v6/scripts/sync-case-catalog.py`，同时生成预览索引与本文件。",
         "", "新增或调整案例时先查此清单，再读对应原页与来源。首页三场景不等于完整案例库。",
         "团队过往实践、工程方法、合作场景、外部公开参考与概念场景各有自己的适用范围；索引不证明客户交付或效果。",
         "", "| 案例 | 来源类型 | 原页 / 原始来源 | 检索词 |", "| --- | --- | --- | --- |"]
for item in catalog:
    link = f"[{item['source']}]({item['source'] if not item['source'] or item['source'].startswith('https:') else '../../' + item['source']})" if item['source'] else "仅概念场景"
    index.append(f"| {item['title']} | {item['type']} | {link} | {item['search']} |")
index += ["", "重点回查：汽车 B 柱 / B-pillar / DFMEA / ECO 对应 `case-automotive-dfmea-ontology-agent.html`。",
          "", "预约入口配置：`output/homepage-v6/src/contact-config.js`。历史来源：Git 提交 `65c839f`。",
          "已确认预约方式：填写需求表，团队联系确认交流时间。",
          "飞书表单：万维流形 AI 转型会后对接；2026-09-12 公开表单元数据和访问权限回读可用，未提交测试线索。",
          "", "当前预览与实际验证：`output/homepage-v6/remote-preview.json`；维护记录：`docs/maintenance/update-log.md`。",
          "", f"清单条目：{len(catalog)}；清单源 SHA-256：`{hashlib.sha256(ast.get_source_segment(text, node).encode()).hexdigest()}`。", ""]
(WORKSPACE / "docs/maintenance/case-catalog.md").write_text("\n".join(index))
print(f"Synced {len(catalog)} case entries from CASE_LIBRARY_ITEMS.")
