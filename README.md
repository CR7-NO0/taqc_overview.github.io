# TAQC 论文展示网站 V14

以 V13 的网站资源和视频为基础，使用最新上传的 `en.json`、`zh.json`、`build_site.py` 重新生成。

**新增：** 三维泛化实验增加六类未见轨迹的成功率 SR（%）精简表格，数值来自用户提供的 Table 5 截图；不列 ATE/AHE/Steps。

## 编辑与构建

- 编辑 `content/zh.json` / `content/en.json`，文字、视频标题及数据均在其中。
- `tools/build_site.py` 控制网页生成。首页主要贡献部分文字目前在此脚本中定义。
- 运行 `python tools/build_site.py` 后更新根目录 `index.html` 与 `cn/index.html`。
- 六段视频在 `assets/video/`，视频封面在 `assets/video/poster/`。
