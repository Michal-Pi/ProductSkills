# Scale 500 Churn Notes

Synthetic data only. IDs are deterministic and safe for local evaluation.

| ID | Segment | Stack | Opportunity | Severity | ARR at Risk | Confidence | Flags | Note |
| --- | --- | --- | --- | --- | ---: | ---: | --- | --- |
| EVID-500-00011 | Enterprise PMO | Confluence + Jira | OPP-RISKY-001 | medium | 140411 | 0.82 | none | Account churned or paused because live sync was unresolved. |
| EVID-500-00047 | Product Ops | Notion + Linear | OPP-STRONG-002 | high | 205245 | 0.69 | none | Account churned or paused because dry-run preview was unresolved. |
| EVID-500-00049 | SMB founder-led | Google Docs + Trello | OPP-WEAK-001 | medium | 8053 | 0.85 | none | Account churned or paused because too much process was unresolved. |
| EVID-500-00053 | SMB founder-led | Google Docs + Trello | OPP-WEAK-001 | medium | 7882 | 0.87 | duplicate:EVID-500-00049 | Account follow-up still cites too much process was unresolved. Same-account follow-up with slightly changed severity and wording. |
| EVID-500-00084 | SMB founder-led | Google Docs + Trello | OPP-WEAK-001 | high | 14350 | 0.78 | none | Account churned or paused because simple template was unresolved. |
| EVID-500-00103 | Enterprise PMO | Confluence + Jira | OPP-RISKY-002 | low | 218604 | 0.59 | none | Account churned or paused because admin policy was unresolved. |
| EVID-500-00108 | Product Ops | Notion + Linear | OPP-STRONG-001 | critical | 263047 | 0.8 | none | Account churned or paused because source citations was unresolved. |
| EVID-500-00127 | Product Ops | Notion + Linear | OPP-STRONG-001 | high | 160638 | 0.69 | none | Account churned or paused because PRD review was unresolved. |
| EVID-500-00145 | Enterprise PMO | Confluence + Jira | OPP-RISKY-001 | low | 386292 | 0.69 | none | Account churned or paused because live sync was unresolved. |
| EVID-500-00152 | Enterprise PMO | Confluence + Jira | OPP-RISKY-001 | low | 197150 | 0.83 | none | Account churned or paused because workspace IDs was unresolved. |
| EVID-500-00166 | Enterprise PMO | Confluence + Jira | OPP-RISKY-002 | medium | 354187 | 0.73 | none | Account churned or paused because SOC 2 was unresolved. |
| EVID-500-00170 | Product Ops | Notion + Linear | OPP-STRONG-002 | critical | 145829 | 0.44 | none | Account churned or paused because dry-run preview was unresolved. |
| EVID-500-00177 | Product Ops | Notion + Linear | OPP-STRONG-001 | low | 248297 | 0.82 | none | Account churned or paused because source citations was unresolved. |
| EVID-500-00188 | GitHub-first SMB | Notion + GitHub Issues | OPP-AMBIG-001 | high | 19630 | 0.36 | none | Account churned or paused because scope mismatch was unresolved. |
| EVID-500-00206 | Product Ops | Notion + Linear | OPP-STRONG-001 | medium | 258738 | 0.85 | none | Account churned or paused because source citations was unresolved. |
| EVID-500-00222 | SMB founder-led | Google Docs + Trello | NOISE-LOW-001 | high | 9012 | 0.53 | conflict | Account churned or paused because button color was unresolved. Conflicting note: another stakeholder says this is not important this quarter. |
| EVID-500-00223 | SMB founder-led | Google Docs + Trello | NOISE-LOW-001 | high | 6957 | 0.79 | none | Account churned or paused because emoji labels was unresolved. |
| EVID-500-00229 | SMB founder-led | Google Docs + Trello | NOISE-LOW-001 | critical | 16748 | 0.39 | none | Account churned or paused because button color was unresolved. |
| EVID-500-00235 | Customer Success Ops | Zendesk + Slack | OPP-DATA-001 | medium | 176373 | 0.57 | none | Account churned or paused because ticket priority was unresolved. |
| EVID-500-00240 | Customer Success Ops | Zendesk + Slack | OPP-DATA-001 | low | 165578 | 0.58 | none | Account churned or paused because ARR risk was unresolved. |
| EVID-500-00246 | SMB founder-led | Google Docs + Trello | OPP-WEAK-001 | low | 21739 | 0.55 | missing:persona | Account churned or paused because simple template was unresolved. |
| EVID-500-00258 | Product Ops | Notion + Linear | OPP-STRONG-002 | high | 154092 | 0.87 | none | Account churned or paused because Notion was unresolved. |
| EVID-500-00266 | Customer Success Ops | Zendesk + Slack | OPP-DATA-001 | high | 97742 | 0.8 | none | Account churned or paused because persona tags was unresolved. |
| EVID-500-00268 | GitHub-first SMB | Notion + GitHub Issues | OPP-AMBIG-001 | high |  | 0.38 | missing:arr_at_risk | Account churned or paused because delivery export was unresolved. |
| EVID-500-00274 | Product Ops | Notion + Linear | OPP-STRONG-002 | medium | 96692 | 0.85 | none | Account churned or paused because Linear was unresolved. |
| EVID-500-00276 | SMB founder-led | Google Docs + Trello | OPP-WEAK-001 | medium | 14636 | 0.51 | none | Account churned or paused because free tier was unresolved. |
| EVID-500-00288 | SMB founder-led | Google Docs + Trello | NOISE-LOW-001 | medium | 22267 | 0.84 | none | Account churned or paused because dashboard theme was unresolved. |
| EVID-500-00315 | SMB founder-led | Google Docs + Trello | OPP-WEAK-001 | medium | 23214 | 0.9 | none | Account churned or paused because contractor PRD was unresolved. |
| EVID-500-00331 | GitHub-first SMB | Notion + GitHub Issues | OPP-AMBIG-001 | low | 35933 | 0.83 | none | Account churned or paused because Linear-first was unresolved. |
| EVID-500-00339 | Product Ops | Notion + Linear | OPP-STRONG-001 | critical | 232585 | 0.45 | none | Account churned or paused because traceability was unresolved. |
| EVID-500-00362 | SMB founder-led | Google Docs + Trello | NOISE-LOW-001 | medium | 7616 | 0.76 | none | Account churned or paused because minor copy was unresolved. |
| EVID-500-00376 | Product Ops | Notion + Linear | OPP-STRONG-002 | high | 273041 | 0.79 | none | Account churned or paused because Notion was unresolved. |
| EVID-500-00397 | Product Ops | Notion + Linear | OPP-STRONG-001 | medium | 242138 | 0.49 | none | Account churned or paused because evidence links was unresolved. |
| EVID-500-00409 | Product Ops | Notion + Linear | OPP-STRONG-001 | medium | 109632 | 0.63 | none | Account churned or paused because evidence links was unresolved. |
| EVID-500-00417 | Enterprise PMO | Confluence + Jira | OPP-RISKY-001 | medium | 287059 | 0.6 | none | Account churned or paused because admin controls was unresolved. |
| EVID-500-00428 | Product Ops | Notion + Linear | OPP-STRONG-002 | medium | 266933 | 0.89 | none | Account churned or paused because Linear was unresolved. |
| EVID-500-00454 | SMB founder-led | Google Docs + Trello | OPP-WEAK-001 | high | 9998 | 0.81 | none | Account churned or paused because contractor PRD was unresolved. |
| EVID-500-00481 | Product Ops | Notion + Linear | OPP-STRONG-002 | medium | 252198 | 0.46 | conflict | Account churned or paused because Linear was unresolved. Conflicting note: another stakeholder says this is not important this quarter. |
| EVID-500-00493 | SMB founder-led | Google Docs + Trello | OPP-WEAK-001 | medium | 17817 | 0.58 | none | Account churned or paused because free tier was unresolved. |
| EVID-500-00499 | Enterprise PMO | Confluence + Jira | OPP-RISKY-002 | medium | 476096 | 0.52 | none | Account churned or paused because admin policy was unresolved. |
