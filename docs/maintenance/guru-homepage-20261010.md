# Guru 设计系统移植 · 2026-10-10

## 有效决定

最新范围修正：用户明确「product/one 还是保持原有的但是风格略微靠一些就好」。Guru 深色营销体系只用于主站首页；产品页保留原有浅色居中首屏、真实工作台与完整讲解顺序，仅导航、品牌强调色和按钮稍作统一。产品首屏移除额外的客户墙、活动条和营销功能／生态墙，原有连接器、CLI、场景、案例与交互继续保留。

用户先强调视觉、ForFlow One 产品内容和 logo 墙；随后明确「文案和 forflow 原先的内容按 guru design system 改造复刻进去」「然后动效补充进去」。因此本轮由浅色微调转为 Guru 的深色营销体系，取代此前本轮浅色方案；真实产品界面仍保持浅色、密度和可操作层级。

范围为主站首页与公共 ForFlow One 展示开场。其他正式详情页不变。客户／合作方与工具生态分开展示；用户允许先沿用 Guru 的 logo，后续更换。参考客户标识只进入带 noindex 的审阅版本，不能当作 ForFlow 客户证明。

## 视觉与内容

参考 https://www.getguru.com/?r=0 的实际 HTML/CSS：深底 #090b0e、绿色主按钮 #7bd58b、宽幅左对齐大字、单色两行 logo、倾斜的连续工作状态条。中文采用本地 Inter 与系统中文字体，按中文长度调整行高与窄屏换行。真实 ForFlow 产品和案例内容来自既有源；不搬用 Guru 的客户效果、资质、数字或评价。

主站保留五项服务、业务诊断、手册、FAQ 和联系；产品介绍增加多智能体并行、审阅、接续工作。主站案例改用既有汽车 B 柱、供应链和 P&ID；标注各自的工程方法／团队过往实践。完整产品页仍有三个业务场景、上下文、优势、资产、治理、连接器、CLI、15 条案例和飞书需求表。

产品首屏从同一份 CTR-1042 / SUP-018 合同开始：提出续约问题 → 对照条款复核 → 生成处理待办，32 秒可跳章、重播和接管。展示是已编写的前端工作过程，不是新增后台引擎或实时企业系统接入。实际桌面产品支持的 Codex、Claude Code、Gemini CLI、Qwen Code、Cursor、Kimi、OpenCode 单独组成生态墙；来源见 logo 清单。

## 动效

三排工作状态条使用 transform 连续滚动，错开方向和时长；复制轨道保持无缝，重复内容不进入读屏。进入视区播放、离屏与隐藏页面暂停、悬停／键盘焦点暂停，提供明确暂停按钮，遵循 prefers-reduced-motion。沿用并调整 .65s 内容入场、卡片轻抬、案例图 1.035 倍缩放和按钮反馈。产品原生流程保留实际控件状态切换与虚拟鼠标。

## 编辑与构建入口

- 首页：templates/index.html → python3 build_site.py --homepage-only；避免全站生成覆盖并行修改。
- 首页基样式和脚本隔离为 assets/site/home-base.css / home-interactions.js，不替换其他正式页面依赖的全局资源。
- 共享视觉和动效：assets/site/guru-system.css、guru-motion.css、guru-motion.js；sync_homepage_theme.py 同步到产品 public/assets/site。
- Logo 清单：docs/maintenance/homepage-brand-assets.json。客户墙通过预览参数注入；正常产品构建不展示临时客户墙。
- 产品：output/homepage-v6/src；目前构建在 /private/tmp/forflow-intelligent-ui-build，使用同一锁文件，未覆盖固定正式 dist 与 product-one-source.json。
- 联合预览：scripts/package_homepage_review.py --product-build <dist/client> --destination <空目录> --reference-logos。只打包主站首页和 /product/one 子树，其他链接回正式站。

## 验证与下一步

同一构建的本地浏览器检查了桌面、440×956、390×844：无页面横向溢出，标题／正文／按钮不重叠，两类 logo 全加载。播放／暂停／离屏暂停／减少动态效果、合同第三章／重播、手机放大／返回通过，控制台 error/warn 为空。Vite 构建与 Sites 4/4 通过；静态检查只剩原有 workbench_prototype.html 三项错误。IAB 截图存在裁切，未作整页逐像素一致性承诺；未测 iOS Safari 真机。

预览：https://6ac9389bb0b5a08718433763--forflow-enterprise-suite-v3.netlify.app/

104 个远程文件 HTTP200 / noindex，逐字节核对（治理交流页只有已知 Pretty URLs 改写）。生产部署 6ac91f00a3371bf5a7fa42d3 保持不变。远程浏览器导航超时，远程资源校验与本地视觉／交互分开记录。

下一步在这一设计方向上由用户审阅，并把临时 Guru 客户标识替换为可以公开的真实客户／合作方。正式发布时使用非参考 logo 构建，重新确认固定产品源，不直接用旧的源回执发布新代码。无 Git push、邮件或 Drive 写入。
