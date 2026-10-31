import json, html, pathlib

R = pathlib.Path(__file__).resolve().parents[1]


def esc(x):
    return html.escape(str(x), quote=True)


def render_figure(prefix, fig):
    if fig.get('video'):
        video_name = fig['video']
        poster_name = pathlib.Path(video_name).stem + '.jpg'
        video_link = f'{prefix}assets/video/{esc(video_name)}'
        poster_link = f'{prefix}assets/video/poster/{esc(poster_name)}'
        return f'''
    <figure class="paper-figure video-figure {esc(fig.get('layout', 'medium'))}">
      <video class="auto-demo" controls autoplay muted loop playsinline preload="metadata" poster="{poster_link}" aria-label="{esc(fig['title'])}">
        <source src="{video_link}" type="video/mp4">
      </video>
      <figcaption>
        <h4>{esc(fig['title'])}</h4>
      </figcaption>
    </figure>
    '''
    return f'''
    <figure class="paper-figure {esc(fig.get('layout', 'medium'))}">
      <a href="{prefix}assets/img/{esc(fig['src'])}" target="_blank" aria-label="Open full image">
        <img src="{prefix}assets/img/{esc(fig['src'])}" alt="{esc(fig['title'])}" loading="lazy">
      </a>
      <figcaption>
        <h4>{esc(fig['title'])}</h4>
        <p>{esc(fig.get('desc',''))}</p>
      </figcaption>
    </figure>
    '''


def render_table(tbl):
    if not tbl:
        return ''
    head = ''.join(f'<th>{esc(x)}</th>' for x in tbl['headers'])
    body = []
    for row in tbl['rows']:
        cells = ''.join(f'<td>{esc(x)}</td>' for x in row)
        body.append(f'<tr>{cells}</tr>')
    body = ''.join(body)
    return f'''
    <div class="table-wrap">
      <div class="table-caption">{esc(tbl['caption'])}</div>
      <table>
        <thead><tr>{head}</tr></thead>
        <tbody>{body}</tbody>
      </table>
    </div>
    '''


def render_experiment_figures(prefix, sec):
    images = sec.get('images', [])
    title = sec.get('title', '')
    is_2d = ('2D' in title) or ('二维' in title)
    is_3d = ('3D path-following' in title) or ('三维路径跟踪' in title)
    if (is_2d or is_3d) and len(images) >= 3:
        top = ''.join(render_figure(prefix, {**img, 'layout': 'medium'}) for img in images[:2])
        trajectory = render_figure(prefix, {**images[2], 'layout': 'medium'})
        extra = ''.join(render_figure(prefix, fig) for fig in images[3:])
        extra_html = f'<div class="figure-stack experiment-figures">{extra}</div>' if extra else ''
        return f'''<div class="figure-row two-up training-row">{top}</div>
        <div class="trajectory-row">{trajectory}</div>{extra_html}'''
    imgs = ''.join(render_figure(prefix, fig) for fig in images)
    return f'<div class="figure-stack experiment-figures">{imgs}</div>'


