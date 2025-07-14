# SR22 Prompt Directory

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
# Add SR26 Support for Commercial Vehicles

We need to support SR26 filings for commercial vehicles in addition to the existing SR22 support.

## Requirements
- Add SR26 document type
- Support commercial vehicle classifications
- Integrate with state filing systems
- Track filing status and expiration
```

## Tips for Good Requirements
- Specify SR22 or SR26 filing type
- Include state-specific requirements
- Mention any DMV integration needs
- Consider compliance and reporting requirements