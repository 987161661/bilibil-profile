# Launch and growth playbook

This is a practical distribution plan for making Bilibili Profile recognizable while keeping the maintainer's identity attached to the work.

## Positioning

Use one sentence consistently:

> 把你的B站关注、收藏和观看历史，变成一份本地生成、证据分层、可审计的兴趣画像。

The project is not “another scraper.” Its memorable category is:

> **Privacy-first personal interest analytics for Bilibili.**

Repeat three proof points:

1. data stays local;
2. it distinguishes recent bursts from durable interests;
3. it explains discovery behavior with auditable metrics.

## Maintainer identity

Use the same identity everywhere:

- GitHub: `@987161661`
- Name: `曾梓安 / Zeng Zi'an`
- Project: `Bilibili Profile`
- Canonical URL: `https://github.com/987161661/bilibil-profile`

Every demo image, video description, article footer, and report template should contain the project URL and maintainer handle. Do not create disconnected brand accounts until the maintainer profile itself has a recognizable biography, avatar, and pinned repository.

Suggested GitHub bio:

> Building privacy-first AI tools that help people understand their own digital behavior. Creator of Bilibili Profile.

## Repository launch checklist

- [x] Add description: `Privacy-first Bilibili interest profiling from follows, favorites and watch history. 本地只读B站兴趣画像。`
- [x] Add topics: `bilibili`, `codex-skill`, `privacy`, `personal-analytics`, `recommendation-system`, `python`, `data-analysis`, `ai-agent`, `chinese`.
- [ ] Upload `assets/social-preview.png` in Settings → General → Social preview.
- [x] Enable Issues and Discussions.
- [x] Enable private vulnerability reporting.
- [ ] Apply to GitHub Sponsors, then verify the Sponsor button.
- [ ] Pin the repository on the maintainer's GitHub profile.
- [x] Publish a tagged first release with a downloadable Skill asset.
- [ ] Add a 45–90 second demo GIF or video to the README after recording.

## Launch assets

### B站视频标题

Choose one:

- 我把自己的1200条B站历史喂给AI，它比我更懂我的兴趣吗？
- B站知道你喜欢什么，但它不会把答案告诉你
- 我做了一个开源工具，分析你的B站信息茧房
- 为什么你刷得惯B站，却用不惯YouTube？我用数据找答案

### B站视频结构

1. 5秒结果钩子：展示“1200条历史、821位创作者、前10只占11.8%”。
2. 提出冲突：推荐算法知道你，但你不知道算法眼里的自己。
3. 展示扫码、本地导出、报告生成。
4. 解释短期热点和长期兴趣为何不同。
5. 说明数据不上传、凭据会清除。
6. 邀请观众到GitHub Star、试用并提交脱敏发现。
7. 片尾固定展示 `@987161661` 和仓库URL。

### 发布文案

```text
我做了一个开源项目 Bilibili Profile。

它会在本地读取你授权的关注、收藏与观看历史，区分“最近上头”和“长期喜欢”，再生成一份可审计的兴趣画像。

我的真实数据里，1200条历史来自821位创作者，前10位只占11.8%。这解释了为什么我喜欢在B站围绕问题到处探索，却总觉得YouTube首页过早收敛。

不上传数据、不要求复制Cookie、只读、分析后清除临时凭据。

GitHub: https://github.com/987161661/bilibil-profile
如果你觉得这个方向有意思，欢迎Star、试用或赞助。
```

### English launch copy

```text
I built Bilibili Profile: a local-first, read-only tool that turns follows, favorites, and watch history into an evidence-weighted interest profile.

It separates recent viewing bursts from durable interests and measures whether you follow creators or explore topics across many sources.

No project server. No pasted cookies. Auditable JSON and Markdown output.

https://github.com/987161661/bilibil-profile
```

## Distribution sequence

### Day 0: proof

- Publish `v0.1.0`.
- Post one real but redacted report.
- Record a short terminal-to-report demo.
- Ask five trusted users to run it and open Issues rather than privately sending feedback.

### Days 1–3: Chinese developer communities

- B站: publish the full story, not a feature list.
- V2EX / Linux.do / 即刻: share the surprising metric and privacy architecture.
- GitHub Discussions: open “晒出你的脱敏画像发现” and “兼容性反馈” threads.
- Reply thoughtfully to every early Issue; visible maintainer presence converts visitors into stars.

Do not paste identical promotional copy everywhere. Lead with a community-specific question and disclose that you are the author.

### Days 4–7: English reach

- Post to Hacker News as `Show HN` only after the English README and one-command path are solid.
- Share to relevant open-source, self-quantification, privacy, and recommendation-system communities.
- Contact maintainers of Codex skill lists or personal analytics collections with a concise pull request.

### Weeks 2–4: compounding content

- Publish one technical article: history pagination, retention boundaries, and safe credential handling.
- Publish one insight article: topic loyalty versus creator loyalty.
- Add a gallery of user-submitted, fully redacted findings.
- Ship at least one visible improvement per week and write release notes.
- Convert recurring questions into documentation and fixtures.

## Metrics

Track weekly:

- repository visitors, unique cloners, stars, forks, and traffic sources;
- README-to-install conversion through release asset downloads;
- successful first reports;
- Issues opened by new users;
- returning contributors;
- sponsors and sponsor conversion after major releases.

GitHub traffic is a rolling 14-day view, so record a weekly snapshot.

## Monetization without compromising privacy

Start with:

1. GitHub Sponsors for maintenance;
2. paid local setup and custom report interpretation;
3. privacy-preserving multi-platform interest migration;
4. workshops or content about recommendation systems and personal analytics.

Avoid hosting user cookies or raw histories. A hosted credential vault creates a much larger security and compliance burden than the likely early revenue justifies.

## What makes this shareable

People share a result, not a repository tree. Optimize for one striking, defensible sentence:

> “我的1200条历史来自821位UP主——我追的不是人，而是问题。”

Build future report versions around safe, visual, redacted “share cards” that include `Bilibili Profile by @987161661`.
