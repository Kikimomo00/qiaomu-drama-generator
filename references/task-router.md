# 任务路由

先判断任务，再按下面的清单读取文件。清单以外的方法论文件不要预读。类型引擎、默认集数、一卡二卡三卡都不是全题材必套的公式。

所有路径都从技能根目录算起。

共用规则：

- 正文、续写、改写后的正文，读取 `references/script-format-spec.md` 和 `references/output-format.md`。
- 交付 `.txt` 后运行 `scripts/validate_script_format.py`。要检查集数是否连续、每集是否有场景和对白时，再加 `--structure`。
- 对外成稿都要过 `references/quality-and-boundaries.md` 的合规边界。
- 用户已经锁定的人名、关系、能力、时间线、关键事件和结局，任何任务都不得为了新爽点改掉。

## 一句话主题

触发：用户只给题材、梗概、关键词或一句话想法。

读取：

1. `references/methodology-expectation.md`
2. 题材依赖隐藏身份、重生、证据、误认或能力差时，再读 `references/methodology-information-gap.md`
3. `references/genre-engines.md`，只选一个主引擎和最多两个副引擎
4. `references/generation-rules.md`
5. 要直接出正文时，再读 `references/methodology-opening.md`、`references/methodology-episode-scene.md`，以及 `references/methodology-cards.md` 里的小卡点

用户没指定阶段划分时，不把一卡、二卡、三卡落成具体集数。

动作：自动补齐目标观众、标题、高概念、核心期待、人物关系、能力或金手指、对手、前 3 集钩子，并直接生成。题材不需要的系统、复仇、爱情和隐藏身份，不补。

默认补齐：

```yaml
target_audience: 根据题材判断，默认泛短剧用户
episode_count: 默认 20 集；用户指定其他集数则按要求，不改回 20/60/100
episode_duration: 默认 1-2 分钟/集
platform_style: 中文竖屏短剧
protagonist: 自动命名，设计处境、目标、能力和缺陷
antagonist: 早期阻力、中期竞争者、后期主要对手；不是每个题材都要坏人
relationship_engine: 能持续产生冲突的关系；没有高压关系时不硬绑
golden_finger: 只在题材需要时使用系统、重生、空间、身份、医术、商业能力、预知或证据链
core_expectation: 观众已经知道并等待兑现的具体结果
information_gap: 只保留会改变行动或期待的信息差
first_hook: 开场即可看懂的冲突、反差或危机
cliffhanger_style: 下一集即将发生的具体结果
card_plan: 未指定则不默认第十集一卡，用阶段大事件
```

## 限制生成

触发：用户给出集数、题材、主角、平台、风格、禁区或参考格式。

读取：`references/methodology-expectation.md`，再加上用户限制实际会用到的文件。例如禁系统，就不按系统引擎补金手指；指定了卡点集数，才读 `references/methodology-cards.md` 的一卡、二卡、三卡。

动作：锁定硬性要求，补齐缺失字段。不得改动用户指定的集数、时长、频道、时代、禁区和参考格式。

## 大纲转正文

触发：用户已有大纲、人物设定或分集梗概。

读取：

1. `references/methodology-episode-scene.md`
2. `references/script-format-spec.md`
3. `references/output-format.md`
4. 大纲没有写清核心期待时，先补读 `references/methodology-expectation.md`
5. 大纲依赖秘密、误认或证据时，补读 `references/methodology-information-gap.md`
6. 集尾使用 `references/methodology-cards.md` 的小卡点

动作：保留主线，强化冲突、爽点、钩子和可拍摄动作，转成标准正文剧本。不更换已确定的人物动机和关键节点。

## 续写

触发：用户给出前几集或上下文，要求继续写。

读取：`references/methodology-episode-scene.md`，以及 `references/methodology-cards.md` 的小卡点。续写跨进新阶段时，再读 `references/methodology-emotion.md`。不重读选题文件。

动作：提取并保持人名、关系、金手指规则、金钱数字、道具来源、反派动机、台词风格和场景格式，从下一集直接开始，不重复长总结。前三集或当前阶段的期待还没成立时，先指出问题，不继续堆集数。

## 改写或优化

触发：用户说更爽、更抓人、加强钩子、短剧化、投流感、参考格式、改成某题材。

读取顺序：

1. `references/methodology-review.md`，先给问题分级
2. 只读有问题的那一层：
   - 期待、主线、关系：`references/methodology-expectation.md`
   - 秘密和误判：`references/methodology-information-gap.md`
   - 重复、不够爽、中段不往前：`references/methodology-emotion.md`
   - 开篇：`references/methodology-opening.md`
   - 集尾、付费点、阶段节点：`references/methodology-cards.md`
   - 场面、人物、台词：`references/methodology-episode-scene.md`
3. `references/quality-and-boundaries.md`

动作：如果用户要求“直接改”，直接输出优化版；否则先给主要问题和优化策略，再给优化后版本。结构性问题不先改台词。

## 质检

触发：用户要求检查、评估、找问题、看能不能继续写。

读取：`references/methodology-review.md` 和 `references/quality-and-boundaries.md`。开篇有疑问时补读 `references/methodology-opening.md`。用户提到钩子、卡点或付费时补读 `references/methodology-cards.md`。有 `.txt` 时运行 `scripts/validate_script_format.py`；要看集数和分集完整性时加 `--structure`。

动作：输出格式、节奏、爽点、钩子、可拍摄性、合规风险和修改建议。跨阶段或用户要看值不值得续写时，追加“七、阶段审核”。必要时给示例改法。不按未指定的第十集一卡挑错。

## 对标拆解

触发：用户要求拉片、对标、拆解某部剧，或从同类作品里抽框架。

读取：`references/methodology-benchmark.md`。

动作：只根据已经拿到的内容拆解。没有完整剧集，就不声称看完全剧。没有可靠数据，就不判断热度原因。用户接着要求原创时，只把可迁移机制交回“一句话主题”，重新写当前项目的核心期待。

## 海外竖屏

触发：用户提到海外、英文市场、ReelShort、DramaBox、werewolf、billionaire、mafia、royal 等。

读取：`references/genre-engines.md` 的海外竖屏段，以及 `references/methodology-expectation.md`。

动作：使用海外竖屏剧套路，默认中文输出，除非用户要求英文。不把国内付费集数套到未说明的海外项目上。

## 品牌短剧

触发：用户提到品牌、产品、文旅、营销、县城、非遗、乡村振兴、公益。

读取：`references/methodology-expectation.md`，以及 `references/genre-engines.md` 的品牌段。

动作：使用品牌短剧结构。产品必须成为剧情解决方案，不要硬塞广告或夸大功效。不硬套复仇、金手指和三卡。