for lang in ['zh', 'en']:
    d = json.loads((R / 'content' / f'{lang}.json').read_text(encoding='utf-8'))
    prefix = '' if lang == 'en' else '../'
    out = R / 'index.html' if lang == 'en' else R / 'cn' / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)

    nav = ''.join(f'<a href="#{esc(k)}">{esc(v)}</a>' for k, v in d['nav'].items())

    # Landing bullets and initial summary cards
    core_feature_map = [
        ('端到端控制', '端到端强化学习使UUV能够直接学习从状态观测到控制指令的映射，降低对精确水动力学模型的依赖，并简化控制器设计。同时，该方法能够通过与环境交互学习协调的控制动作，为不确定水下环境中的路径跟踪提供一种灵活的解决方案。'),
        ('自适应分位表示', '引入 FPN 生成非均匀分位区间，更灵活地近似复杂回报分布。'),
        ('截断多评论家机制', '通过多评论家混合分布与尾部截断抑制高估并提升学习稳定性。'),
        ('域随机化增强泛化', '在训练中随机化扰动、参数和初始状态，提升策略泛化性能。'),
    ]
    if lang == 'en':
        core_feature_map = [
            ('End-to-end control', 'End-to-end reinforcement learning enables UUVs to learn control policies directly from state observations to control commands, reducing the need for accurate hydrodynamic models and simplifying controller design. This approach also allows UUVs to learn coordinated control actions through interaction with the environment, offering a flexible solution for path following under uncertain underwater conditions.'),
            ('Adaptive quantile representation', 'An FPN generates non-uniform quantile fractions for flexible return-distribution modeling.'),
            ('Truncated multi-critic learning', 'A pooled multi-critic target with truncation is used to reduce overestimation and improve stability.'),
            ('Domain randomization', 'Training-time randomization of disturbances, parameters, and initial states improves robustness and generalization.'),
        ]

    core_bullets = []
    if lang == 'zh':
        core_bullets = [
            ('端到端 UUV 跟踪控制', '基于强化学习的多航点连续跟踪策略。'),
            ('分布式强化学习', '通过回报的分布建模提升学习效率与稳定性。'),
            ('TAQC 方法', '在 TQC 框架中引入可学习分位提议网络与区间质量加权损失。'),
            ('域随机化训练', '增强在存在干扰情况下对未见轨迹的泛化能力。'),
        ]
    else:
        core_bullets = [
            ('End-to-end UUV tracking control', 'RL framework for sequential waypoint tracking.'),
            ('Distributional RL', 'Return-distribution modeling improves learning efficiency and stability.'),
            ('TAQC method', 'TQC extended with a learnable fraction proposal network and a mass-weighted critic loss.'),
            ('Domain randomization', 'Enhance the generalization capability for unseen trajectories under disturbances.'),
        ]
    core_bullets_html = ''.join(f'<li><b>{esc(t)}：</b>{esc(v)}</li>' for t, v in core_bullets)
    summary_cards = ''.join(
        f'<div class="summary-card"><div class="num">{i}</div><p><b>{esc(t)}</b></p><p>{esc(v)}</p></div>'
        for i, (t, v) in enumerate(core_feature_map, start=1)
    )

    motivation_paras = ''.join(f'<p>{esc(p)}</p>' for p in d['motivation']['paragraphs'])
    task_figs = ''.join(render_figure(prefix, x) for x in d['task']['images'])
    framework_figs = ''.join(render_figure(prefix, x) for x in d['framework']['images'])
    terrain = d.get('terrain', {})
    terrain_paras = ''.join(f'<p>{esc(p)}</p>' for p in terrain.get('paragraphs', []))
    terrain_figs = ''.join(render_figure(prefix, x) for x in terrain.get('images', []))
    terrain_html = (f'''<section id="terrain" class="section">
      <h2>{esc(terrain['title'])}</h2>
      <p class="section-subtitle">{esc(terrain.get('subtitle', ''))}</p>
      <div class="text-block">{terrain_paras}</div>
      <div class="figure-stack terrain-figures">{terrain_figs}</div>
    </section>''' if terrain else '')


    baseline_html = []
    for group in d['baselines']['groups']:
        items = ''.join(f'<li><b>{esc(item["name"])}：</b>{esc(item["desc"])} </li>' for item in group['items'])
        baseline_html.append(f'<h3>{esc(group["group"])} </h3><ul>{items}</ul>')
    baseline_html = ''.join(baseline_html)

    metrics_html = ''.join(
        f'<li><b>{esc(item["name"])} ({esc(item["full"])}):</b> {esc(item["desc"])} </li>'
        for item in d['metrics']['items']
    )

    exp_sections = []
    for sec in d['experiments']['sections']:
        figs_html = render_experiment_figures(prefix, sec)
        notes = sec.get('notes', [])
        notes_html = f"<ul>{''.join(f'<li>{esc(n)}</li>' for n in notes)}</ul>" if notes else ''
        video_note_html = (
            f'<p class="video-speed-note">{esc(sec["video_note"])}</p>'
            if sec.get('video_note') and any(fig.get('video') for fig in sec.get('images', []))
            else ''
        )
        exp_sections.append(f'''
        <div class="subsection">
          <h3>{esc(sec['title'])}</h3>
          <p>{esc(sec['summary'])}</p>
          {notes_html}
          {video_note_html}
          {render_table(sec.get('table'))}
          {figs_html}
        </div>
        ''')
    exp_sections = ''.join(exp_sections)

    if lang == 'zh':
        small_title = '主要贡献'
        mot_title = '研究动机'
        task_title = d['task']['title']
        framework_title = d['framework']['title']
        baseline_title = '对比算法与实验设置'
        metric_title = '评价指标'
        exp_title = d['experiments']['title']
        conclusion_title = d['conclusion']['title']
        contact_title = '联系'
        contact_text = '如需补充代码、视频或正式论文链接，可在后续版本中继续加入。'
    else:
        small_title = 'Main contributions'
        mot_title = 'Research motivation'
        task_title = d['task']['title']
        framework_title = d['framework']['title']
        baseline_title = 'Baselines and experimental setting'
        metric_title = d['metrics']['title']
        exp_title = d['experiments']['title']
        conclusion_title = d['conclusion']['title']
        contact_title = 'Notes'
        contact_text = 'Code, video, or publication links can be added later if needed.'

    page = f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{esc(d['intro'])}">
  <title>{esc(d['title'])}</title>
  <link rel="stylesheet" href="{prefix}assets/style.css">
