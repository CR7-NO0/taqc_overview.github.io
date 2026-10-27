# 六段视频映射（V13）

六段视频使用本轮重新上传的文件重新编码为 H.264，已取代泛化实验区中的图片。

| 页面显示标题（中英文页相同） | 网页中的视频文件 | 本轮上传原文件 |
| --- | --- | --- |
| Unseen trajectory: S-shape | s_path.mp4 | s_path(1).mp4 |
| Unseen trajectory: Double Helix | double_spiral.mp4 | double_spiral(1).mp4 |
| Unseen trajectory: Polyline | square.mp4 | square(1).mp4 |
| Unseen trajectory: Figure-8 | figure8.mp4 | figure8(1).mp4 |
| Unseen trajectory: Conical Helix | conical_helix.mp4 | conical_helix(1).mp4 |
| Unseen trajectory: Comb Scanning | zigzag_3d.mp4 | zigzag_3d.mp4 |

请注意：`square.mp4` 与原有的 `Polyline` 名称不完全一致，`zigzag_3d.mp4` 与原有的 `Comb Scanning` 名称也不完全一致。这里按页面标题要求保留这两个标签，正式展示前请核对轨迹定义是否相符。

修改文本与文件名：编辑 `content/zh.json` 和 `content/en.json` 对应视频对象的 `title` 与 `video`，再运行 `python tools/build_site.py`。
