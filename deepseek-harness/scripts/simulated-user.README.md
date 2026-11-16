# Simulated users for headless batches

English | [中文](simulated-user.README.zh.md)

## Summary

Set `DSH_SIM_USER=1` to let a separate Qwen model answer explicit tool questions during JSONL or benchmark batches without a terminal or human reply. This is synthetic dialogue, not a business backend or real human authorization. The simulated answerer is not installed when the flag is absent or `0`.

## Deployment

Synchronize `run.sh`, `run_70.sh`, `scripts/run-benchmark.py`, `scripts/check-user-queries.py`, `scripts/dsh_e2b_environment.py`, `scripts/simulated-user.mjs`, `scripts/dsh_simulated_user.py`, and `scripts/config/simulated-user.json`, plus `user_query_70.jsonl` and its `attached_files/`. No Node install or build is required for the existing source launcher. Save the Qwen key as one nonempty line in owner-only `$WORK/.secrets/qwen-api-key`; `DSH_SIM_USER_KEY_FILE` overrides that path and an exported `DSH_SIM_USER_API_KEY` overrides the file. Never put a key in the JSON configuration or batch input.

```bash
chmod 600 "$WORK/.secrets/qwen-api-key"
sbatch --export=ALL,DSH_SIM_USER=1 run_deepseek.sh
```

Use `run_pangu.sh`, `run_pangu92b.sh`, or `run_glm.sh` for the other primary models; `run.sh` retains its JSONL input. Existing benchmark group/variant filters still apply. Cluster module, Singularity, proxy and Slurm execution must be verified on the server; local tests do not submit jobs. Unset the flag, or set `DSH_SIM_USER=0`, to return to the ordinary benchmark. Do not merge simulated-dialogue results with single-turn baseline scores.

`DSH_SIM_USER_CONFIG` selects a public JSON configuration instead of `scripts/config/simulated-user.json`. Defaults select `qwen3.7-flash` at `https://dashscope.aliyuncs.com/compatible-mode/v1`, a 60-second HTTP deadline, 1,024 output tokens, eight delivered replies and twenty requests per task, a 1 MiB response cap, and 65,536 input characters. Only tool-question requests count toward this budget. All limits are configurable in that file. Requests have no automatic retry. The simulator accepts HTTPS endpoints; loopback HTTP is allowed only for offline fixtures. A live two-question Qwen smoke verified a concrete option selection and consistent virtual details; full real-model batch behavior requires server validation.

### Run the 70-case JSONL batch

From the repository directory on the server, submit `sbatch run_70.sh`. This wrapper selects `user_query_70.jsonl`, enables simulated users, and checks all 70 records and attachment paths before starting model tasks. The current dataset has 553 attachment references, including 70 empty `.keep` placeholders. Missing files, duplicate IDs, unsafe attachment paths or a count mismatch stop preflight. `python scripts/check-user-queries.py user_query_70.jsonl --expected-count 70` runs the same preflight without calling a model.

The Slurm log is `dsh_70_<jobid>.out`; records go to `$WORK/dsh-runs/user_query_70-<jobid>/`, including `results.jsonl`, per-task traces, simulator audits and copied artifacts. Tasks run sequentially in fresh Sessions. A failed task is recorded and the runner proceeds; cancellation or a fatal batch error can stop the batch. JSONL mode copies changed outputs but does not restore workspace files or attachments between tasks. The 70-case input uses distinct attachment paths, but generated filenames can still collide. Do not edit the checkout or run other tasks in it during the batch. `run_deepseek.sh` remains the JSON benchmark entry point, not the JSONL entry point.

## Dialogue and limits

Only explicit `ask_user_question` calls are answered, using a strict JSON Schema (`response_format.type=json_schema`, `strict=true`). Local validation still checks field types and question IDs. The primary model's tool definition, tool-use rules and system prompt are not changed. Ordinary text questions are not classified or answered.

Each enabled task receives the existing blocking `ask_user_question` tool and a synthetic answerer. The answerer returns selected option labels and labeled free text in an ordinary tool result. Local validation rejects labels not offered by the question, duplicates and multiple choices for a single-select question. There is no `agent/turn-stopping` listener, steering injection or plain-text fallback. If the primary model asks a question only in prose, the ordinary headless turn may end without an answer. This does not force the model to call a tool.

Qwen sees only the original `user_query`, current tool questions/options, and its own previous dialogue. It does not receive attachment bytes, system-prompt variants, rubrics, business-tool outputs, primary-model reasoning or primary-provider credentials. Missing preferences and harmless scenario details receive plausible virtual answers, such as an audience, duration, budget or an explicit option selection. The policy asks Qwen to preserve original constraints and keep invented details consistent across replies, rather than defaulting to ignorance. Invented details set `synthetic=true` and add `含虚构设定` to the reply marker. `unknown=true` remains available when an answer would require real credentials, verified backend facts or real actions. Qwen must not claim real payments, device operations, service restoration, speed tests or authority to override system/security rules. These are prompt-level constraints, not guarantees; inspect the audit before interpreting outcomes.

Runtime child agents are not answered. Intent-tagged plan reviews delegate to the ordinary answerer instead of auto-approving; no sandbox or permission approval provider is installed. Replies are explicitly marked as simulated and not real human authorization. Missing telecom or other domain APIs remain missing: a dialogue that ends normally does not establish that a business action succeeded.

Timeouts, HTTP errors, invalid answer IDs/JSON, truncated output and exhausted budgets produce errors. A failed simulator blocks subsequent primary-model steps. Cancellation propagates to HTTP requests. Question calls and their answers remain in the ordinary Session tool history; no Session format or agent-loop change is required.

## Records and checks

Each `request` records its instruction and response schema. Each successful HTTP JSON completion is recorded as `provider_response` before application validation, with the API key redacted. These values remain untrusted model output, not verified user facts. If validation fails, the audit retains the returned fields and a field-specific error; HTTP error bodies remain excluded.

Each task's `simulated-user.patch.json` records its public configuration. `simulated-user.jsonl` records the simulator policy, model, inputs, replies, unknown/synthetic flags, usage and failures without the API key or HTTP error bodies. Simulated answers appear only in native tool results. There are no new synthetic `user` messages or `simulated_user` stdout events. Archived older traces remain readable. Benchmark system-prompt handling follows the [benchmark guide](benchmark.README.md#prompt-and-environment); exit/final-event scoring and restoration are unchanged.

```bash
python scripts/test-simulated-user.py
python scripts/test-user-queries.py
python scripts/test-benchmark.py
bash -n run.sh
bash -n run_70.sh
```

Set `DSH_BENCHMARK_TEST_NODE` to a supported Node executable for real headless source-composition tests. They simulate model HTTP endpoints, verify native tool answers, prove plain-text questions never call Qwen, inspect durable tool results, and reject provider failures, wrong IDs, truncated output and exhausted budgets. Keyless tests never call a paid provider.