</head>
<body>
<header class="topbar">
  <div class="bar-inner">
    <a class="brand" href="#top">TAQC</a>
    <nav>{nav}</nav>
    <a class="lang" href="{'cn/index.html' if lang == 'en' else '../index.html'}">{'中文' if lang == 'en' else 'EN'}</a>
  </div>
</header>
<main class="page" id="top">
  <section class="landing">
    <h1>{esc(d['title'])}</h1>
    <div class="subtitle">{esc(d['subtitle'])}</div>
    <p class="intro">{esc(d['intro'])}</p>

    <h2>{small_title}</h2>
    <ul class="feature-bullets">{core_bullets_html}</ul>

    <section id="motivation" class="section first-section">
      <h2>{mot_title}</h2>
      <div class="text-block">{motivation_paras}</div>
      <div class="summary-grid">{summary_cards}</div>
    </section>
  </section>

  <section id="framework" class="section">
    <h2>{framework_title}</h2>
    <p>{esc(d['framework']['summary'])}</p>
    <ul>
      {''.join(f'<li><b>{esc(c["name"])}：</b>{esc(c["desc"])} </li>' for c in d['framework']['components'])}
    </ul>
    <div class="figure-stack framework-figures">{framework_figs}</div>
  </section>

  <section id="task" class="section">
    <h2>{task_title}</h2>
    <p>{esc(d['task']['text'])}</p>
    <div class="figure-stack task-figures">{task_figs}</div>
  </section>

  {terrain_html}

  <section id="baselines" class="section">
    <h2>{baseline_title}</h2>
    <p>{esc(d['baselines']['setting'])}</p>
    {baseline_html}
  </section>

  <section id="metrics" class="section">
    <h2>{metric_title}</h2>
    <ul>{metrics_html}</ul>
  </section>

  <section id="experiments" class="section">
    <h2>{exp_title}</h2>
    <p>{esc(d['experiments']['subtitle'])}</p>
    {exp_sections}
  </section>

  <section id="conclusion" class="section">
    <h2>{conclusion_title}</h2>
    <p>{esc(d['conclusion']['text'])}</p>
  </section>

</main>
<script src="{prefix}assets/js/video-autoplay.js" defer></script>
</body>
</html>'''

    out.write_text(page, encoding='utf-8')

print('Rebuilt site with simplified article layout.')
