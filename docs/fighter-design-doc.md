# Fighter (Game 1) — Design Reference

*Living document — current-state reference only. Companion changelog: `changelog.md`.*

---

## 1. Trilogy Position & Rationale

Fighter is the **first** game in the trilogy, despite the tactics RPG (now Game 2) originally being conceived first. The trilogy order was deliberately restructured mid-development:

- **Game 1 — Fighter:** turn-based fantasy tournament fighter (this document)
- **Game 2 — RPG:** the tactics RPG (originally conceived as Game 1)
- **Game 3 — Expanded RPG:** the unnamed sequel, built on Game 2's foundation

**Why reorder:** combat and animation are the highest-risk, highest-cost elements shared across all three games. Perfecting them in a standalone fighter first gives Games 2 and 3 a proven, battle-tested engine to inherit rather than prototyping combat under the higher stakes of a full RPG. This is **risk-front-loading as trilogy strategy** — Games 2 and 3 build on tested foundations instead of each re-solving combat and animation from scratch.

---

## 2. Core Concept

Fighter is a **turn-based fantasy tournament fighter** built around the 64 hexagrams of the King Wen I Ching sequence as its structural and cosmological foundation. The cast maps directly to the hexagram space:

- **28 unordered trigram combinations** (non-mirror pairings, collapsed the same way Game 2 collapses them — order-agnostic)
- **+ 8 self-pair outcomes** (a trigram mirrored with itself)
- **= 36 total fighters/characters**

This roster size and structure intentionally mirrors the hexagram-space logic already established for Game 2, giving the trilogy a consistent cosmological backbone from the very first game.

---

## 3. Roster & Unlock Curve

- **Roster size:** 36 fighters, drawn from the hexagram space (see above)
- **Unlock curve:** Triangular progression — 1 match unlocks fighter 2, 2 more matches unlock fighter 3, and so on, with the required match count increasing by one each time
- **Total matches to fully unlock the roster:** 630 matches
- **Estimated playtime:** a substantial but fully completable arc, at a few minutes per match

---

## 4. Spawn Mechanic — Fate as Onboarding

- On **first launch**, the game performs an **automatic I Ching coin-cast** to assign the player's starting fighter.
- This is not cosmetic — it's a **functional randomization system** for player onboarding, consistent with the trilogy's cosmological theme.
- This spawn mechanic is the Fighter-scale echo of Game 2's much larger "Fate over Choice" philosophy (where fate, not player choice, determines a unit's ultimate class) — Fighter establishes the fate-driven identity of the whole trilogy at its smallest, most immediate scale.

---

## 5. Unlock Reveal — "New Challenger Approaches"

- Each new character is revealed via a **silhouette mechanic**: the player sees a shadowed outline of the upcoming fighter before earning them.
- The player must **defeat** each new challenger to unlock them — unlocking is earned through combat, not simply awarded for reaching a match-count threshold.

---

## 6. Combat System

**Combat Loop:**
- **Attacker** chooses an attack type **and** a live cadence (timing of the attack's delivery).
- **Defender** reacts in real time, choosing between three responses: **Dodge**, **Block**, or **Parry**.
- This real-time reactive layer sits on top of the game's turn-based structure — turns determine initiative/sequencing, but the attack/defense exchange itself is a live skill check.

**HP & Attack Economy:**
- **100 HP** per fighter.
- **Three base attack tiers:** Regular, Heavy, and Critical.
- Each of the **eight trigram archetypes** has its own speed and power multipliers across all three attack tiers — an archetype's identity is expressed through how its Regular/Heavy/Critical attacks feel to use and to defend against, not just through flat stat differences.

**Defensive Skill Ladder (four tiers, weakest to strongest outcome):**
1. **Standard Block** — chip damage still gets through (~15% of the attack's value).
2. **Perfect Block** — full damage negation, requires correct timing.
3. **Dodge** — full damage negation, requires correctly reading the attack *type* (not just timing).
4. **Parry** — full damage negation **plus** a counter-hit that returns the parried attack's own damage value back at the attacker.

**Parry scales automatically:** counter-hit damage on a successful parry equals the parried attack's own value, rather than needing a separate damage table. This is an elegant, self-balancing design — a Critical-tier attack that gets parried costs the attacker Critical-tier damage right back, with no extra tuning required as new attacks or archetypes are added.

**Cadence Variability — Deliberately Deferred:**
- **Cadence variability** (varying the live timing/rhythm of attacks beyond a fixed baseline) is intentionally **deferred** until stable base animation timings are established.
- Rationale: locking down base timings first avoids having to re-tune cadence variation every time an animation timing changes. This is the current item "on the horizon" — establishing those stable base animation timings is the next concrete step before cadence variability work begins.

---

## 7. Art Direction (Locked, Trilogy-Wide)

- **In-match animation style:** GBA-era Fire Emblem pixel art — specifically sprites sourced from *Fire Emblem: The Blazing Blade*.
- **Character portraits & key art:** classic Yu-Gi-Oh OCG card art, Volume 1 through Rise of Destiny (1999–2004 era).
- Both choices are **locked** as standards for the entire trilogy, not just Fighter — establishing them here in Game 1 is part of the risk-front-loading strategy (see Section 1).

---

## 8. Voice & Localization Direction (Locked, Trilogy-Wide)

- **Japanese voice acting with English subtitles** — confirmed as the VO direction for the trilogy, no English dub planned.

---

## 9. Tools & Art References

- **GBA-era *Fire Emblem: The Blazing Blade* sprite sheets** as the primary art reference, including:
  - Player Units: Athos (Archsage), Eliwood (Lord & Knight Lord), Hector (Lord), Lyn (Blade Lord), Guy (Swordmaster), Hawkeye
  - Generic Units: Sniper (Female), Archer, Troubadour, Warrior, Cavalier, Assassin, General, Paladin
  - Enemy Units: Magic Seal, Soldier, Sonia, Brigand
- **King Wen hexagram lookup grid** as the structural reference for the trigram/hexagram system (rows = lower trigram, columns = upper trigram, cells = the traditional King Wen hexagram number).
- **Classic Yu-Gi-Oh OCG card art** (1999–2004 era) as the portrait/key art reference.

---

## 10. On the Horizon

- Establishing **stable base animation timings** for Fighter's combat before introducing cadence variability (see Section 6).
- Fighter's proven combat/animation engine is intended to be the foundation Game 2 and Game 3 build on — no rework of core timing/feel systems planned once this is locked.

---

## 11. Trilogy-Wide Design Principles Established Here

- **Risk-front-loading as trilogy strategy:** the hardest shared systems (combat, animation) are solved once, in Fighter, so Games 2 and 3 inherit a tested engine.
- **Simplification over optionality:** carried forward into Game 2's promotion system, where self-pair hexagram outcomes were collapsed from a dual mirror-outcome model to a single outcome per hexagram — the same "cleaner over more optional" instinct that shapes Fighter's own scope choices (e.g. deferring cadence variability rather than shipping it half-tuned).
- **Fate as mechanic, not flavor:** Fighter's coin-cast spawn mechanic is the first, smallest-scale expression of a philosophy that becomes Game 2's headline pillar ("Fate over Choice") before Game 3 deliberately inverts it into "Choose Your Own Destiny."
