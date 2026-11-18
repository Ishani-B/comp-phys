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
