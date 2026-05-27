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
```

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
