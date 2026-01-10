# context_prompt.md

This document defines the minimal context I want to provide to the AI when working on this repository.

## Project Description
This repository contains tools and scripts for managing Git submodules in a clean, deterministic, and automation-friendly way. The codebase favors clarity, minimalism, and explicit behavior over abstraction.

## Coding Style
- Prefer simple, readable, linear code.
- Avoid unnecessary abstractions.
- Use explicit type checks when they improve clarity.
- Keep functions deterministic and side-effect aware.
- Prefer standard library solutions unless GitPython is required.

## AI Expectations
When interacting with the AI:
- Provide explanations that are concise and technically accurate.
- Respect the project's minimalist style.
- Avoid over-engineering or unnecessary complexity.
- When debugging, focus on root causes and type inference issues.
- When suggesting improvements, keep them aligned with the existing code philosophy.

## Repository Conventions
- `.ai_support/` contains AI-related notes, interactions, and prompts.
- `AI_interaction.md` stores important debugging conversations.
- `context_prompt.md` (this file) defines the context for future AI sessions.
- Additional files may be added as needed, but the folder should remain lightweight.

## Purpose
This file exists to give future AI interactions a stable reference about:
- how the project works,
- how I prefer code to be written,
- and what kind of assistance is most useful.
