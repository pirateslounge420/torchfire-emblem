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

Fighter is a **turn-based fantasy tournament fighter** built on the 64 hexagrams of the King Wen I Ching sequence. Every fighter is a full hexagram: two of the eight trigrams stacked, one on the bottom and one on top, and **the order matters**.

- **56 mixed fighters:** two different trigrams. The same pair in the opposite order (Fire over Mountain vs. Mountain over Fire) is a different fighter.
- **8 pure fighters:** a trigram doubled with itself. These keep the named archetypes (see Section 3).
- **= 64 fighters**, one per hexagram.

The roster's hexagram logic carries across the trilogy, giving all three games one cosmological backbone.

---

## 3. The Eight Trigrams

Each trigram brings one archetype and one weapon to every fighter it appears in.

| Trigram | Archetype | Weapon | Color | Mount | Steed creature (male / female) | Pure fighter (doubled) |
|---|---|---|---|---|---|---|
| ☰ Qián (Heaven) | Vanguard (ground cavalry) | Axes | Purple | Ground | War horse / zebra | Paladin |
| ☳ Zhèn (Thunder) | Damage Magic | Heavy staff (long, heavy-headed, two-handed, slow) | Cyan | — | Wolf / jackal | Shaman |
| ☵ Kǎn (Water) | Trickster Mage | Throwing cards | Indigo | — | Crane / heron | Jester |
| ☶ Gèn (Mountain) | Heavy Armor | Glaive | Orange | — | Tortoise / turtle | Bastion |
| ☷ Kūn (Earth) | Support Magic | Short staff (healer's rod, quick) | Yellow | — | Boar / warthog | Sage |
| ☴ Xùn (Wind) | Flying Cavalry | Lance | Seafoam (light green) | Flying | Wyvern / drake | Valkyrie |
| ☲ Lí (Fire) | Rogue | Daggers | Red | — | Lion / tiger | Shinobi |
| ☱ Duì (Lake) | Swordsman | Sword | Silver | — | Mountain goat / sheep | Samurai |

*The steed creature column is the creature a mounted fighter rides when this trigram is its base (Section 6). Only the male creature ships at launch.*

**Weapon lineup (locked Oct 15, 2026).** Fighter is a gladiator-style tournament, so there are no ranged weapons: the bow, shield and gauntlets are gone. The two staffs must read differently on the sprite — Earth's is short and fast, Thunder's is long and heavy. Shinobi (Fire) and Samurai (Lake) are now in Fighter; Shinobi is released from the Game 3 reserved list, and Captain is no longer used. *OPEN: whether Water's throwing cards get a ranged exemption as spell delivery rather than archer's reach.*

**Colors** follow the traditional Five Elements colors (as color only — the Five Elements aren't a mechanic in Fighter): Thunder and Wind share Wood's blue-green family, Earth and Mountain share Earth's warm tones, Lake takes Metal's silver, Fire is red and Water is indigo. Heaven is the exception: its purple comes from the Purple Forbidden Enclosure, the Celestial Emperor's star-palace. Shading notes: keep Thunder's cyan leaning blue and Wind's seafoam leaning green, and keep Water's indigo on the blue side so it doesn't drift into Heaven's purple.

---

## 4. How the Two Trigrams Combine

- **Both weapons:** a fighter wields the weapons of both its trigrams, so Fire over Mountain fights with daggers and a glaive. A pure fighter wields its trigram's single weapon.
- **Both colors:** a fighter carries both of its trigrams' color palettes, each kept clean and readable — never mixed into one blended hue. A pure fighter carries its trigram's single palette.
- **Bottom trigram = base archetype:** who the fighter started as.
- **Top trigram = what they became:** the class their base grew into.
- **No leveling up in Fighter:** every fighter arrives as a full hexagram. Promotion as a mechanic (starting as a single-trigram unit and growing into a hexagram) arrives in Game 2.
- **Order matters:** because bottom and top play different roles, the two orders of a pair are different fighters. *How the order shows up in combat (for example, which weapon a fighter leads with) — OPEN, see Section 13.*

---

## 5. The 64 Fighters — King Wen Grid

Rows are the **bottom (base)** trigram; columns are the **top** trigram. Each cell is the traditional King Wen hexagram number, which gives every fighter an authentic I Ching identity (number, name, imagery) to draw names and lore from. The bold diagonal holds the 8 pure fighters.

| Bottom ↓ / Top → | ☰ Heaven | ☳ Thunder | ☵ Water | ☶ Mountain | ☷ Earth | ☴ Wind | ☲ Fire | ☱ Lake |
|---|---|---|---|---|---|---|---|---|
| **☰ Heaven** | **1** | 34 | 5 | 26 | 11 | 9 | 14 | 43 |
| **☳ Thunder** | 25 | **51** | 3 | 27 | 24 | 42 | 21 | 17 |
| **☵ Water** | 6 | 40 | **29** | 4 | 7 | 59 | 64 | 47 |
| **☶ Mountain** | 33 | 62 | 39 | **52** | 15 | 53 | 56 | 31 |
| **☷ Earth** | 12 | 16 | 8 | 23 | **2** | 20 | 35 | 45 |
| **☴ Wind** | 44 | 32 | 48 | 18 | 46 | **57** | 50 | 28 |
| **☲ Fire** | 13 | 55 | 63 | 22 | 36 | 37 | **30** | 49 |
| **☱ Lake** | 10 | 54 | 60 | 41 | 19 | 61 | 38 | **58** |

*Example: Fire over Mountain (Mountain row, Fire column) is #56; Mountain over Fire is #22.*

---

## 6. Steeds (Heaven & Wind Only)

- Only the two archetypally mounted trigrams grant a steed: **Heaven** (ground) and **Wind** (flying). A fighter is mounted if Heaven or Wind appears in **either** trigram slot, base or top. That is 28 of the 64 fighters (confirmed count).
- **The base trigram picks the creature.** Each trigram has its own creature (Section 3 and the table below), and a mounted fighter's steed is the creature of its bottom (base) trigram.
- **Heaven or Wind decides grounded vs. flying.** If Heaven is the mount trigram, the steed is a ground version of the creature; if Wind is, it's a flying version.
- **Fighters with both Heaven and Wind:** the top (non-base) trigram decides grounded vs. flying, while the base still picks the creature. Heaven over Wind rides a flying war horse; Wind over Heaven rides a ground wyvern. The pure fighters ride a ground war horse (Heaven over Heaven) and a flying wyvern (Wind over Wind). For example, Water over Heaven rides a ground crane, and Earth over Wind rides a flying boar.
- **No hybrid steeds.** Fusing two creatures into one per pairing was considered and rejected in favor of this simpler system: one creature, in a ground or flying variant.
- **Custom creature set.** The steeds are Mike's own picks, not the traditional Shuo Gua animals. Each trigram's creature has a **male** and a **female** variant: two closely related but distinct species, in the spirit of lion and tiger. Silhouettes should read clearly, not as recolored horses.

| Trigram (base) | Male (ships at launch) | Female (post-launch) |
|---|---|---|
| ☰ Heaven | Strong war horse | Zebra |
| ☳ Thunder | Wolf | Jackal |
| ☵ Water | Crane — big, elegant, almost dinosaur-like; trumpeting calls and display dancing | Heron — leaner, silent stalking predator |
| ☶ Mountain | Big, hefty, heavily armored tortoise | Turtle |
| ☷ Earth | Wild tusked boar | Warthog |
| ☴ Wind | Wyvern (two-legged) | Drake (four-legged) |
| ☲ Fire | Lion | Tiger |
| ☱ Lake | Horned mountain goat (ram-like) | Sheep (ewe) |

- **Launch scope: male variants only.** Fighter ships with just the male creature of each pair (goat, wyvern, war horse, boar, wolf, lion, crane, tortoise) to halve the sprite workload. The female variants (sheep, drake, zebra, warthog, jackal, tiger, heron, turtle) are a planned post-launch quality-of-life update, not part of the initial scope.
- *How a fighter gets its female variant once those are added — OPEN, see Section 13.*
- The creature look is **reserved for riders**. Non-mounted fighters are recognized by their two weapons and two colors.
- *Art and visual design for each of the 28 steeds — OPEN, see Section 13.*

---

## 7. Starting Fighter — Fate as Onboarding

- On **first launch**, an automatic I Ching cast assigns the player's starting fighter: one random hexagram from all 64.
- Casts in Fighter are **plain random hexagrams** — every fighter is equally likely, so pure fighters are no rarer than mixed ones. Changing lines and cast-based rarity are saved for Game 2.
- This is not cosmetic — it's a **functional randomization system** for player onboarding, and the Fighter-scale echo of Game 2's much larger "Fate over Choice" philosophy (where fate, not player choice, determines a unit's ultimate class).

---

## 8. Unlocking — "New Challenger Approaches"

- New fighters are unlocked by **casting**. Each cast lands on a hexagram, and that fighter shows up as the next challenger.
- The challenger is revealed in **silhouette** first; the player must **defeat** them to unlock them. Unlocking is earned through combat.
- A cast that lands on a fighter the player already owns is **re-rolled** until it lands on a new one.
- *How often a cast happens — OPEN, see Section 13.*

---

## 9. Combat System

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

## 10. Art Direction (Locked, Trilogy-Wide)

- **In-match animation style:** GBA-era Fire Emblem pixel art — specifically sprites sourced from *Fire Emblem: The Blazing Blade*.
- **Character portraits & key art:** classic Yu-Gi-Oh OCG card art, Volume 1 through Rise of Destiny (1999–2004 era).
- Both choices are **locked** as standards for the entire trilogy, not just Fighter — establishing them here in Game 1 is part of the risk-front-loading strategy (see Section 1).

---

## 11. Voice & Localization Direction (Locked, Trilogy-Wide)

- **Japanese voice acting with English subtitles** — confirmed as the VO direction for the trilogy, no English dub planned.

---

## 12. Tools & Art References

- **GBA-era *Fire Emblem: The Blazing Blade* sprite sheets** as the primary art reference, including:
  - Player Units: Athos (Archsage), Eliwood (Lord & Knight Lord), Hector (Lord), Lyn (Blade Lord), Guy (Swordmaster), Hawkeye
  - Generic Units: Sniper (Female), Archer, Troubadour, Warrior, Cavalier, Assassin, General, Paladin
  - Enemy Units: Magic Seal, Soldier, Sonia, Brigand
- **King Wen hexagram lookup grid** as the structural reference for the trigram/hexagram system (reproduced in Section 5).
- **Shuo Gua** ("Discussion of the Trigrams," one of the Ten Wings commentaries) as the traditional source of trigram animals. Fighter's steeds now use a custom creature set instead (Section 6).
- **Classic Yu-Gi-Oh OCG card art** (1999–2004 era) as the portrait/key art reference.

---

## 13. Open Questions

1. **How trigram order shows up in combat** — for example, which of a fighter's two weapons leads.
2. **Unlock pacing** — how many matches between casts. The earlier triangular curve (1 match, then 2 more, then 3 more…) was sized for 36 fighters (630 matches); applied to 64 it becomes 2,016 matches, roughly 70–100 hours at 2–3 minutes a match.
3. **Female steed variants (post-launch)** — launch is male-only (Section 6), so nothing is needed for launch. For the later update, how a fighter gets the female version is still open; the doc doesn't give fighters a gender yet.
4. **Steed art for the 28 mounted fighters** — the visual design of each steed.
5. **Names for the 56 mixed fighters** — each already has a King Wen number and traditional name to draw from (Section 5).

---

## 14. On the Horizon

- Establishing **stable base animation timings** for Fighter's combat before introducing cadence variability (see Section 9).
- Fighter's proven combat/animation engine is intended to be the foundation Game 2 and Game 3 build on — no rework of core timing/feel systems planned once this is locked.

---

## 15. Trilogy-Wide Design Principles Established Here

- **Risk-front-loading as trilogy strategy:** the hardest shared systems (combat, animation) are solved once, in Fighter, so Games 2 and 3 inherit a tested engine.
- **Simplification over optionality:** carried forward into Game 2's promotion system, where self-pair hexagram outcomes were collapsed from a dual mirror-outcome model to a single outcome per hexagram — the same "cleaner over more optional" instinct that shapes Fighter's own scope choices (e.g. deferring cadence variability rather than shipping it half-tuned).
- **Fate as mechanic, not flavor:** Fighter's casts (for the starting fighter and every challenger) are the first, smallest-scale expression of a philosophy that becomes Game 2's headline pillar ("Fate over Choice") before Game 3 deliberately inverts it into "Choose Your Own Destiny."
- **Trilogy sync note:** Fighter now uses the full order-sensitive 64 hexagrams, which earlier docs listed as a Game 3 feature. The Game 2 and Game 3 docs (kept outside this repo) need a sync pass.
