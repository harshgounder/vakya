# Concept pack: what to pitch, and every number behind it

Written 2026-10-20 22:05 IST. 115 minutes to the 23:59 upload close.
Nothing built yet. Template untouched.

---

## 0. One tactic, not a lecture

Every number below is a real number from a real source, and our contribution is framed as a **proposal with an evaluation plan**, not a shipped product with invented metrics. That reads as a research team, not a brochure, and there is nothing in the deck for a judge to catch. You still get the fairy dust, it just comes with a lid on it. This matters more than it sounds: the CCE bench has 15 of 28 faculty with AI/ML strings, they know this field cold, and a field-native judge can smell a fabricated number in one glance. A proposal with a crisp hypothesis and a benchmark design is *harder* to dismiss than fake metrics.

---

## 1. The fact base, verified tonight

### 1.1 Cactus and Needle

| fact | value | source |
|---|---|---|
| Cactus | hybrid edge-cloud inference engine built from scratch for mobile, wearables, smart home, robots | cactus-compute/cactus, 20.2k stars, 968 commits |
| Cactus Quants | CQ2-bit at **2.125 bits per weight**; weights, activations and KV cache quantized **from pretraining, never post-hoc** | cactuscompute.com/blog/cact-format, /blog/needle-2 |
| The quantization thesis | "The 2-bit model you deploy is the model that was trained" | /blog/needle-2 |
| Cactus engine | 6000 tok/s prefill, 1200 tok/s decode | HF Cactus-Compute/needle model card |
| Needle 1 (May 2026) | 26M params, function calling, 6000 tok/s prefill / 1200 tok/s decode, MIT | cactuscompute.com/blog/needle |
| Needle 2 (Aug 2026) | 45M params, **14 MB binary, 28 MB session RAM**, CQ2-bit, **500 tok/s on Raspberry Pi 5**, 300-700 tok/s on sub-$200 Samsung A-series | /blog/needle-2, HF needle2 |
| Needle 2 vs peers | trades wins with FunctionGemma 270M, LFM2.5 230M, Apple FM at **5x to 70x smaller**, 2 bits vs their f16 | /blog/needle-2 |
| Needle 3 (Sep 2026) | **8-29 MB binary**, 29-121M params, subnetworks at **20 / 16 / 8 / 4 layers**; 35 MB `.cact` weights, sub-1 MB engine | cactuscompute.com/needle, HF needle3 |
| The capacity ladder | "a subnetwork as small as **2 layers**, fine-tuned on one product's tools, runs optimally on devices far smaller than the full model needs" | cactus-compute/needle README |
| The ladder result | fine-tuning on DroidCall lifts **every** subnetwork by **18 to 36 points**; from 4 layers up, a tuned subnetwork **passes DeepSeek V4 Flash, starting at 29M parameters** | cactus-compute/needle README |
| Fine-tuning | local `needle finetune` = **LoRA on the attention projections, base frozen**; platform = full model at every depth from 2 layers up | cactus-compute/needle README |
| The structural constraint | decoding is constrained by a **byte-level grammar compiled from the declared schemas**; "the call is always well-formed" | /blog/needle, HF needle2 README |
| The refusal rule | "ask for something no tool covers and you get an **empty list, not a guess**" | cactuscompute.com/needle |
| Confidence | every response carries a **learned confidence score**; set a threshold: act above it, ask again, or **escalate to the cloud below it** | /blog/needle-2, cactus-compute/cactus CLI |
| System facts | an optional system turn carries `date, locale, device, battery, network, location, user, assistant` as **facts, never instructions** | HF needle2 README |
| Hybrid routing (Jul 2026) | post-trained models that **know when they are wrong and request help from the cloud** | cactuscompute.com/blog/hybrid |
| Whistle (Oct 2026) | **16.9 MB** open speech recognition model, **7 languages, CPU only**; benchmarked against Whisper tiny/base and Moonshine tiny v2 | cactuscompute.com/blog/whistle |
| Architecture | Simple Attention Networks, arXiv **2607.18363** | HF Cactus-Compute/needle |
| Licence | Needle Apache 2.0, MIT on the original weights; Cactus engine source-available | cactus-compute/needle, cactus-compute/cactus |
| The market | **21 billion IoT devices vs roughly 1.5 billion PCs**; "roughly **four in five edge devices cost under $200**"; most phones in emerging markets ship under $200 | /blog/needle-2 |
| Cactus traction | 20.2k GitHub stars, 185k HF downloads/month, YC-backed, powers Pebble watches and rings; quote from Eben Upton, Raspberry Pi CEO | cactuscompute.com |
| Air-gapped operation | `NEEDLE3_LIB_PATH` and `HF_HUB_OFFLINE` for air-gapped devices | cactuscompute.com/blog/needle-python-docs |

