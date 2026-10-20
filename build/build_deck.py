#!/usr/bin/env python3
"""Build the Hypnexis round-1 deck from the official template.

Fills slide 1's four cover fields, lays content onto slides 2-6, deletes the
guidelines slide 7, saves pptx, exports PDF.
"""
import copy, os, shutil, subprocess, sys
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

TPL = "/home/liebert511/Music/6abccdae89c4b_hypnexis_presentation_template.pptx"
OUTDIR = "/home/liebert511/hypnexis-2026/docs"
PPTX = os.path.join(OUTDIR, "RISC_Hypnexis2026_Round1.pptx")

INK   = RGBColor(0x0B, 0x1B, 0x33)
INK2  = RGBColor(0x2A, 0x4A, 0x77)
ACC   = RGBColor(0x0B, 0x5E, 0xD7)
ACC2  = RGBColor(0xA8, 0x3A, 0x06)
GREEN = RGBColor(0x0B, 0x6B, 0x4F)
CARD  = RGBColor(0xFF, 0xFF, 0xFF)
CARD2 = RGBColor(0xEC, 0xF6, 0xFF)
RULE  = RGBColor(0x9E, 0xC8, 0xEE)
BODYF = "Arial"

prs = Presentation(TPL)
SW, SH = prs.slide_width, prs.slide_height
IN = 914400


