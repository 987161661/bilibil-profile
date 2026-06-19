# Privacy policy / 隐私说明

[中文](#中文) · [English](#english)

## 中文

本仓库提供本地运行的代码和 Codex Skill，项目维护者不运营数据收集服务器。

### 默认数据流

- 登录凭据仅写入用户指定的本地隔离目录。
- 关注、收藏、观看历史、稍后再看和动态数据仅写入本地输出目录。
- 分析脚本不向项目维护者发送数据。
- 项目不包含遥测、广告 SDK、分析像素或远程错误上报。
- 用户应在导出完成后删除临时凭据；Skill 默认要求执行并验证这一步。

### 敏感数据

观看历史、收藏、关注和兴趣画像可能反映个人身份、行为与偏好。请勿：

- 把 `SESSDATA`、`bili_jct`、密码、验证码、Cookie 或二维码登录链接提交到 Issue、PR、Discussion 或聊天；
- 把未经脱敏的导出文件上传到公开仓库；
- 使用本项目收集、分析或发布未取得适当授权的第三方数据。

### Issue 与安全报告

公开 Issue 中只提交最小化、脱敏、可复现的信息。凭据泄漏或其他安全问题请按照 [SECURITY.md](SECURITY.md) 私下报告。

### 在线服务

若第三方基于本项目提供在线托管服务，其数据处理行为不由本政策覆盖。使用前应单独审查其隐私政策、保存期限、删除机制和安全措施。

## English

This repository provides local code and a Codex Skill. The maintainer does not operate a data-collection server.

- Credentials remain in an isolated directory chosen by the user.
- Exports and reports remain in a local output directory.
- The scripts contain no telemetry, advertising SDK, analytics pixel, or remote crash reporting.
- Users should remove temporary credentials after export.

Watch history, favorites, follows, and inferred interests may be sensitive. Never post credentials or raw personal exports in public issues or pull requests. Do not collect or publish another person's data without appropriate authorization.

Third-party hosted services built from this repository are outside this policy. Review their privacy terms separately.
