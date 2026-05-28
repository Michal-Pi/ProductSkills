# Scale 100 Churn Notes

Synthetic data only. IDs are deterministic and safe for local evaluation.

| ID | Segment | Stack | Opportunity | Severity | ARR at Risk | Confidence | Flags | Note |
| --- | --- | --- | --- | --- | ---: | ---: | --- | --- |
| EVID-100-00024 | Customer Success Ops | Zendesk + Slack | OPP-DATA-001 | medium | 158767 | 0.85 | none | Account churned or paused because ARR risk was unresolved. |
| EVID-100-00032 | Customer Success Ops | Zendesk + Slack | OPP-DATA-001 | low | 161926 | 0.87 | none | Account churned or paused because ticket priority was unresolved. |
| EVID-100-00040 | Enterprise PMO | Confluence + Jira | OPP-RISKY-001 | high | 289958 | 0.75 | none | Account churned or paused because confirmation was unresolved. |
| EVID-100-00041 | Product Ops | Notion + Linear | OPP-STRONG-002 | low | 97547 | 0.85 | missing:persona | Account churned or paused because Linear was unresolved. |
| EVID-100-00044 | Enterprise PMO | Confluence + Jira | OPP-RISKY-002 | high | 230571 | 0.61 | none | Account churned or paused because admin policy was unresolved. |
| EVID-100-00049 | SMB founder-led | Google Docs + Trello | NOISE-LOW-001 | high | 14501 | 0.59 | none | Account churned or paused because emoji labels was unresolved. |
| EVID-100-00053 | SMB founder-led | Google Docs + Trello | NOISE-LOW-001 | high | 14453 | 0.55 | duplicate:EVID-100-00049 | Account follow-up still cites emoji labels was unresolved. Same-account follow-up with slightly changed severity and wording. |
| EVID-100-00057 | Product Ops | Notion + Linear | OPP-STRONG-001 | medium | 154207 | 0.91 | none | Account churned or paused because traceability was unresolved. |
| EVID-100-00072 | SMB founder-led | Google Docs + Trello | OPP-WEAK-001 | high | 6838 | 0.41 | none | Account churned or paused because contractor PRD was unresolved. |
