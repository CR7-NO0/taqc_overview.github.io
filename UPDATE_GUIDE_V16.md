# V16 GitHub Pages update instructions

1. Extract the ZIP and open `site/`.
2. Upload the CONTENTS of `site/` to the repository root (do not upload the enclosing `site` directory).
3. The two regenerated HTML files (`index.html` and `cn/index.html`) and updated JSON files must replace the previous versions.
4. Upload new `assets/video/01.mp4` ... `06.mp4` and their poster images.
5. Delete the six old seabed-specific video files (`bypass.mp4`, `hills_arc.mp4`, `wave.mp4`, `hills.mp4`, `escarpment.mp4`, `curve.mp4`) and corresponding posters if present. This step is optional, to save repository space.
6. Original six 3D generalization videos are kept unchanged.
7. Commit changes. GitHub Pages deploys from `main` branch and `/ (root)`.

For reliable folder uploads, use GitHub Desktop or git CLI; GitHub web UI may restrict large batch folder uploads.
