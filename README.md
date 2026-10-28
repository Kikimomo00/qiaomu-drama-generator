# qiaomu-drama-generator

> 把一句话灵感、粗略大纲或参考剧本，稳定生成中文竖屏短剧的大纲、正文、续写、改写、质检报告和 `.txt` / PDF 剧本文档。

## 为什么值得用

短剧创作最容易卡在三件事：开头不够抓人、正文格式乱、爽点和钩子断掉。这个 skill 把中文微短剧常见的高转化叙事、前 3 集强开局、分集节奏、行级剧本标记和质量自检收进一个可复用工作流，并按阶段使用核心期待、信息差、情绪递进、大小卡点、开篇四项任务、对标拆解和阶段性审核。固定集数和一卡、二卡、三卡只在项目写明时使用。

它不绑定某个题材。你可以写荒年穿越、都市爱情、黑帮双身份、美食综艺、银发逆袭、品牌文旅、海外竖屏，也可以按参考剧本的格式写一个完全不同的新故事。

## 安装

本仓库是 [Kikimomo00/qiaomu-drama-generator](https://github.com/Kikimomo00/qiaomu-drama-generator)，在原有生成、续写、改写、类型引擎、严格格式和质量检查之上接入短剧创作方法论。

Codex：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/Kikimomo00/qiaomu-drama-generator.git ~/.codex/skills/qiaomu-drama-generator
```

目录已经存在时，在该目录执行 `git pull`。新开一轮 Codex 会话后即可按 `SKILL.md` 使用。

其他支持 skills 的 agent：

```bash
npx skills add Kikimomo00/qiaomu-drama-generator
```

验证：

```bash
ls ~/.codex/skills/qiaomu-drama-generator/SKILL.md
ls ~/.agents/skills/qiaomu-drama-generator
```

## 你可以这样说

- “荒年穿越，带系统，全家致富，写一个 20 集短剧。”
- “帮我把这个大纲改成更像短剧的版本，前三集要强钩子。”
- “按参考文档的格式，写一个现代爱情短剧 txt 剧本文档。”
- “检查这个剧本有没有爽点、钩子和可拍摄性问题。”
- “按核心期待和卡点审这 10 集，先别改写。”
- “写一个海外 ReelShort 风格的契约婚姻短剧。”

## 它会做什么

1. 判断任务类型：一句话主题、限制生成、大纲转正文、续写、改写、质检、对标拆解、海外竖屏或品牌短剧。
2. 按任务读取对应规则，自动补齐目标观众、主爽点、核心期待、标题、人物关系、对手、金手指或核心能力。
3. 按短剧节奏设计前 3 集。用户没指定集数时默认 20 集；20 / 60 / 100 集段落只作可选骨架，不强迫所有题材使用同一套节点。
4. 按严格剧本标记输出正文：`一、剧本 / 二、正文剧本 / 第 N 集 / N-M 场景 / 人物： / OS / VO / 字幕 / 系统面板`。
5. 根据需要生成 `.txt` 剧本文档，用户明确要求时可导出 PDF。
6. 用格式、节奏、爽点、钩子、可拍摄性、合规边界和阶段性审核做自检。

## 输出示例

```text
《剧名》

一、剧本
[项目简介]

二、正文剧本
剧名

第 1 集
1-1 场景名 日内
人物：人物甲，人物乙
△ 关键动作。
人物甲（状态）：对白。
人物乙（OS）：内心独白。
【字幕：关键信息】
```

## 前置条件

- [ ] 已安装支持 skills 的 agent 运行环境。
- [ ] 如需从 GitHub 安装：Node.js 和 `npx` 可用。
- [ ] 如需发布或二次开发：GitHub CLI 可用，并已登录。

验证命令：

```bash
node --version
npx --version
gh auth status
```

## 配置

不需要环境变量。这个 skill 默认只生成文本和本地文件，不调用外部付费 API。

## 质量边界

- 参考剧本只复用格式和写法，不复制原人物、原剧情或连续台词。
- 强冲突可以写，但不输出低俗擦边、恶意猎奇、未成年人不当情节或真实人物造谣。
- 复仇要靠证据、法律、公开真相、商业反击或正当防卫。
- 品牌短剧要让产品自然参与剧情，不夸大功效，不硬塞口播。

## Troubleshooting

| 问题 | 原因 | 解决 |
|---|---|---|
| 生成内容像小说，不像剧本 | 没有触发严格标记格式 | 明确说“按参考文档格式写正文剧本” |
| 场景缺少 `人物：` | 输出被压缩或续写时格式漂移 | 让 agent 使用 `scripts/validate_script_format.py` 校验 `.txt` |
| 安装后找不到 skill | skills 安装目录不同 | 检查 `~/.agents/skills/qiaomu-drama-generator` |
| `npx skills add` 失败 | Node.js、网络或 GitHub 权限问题 | 先运行 `node --version`、`npx --version`，再检查 GitHub 可访问性 |
| 所有题材都被写成第十集付费 | 把可选骨架当成了必用卡点 | 说明项目的集数和是否有付费节点；没指定时使用阶段大事件 |

## 包结构

```text
SKILL.md
agents/interface.yaml
references/task-router.md
references/generation-rules.md
references/genre-engines.md
references/output-format.md
references/script-format-spec.md
references/quality-and-boundaries.md
references/methodology-expectation.md
references/methodology-information-gap.md
references/methodology-emotion.md
references/methodology-cards.md
references/methodology-opening.md
references/methodology-benchmark.md
references/methodology-review.md
references/methodology-episode-scene.md
scripts/validate_script_format.py
tests/test_validate_script_format.py
```

## 致谢

格式规范来自中文短剧制作实践和用户提供的参考剧本文档；skill 包装流程参考 Qiaomu Meta Skill 的发布约定。

## License

MIT
