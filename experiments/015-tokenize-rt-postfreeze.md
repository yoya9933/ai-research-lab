# Experiment 015: tokenize-rt post-freeze edge observations

- **Date:** 2026-11-01 (Taiwan).
- **Public provenance:** https://github.com/asottile/tokenize-rt/issues/33, pre-fix source `7f89433be049d73e189a903485a93bdf3e56f1a0` (MIT).
- **Previously frozen repair:** [PR #27](https://github.com/yoya9933/ai-research-lab/pull/27) merged at `9e539f746a023e64fa252677895e8bc7791eddc5` **before** this new suite was added. Never modify that candidate while reporting this follow-up.
- **Independent mathematical oracle (from literal source byte counts):** non-EOL `x=1 ` offset 4, `ä=1 ` offset 5, second line in `x=1\\nä=2` offset 4, `s='😀'` offset 8. Controls: `x=1\\nä=2\\n` offset 4, `ä=1\\r\\n` offset 4, empty input has no NEWLINE.
- **Procedure:** run the exact same seven source strings against the untouched baseline and the frozen local candidate; record actual offsets, roundtrip results and both fixed and regressed counts. A `roundtrip` failure is retained, not silently counted as a successful end-to-end repair. CI runs `tests/test_tokenize_rt_33_followup.py` and separately prints the full JSON.
- **Research validity:** These cases are investigator-created *after* candidate commit but within the same chat-based research process, not from an independent reviewer or pretraining-controlled held-out source. No claim of blind performance, independent AI trials, or model progress; no paid APIs, model agents, network packages or upstream changes.
