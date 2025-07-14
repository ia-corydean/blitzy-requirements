# Reinstatement Prompt Directory

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
# Update Reinstatement Grace Period

We need to extend the reinstatement grace period from 30 days to 45 days for policies cancelled due to non-payment.

## Requirements
- Update grace period to 45 days
- Apply only to non-payment cancellations
- Maintain existing lapse fee structure
- Update all relevant notifications
```

## Tips for Good Requirements
- Specify the type of reinstatement (non-payment, underwriting, etc.)
- Include any regulatory requirements
- Mention notification changes needed
- Consider impact on payment schedules