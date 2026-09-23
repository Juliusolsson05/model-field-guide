---
id: deepseek-v4-pro
display: DeepSeek V4 Pro
reviewed: 2026-09-22
review_by: 2026-10-22
status: settled
superseded_by: null
---
# DeepSeek V4 Pro — open MIT weights; the API name now serves Flash

**Feel:** A capable, MIT-licensed open model — but if you call `deepseek-v4-pro` on DeepSeek's API today, you are not getting it.

**Important:** Since 2026-09-14 04:00 UTC, DeepSeek routes every `deepseek-v4-pro` API request to V4.1-Flash, billed at Flash rates, until V4.1-Pro launches (vendor). Scores measured on "V4 Pro" via the API after that date are really V4.1-Flash.

**Shines:**
- MIT-licensed weights, 1M context, 1.6T-parameter MoE — among the most permissive large open models.
- Very cheap API with off-peak pricing at half the peak rate.
- Long outputs.

**Falls over:**
- Agentic benchmark gains were not independently reproduced.
- DeepSeek's own numbers show V4.1-Flash beating it on agentic coding (DeepSWE).
- Self-hosting a 1.6T MoE is heavy.

**Reach for it when:** you self-host and want MIT terms at this scale.

**Avoid when:** calling the DeepSeek API (you'll get Flash anyway — call `deepseek-flash` explicitly); agentic work where you need verified results.

**Effort:** low / high / max.

**Evidence:**
- [DeepSeek V4.1-Flash release note](https://api-docs.deepseek.com/news/news260910/) (vendor) — rerouting notice
- [DeepSeek V4 preview release](https://api-docs.deepseek.com/news/news260424/) (vendor)
- [Hugging Face model card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro) (vendor) — license
- [SiliconANGLE on V4.1-Flash](https://siliconangle.com/2026/09/10/deepseek-releases-v4-1-flash-says-it-outperforms-flagship-v4-pro/) (independent, press)
