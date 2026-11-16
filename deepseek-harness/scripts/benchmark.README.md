# Model benchmark batches

English | [中文](benchmark.README.zh.md)

## Summary

Submit `run_deepseek.sh`, `run_pangu.sh`, `run_glm.sh`, or `run_pangu92b.sh` to execute every selected variant in `benchmark_groups.json` as a fresh headless Session. Each variant uses the group's `user_query` and preserves the harness/provider system prompt. Its `effective_system_prompt` is metadata only and is not applied. The runner copies task outputs and Session records into `dsh-runs`, then restores the repository to the batch's starting files before the next variant.

## Table of Contents

- [Submit](#submit)
- [Prompt and environment](#prompt-and-environment)
- [Records](#records)
- [Workspace restoration](#workspace-restoration)
- [Verification](#verification)

## Submit

The DeepSeek, Pangu, and GLM wrappers reuse `run.sh` for Slurm, Singularity, Conda, protected credentials, proxies, and Serper/E2B configuration. Provider patches remain under `$WORK/dsh-config/`: `deepseek.patch.yml`, `pangu.patch.yml`, and `glm.patch.yml`; matching deployment templates live in `scripts/config/`. Each wrapper selects the corresponding patch and owner-only `$WORK/.secrets/<model>-api-key` file, where `<model>` is `deepseek`, `pangu`, or `glm`. Upload the wrappers, updated `run.sh`, `scripts/run-benchmark.py`, and `scripts/dsh_simulated_user.py` together with the external configuration directory. No Node dependency or build changes are required. Submit from the repository directory; the default partition and GPU request match `run.sh`, and normal `sbatch` resource overrides still apply. Actual cluster execution requires the server's existing modules and credentials and must be verified there.

```bash
sbatch run_deepseek.sh
sbatch run_pangu.sh
sbatch run_glm.sh
sbatch run_pangu92b.sh
```

The patches select `deepseek-v4-pro`, `glm-5.3`, and `openPangu-v21-pro` through OpenAI Chat Completions and Bearer authentication; [batch tools](batch-tools.README.md#model-provider) owns their endpoints, credential overrides, and Pangu's bounded retry backoff. Pangu no longer requires Huawei hardware/app credentials and uses a separate DeepSeek credential for the existing vision bridge. GLM capacities retain the harness's generic 262,144-token context and 32,768-token output defaults, overridable through `COMPANY_GLM_CONTEXT_WINDOW` and `COMPANY_GLM_MAX_TOKENS`; these are not verified gateway limits. Pangu retains its configured capacities and stream timeout. The GLM patch does not declare image input support or enable Pangu's vision bridge. No secret belongs in a YAML template.

The input defaults to the repository's `benchmark_groups.json`; a wrapper's first argument can select another JSON file. The runner executes all selected variants in group and variant order. Each wrapper fixes its provider regardless of an inherited `DSH_MODEL_PROVIDER`; an explicit `DSH_PATCH_FILE` still overrides its patch, so unset a previous provider's override before switching models. Use `DSH_BENCHMARK_GROUPS` and `DSH_BENCHMARK_VARIANTS` as comma-separated identifier filters; omitted filters select all variants. Unknown identifiers fail before any task starts. Jobs sharing this repository wait on the same lock. Do not edit its files or run another non-cooperating agent during a batch; those writes cannot be distinguished from the benchmark's writes.

```bash
sbatch --export=ALL,DSH_BENCHMARK_GROUPS=G-code-001 run_pangu.sh
```

The `pangu92b` provider selects `pangu92b_wandr` with `$WORK/dsh-config/pangu92b.patch.yml` and the owner-only `$WORK/.secrets/pangu92b-api-key.yml` bundle; [batch tools](batch-tools.README.md#model-provider) defines its Huawei authentication and capacity overrides. Synchronize `run_pangu92b.sh`, updated `run.sh`, and `batch-tools.patch.yml` along with those external files; no Node build is required. Records use `$WORK/dsh-runs/benchmark-pangu92b-<job-id>/`. It shares the existing Serper, E2B, DeepSeek vision credential, variant filtering, recording, and restoration behavior. Local mocked checks cover the request headers and file tools; live streaming and Function Calling support must be verified on the cluster before a full evaluation.

## Prompt and environment

For opt-in Qwen answers to `ask_user_question` on a headless server, see [simulated users](simulated-user.README.md). This changes tool answers and the tool schema, not the harness system prompt, and must be reported separately from the single-turn baseline.

The runner does not load `benchmark-prompt` or create `prompt.patch.json`. It neither replaces nor appends the benchmark's `effective_system_prompt`. The original profile/provider system prompt, tool guidance, workspace instructions and skill catalog remain in effect. `variant_system_prompt_applied: false` in task, result and plan records makes this explicit. Variants differing only in system prompt now repeat the same task condition; their runs cannot measure the original prompt differences.

The runner does not interpret `tools`, `env`, `rubric.exec`, `environment_override`, `env_snapshot`, or `user_query_append` as executable configuration. It saves those fields as metadata and applies only the group query. In particular, the two S5 variants with natural-language injection descriptions do not receive injected webpage or source-comment fixtures; `task.json` records `environment_override_applied: false`. Search, fetching, and E2B remain live rather than replaying the dataset's abstract baseline. Rubric scoring is a separate operation.

Attachment paths are resolved relative to the input JSON file. Each attachment must be a regular file inside the repository and outside excluded runtime directories. The runner lists the original absolute paths in the user message and copies the starting attachment bytes to `inputs/` before execution. It does not move the working directory or redirect model-selected deliverable paths.

## Records

Default records are `$WORK/dsh-runs/benchmark-deepseek-<job-id>/`, `$WORK/dsh-runs/benchmark-pangu-<job-id>/`, and `$WORK/dsh-runs/benchmark-glm-<job-id>/`. `DSH_RUN_ROOT` and `DSH_BATCH_ID` retain their existing overrides. Records and `DSH_HOME` must remain outside the repository. An existing benchmark output directory with `plan.json` is not reused; choose a new batch ID for a rerun.

```text
benchmark-pangu-<job-id>/
  plan.json
  benchmark_groups.json
  workspace-baseline/manifest.json
  workspace-baseline/files/...
  G-code-001/S1/
    task.json
    variant_system_prompt.txt
    trace.jsonl
    trace.json
    final.txt
    diagnostics.log
    inputs/...
    artifacts/...
    artifacts.json
    session-records/...
    session-records.json
    result.json
  results.jsonl
  summary.json
```

`trace.jsonl` is the headless event stream. `trace.json` omits the system role because the actual prompt is not present in that projection; read the archived Session's `system/message` events for the actual request. `variant_system_prompt.txt` and `variant_system_prompt_sha256` describe the unused input variant, not the runtime prompt. `result.json` reports exit/final-event checks, tool statistics, recording and restore outcomes. Successful execution is not rubric success. Failed tasks can be recorded and restored before the next variant starts.

## Workspace restoration

The runner saves one private baseline of the actual working files, including pre-existing uncommitted changes and artifacts. After each task it detects changes by file bytes, permissions, entry types, and symbolic-link targets, archives new or modified regular files with SHA-256 verification, records deleted paths and link changes, copies the Session, and only then restores originals and removes new entries. Existing artifacts from before the batch remain part of the baseline. `.git`, every `node_modules` directory, and root `dsh_*.out`/`dsh_*.err` logs are excluded; harness home, Sessions, caches outside the repository, and remote E2B contents are not rolled back. Cleanup never follows a symbolic link outside the repository and does not use Git reset or clean.

If recording or restore verification fails, the runner stops subsequent variants and retains the baseline and a per-repository recovery journal under `$WORK/.locks`. Other cooperating batches refuse to start until recovery. The wrappers request a Slurm TERM warning before the time limit; graceful cancellation stops the child, records available output, and restores the workspace. SIGKILL, node loss, or insufficient cleanup time can prevent automatic restoration. Cancel the original job and wait for it to exit, inspect the logged journal and records, then run recovery from the original repository inside the same Linux/Conda environment:

```bash
python scripts/run-benchmark.py --restore "$WORK/dsh-runs/benchmark-pangu-<job-id>"
```

Recovery takes the repository lock, copies residual changes into a new `recovery-*` directory, verifies the saved baseline, restores the workspace, and clears the journal. It does not report the interrupted task as successful. Artifact recording retains the existing 100 MiB per-file and 1 GiB total limits (`DSH_ARTIFACT_MAX_FILE_BYTES`, `DSH_ARTIFACT_MAX_TOTAL_BYTES`); exceeding them stops cleanup and leaves the workspace for recovery. Baseline storage defaults to at most 10 GiB (`DSH_BENCHMARK_BASELINE_MAX_BYTES`). Cancellation escalates after `DSH_BENCHMARK_STOP_GRACE_SECONDS` (default 20 seconds).

## Verification

Dataset validation requires only Python and does not read credentials or execute tasks:

```bash
python scripts/run-benchmark.py --check benchmark_groups.json
python scripts/test-benchmark.py
bash -n run.sh
bash -n run_deepseek.sh
bash -n run_pangu.sh
bash -n run_glm.sh
bash -n run_pangu92b.sh
```

The filesystem tests verify recording and restoration, failed tasks, interruption, unsafe paths, corrupt backups, and late changes. The source-profile smokes are opt-in through `DSH_BENCHMARK_TEST_NODE` pointing to a supported Node executable; they use the real headless launcher and file tools with a local simulated model, verify that the actual HTTP system prompt is preserved rather than replaced by the variant, and check archived and restored attachment bytes. All four provider cases load deployment templates and verify the model name, Bearer credential, and Chat Completions URL; only Pangu92B sends Huawei hardware/app headers. Set `DSH_BENCHMARK_TEST_CONFIG_DIR` to check deployed patches instead of `scripts/config/`. `DSH_BENCHMARK_TEST_BASH` enables wrapper and renamed-secret setup checks with simulated cluster dependencies. These tests do not call the company, Pangu, Serper, or E2B services. Inspect the first real cluster batch before interpreting benchmark scores.
