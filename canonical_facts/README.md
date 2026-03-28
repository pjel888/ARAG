# Canonical Facts

Drop one `.json` file per canonical fact card into [`cards/`](./cards).

Each card supports:

- `card_id`: stable identifier
- `priority`: higher numbers win when multiple cards match
- `required_terms`: all terms that must be present in the topic title/query
- `content`: the canonical official fact card text injected into the AI prompts
- `overclaim_terms`: optional extra terms that trigger a title-overclaim guardrail
- `title_guardrail_content`: optional warning text the article must acknowledge
- `required_acknowledgement_groups`: optional list of term-groups the final article must satisfy when the guardrail applies

Cards can also be partial anchors for comparison topics.
Example: a `BP 344 vs PD 1096` article can load a BP 344 canonical card that explicitly says it only covers the BP 344 side, while retrieval supplies the PD 1096 side separately.

Minimal example:

```json
{
  "card_id": "example_card",
  "priority": 100,
  "required_terms": ["bp 344", "2024", "ramp"],
  "content": "AUTHORITY: PRIMARY OFFICIAL\nSOURCE: ...\nCANONICAL FACTS:\n- ...",
  "overclaim_terms": ["1:12"],
  "title_guardrail_content": "TITLE_OVERCLAIM_GUARDRAIL:\n- ...",
  "required_acknowledgement_groups": [
    ["1:12"],
    ["does not list", "not listed"],
    ["table a.1.1", "official 2024 ramp table"]
  ]
}
```
