# ForFlow 首页设计原型 v4

远程预览：https://6a9ba5a7a3128710a3261c29--forflow-enterprise-suite-v3.netlify.app

开发预览：http://127.0.0.1:8894/

```sh
npm install
npm run dev -- --host 127.0.0.1 --port 8894 --strictPort
```

使用 React / Vite 构建。首页包含可切换场景的产品工作台、流程重播、依据弹窗、人工确认演示、能力说明和现有案例入口。产品区使用演示数据，确认操作仅改变本地状态。

主要文件：`src/App.jsx`、`src/styles.css`。视觉与交互检查记录见 `design-qa.md`。`npm run build` 已通过。

这是独立设计原型，已发布为 Netlify 预览，未替换正式官网。远程页面、脚本、样式和两张图片返回 HTTP 200，内容与本地构建一致。