### 1.2 The failure we are attacking, from the literature

| fact | source |
|---|---|
| "When user queries are expressed in non-English languages, models frequently generate tool calls that are **semantically appropriate yet operationally invalid**" | arXiv 2601.05366, "Lost in Execution: On the Multilingual Robustness of Tool Calling in LLMs" |
| "Parameter values are expected to conform to execution-level conventions, such as using **English string identifiers**" | same |
| They name it: **parameter value language mismatch**, "rendering otherwise correct tool calls non-executable, exposing failures that arise at the **language-execution boundary rather than from intent misunderstanding**" | same |
| MLCL, a diagnostic multilingual benchmark, extends **BFCL** with Chinese, Hindi and Igbo, keeping the execution interface fixed | same |
| "Tool-calling failures in non-English settings can cause **silent non-executable calls** or incorrect downstream actions, which may **disproportionately affect non-English users**" | same, Ethical Considerations |
| English pretraining bias: subpar performance on low-resource languages; only **160K Hindi Wikipedia articles vs 6.6M+ English** | arXiv 2404.16816 IndicGenBench |
| IndicGenBench: 29 Indic languages, **13 scripts, 4 language families**, 1.4 billion people | arXiv 2404.16816 |
| Indic-QA: 11 languages, 2 families; low-resource performance weak; **Translate-Test beats direct multilingual inference for low-resource languages** | arXiv 2407.13522, Findings NAACL 2025 |
| Tool-calling is the natural action layer for Indic users, and it is exactly where the failure concentrates | synthesis of the above |

### 1.3 The offline thesis, already being fielded

| fact | source |
|---|---|
| NCMS (est. 1986, Ann Arbor MI) is the US technology-development consortium running the Maintenance Innovation Challenge and its sustainment accelerators | ncms.org |
| Its 2026 exhibit portfolio is explicitly about **"disconnected and contested environments"** and "communications-denied" operation | ncms.org 2026 ALC exhibit directory |
| The Edlore AI-Server: ruggedized edge platform, maintenance intelligence with **no requirement for internet or cloud connectivity**, 3D viewer, embedded manuals, **offline AI**, voice-assisted navigation, peer-to-peer sync, NIST-aligned architecture, **TRL-6** | ncms.org/25010-edlore |
| Shipcom AI: resilient edge computing and **sustained operations in disconnected and contested environments** | NCMS 2026 ALC exhibit directory |
| NCMS white paper, "Artificial Intelligence to Improve Supply Chain Resilience Throughout American Manufacturing", Dec 2024 | ncms.org news |
| NCMS Technology Brief on hybrid AI, Oct 2026 | GlobeNewswire, 8 Oct 2026 |

**The point for the deck: the offline, disconnected, no-cloud, voice-first deployment thesis is not speculative. It is already at TRL-6 in the harshest environments on earth, and the gap is that the model layer there is not multilingual and not tiny.**

---

## 2. The concept

### Name

**VYĀKĀRAṆA**. Sanskrit for the science of grammar and linguistic analysis, and a 2500-year-old Indic tradition of *constrained generation*: a rule system that makes the utterance well-formed by construction rather than by filtering afterwards. That is precisely the technical mechanism, and the name carries it in one word.

Alternates if you want something less heavy: **BHAASHA** (bhasha, language/speech), **DHVANI** (voice), **NIVAAN** (a new/original coin, and also "nivaran"/endowment in other usages, so usable both ways). Or keep it plain and put the weight on the team name: **RISC**, which the deck then explains.

### The RISC fit, which is better than a coincidence

Your team name is RISC. The thesis is:

> **One core. Many instruction sets.**

A RISC-V core is small and general, and gets its power from many instruction-set extensions. Our model is the same shape: a small base core, and the **app's JSON schema compiled to a byte-level grammar** is the instruction set. One 29 MB binary; every app gets its own dialect; nothing about the app is baked into the weights. That is a genuinely novel framing and the team name becomes the argument rather than a label.

### The one-line pitch

> **Move the constraint from the model to the decoder.** A 29 MB Indic lattice that cannot emit a malformed action, in any of 13 scripts, on a phone that costs less than the API call it replaces.

### The title on slide 2

**VYĀKĀRAṆA: grammar-as-instruction-set for on-device Indic tool calling**

---

## 3. The six slides, drafted

