# 质检与边界

## 质量自检

生成前和生成后都检查，失败则自动修正。

```yaml
hook_check:
  first_3_seconds_has_conflict: true
  first_episode_no_long_background: true
  first_three_episodes_have_clear_progress: true

emotion_check:
  protagonist_is_wronged: true
  antagonist_is_hateable_but_motivated: true
  protected_object_is_clear: true
  audience_knows_what_to_expect: true

pacing_check:
  each_episode_has_one_core_event: true
  each_episode_has_cliffhanger: true
  every_5_episodes_has_mini_climax: true
  every_10_to_15_episodes_has_big_reversal: true

clarity_check:
  story_can_be_understood_immediately: true
  no_excessive_lore: true
  character_relations_clear: true
  golden_finger_rules_clear: true

continuity_check:
  names_consistent: true
  relationships_consistent: true
  money_and_numbers_consistent: true
  props_and_evidence_consistent: true
  system_rules_consistent: true

shootability_check:
  scenes_are_filmable: true
  action_is_visual: true
  dialogue_is_short: true
  locations_are_not_excessive: true
  no_unfilmable_abstract_description: true

compliance_check:
  no_vulgar_or_malicious_guidance: true
  no_glorification_of_crime: true
  no_exploitative_minors_content: true
  revenge_has_moral_legitimacy: true
  value_orientation_not_malicious: true

expectation_check:
  viewer_can_name_the_next_important_event: true
  expectation_is_specific: true
  expectation_not_replaced_by_withholding_all_information: true

information_gap_check:
  gap_changes_action_or_expectation: true
  repeated_misunderstanding_changes_at_least_one_condition: true
  ability_has_limit_cost_and_goal: true

emotion_progression_check:
  repetition_changes_mechanism: true
  payoff_has_visible_consequence: true
  stage_is_not_a_pile_of_unrelated_troubles: true

card_check:
  small_card_names_a_concrete_next_result: true
  big_card_changes_story_state: true
  card_positions_follow_project: true
  no_default_paywall_at_episode_ten: true

opening_check:
  episode_one_stops_viewer: true
  episode_one_is_understandable: true
  episode_one_creates_emotion: true
  episode_one_promises_what_comes_next: true

stage_gate:
  do_not_continue_long_draft_if_opening_fails: true
  issue_order: structure_then_event_then_scene_then_language
```

## 阶段性审核怎么接进质检

任何检查、改写前诊断、以及决定要不要续写长篇时，读取 [阶段性审核](methodology-review.md)。原有六段标题保持不变，新规则写进对应段落：

- 格式问题：标记和脚本结果。`scripts/validate_script_format.py` 默认只查标记；`--structure` 额外检查集数连续、场景序号、每集对白。脚本不判断期待和卡点质量。
- 节奏问题：手段是不是只在加码，中段是不是互不相关的小麻烦，该停时有没有继续堆集。
- 爽点问题：核心期待是否具体，五个环节是否齐全，有没有只憋屈、不给局部回报。
- 钩子问题：小卡点是否写出下一集的具体结果。项目写明了大卡点或一卡、二卡、三卡时，再看主线状态有没有变。没写明，就不按第十集付费点挑错。
- 可拍摄性问题：一场戏离开时，局面是否和进入时不同。
- 修改建议：先结构，再事件，再场景，最后语言。

跨阶段或用户要看值不值得往下写时，追加“七、阶段审核”。前三集没立住核心期待，就停在改框架，不先把后面几十集写完。

开篇四项任务的细则见 [第一集与前三集](methodology-opening.md)。小卡点和阶段节点的细则见 [卡点](methodology-cards.md)。

## 参考附件适配

当用户提供参考剧本或要求“按附件格式”，先提取并复用结构，不复制剧情。

识别：

```yaml
reference_style:
  structure: 一、剧本 / 二、正文剧本
  episode_format: 第 N 集
  scene_format: N-M 地点 时间内外
  character_line: 人物：...
  action_marker: △ / Δ
  inner_voice: OS
  voice_over: VO
  subtitles: 【字幕】
  system_panel: 系统面板（字幕）
  flash_insert: 【闪入】...【闪入结束】
  pacing: 每集小冲突和结尾钩子
  language: 口语、短句、强情绪、信息密度高
```

可以复用：结构、场景编号、对白格式、动作格式、OS/VO/字幕/系统面板表达方式、强情绪短句风格、每集推进一个小目标的节奏。

不得复制：原人物、原剧情、原台词连续表达、原商业路径的具体独创组合。

## 合规与价值边界

短剧可以强冲突，但要爽而有度。

避免：

- 低俗擦边。
- 恶意猎奇。
- 过度血腥。
- 美化犯罪。
- 侮辱现实群体。
- 鼓励违法报复。
- 未成年人不当情节。
- 真实人物造谣。

处理原则：

- 复仇靠证据、法律、公开真相、商业反击或正当防卫。
- 打脸服务人物成长，不写纯恶意羞辱。
- 亲情冲突要有现实动机，不把所有角色写成无脑工具人。
- 品牌短剧要真实可信，不夸大产品功效。
- 海外题材可高概念，但不要输出露骨内容。
