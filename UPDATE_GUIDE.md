# Update the GitHub Pages website / 更新网页

This package includes the complete bilingual static website.

1. Open the existing repository `CR7-N00/taqc_overview.github.io`.
2. Upload the **contents inside this folder** to the repository root (`main` branch), maintaining the folder structure, replacing files with the same names. Do not upload only the ZIP or the enclosing folder.
3. Commit the changes. GitHub Pages automatically redeploys from `main` / `(root)`.
4. Check the English homepage `index.html`, Chinese homepage `cn/index.html`, and the new six seabed terrain clips.

For later edits: modify `content/en.json`, `content/zh.json` and run `python tools/build_site.py` from the site folder, then commit regenerated HTML.

New assets: `assets/img/region.png`, `assets/img/seabed.png`, and six H.264 videos (plus JPG posters) in `assets/video/`. Original six unseen-path videos are preserved.

注意：上传的是本文件夹里的内容，确保 `index.html` 位于仓库根目录；不需要重新设置 Settings > Pages。