Word budget in brackets. Points and diagrams, zero paragraphs, per the parent template rule.

### Slide 1, cover

| field | value |
|---|---|
| Problem Statement | Indian-language tool calls fail at the language-execution boundary: semantically right, operationally invalid. 1.4B people, 13 scripts, and the fix is not a bigger model. |
| Theme | AI & Machine Learning |
| Team Name | RISC |
| Team Members | Harsh Gounder (Team Lead) · Farhan Fidin · Shlok Srivastava · Shivam Dureja |

### Slide 2, ABOUT THE PROJECT [~55 words + one diagram]

Headline: **VYĀKĀRAṆA**

- **The failure.** Non-English tool calls are "semantically appropriate yet operationally invalid". The model copies the user's words into parameters the executor expects in English. Silent non-executable calls, and non-English users hit hardest. (arXiv 2601.05366, MLCL over BFCL, Hindi)
- **Why the usual answers fail.** Translate-Test needs a cloud round trip and still mismatches parameters. Post-hoc validators filter after the damage. A bigger multilingual model needs more RAM than the device has.
- **Our move.** The constraint moves from the model to the decoder. A byte-level grammar compiled from the app's tool schemas constrains every token, so the call is well-formed **by construction**, in any script. Constraint becomes an architectural primitive.
- **The lattice.** One 29 MB binary. A router picks a per-language subnetwork (2 to 20 layers), so Tamil pays for 4 layers and Hindi-English code-mixed pays for 16.
- **The ISA.** The app's schema compiles to a grammar; the grammar is the instruction set. One core, many instruction sets. RISC.

### Slide 3, TECHNICAL APPROACH [~70 words + the flow diagram]

Diagram, left to right:

```
mic  ->  [Whistle 16.9MB ASR, CPU only, 7 langs]
      ->  [Router: script + code-mix + confidence]
      ->  [Indic subnetwork: 4 / 8 / 16 / 20 layers]
      ->  [byte-level grammar compiled from tool schemas]
      ->  [valid call  |  refusal  |  cloud handoff]
      ->  [executor + signed audit log]
```

Stack table, right column, every row a real number:

| layer | choice | number |
|---|---|---|
| base | Cactus Needle 3, Apache 2.0 | 8-29 MB, 29-121M params, subnetworks 20/16/8/4 |
| quantization | Cactus Quants CQ2-bit, trained-in not post-hoc | 2.125 bits/weight |
| architecture | Simple Attention Networks | arXiv 2607.18363 |
| adaptation | LoRA on attention projections, base frozen, per language | 2 to 20 layer ladder |
| ladder result (prior art) | narrow-task subnetwork passes DeepSeek V4 Flash | from 29M params, 4 layers up |
| ASR | Cactus Whistle, CPU only | 16.9 MB, 7 languages |
| runtime | Cactus engine | 6000 tok/s prefill, 1200 tok/s decode |
| device envelope | Raspberry Pi 5 / sub-$200 phone | 500 tok/s RPi 5, 300-700 tok/s phone, 28-45 MB RAM |
| grammar | byte-level, compiled from declared schemas | call well-formed by construction |
| data | synthesized over IndicGenBench + Indic-QA seeds | 29 languages, 13 scripts, human-verified |

### Slide 4, FEASIBILITY AND VIABILITY [~60 words]

**Feasibility in one line:** the technique is already proven, only the language axis is new. Cactus demonstrated that per-task subnetwork fine-tuning lifts every subnetwork by 18 to 36 points and reaches DeepSeek-V4-Flash-class performance from 29M params on a narrow tool set. We run the same recipe along the language axis. LoRA, base frozen, so the compute is hours, not weeks.

Five risks, five strategies:

| risk | strategy |
|---|---|
| No Indic tool-call corpus exists | synthesize over IndicGenBench and Indic-QA with human verification, the Indic-QA method exactly; publish it as Indic-ToolCall-Indic |
| English-first pretraining bias, worst on low-resource | per-language subnetworks instead of one Indic model; Translate-Test is the baseline to beat, not our method |
| Code-mixed ASR errors | the grammar bounds the action space, so a garbled utterance can only yield a valid call or a refusal, never a malformed one. This is the structural payoff of constraining at the decoder |
| 13 scripts inside a 29 MB budget | the lattice. Worst case falls back to a 20-layer code-mixed subnetwork. Nothing exceeds 29 MB |
| No evaluation exists | propose Indic-ToolCall-Indic as a BFCL/MLCL extension and publish it alongside the model |

