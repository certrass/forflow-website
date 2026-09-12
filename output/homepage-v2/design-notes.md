# ForFlow 首页迭代视觉稿 v2

日期：2026-09-05

这是完整桌面首页的视觉设计稿，由内置 Image Gen 根据本次实际访问的 ForFlow、Attio 和 Databricks 页面截图生成。它用于审阅信息层次、页面节奏和产品演示方向；尚未实现网页交互。

## 页面顺序

1. **首屏业务演示**：保留“让 AI 真正流入业务”，把供应链异常查询、原因和人工审批放到同一个界面。页内标记“场景演示”，保留团队过往项目的来源说明。
2. **能力展开**：知识、工作流、评估三项能力，配合金融文档字段复核演示。参考 Databricks 的左侧能力说明、右侧操作界面布局。
3. **案例依据**：P&ID、金融文档、Agent 评估三篇已有内容，使用业务对象和操作界面作为缩略图。
4. **交付过程**：场景诊断、小范围验证、部署与采用、持续复评。
5. **行动入口**：场景诊断和 30 分钟沟通。

## 延续与变化

- 延续 ForFlow 黑、白、绿色调，以现有 CSS 的 Flow Green #6cf67e 为参照。
- 参考 Attio 的真实业务对象、任务状态和可见结果；参考 Databricks 的能力、用例、依据、行动的层次。
- 供应链是首页主示例，文档和工业知识保留跨行业入口。
- 产品界面属于设计演示，不能当作现有上线系统的截图；案例数字、项目身份和原始资料应在实现时保持现有披露口径。
- 生成图中的文本、标志和字段在代码实现时应使用确定性排版与现有品牌资产重新制作。

## 现有内容链接

- https://forflow.ai/case-supply-chain-agentic-decision
- https://forflow.ai/case-financial-bda-document-automation
- https://forflow.ai/case-manufacturing-pid-intelligence
- https://forflow.ai/case-agent-evaluation-first
- https://forflow.ai/service-agent-build

## 视觉参考

- https://attio.com/
- https://attio.com/platform/workflows
- https://www.databricks.com/product/lakebase

完整生成提示词见 generation-prompt.txt；同目录 forflow-homepage-v2-design.png 为生成原图，实际尺寸 864 × 1821。它用于审阅整页方向，代码实现时应重新排版文字、使用现有品牌资产并补齐桌面及移动端细节。
