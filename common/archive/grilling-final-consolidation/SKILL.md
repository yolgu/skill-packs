---
name: grilling-final-consolidation
description: Produce the complete closing consolidation for a finished grilling session. Use only after every material question has been resolved and the user has explicitly confirmed shared understanding; never use during the interview.
disable-model-invocation: true
---

# Grilling Final Consolidation

Apply this instruction to the entire completed grilling session:

> Based on everything we have discussed so far while working to bring this together, consolidate your recommendations and the preferences I have expressed. Do not merely summarize. Include every point discussed, without omitting, skipping, or condensing anything. Save the complete consolidation as a Markdown file instead of returning the full content inline, at `docs/plans/YYYY-MM-DD-<topic>/design.md` in the current workspace, creating the folder if necessary. Leave process records such as the decision tree where they already are (for example under `outputs/`).

Return only a concise confirmation, a link to the saved file, and one handoff line as the closing response: the next step is for the user to invoke the planning skill (writing-plans) with this design document's path. Do not invoke it yourself and do not proceed to implementation.
