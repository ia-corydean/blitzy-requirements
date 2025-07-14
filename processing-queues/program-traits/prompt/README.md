# Program Traits Prompt Directory

Place your requirement files here for processing.

## File Naming Convention
- `prompt-{feature-name}.md` for new features
- `update-{feature-name}.md` for updates
- `fix-{issue-description}.md` for fixes

## What Happens Next
1. System analyzes your requirement
2. Generates `-approach.md` file in `../in-progress/approaches/`
3. Waits for your approval
4. Implements after approval in `../in-progress/implementations/`
5. Moves to `../completed/` when done

## Example Submission

```markdown
# Add Aguila Dorada Rate Adjustment

We need to add a new rate adjustment factor for the Aguila Dorada program that applies a 5% discount for drivers with 5+ years of continuous insurance.

## Requirements
- Apply only to Aguila Dorada program
- Check continuous insurance history
- Apply 5% discount if qualified
- Log the discount application
```

## Tips for Good Requirements
- Be specific about the business need
- Include acceptance criteria
- Mention any existing patterns to follow
- Specify which program traits are affected