# Multi-Domain Prompt Directory

Place your requirement files here that affect multiple business domains.

## File Naming Convention
- `prompt-{feature-name}.md` for new features
- `update-{feature-name}.md` for updates  
- `fix-{issue-description}.md` for fixes

## What Happens Next
1. System analyzes your requirement across all affected domains
2. Generates `-approach.md` file in `../in-progress/approaches/`
3. Coordinates impact across domains
4. Waits for your approval
5. Implements after approval in `../in-progress/implementations/`
6. Moves to `../completed/` when done

## Example Submission

```markdown
# Implement Quote-to-Policy Conversion Workflow

We need to create a seamless workflow that converts approved quotes to active policies, affecting ProducerPortal, Accounting, and PolicyManagement domains.

## Requirements
- Convert quote data to policy structure
- Initialize billing and payment schedules
- Generate policy documents
- Send confirmation notifications
- Update producer commission tracking

## Affected Domains
- ProducerPortal: Quote completion and conversion
- Accounting: Payment initialization and billing setup
- PolicyManagement: Policy creation and document generation
```

## Tips for Good Requirements
- List all affected domains explicitly
- Describe interactions between domains
- Include data flow between systems
- Consider timing and synchronization needs
- Mention any shared entities or services