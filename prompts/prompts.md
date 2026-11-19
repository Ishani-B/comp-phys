# Prompts

Every prompt you send gets an ID here. Your run log records the ID. If you
change one word of a prompt, give it a new ID.

---

## P1

**Used for:** Every free-fall item (Starter: all 30 items in `data/freefall_starter.csv`). Sent as the only user message in a new chat, no system prompt.
**Added:** 18 November 2026

```
A ball is dropped on a planet. The table shows how far it has fallen (meters) after each number of seconds.

[TABLE]

How far has it fallen at [T] seconds? End with 'Answer: X'.
```

`[TABLE]` is replaced by a header line and six rows, one per second:

```
Seconds | Meters
1 | 4.9
2 | 19.6
3 | 44.1
4 | 78.4
5 | 122.5
6 | 176.4
```

`[T]` is the item's `test_t`. The `prompt` column of the data file holds the full text of every prompt as sent.

---

## P2

**Used for:** Virtual lab, physics framing: one user message, no system prompt, with the tool below. 60 episodes (exact and noisy readings).
**Added:** 18 November 2026

```
You are in a lab on a planet. You can drop a ball and measure how far it has fallen, in meters, after any number of seconds you choose between 0 and 6, using the drop_ball tool. The drop tower only allows up to 6 seconds of fall, so you can't measure [T] seconds directly. You can take up to 8 measurements. Your goal is to work out how far the ball will have fallen after [T] seconds. When you're done measuring, state the rule you found, then end with 'Answer: X'.
```

`[T]` is the item's `test_t`. Tool offered (OpenAI-style function definition, `tool_choice: auto`):

```json
{
  "type": "function",
  "function": {
    "name": "drop_ball",
    "description": "Drop the ball and measure how far it has fallen after the given number of seconds. Returns the distance in meters.",
    "parameters": {
      "type": "object",
      "properties": {
        "seconds": {
          "type": "number",
          "description": "Time after release, in seconds. Must be greater than 0 and at most 6."
        }
      },
      "required": [
        "seconds"
      ]
    }
  }
}
```

Tool replies, sent back as JSON: a valid call returns `{"seconds": t, "meters": reading, "measurements_left": n}`. A time outside 0 < t ≤ 6 returns `{"error": "Only times between 0 and 6 seconds are possible."}` and uses no measurement. After 8 valid measurements every call returns `{"error": "No measurements left. Give your answer."}`. An unreadable value returns an error and uses no measurement. At most 12 model turns per episode.

---

## P3

**Used for:** Virtual lab, neutral framing (no physics cues): one user message, no system prompt, with the tool below. 60 episodes (exact and noisy readings).
**Added:** 18 November 2026

```
You are working with a device that has a dial and a counter. You can set the dial to any number of tocks you choose between 0 and 6 and read how many glims the counter shows, using the read_counter tool. The dial only goes up to 6 tocks, so you can't read [T] tocks directly. You can take up to 8 readings. Your goal is to work out how many glims the counter will show at [T] tocks. When you're done taking readings, state the rule you found, then end with 'Answer: X'.
```

`[T]` is the item's `test_t`. Tool offered (OpenAI-style function definition, `tool_choice: auto`):

```json
{
  "type": "function",
  "function": {
    "name": "read_counter",
    "description": "Set the dial to the given number of tocks and read the counter. Returns the number of glims.",
    "parameters": {
      "type": "object",
      "properties": {
        "tocks": {
          "type": "number",
          "description": "Dial setting, in tocks. Must be greater than 0 and at most 6."
        }
      },
      "required": [
        "tocks"
      ]
    }
  }
}
```

Tool replies, sent back as JSON: a valid call returns `{"tocks": t, "glims": reading, "readings_left": n}`. A time outside 0 < t ≤ 6 returns `{"error": "Only dial settings between 0 and 6 tocks are possible."}` and uses no measurement. After 8 valid measurements every call returns `{"error": "No readings left. Give your answer."}`. An unreadable value returns an error and uses no measurement. At most 12 model turns per episode.

