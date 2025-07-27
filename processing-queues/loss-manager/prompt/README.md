# Loss Manager Prompt Directory

Place your loss management and claims processing requirement files here for comprehensive claims lifecycle management.

## File Naming Convention
- `prompt-{feature-name}.md` for new features
- `update-{feature-name}.md` for updates  
- `fix-{issue-description}.md` for fixes

## What Happens Next
1. System analyzes your requirement using 5-agent architecture
2. Generates `-approach.md` file in `../in-progress/approaches/`
3. Waits for your approval
4. Implements after approval in `../in-progress/implementations/`
5. Moves to `../completed/` when done

## Loss Manager Domain Scope

### Core Responsibilities
- **Claims Processing**: First notice of loss through claim closure
- **Loss Adjusting**: Investigation, evaluation, and settlement
- **Claims Workflow**: Status tracking, task management, approvals
- **Settlement Processing**: Payment authorization and disbursement
- **Claims Documentation**: Photos, reports, correspondence
- **Regulatory Compliance**: State reporting requirements, CMS Section 111
- **Fraud Detection**: Suspicious claims identification and investigation

### Key Integration Points
- **Policy Manager**: Coverage verification, policy status checks
- **Accounting**: Reserve management, payment processing
- **Entity Integration**: External services (appraisers, attorneys, vendors)
- **Producer Portal**: Claims visibility and producer notifications
- **Program Manager**: Claims rules and coverage determination

### Common Use Cases
- First notice of loss (FNOL) processing
- Claims investigation and documentation
- Coverage analysis and determination
- Settlement negotiations and processing
- Subrogation and recovery workflows
- Claims reporting and analytics
- Regulatory compliance reporting

## Example Submission

```markdown
# Implement Claims Investigation Workflow

We need to create a comprehensive claims investigation system that manages the complete investigation lifecycle from assignment to completion.

## Requirements
- Automatic assignment of claims to adjusters based on coverage type and complexity
- Investigation task management with deadlines and priorities
- Document collection and storage (photos, statements, reports)
- Coverage analysis and determination workflow
- Settlement recommendation and approval process
- Integration with external vendors and service providers

## Affected Systems
- Claims management database
- Document management system
- Task and workflow engine
- External vendor integrations
- Settlement processing system

## Success Criteria
- 95% of claims assigned within 24 hours
- Complete investigation documentation
- Accurate coverage determinations
- Timely settlement processing
- Comprehensive audit trails
```

## Tips for Good Requirements
- Specify the claims lifecycle stage affected
- Include regulatory compliance considerations
- Describe integration with external vendors
- Consider timing and SLA requirements
- Mention data security and privacy needs
- Include performance and scalability requirements
- Consider fraud detection and prevention

## Related Global Requirements
- **GR-52**: Universal Entity Management (for vendors/attorneys)
- **GR-44**: Communication Architecture (for notifications)
- **GR-41**: Database Standards
- **GR-48**: External Integrations Catalog
- **GR-37**: Locking & Action Tracking
- **GR-12**: Security Considerations (PII/PHI protection)

## Special Considerations

### Regulatory Compliance
- CMS Section 111 Medicare reporting requirements
- State insurance department reporting
- Fraud reporting obligations
- Data retention requirements

### External Integrations
- Appraisal services and vendors
- Attorney networks and counsel
- Medical providers and IME services
- Auto body shops and repair facilities
- Salvage and towing services

### Data Security
- PII/PHI protection for claimants
- Secure document storage and transmission
- Access controls and audit logging
- Encryption for sensitive data