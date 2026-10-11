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

| Trigram | Archetype | Weapon | Color | Mount | Pure fighter (doubled) |
|---|---|---|---|---|---|
| ☰ Qián (Heaven) | Vanguard (ground cavalry) | Axes | Purple | Ground | Paladin |
| ☳ Zhèn (Thunder) | Damage Magic | Staff | Cyan | — | Shaman |
| ☵ Kǎn (Water) | Ranged Skirmisher | Bows | Indigo | — | Jester |
| ☶ Gèn (Mountain) | Heavy Armor | Shields | Orange | — | Bastion |
| ☷ Kūn (Earth) | Support Magic | Club/Hammer | Yellow | — | Sage |
| ☴ Xùn (Wind) | Flying Cavalry | Lance | Seafoam (light green) | Flying | Valkyrie |
| ☲ Lí (Fire) | Rogue | Blades | Red | — | Samurai |
| ☱ Duì (Lake) | Brawler | Gauntlets | Silver | — | Captain |

*Steed creatures are not tied to trigrams in this table yet — the eight creature pairs are set (Section 6), but which trigram gets which is OPEN, see Section 13.*

**Colors** follow the traditional Five Elements colors (as color only — the Five Elements aren't a mechanic in Fighter): Thunder and Wind share Wood's blue-green family, Earth and Mountain share Earth's warm tones, Lake takes Metal's silver, Fire is red and Water is indigo. Heaven is the exception: its purple comes from the Purple Forbidden Enclosure, the Celestial Emperor's star-palace. Shading notes: keep Thunder's cyan leaning blue and Wind's seafoam leaning green, and keep Water's indigo on the blue side so it doesn't drift into Heaven's purple.

---

## 4. How the Two Trigrams Combine

- **Both weapons:** a fighter wields the weapons of both its trigrams, so Fire over Mountain fights with blades and a shield. A pure fighter wields its trigram's single weapon.
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
- **The base trigram picks the creature.** Each trigram gets one of eight creature slots (listed below), and a mounted fighter's steed comes from the slot of its bottom (base) trigram. *Which slot goes with which trigram — OPEN, see Section 13.*
- **Heaven or Wind decides grounded vs. flying.** If Heaven is the mount trigram, the steed is a ground version of the creature; if Wind is, it's a flying version.
- **Fighters with both Heaven and Wind:** the top (non-base) trigram decides grounded vs. flying, while the base still picks the creature. Heaven over Wind rides a flying version of the Heaven-slot creature; Wind over Heaven rides a ground version of the Wind-slot creature. The pure fighters ride a ground version (Heaven over Heaven) and a flying version (Wind over Wind) of their own trigram's creature.
- **No hybrid steeds.** Fusing two creatures into one per pairing was considered and rejected in favor of this simpler system: one creature, in a ground or flying variant.
- **Custom creature set.** The steeds are Mike's own picks, not the traditional Shuo Gua animals. Each slot has a **male** and a **female** variant: two closely related but distinct species, in the spirit of lion and tiger. Silhouettes should read clearly, not as recolored horses.

| Creature slot | Male | Female |
|---|---|---|
| Goat | Horned mountain goat (ram-like) | Sheep (ewe) |
| Dragon | Wyvern (two-legged) | Drake (four-legged) |
| Horse | Strong war horse | Zebra |
| Pig | Wild tusked boar | Warthog |
| Dog | Wolf | Jackal |
| Cat | Lion | Tiger |
| Crane | Crane — big, elegant, almost dinosaur-like; trumpeting calls and display dancing | Heron — leaner, silent stalking predator |
| Tortoise | Big, hefty, heavily armored tortoise | Turtle |

- *How a fighter gets its male or female variant — OPEN, see Section 13.*
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
3. **Steed creature-to-trigram assignment** — the eight creature slots and their male/female variants are set (Section 6), but which slot goes with which trigram is not decided. The grounded/flying rule stays as locked.
4. **Male/female variant** — how a fighter gets the male or female version of its steed creature. The doc doesn't give fighters a gender yet.
5. **Steed art for the 28 mounted fighters** — the visual design of each steed.
6. **Names for the 56 mixed fighters** — each already has a King Wen number and traditional name to draw from (Section 5).

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
