# Lesson 07 — Implied Fair Value Gap (iFVG) & Balanced Price Range (BPR)

## Narration (Edge/Bing TTS — Male)
- Voice: `en-US-GuyNeural`
- Style: Neutral / Standard
- Rate: 1.0x | Pitch: 0 | Volume: 1.0

**Video length (suggested):** 14–18 minutes  
**Level:** Beginner → Intermediate

## Learning Objectives
By the end of this lesson, you will be able to:
- Explain what an Implied Fair Value Gap is (and how it differs from a “normal” FVG)
- Identify bullish and bearish implied FVG using the overlap/wick logic
- Explain what Balanced Price Range (BPR) means
- Identify BPR as overlap of opposite fair value gaps

## Lesson Script

### 1) Hook: why ICT needs “hidden” gaps (0:00–1:30)
In the last lessons, we learned that a Fair Value Gap is visible inefficiency.  
But ICT also describes inefficiency that’s not obvious as a clean “gap on the chart.”

That’s where the **Implied Fair Value Gap** comes in.

---

### 2) Implied Fair Value Gap (iFVG) — definition (1:30–5:00)
From the book:

- **ICT implied fair value gap is not a typical Fair Value Gap**
- It is basically a **hidden fair value gap**
- The “algorithm” uses it to **reprice and balance price delivery**

In practical terms for a trader:
- You’re looking for a situation where price moves with displacement,
- but the classic visible FVG isn’t clearly drawn—
- because the wicks overlap in a way that hides the inefficiency visually.

---

### 3) How to identify an Implied FVG (5:00–10:30)
The book’s identification logic:

1) Look for **displacement-style movement**
2) Then look for **large-bodied candles** where:
   - the **body is overlapped by the wicks** of the previous and next candlesticks
   - there is **no visual fair value gap** left, but imbalance is still present

Then the book tells you two key measurement steps using Fibonacci:

#### Bullish Implied Fair Value Gap (iFVG)
- Identify a **large bullish candle**
- Its **body is overlapped** by the wicks of:
  - the candlestick before it
  - the candlestick after it
- Using Fibonacci, measure the **Consequent Encroachment (50%) level**
  - of the **upper wick** of the first candle (before the large bullish candle)
- Then measure the **50% level** of the:
  - **lower wick** of the third candle (after the large bullish candle)

**Result:** the overlapping zone is your bullish implied FVG area.

#### Bearish Implied Fair Value Gap (iFVG)
- Identify a **large bearish candle**
- Its **body is overlapped** by the wicks of:
  - the candlestick before it
  - the candlestick after it
- Fibonacci steps:
  - measure the 50% level of the **lower wick** of the first candle (before the large bearish candle)
  - then measure the 50% level of the **upper wick** of the third candle (after the large bearish candle)

**Result:** the zone between those 50% encroachment levels is your bearish implied FVG.

---

### 4) Example explanation (10:30–12:30)
When you teach it in a way students can follow, use this template:

- “Step 1: find displacement.”
- “Step 2: locate the large-body candle.”
- “Step 3: confirm that wicks overlap and there’s no clean visible gap.”
- “Step 4: apply 50% consequential encroachment with Fibonacci.”
- “Step 5: the overlap becomes the iFVG zone.”

---

## 5) Balanced Price Range (BPR) — definition (12:30–16:00)
From the book:

- **Balanced price range (BPR)** is the area on price chart
- where **two opposite fair value gaps overlap**

How to identify BPR:
1) Mark the **fair value gap on the sell side of price**
2) Mark another **fair value gap on the buy side of price**
3) Ensure they are **horizontally opposite** (one corresponds to sells, the other to buys)
4) Find the overlap area where both FVGs intersect
5) That overlap = **BPR**

---

## 6) How to use BPR conceptually (16:00–18:00)
BPR represents a “balanced” zone where:
- price delivery may slow,
- and decisions often happen (in a full ICT system you’d combine with PD-Array context and execution logic).

For this critical-path course version:
- treat BPR as a **zone-building** tool you’ll later use with confirmation.

---

## Practice / Assignment
Pick a chart (replay is fine) and do the following:

1) Find 1 implied FVG and label it bullish or bearish.
2) Write down:
   - where the overlap is
   - which wick measurement you used (50% encroachment)
3) Find 2 opposite FVGs and show where they overlap.
4) Label that overlap as BPR.

## Recap (Last 30 seconds)
- Implied FVG is hidden inefficiency created by displacement + overlapped wicks.
- You locate iFVG using a 50% consequential encroachment measurement.
- Balanced Price Range (BPR) is overlap of opposite fair value gaps.
- Next lesson: Rejection Block → Vacuum Block → Mitigation Block.
