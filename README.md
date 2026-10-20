# VĀKYA

**A $5 device that hears Indian speech and performs a verified action, offline, forever.**

Team **RISC** · Hypnexis 2026, Manipal University Jaipur · Round 1 online PPT submission

> One core. Many instruction sets. The task compiles to a grammar; the grammar IS the
> instruction set, so nothing task-specific is baked into the weights.

---

## The problem, measured

- **55%** of the 455 teams that built voice agents abandoned the project. Top reason:
  **first-turn understanding**. 95% of users report frustration with voice AI at some
  point, and a third still prefer a human.
- Drive-thru voice AI reaches **85%** accuracy. Humans deliver **89-92%**. IVR abandonment
  is **38%**, and **67%** of calls escalate to a human anyway.
- In Indian fields, open-source speech-to-text errs by **50%+** because of dialect, slang
  and noise. (Farm Vaidya / IFPRI, 2026)

Every one of those systems answers in an **open vocabulary**. The failure lives in the gap
between what was heard and what was executed.

## The move

**Move the constraint from the model to the decoder.**

A byte-level grammar compiled from the target's own schemas constrains every decoded token,
so the action is **well-formed by construction**, in any script. A garbled utterance can only
produce a valid action or a refusal. Never a wrong one.

Guardrail, audit trail and refusal stop being aspirations and become architecture. The
grammar also becomes the **localisation layer**: it carries date formats, numeral systems,
currency units and enum members, so the model never has to learn them.

## Three tiers, one binary

| Tier | Hardware | Model | Envelope |
|---|---|---|---|
| **A** | ESP32-S3, ~$5 | 13M int8 open-vocabulary ASR + wake word + grammar-constrained decoder | 8 MB PSRAM, mW, weeks on battery |
| **B** | sub-$200 Android / Raspberry Pi 5 | Whistle 16.9 MB ASR + Needle 3, 8-29 MB | 500 tok/s, 28-45 MB RAM |
| **C** | cloud, only if confidence < threshold | frontier model | metered $0.08-0.20/min |

**₹0 per action. 0 network bytes.**

## The three contributions

1. **Per-language subnetwork lattice.** Tamil pays for 4 layers, code-mixed Hindi pays for
   16. One download, 13 scripts.
2. **Grammar as instruction set.** One core, one compiled dialect per app, nothing baked
   into the weights.
3. **Refusal as a first-class output**, calibrated per script, in the user's own register.

## Standing on open work

We did not build the substrate. We stand on it, and we say so.

| Work | What it gives us | Licence |
|---|---|---|
| [Cactus Compute Needle 3](https://github.com/cactus-compute/needle) | 8-29 MB grammar-constrained on-device model, 20/16/8/4-layer subnetworks, 2.125 bits/weight trained in from pretraining | Apache 2.0 |
| [Cactus Compute Cactus](https://github.com/cactus-compute/cactus) | the inference engine, and a **published porting oracle** to test a runtime against | source-available |
| [Simple Attention Networks](https://arxiv.org/abs/2607.18363) | the architecture family | arXiv |
| [Oído, arXiv 2610.13447](https://arxiv.org/abs/2610.13447) | open-vocabulary ASR at **3.70% WER on a $5 microcontroller** with no neural accelerator | CC BY 4.0 |
| [Espressif ESP-SR](https://github.com/espressif/esp-sr) | WakeNet wake word, MultiNet with up to 200 commands, on-chip TTS on ESP32-S3 | free for commercial use |
| [DroidCall](https://github.com/UbiquitousLearning/DroidCall) · [mobile-actions](https://huggingface.co/datasets/google/mobile-actions) | public tool-calling training and evaluation data | open |
| [IndicGenBench](https://arxiv.org/abs/2404.16816) · [Indic-QA](https://arxiv.org/abs/2407.13522) | 29 languages, 13 scripts, 4 families | open |

The gap: **offline + $5 + grammar-safe + Indic + zero marginal cost.** Bhashini has $600M for
100 Indian LLMs; FarmerChat has 1M+ users and 30,000 hours of farm audio; the drive-thru
industry has 85% accuracy at $0.08-0.20 per minute. **Nobody has built the last mile, and
every hard component to build it is already open.**

## Ours

`Indic-ToolCall-Indic`, a published benchmark extension of BFCL and MLCL · the per-language
subnetwork lattice · the grammar-as-instruction-set compiler · the per-script calibration
and refusal protocol · the ablation plan.

## Repo layout

```
build/build_deck.py     the script that produces the deck from the official template
docs/                   the deck (pdf + pptx) and the full sourced concept document
site/                   the deployment
```

Rebuild the deck:

```bash
python3 -m venv .venv && .venv/bin/pip install python-pptx
.venv/bin/python build/build_deck.py
soffice --headless --convert-to pdf --outdir docs docs/RISC_Hypnexis2026_Round1.pptx
```

## Team

Harsh Gounder (Team Lead) · Farhan Fidin · Shlok Srivastava · Shivam Dureja