def set_text(tf, blocks, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    """blocks: list of dicts {t, sz, b, c, sp_before, sp_after, bullet, align, font}"""
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Emu(int(0.08 * IN))
    tf.margin_top = tf.margin_bottom = Emu(int(0.04 * IN))
    first = True
    for blk in blocks:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = blk.get("align", align)
        if blk.get("sp_before"):
            p.space_before = Pt(blk["sp_before"])
        if blk.get("sp_after"):
            p.space_after = Pt(blk["sp_after"])
        if blk.get("ls"):
            p.line_spacing = blk["ls"]
        txt = blk.get("t", "")
        if blk.get("bullet"):
            txt = "•  " + txt
        r = p.add_run()
        r.text = txt
        f = r.font
        f.size = Pt(blk.get("sz", 10))
        f.bold = blk.get("b", False)
        f.color.rgb = blk.get("c", INK)
        f.name = blk.get("font", BODYF)
        if blk.get("italic"):
            f.italic = True


def card(slide, x, y, w, h, blocks, fill=CARD, line=RULE, line_w=0.75, pad=0.09):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.adjustments[0] = 0.045
    sh.fill.solid(); sh.fill.fore_color.rgb = fill
    sh.line.color.rgb = line; sh.line.width = Pt(line_w)
    sh.shadow.inherit = False
    tf = sh.text_frame
    tf.margin_left = tf.margin_right = Emu(int(pad * IN))
    tf.margin_top = tf.margin_bottom = Emu(int(0.06 * IN))
    set_text(tf, blocks)
    return sh


def bar(slide, x, y, w, h, color=ACC):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = color
    sh.line.fill.background()
    sh.shadow.inherit = False
    return sh


def tbox(slide, x, y, w, h, blocks, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    set_text(tb.text_frame, blocks, align=align, anchor=anchor)
    return tb


def label(txt, color=ACC, sz=9.5, b=True, after=2.5, before=0):
    return {"t": txt, "sz": sz, "b": b, "c": color, "sp_after": after, "sp_before": before, "ls": 0.95}


def line(txt, sz=9.3, c=INK, b=False, after=1.6, bullet=False, i=False):
    return {"t": txt, "sz": sz, "c": c, "b": b, "sp_after": after, "bullet": bullet, "ls": 0.94, "italic": i}


def big(txt, sz=19, c=ACC, after=0, b=True, align=PP_ALIGN.CENTER):
    return {"t": txt, "sz": sz, "c": c, "b": b, "sp_after": after, "align": align, "ls": 0.9}


def tiny(txt, sz=7.6, c=INK2, after=1.0, b=False, bullet=False):
    return {"t": txt, "sz": sz, "c": c, "b": b, "sp_after": after, "bullet": bullet, "ls": 0.92}


# ----------------------------------------------------------------- slide 1
s1 = prs.slides[0]
COVER = {
    "Problem Statement: ": "55% of the teams that shipped voice AI abandoned it, top reason first-turn understanding, and Indian field speech recognition errs over 50%. "
                            "We constrain the decoder, then run it offline on a $5 chip, in any Indian language.",
    "Theme:": "AI & Machine Learning",
    "Team Name: ": "RISC",
    "Team Members: ": "Harsh Gounder (Team Lead)  ·  Farhan Fidin  ·  Shlok Srivastava  ·  Shivam Dureja",
}
def walk_all(shapes):
    for sh in shapes:
        yield sh
        if sh.shape_type == 6:  # GROUP
            yield from walk_all(sh.shapes)


for sh in walk_all(s1.shapes):
    if not sh.has_text_frame:
        continue
    for p in sh.text_frame.paragraphs:
        for r in p.runs:
            key = r.text
            if key not in COVER:
                key = key.strip()
                if key not in COVER:
                    continue
            if True:
                r.text = COVER[key]
                r.font.size = Pt(10.5 if key.startswith("Problem") else 12.5)
                r.font.bold = False
                r.font.color.rgb = INK
                r.font.name = BODYF
                break

# ----------------------------------------------------------------- slide 2
s2 = prs.slides[1]
card(s2, 0.67, 1.22, 11.99, 0.92,
     [{"t": "VĀKYA:  a $5 device that hears Indian speech and performs a verified action, offline, forever.",
       "sz": 16.5, "b": True, "c": INK, "sp_after": 3, "ls": 0.95},
      {"t": "One core. Many instruction sets.  The task compiles to a grammar; the grammar IS the instruction set, so nothing task-specific is baked into the weights.",
       "sz": 10.2, "c": INK2, "ls": 0.95}])
card(s2, 0.67, 2.28, 3.88, 4.42,
     [label("THE FAILURE, MEASURED", ACC2),
      line("55% of the 455 teams that built voice agents abandoned the project. Top reason: first-turn understanding.", bullet=True),
      line("95% of users report frustration with voice AI at some point, and a third still prefer a human.", bullet=True),
      line("Drive-thru voice AI: 85% accuracy. Humans deliver 89-92%. IVR abandonment 38%, and 67% of calls escalate anyway.", bullet=True),
      line("In Indian fields: 50%+ speech-to-text error from dialect, slang and noise. (Farm Vaidya / IFPRI, 2026)", bullet=True),
      line("It fails silently, and it fails hardest on the people with the least power.", bullet=True, c=ACC2, b=True),
      line("", after=2),
      line("Every one of those systems answers in an OPEN vocabulary. The failure lives in the gap between what was heard and what was executed.", c=INK, b=True)])
card(s2, 4.72, 2.28, 3.88, 4.42,
     [label("THE MOVE", ACC),
      line("Move the constraint from the model to the decoder.", b=True, c=ACC, sz=10.5),
      line("A byte-level grammar compiled from the target's own schemas constrains every decoded token, so the action is well-formed by construction, in any script.", bullet=True),
      line("A garbled utterance can only produce a valid action or a refusal. Never a wrong one.", bullet=True, c=GREEN, b=True),
      line("Guardrail, audit trail and refusal stop being aspirations and become architecture.", bullet=True),
      line("", after=2),
      line("The grammar becomes the localisation layer: it carries date formats, numeral systems, currency units and enum members, so the model never has to learn them.", bullet=True)])
card(s2, 8.77, 2.28, 3.89, 4.42,
     [label("THE SYSTEM", GREEN),
      line("One binary. Three hardware tiers. Zero network bytes. Zero marginal cost.", b=True, c=GREEN, sz=10.2),
      line("Tier A  $5 MCU, wake word plus a grammar-constrained decoder", bullet=True),
      line("Tier B  sub-$200 phone or RPi 5, full multilingual tool calling", bullet=True),
      line("Tier C  cloud, only when confidence falls below the threshold", bullet=True),
      line("", after=2),
      line("One box, any task. Re-point it by recompiling the grammar, not by retraining the model.", bullet=True, b=True),
      line("", after=2),
      line("Grounded entirely on open work: Cactus Needle 3 (Apache 2.0), Espressif ESP-SR, Oído.", c=INK2, i=True, sz=8.8)])

# ----------------------------------------------------------------- slide 3
s3 = prs.slides[2]
FLOW = [
    ("MIC", "WakeNet wake word, 98% at 1 m, one false trigger per 12 h"),
    ("SPEECH TO TEXT", "Whistle 16.9 MB, 7 languages, CPU only   |   Oído 13M int8, 3.70% WER on a $5 MCU"),
    ("ROUTER", "script + code-mix + confidence  →  a language simplex, not a classifier"),
    ("INDIC SUBNETWORK", "4 / 8 / 16 / 20 layers  ·  29-121M params  ·  8-29 MB binary"),
    ("GRAMMAR", "byte-level, compiled from the task's schemas  →  well-formed by construction"),
    ("OUTCOME", "valid action   |   refusal   |   cloud handoff   →   executor + audit log"),
]
fy = 1.32
for i, (h, d) in enumerate(FLOW):
    y = fy + i * 0.86
    bar(s3, 0.67, y, 0.055, 0.62, ACC if i < 5 else GREEN)
    card(s3, 0.73, y, 5.62, 0.62,
         [{"t": h, "sz": 9.6, "b": True, "c": ACC if i < 5 else GREEN, "sp_after": 1},
          {"t": d, "sz": 8.3, "c": INK, "ls": 0.92}],
         fill=CARD, pad=0.1)
    if i < 5:
        tbox(s3, 3.4, y + 0.60, 0.4, 0.26, [{"t": "▼", "sz": 9, "c": ACC, "b": True, "align": PP_ALIGN.CENTER}])

card(s3, 6.62, 1.32, 6.04, 2.62,
     [label("THREE TIERS, ONE BINARY", ACC),
      {"t": "TIER", "sz": 8.2, "b": True, "c": ACC, "sp_after": 1.5},
      {"t": "A   ESP32-S3, $5      13M int8 ASR + wake word + grammar decoder      8 MB PSRAM, mW, weeks on battery",
       "sz": 8.6, "c": INK, "sp_after": 2.2, "ls": 0.95},
      {"t": "B   sub-$200 Android / RPi 5      Whistle 16.9 MB + Needle 3, 8-29 MB      500 tok/s, 28-45 MB RAM",
       "sz": 8.6, "c": INK, "sp_after": 2.2, "ls": 0.95},
      {"t": "C   cloud, only if confidence < threshold      frontier model      metered $0.08-0.20 per minute",
       "sz": 8.6, "c": INK, "sp_after": 3, "ls": 0.95},
      {"t": "Same core, same grammar compiler, three power envelopes. Tier A does the wake word and the constrained decode; tier B does open-ended reasoning; tier C is the safety valve.",
       "sz": 8.4, "c": INK2, "ls": 0.95}])

card(s3, 6.62, 4.06, 6.04, 1.42,
     [label("THE SUBSTRATE, IN REAL NUMBERS", GREEN),
      line("2.125 bits per weight, trained in from pretraining, never post-hoc", bullet=True, sz=8.4),
      line("29 MB binary  ·  29-121M params  ·  8-29 MB  ·  6000 tok/s prefill, 1200 tok/s decode", bullet=True, sz=8.4),
      line("3.70% WER on a $5 microcontroller with no neural accelerator", bullet=True, sz=8.4),
      line("a 2-layer subnetwork, fine-tuned on one tool set, runs on devices far smaller than the full model needs", bullet=True, sz=8.4)])
card(s3, 6.62, 5.60, 6.04, 1.10,
     [label("THE THREE CONTRIBUTIONS", ACC2),
      line("1.  Per-language subnetwork lattice: Tamil pays for 4 layers, code-mixed Hindi pays for 16. One download.", bullet=True, sz=8.6),
      line("2.  Grammar as instruction set: one core, one compiled dialect per app, nothing baked into the weights.", bullet=True, sz=8.6),
      line("3.  Refusal as a first-class output, calibrated per script, in the user's own register.", bullet=True, sz=8.6)])

# ----------------------------------------------------------------- slide 4
s4 = prs.slides[3]
card(s4, 0.67, 1.32, 5.72, 2.52,
     [label("WHAT IS ALREADY PROVEN", GREEN),
      line("Only the language axis is new. Every hard piece exists, in the open, today.", c=INK2, i=True, sz=8.6, after=2.4),
      line("Per-task subnetwork fine-tuning lifts every subnetwork 18-36 points; from 4 layers up, a tuned subnetwork passes DeepSeek V4 Flash at 29M params. (Cactus, 2026)", bullet=True, sz=8.7),
      line("Open-vocabulary ASR at 3.70% WER on a $5 MCU with no neural accelerator. (Oído, arXiv 2610.13447, 9 Oct 2026)", bullet=True, sz=8.7),
      line("Wake word, 200-command recogniser and TTS already run on an ESP32-S3. (Espressif ESP-SR)", bullet=True, sz=8.7),
      line("30,000 hours of real farm audio across 10 Indian languages and 5,000 vernacular terms already collected. (Farm Vaidya)", bullet=True, sz=8.7)])
card(s4, 0.67, 3.96, 5.72, 2.74,
     [label("THE SCALABILITY LINE", ACC),
      line("At 10x the tool set breaks before the model does.", b=True, c=ACC, sz=10.2, after=2.2),
      line("Fix: pre-compile and cache the grammar per tool set, shard the tool set by domain, and ship the grammar with the app. The model is the cheap part.", bullet=True, sz=8.8),
      line("", after=3),
      label("THE UNIT COST", ACC2),
      line("₹0 per action. 0 network bytes. 29 MB of RAM.", b=True, c=ACC2, sz=10.2, after=2.2),
      line("Against a metered API call at $0.08-0.20 per minute, a 38% IVR abandonment rate, and a data-centre round trip for every question.", bullet=True, sz=8.8)])

card(s4, 6.62, 1.32, 6.04, 5.38,
     [label("SIX RISKS, SIX ANSWERS", ACC2),
      {"t": "RISK", "sz": 8.2, "b": True, "c": ACC2, "sp_after": 1.5},
      {"t": "1.  No Indic tool-call corpus exists.", "sz": 8.8, "b": True, "c": INK, "sp_after": 0.8},
      {"t": "Synthesise over IndicGenBench and Indic-QA with human verification, the Indic-QA method exactly, and publish it as Indic-ToolCall-Indic.",
       "sz": 8.4, "c": INK2, "sp_after": 3.2, "ls": 0.94},
      {"t": "2.  English-first pretraining, worst on low-resource languages.", "sz": 8.8, "b": True, "c": INK, "sp_after": 0.8},
      {"t": "Per-language subnetworks instead of one Indic model. Translate-Test is the baseline we have to beat, not our method.",
       "sz": 8.4, "c": INK2, "sp_after": 3.2, "ls": 0.94},
      {"t": "3.  Code-mixed speech, field noise, dialect.", "sz": 8.8, "b": True, "c": INK, "sp_after": 0.8},
      {"t": "The grammar bounds the action space, so noise yields a valid action or a refusal, never a malformed one. This is the structural payoff of constraining at the decoder.",
       "sz": 8.4, "c": INK2, "sp_after": 3.2, "ls": 0.94},
      {"t": "4.  Thirteen scripts inside a 29 MB budget.", "sz": 8.8, "b": True, "c": INK, "sp_after": 0.8},
      {"t": "The lattice. Script-clustered vocabularies with shared subword units, and a per-script subnetwork. Worst case falls back to a 20-layer code-mixed subnetwork.",
       "sz": 8.4, "c": INK2, "sp_after": 3.2, "ls": 0.94},
      {"t": "5.  There is no benchmark to be judged on.", "sz": 8.8, "b": True, "c": INK, "sp_after": 0.8},
      {"t": "Propose Indic-ToolCall-Indic as a BFCL and MLCL extension, and publish the set with the model. A published benchmark is a moat.",
       "sz": 8.4, "c": INK2, "sp_after": 3.2, "ls": 0.94},
      {"t": "6.  The buyer is not the user.", "sz": 8.8, "b": True, "c": INK, "sp_after": 0.8},
      {"t": "True, and we name it. The payer is a state programme, an FPO, an NGO or a device maker. At ₹0 marginal cost, a state programme can put 100,000 devices in the field for the cost of the devices.",
       "sz": 8.4, "c": INK2, "ls": 0.94}])

# ----------------------------------------------------------------- slide 5
s5 = prs.slides[4]
NUMS = [("140M", "farmers addressable in India"),
        ("1.86 lakh", "Anganwadi centres, 540 crore visits"),
        ("122+", "languages spoken in India"),
        ("₹0", "marginal cost per AI action")]
for i, (n, cap) in enumerate(NUMS):
    x = 0.67 + i * 3.03
    card(s5, x, 1.30, 2.92, 1.10,
         [big(n, sz=21, c=ACC if i != 3 else GREEN, after=1.5),
          {"t": cap, "sz": 8.5, "c": INK2, "align": PP_ALIGN.CENTER, "ls": 0.92}])

card(s5, 0.67, 2.52, 7.30, 4.18,
     [label("EVERYONE HAS ONE PIECE. NOBODY HAS THE LAST MILE.", ACC),
      {"t": "WHO", "sz": 8.0, "b": True, "c": ACC, "sp_after": 1.2},
      {"t": "Bhashini, Government of India", "sz": 8.7, "b": True, "c": INK, "sp_after": 0.4},
      {"t": "$600M budget, LLMs for 100 Indian languages. Cloud scale.", "sz": 8.3, "c": INK2, "sp_after": 2.6},
      {"t": "Trilateral AI Hub (India, Italy, Africa)", "sz": 8.7, "b": True, "c": INK, "sp_after": 0.4},
      {"t": "Offline voice for agriculture and fintech, but powered by European supercompute.", "sz": 8.3, "c": INK2, "sp_after": 2.6},
      {"t": "FarmerChat / Digital Green", "sz": 8.7, "b": True, "c": INK, "sp_after": 0.4},
      {"t": "1M+ users, 30,000 h of farm audio, 16-23% WER reduction. Cloud.", "sz": 8.3, "c": INK2, "sp_after": 2.6},
      {"t": "Farm Vaidya, Farm Vighnaharta", "sz": 8.7, "b": True, "c": INK, "sp_after": 0.4},
      {"t": "5,000+ crop Q&A across 100+ crops, Telugu. Cloud, and field WER above 50%.", "sz": 8.3, "c": INK2, "sp_after": 2.6},
      {"t": "BharatSahayak, Yuverse, Bharosa AI", "sz": 8.7, "b": True, "c": INK, "sp_after": 0.4},
      {"t": "Voice-first, 3,400+ schemes, offline on 1 GB RAM. Cloud or app layer.", "sz": 8.3, "c": INK2, "sp_after": 2.6},
      {"t": "Cactus, Oído, Espressif", "sz": 8.7, "b": True, "c": INK, "sp_after": 0.4},
      {"t": "The on-device substrate, at $5 to $150, in English.", "sz": 8.3, "c": INK2, "sp_after": 3.2},
      {"t": "THE GAP:  offline  +  $5  +  grammar-safe  +  Indic  +  zero marginal cost.  Nobody has built it, and every hard component to build it is already open.",
       "sz": 9.6, "b": True, "c": GREEN, "ls": 0.95}])

card(s5, 8.20, 2.52, 4.46, 4.18,
     [label("THE THREE BUCKETS", ACC2),
      {"t": "SOCIAL", "sz": 9.0, "b": True, "c": ACC2, "sp_after": 1.2},
      {"t": "Voice is the only interface for the roughly 250 million adults who cannot read a screen. It also removes the human intermediary who today translates the question and fills the form.",
       "sz": 8.5, "c": INK, "sp_after": 3.2, "ls": 0.94},
      {"t": "ECONOMIC", "sz": 9.0, "b": True, "c": ACC2, "sp_after": 1.2},
      {"t": "The marginal cost of an AI action collapses from a metered API call to a local forward pass. No vendor lock, no per-seat pricing, no data leaving the device.",
       "sz": 8.5, "c": INK, "sp_after": 3.2, "ls": 0.94},
      {"t": "ENVIRONMENTAL", "sz": 9.0, "b": True, "c": ACC2, "sp_after": 1.2},
      {"t": "Zero network bytes per action, at 1.4 billion people. Every avoided round trip is avoided data-centre energy.",
       "sz": 8.5, "c": INK, "sp_after": 3.2, "ls": 0.94},
      {"t": "FIRST ADOPTER", "sz": 9.0, "b": True, "c": GREEN, "sp_after": 1.2},
      {"t": "One district health or agricultural app. One sub-$200 Android. One 2G-only taluka. Measured by actions completed per device per day with zero network dependence.",
       "sz": 8.5, "c": INK, "sp_after": 3.2, "ls": 0.94},
      {"t": "THE COMPILER TEST", "sz": 9.0, "b": True, "c": ACC, "sp_after": 1.2},
      {"t": "Farm advisory, scheme eligibility, price and weather, appointment booking, status check, record lookup. All enumerable, all machine-callable, all safety-critical where a wrong action destroys a crop.",
       "sz": 8.5, "c": INK, "ls": 0.94}])

# ----------------------------------------------------------------- slide 6
s6 = prs.slides[5]
REFS = [
    ("THE FAILURE WE ATTACK", ACC, [
        "arXiv 2601.05366, Lost in Execution: On the Multilingual Robustness of Tool Calling in LLMs. MLCL extends BFCL with Chinese, Hindi and Igbo.",
        "Semantically appropriate yet operationally invalid. Parameter values must follow execution conventions such as English string identifiers.",
        "Parameter value language mismatch. Failures arise at the language-execution boundary, not from intent misunderstanding. Silent non-executable calls.",
        "arXiv 2404.16816, IndicGenBench: 29 Indic languages, 13 scripts, 4 families, 1.4 billion people.",
        "arXiv 2407.13522 and Findings NAACL 2025, Indic-QA: 11 languages, subpar on low-resource, Translate-Test beats direct multilingual inference.",
    ]),
    ("THE SUBSTRATE WE STAND ON", GREEN, [
        "Cactus Compute, Needle 3 and Cactus engine. Apache 2.0. github.com/cactus-compute/needle, github.com/cactus-compute/cactus, HF Cactus-Compute/needle3.",
        "cactuscompute.com/blog: needle, needle-2, whistle, hybrid, cact-format, finetuning-needle, porting-needle. Includes a published porting oracle to test a runtime against.",
        "arXiv 2607.18363, Simple Attention Networks.",
        "Oído, arXiv 2610.13447, 9 Oct 2026. Open-vocabulary speech recognition on a $5 microcontroller without a neural accelerator.",
        "Espressif ESP-SR: WakeNet wake word, MultiNet with up to 200 commands, and on-chip TTS.",
        "DroidCall, Findings EMNLP 2025. google/mobile-actions, 9,654 rows. Salesforce xlam-function-calling-60k.",
    ]),
    ("THE DEPLOYMENT PRECEDENT", ACC2, [
        "NCMS 2026 ALC exhibit directory. Edlore AI-Server: TRL-6, no cloud connectivity, voice-assisted, peer-to-peer sync, NIST-aligned, in disconnected and contested environments.",
        "NCMS, Artificial Intelligence to Improve Supply Chain Resilience Throughout American Manufacturing, 2024. NCMS Technology Brief on hybrid AI, Oct 2026.",
        "FarmerChat, Digital Green, with a 60 Decibels study: 1M+ users, 60% acted on the advice, 83% said information was easier to access, 91% greater confidence.",
        "Farm Vaidya, IFPRI, Apr 2026: 50%+ field STT error, 30,000 h across 10 Indian languages, target under 3% WER, 5,000+ vernacular terms collected.",
        "BharatGen and IIIT Hyderabad: 13K questions across 11 low-resource Indic languages, best model near 58%.",
        "Bhashini: $600M, 100 Indian languages. Trilateral AI Hub: India, Italy and Africa.",
    ]),
]
for i, (h, col, items) in enumerate(REFS):
    x = 0.67 + i * 4.03
    blocks = [label(h, col, sz=9.2)]
    for it in items:
        blocks.append(tiny(it, sz=7.5, c=INK, after=2.0))
    card(s6, x, 1.30, 3.90, 4.80, blocks, pad=0.11)

card(s6, 0.67, 6.20, 11.99, 0.62,
     [{"t": "OURS:  Indic-ToolCall-Indic, a published benchmark extension  ·  the per-language subnetwork lattice  ·  the grammar-as-instruction-set compiler  ·  the per-script calibration and refusal protocol  ·  the ablation plan",
       "sz": 9.0, "b": True, "c": INK, "align": PP_ALIGN.CENTER, "ls": 0.95}],
     fill=CARD2)

# ----------------------------------------------------------------- delete slide 7
xml_slides = prs.slides._sldIdLst
slides = list(xml_slides)
sldId = slides[6]
rId = sldId.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
prs.part.drop_rel(rId)
xml_slides.remove(sldId)

os.makedirs(OUTDIR, exist_ok=True)
prs.save(PPTX)
print("saved:", PPTX)
