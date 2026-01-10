# style_guidelines.md

These guidelines describe the coding and documentation style preferred in this repository. They exist to keep the codebase consistent, readable, and easy to maintain.

## General Principles
- Favor clarity over cleverness.
- Keep functions small, explicit, and deterministic.
- Avoid unnecessary abstractions or indirection.
- Prefer straightforward control flow.
- Use the standard library whenever possible.
- When in doubt, choose the simplest readable solution.

## Python Style
- Use explicit imports, avoid wildcard imports.
- Prefer simple expressions over compact one-liners.
- Avoid hidden side effects.
- Use type checks only when they improve clarity.
- Prefer returning simple tuples or dicts over custom classes unless needed.
- Keep error handling explicit and minimal.
- Avoid magic; make behavior obvious from reading the code.

## Naming
- Use descriptive but concise names.
- Avoid abbreviations unless they are universally understood.
- Functions should be verbs or verb phrases.
- Variables should reflect their purpose, not their type.

## File and Folder Structure
- Keep the repository flat and simple.
- Use `.ai_support/` for AI-related notes and prompts.
- Keep scripts self-contained unless sharing logic is necessary.

## Documentation
- Use docstrings for functions that are not self-explanatory.
- Keep comments short and factual.
- Document intent, not mechanics.
- Avoid over-commenting obvious code.

## GitPython-Specific Notes
- Be explicit about types when interacting with GitPython objects.
- Convert paths to strings when passing to os.path functions.
- Use assertions to enforce assumptions when helpful.
- Handle missing directories defensively.

## Interaction With AI
- Keep prompts minimal and context-focused.
- Maintain a record of important AI-assisted debugging sessions in AI_interaction.md.
- Use this style guide to ensure AI-generated suggestions stay aligned with the project philosophy.
