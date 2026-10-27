# Storyboard request: pointer

The canonical prompt template is `12_advanced_animations_with_claude/06_prompts_and_templates/storyboard_request.md` (owned by the prompts-and-templates folder). Do not fork it here.

When filling it for a generated grid, this skill adds or checks:
- **Panels:** nine portrait (9:16) panels in beat order, thin gutters in the style background colour.
- **No text:** "no text, no letters, no numbers, no labels" in the prompt; panel numbers are overlaid in code afterwards (#54).
- **Reference image:** the hero character reference (asset-library ID) attached for every grid with the recurring character (#48).
- **Style:** the pinned style guide's look paragraph, palette names and "flat, straight-on" composition ([V4-MP]); no 3D, gloss or heavy blur for collage.
- **Model:** as configured in the provider worker (in [V4-MP]: `gpt_image_2_5`); never a premium video model.
- **Beats:** one line per panel from `beats.json` descriptions, nothing invented.
- **Estimate approval ID:** the approved estimate's SHA-256, so the provider worker can refuse an unapproved job.
