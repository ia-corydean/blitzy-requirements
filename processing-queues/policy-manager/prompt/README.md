# Policy Manager Prompt Directory

Place your policy management requirement files here for comprehensive policy lifecycle management.

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

## Policy Manager Domain Scope

### Core Responsibilities
- **Policy Lifecycle Management**: Creation, modification, renewal, cancellation
- **Policy Changes & Endorsements**: Mid-term adjustments, coverage changes
- **Policy Renewals**: Automated and manual renewal processing
- **Policy Cancellations**: Voluntary and involuntary cancellation workflows
- **Policy Reinstatements**: Lapse processing and reinstatement workflows
- **Policy Documentation**: Policy documents, ID cards, certificates
- **Policy Compliance**: Regulatory requirements, state-specific rules

### Key Integration Points
- **Producer Portal**: Policy servicing and management interfaces
- **Accounting**: Premium calculations, billing integration
- **Entity Integration**: External verification and validation services
- **Loss Manager**: Claims impact on policy status
- **Program Manager**: Rate and rule application

### Common Use Cases
- Policy issuance and binding workflows
- Mid-term policy changes and endorsements
- Renewal processing and notifications
- Cancellation and reinstatement procedures
- Policy document generation and delivery
- Compliance monitoring and reporting

## Example Submission

```markdown
# Implement Policy Renewal Workflow

We need to create an automated policy renewal system that handles the complete renewal lifecycle from notice generation to policy activation.

## Requirements
- Generate renewal notices 45 days before expiration
- Calculate renewal premiums with updated rates
- Handle customer responses and payment processing
- Automatically renew policies or process non-renewals
- Generate new policy documents for renewed policies
- Track renewal metrics and compliance

## Affected Systems
- Policy management database
- Rating engine integration
- Document generation system
- Billing and payment processing
- Customer notification system

## Success Criteria
- 95% automated renewal processing
- Timely notice generation
- Accurate premium calculations
- Seamless policy transitions
```

## Tips for Good Requirements
- Specify the policy lifecycle stage affected
- Include regulatory compliance considerations
- Describe integration with other systems
- Consider timing and automation requirements
- Mention data retention and audit needs
- Include performance and scalability requirements

## Related Global Requirements
- **GR-64**: Policy Reinstatement Process
- **GR-20**: Business Logic Standards
- **GR-41**: Database Standards
- **GR-52**: Universal Entity Management
- **GR-44**: Communication Architecture