**Scalability line** (one, with a number): the first thing to break at 10x is the tool set, not the model. At 10x the number of tools a user can hold, grammar compilation dominates. Fix: pre-compile and cache per tool set, shard by domain, ship the grammar with the app.

**Unit cost line:** zero rupees per action. Zero network bytes. 29 MB of RAM. Against a metered API call and a round trip.

### Slide 5, IMPACT AND BENEFITS [~55 words + one number wall]

- **The audience.** 21 billion IoT devices against roughly 1.5 billion PCs, and roughly four in five edge devices cost under $200. The real edge is not a MacBook, it is the cheapest phone in the room.
- **Social.** The tool call is the only way a farmer, an ASHA worker, a shopkeeper or a student actually uses AI. That path is broken in their language, and it fails silently.
- **Economic.** The marginal cost of an AI action collapses from "a metered API call" to "a local forward pass". No vendor lock, no per-seat pricing, no data leaving the device.
- **Environmental.** Zero network bytes per action, at 1.4-billion-person scale. Every avoided round trip is avoided data-centre energy.
- **The precedent.** NCMS's sustainment accelerator fields an offline AI-server at TRL-6: no cloud connectivity, voice-assisted, peer-to-peer sync, NIST-aligned, in disconnected and contested environments. The offline thesis is already fielded in the harshest conditions on earth. The model layer there is not multilingual and not tiny. That is the gap.
- **First adopter.** One district health or agri app. One sub-$200 Android. One 2G-only taluka. Metric: actions completed per device per day with zero network dependence.

### Slide 6, RESEARCH AND REFERENCES [~25 words + the list]

- arXiv 2601.05366, MLCL over BFCL: the language-execution boundary failure
- arXiv 2607.18363, Simple Attention Networks
- arXiv 2404.16816, IndicGenBench, 29 languages, 13 scripts
- arXiv 2407.13522, Indic-QA, Findings NAACL 2025
- cactus-compute/needle (Apache 2.0), cactus-compute/cactus, Cactus-Compute/needle3
- cactuscompute.com/blog: needle, needle-2, whistle, hybrid, cact-format, porting-needle
- NCMS 2026 ALC exhibit directory, Edlore AI-Server (TRL-6), NCMS supply-chain white paper 2024, NCMS Technology Brief 2026
- **Ours:** Indic-ToolCall-Indic, the lattice recipe, the grammar-ISA compiler, the ablation plan

---

## 4. Two other concepts, if you want to compare

**B. Air-gapped sovereign mesh.** A Needle-class model per site, with model updates and federated learning moving over a delay-tolerant, signed, peer-to-peer channel that never touches a cloud. NCMS's disconnected-environments programme is the validation. Bleeding edge, and it maps to the "audit/trace/replay" and "privacy/on-device" lines of the house rubric, but it reads more defence-flavored, and the audience is harder to name.

**C. The model that can say no in your language.** Refusal as the primary product: a confidence-calibrated, grammar-bounded model whose KPI is *correct refusal rate*, not accuracy, for anything that touches money, medicine or a physical actuator. A short, extremely quotable pitch ("a model you can trust with a switch"), and it maps to the "human fallback" and "guardrail" lines. It works best as a **beat inside the main concept** rather than as a separate deck, and it is the best single line for the offline pitch on 25 Oct if a judge asks "what happens when it is wrong".

---

## 5. Open decisions, in the order they block work

1. **Project name**: VYĀKĀRAṆA (my pick), BHAASHA, DHVANI, or keep the deck headlined as RISC and let the team name carry it.
2. **Theme field**: `AI & Machine Learning` (my pick: the bench that judges it is deepest there, and our system is literally a foundation model plus an agent runtime), or `Open Innovation` if you want the "no constraints" signal. Note the cover's Problem Statement field is free text, so we can use the Wildcard-style free problem statement while sitting in a named track.
3. **NCMS**: I read it as the National Center for Manufacturing Sciences and used their offline/disconnected deployment portfolio as the real-world validation on slide 5. Tell me if you meant something else and I will swap it.
4. **Concept**: A (VYĀKĀRAṆA lattice) or B (air-gapped mesh) or C (refusal-first) or a fusion of A and C.
5. **How far to push**: do you want the deck to read as a *proposal* (safe, unimpeachable, research-lab energy) or as a *shipped product* (flashier, needs invented metrics, and the accuracy clause is live)? My recommendation is proposal, and I will write it that way unless you say otherwise.

Say the word and I build it into the template: 6 slides, slide 7 deleted, PDF, and the real Cactus/Needle numbers with citations in the reference slide.