---

## P4

**Used for:** Standard run, Hooke items (`data/hooke_standard.csv`), both models. One user message, no system prompt.
**Added:** 19 November 2026

```
Weights are hung from a spring. The table shows how far the spring stretches (centimeters) for each weight (grams).

[TABLE]

How far will it stretch with [X] grams? End with 'Answer: X'.
```

`[TABLE]` is a header line (`Grams | Centimeters`) and six rows. `[X]` is the item's `test_x`.

---

## P5

**Used for:** Standard run, Kepler items (`data/kepler_standard.csv`), both models. One user message, no system prompt.
**Added:** 19 November 2026

```
Moons travel in circles around a planet. The table shows how many days one full circle takes for a moon at each distance from the planet (thousands of kilometers).

[TABLE]

How many days does one full circle take at [X] thousand kilometers? End with 'Answer: X'.
```

`[TABLE]` is a header line (`Thousand km | Days`) and six rows. `[X]` is the item's `test_x`.

---

## P6

**Used for:** Lab extension, Hooke, spring story: one user message, no system prompt, with the tool below. 30 episodes per model (Gemma 4 31B, Claude Sonnet 4.6).
**Added:** 19 November 2026

```
You are in a lab with a spring. You can hang any weight you choose between 0 and 600 grams on the spring and measure how far it stretches, in centimeters, using the hang_weight tool. The spring can only be tested with up to 600 grams, so you can't measure [T] grams directly. You can take up to 8 measurements. Your goal is to work out how far the spring will stretch with [T] grams. When you're done measuring, state the rule you found, then end with 'Answer: X'.
```

`[T]` is the item's `test_x` (700–1600). Tool offered (`tool_choice: auto`):

```json
{
  "type": "function",
  "function": {
    "name": "hang_weight",
    "description": "Hang the given weight on the spring and measure how far it stretches. Returns the stretch in centimeters.",
    "parameters": {
      "type": "object",
      "properties": {
        "grams": {
          "type": "number",
          "description": "Weight to hang, in grams. Must be greater than 0 and at most 600."
        }
      },
      "required": [
        "grams"
      ]
    }
  }
}
```

A valid call returns `{"grams": x, "centimeters": reading, "measurements_left": n}`. Outside 0 < x ≤ 600 returns `{"error": "Only weights between 0 and 600 grams are possible."}` and uses no measurement. After 8 measurements: `{"error": "No measurements left. Give your answer."}`. At most 12 model turns.

---

## P7

**Used for:** Lab extension, Hooke, neutral dial (no physics cues): one user message, no system prompt, with the tool below. 30 episodes per model (Gemma 4 31B, Claude Sonnet 4.6).
**Added:** 19 November 2026

```
You are working with a device that has a dial and a counter. You can set the dial to any number of tocks you choose between 0 and 600 and read how many glims the counter shows, using the read_counter tool. The dial only goes up to 600 tocks, so you can't read [T] tocks directly. You can take up to 8 readings. Your goal is to work out how many glims the counter will show at [T] tocks. When you're done taking readings, state the rule you found, then end with 'Answer: X'.
```

`[T]` is the item's `test_x` (700–1600). Tool offered (`tool_choice: auto`):

```json
{
  "type": "function",
  "function": {
    "name": "read_counter",
    "description": "Set the dial to the given number of tocks and read the counter. Returns the number of glims.",
    "parameters": {
      "type": "object",
      "properties": {
        "tocks": {
          "type": "number",
          "description": "Dial setting, in tocks. Must be greater than 0 and at most 600."
        }
      },
      "required": [
        "tocks"
      ]
    }
  }
}
```

A valid call returns `{"tocks": x, "glims": reading, "readings_left": n}`. Outside 0 < x ≤ 600 returns `{"error": "Only dial settings between 0 and 600 tocks are possible."}` and uses no measurement. After 8 measurements: `{"error": "No readings left. Give your answer."}`. At most 12 model turns.
