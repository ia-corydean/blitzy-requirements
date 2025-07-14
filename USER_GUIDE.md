# Requirements Generation User Guide

## Overview

This guide provides practical instructions for using the multi-agent requirements generation system. Whether you're creating new requirements, reviewing existing ones, or working across multiple domains, this guide will help you navigate the system effectively.

## Table of Contents

- [Getting Started](#getting-started)
- [Submitting Requirements](#submitting-requirements)
- [Understanding the Queue System](#understanding-the-queue-system)
- [Working with Different Domains](#working-with-different-domains)
- [Quality Checklist and Validation](#quality-checklist-and-validation)
- [Monitoring Progress](#monitoring-progress)
- [Troubleshooting Common Issues](#troubleshooting-common-issues)
- [Best Practices](#best-practices)

## Getting Started

### Prerequisites

Before using the system, ensure you have:
- Access to the `/app/workspace/requirements/` directory
- Understanding of your business domain (ProducerPortal, Accounting, etc.)
- Familiarity with Global Requirements standards
- Basic knowledge of requirement structure and format

### System Access

The requirements generation system is organized around these key locations:
- **Queue System**: `/app/workspace/requirements/processing-queues/`
- **Global Standards**: `/app/workspace/requirements/GlobalRequirements/`
- **Domain Patterns**: `/app/workspace/requirements/{Domain}/`
- **Shared Knowledge**: `/app/workspace/requirements/shared-infrastructure/`

### Initial Setup Checklist

- [ ] **Review Domain Standards**: Check `/app/workspace/requirements/{YourDomain}/CLAUDE.md`
- [ ] **Understand Global Requirements**: Browse `/app/workspace/requirements/GlobalRequirements/`
- [ ] **Check Approved Patterns**: Review `/app/workspace/requirements/{YourDomain}/approved-requirements/`
- [ ] **Access Queue System**: Verify access to `/app/workspace/requirements/processing-queues/{YourDomain}/`

## Submitting Requirements

### Single Domain Requirements

**Step 1: Prepare Your Requirement**
```bash
# Create requirement file in appropriate domain queue
touch /app/workspace/requirements/processing-queues/{domain}/pending/{requirement-name}.md
```

**Step 2: Use the Template Structure**
```markdown
# Requirement Title

## Pre-Analysis Checklist
- [ ] Reviewed applicable Global Requirements
- [ ] Checked domain-specific approved requirements
- [ ] Verified entity catalog for reuse opportunities
- [ ] Confirmed infrastructure compatibility

## Requirement Description
[Clear description of what needs to be implemented]

## Entity Analysis
[Identify entities involved and check for reuse]

## Implementation Requirements
[Detailed implementation specifications]

## Quality Validation
[Compliance and testing requirements]
```

**Step 3: Submit for Processing**
- Save the file in `pending/` directory
- System automatically detects and begins processing
- Monitor progress through queue status updates

### Multi-Domain Requirements

**Step 1: Identify Affected Domains**
- List all business domains that will be impacted
- Identify shared entities and workflows
- Determine cross-domain dependencies

**Step 2: Submit to Multi-Domain Queue**
```bash
# Place in multi-domain queue for coordinated processing
touch /app/workspace/requirements/processing-queues/multi-domain/pending/{requirement-name}.md
```

**Step 3: Include Cross-Domain Analysis**
```markdown
# Multi-Domain Requirement Title

## Affected Domains
- ProducerPortal: [specific impact]
- Accounting: [specific impact]
- [Other domains as applicable]

## Shared Entities
- [Entity 1]: Used by [domains]
- [Entity 2]: Used by [domains]

## Cross-Domain Dependencies
- [Dependency 1]: [description]
- [Dependency 2]: [description]

## Integration Requirements
[How domains will work together]
```

### System-Wide Requirements

For requirements affecting 4+ domains or fundamental system changes:

**Step 1: Comprehensive Impact Analysis**
- Document all affected domains
- Identify infrastructure implications
- List Global Requirements that may need updates

**Step 2: Submit with Full Context**
- Use multi-domain queue with system-wide flag
- Include comprehensive dependency mapping
- Provide detailed integration specifications

## Understanding the Queue System

### Queue Structure

Each domain has a standardized queue structure:

```
processing-queues/{domain}/
├── pending/                    # Requirements awaiting processing
├── in-progress/               # Currently being processed
│   ├── individual/           # Single requirement processing
│   └── batch-{id}/           # Grouped requirements
├── completed/                # Finished requirements
├── intelligence/             # Pre-processing analysis results
└── cross-domain-batches/     # Multi-domain requirement sets
```

### Queue Status Indicators

**Pending Queue**
- Requirements waiting for agent availability
- Automatic prioritization based on dependencies
- Cross-domain coordination scheduling

**In-Progress Queue**
- Active processing by Domain Specialists
- Real-time collaboration between agents
- Progressive validation stages

**Completed Queue**
- Finished requirements with full documentation
- Pattern library updates applied
- Performance metrics collected

### Processing Priority

**High Priority:**
- System-wide infrastructure changes
- Multi-domain requirements with dependencies
- Global Requirements updates

**Medium Priority:**
- Single domain requirements with new patterns
- Cross-domain requirements without critical dependencies
- Enhancement to existing workflows

**Low Priority:**
- Minor modifications to existing requirements
- Documentation updates
- Pattern library maintenance

## Working with Different Domains

### ProducerPortal Domain

**Typical Requirements:**
- Quote management workflows
- Producer portal features
- Entity relationship management
- DCS integration enhancements

**Key Considerations:**
- Check existing quote patterns in approved requirements
- Verify DCS integration requirements (GR-53)
- Ensure Universal Entity Management compliance (GR-52)
- Consider communication workflow integration (GR-44)

**Domain-Specific Queue:**
```bash
/app/workspace/requirements/processing-queues/producer-portal/
```

### Accounting Domain

**Typical Requirements:**
- Billing cycle enhancements
- Payment processing workflows
- Commission calculation updates
- ACH integration modifications

**Key Considerations:**
- Review payment entity patterns for reuse
- Check integration with ProducerPortal for quote-to-billing workflows
- Ensure financial compliance requirements
- Validate against existing commission structures

**Domain-Specific Queue:**
```bash
/app/workspace/requirements/processing-queues/accounting/
```

### ProgramManager Domain

**Typical Requirements:**
- Rate factor updates
- Underwriting rule modifications
- Program configuration changes
- Rate calculation enhancements

**Key Considerations:**
- Check integration with ProgramTraits for program-specific rules
- Ensure rate calculation consistency across programs
- Validate against existing underwriting patterns
- Consider impact on quote generation workflows

**Domain-Specific Queue:**
```bash
/app/workspace/requirements/processing-queues/program-manager/
```

### ProgramTraits Domain

**Typical Requirements:**
- Aguila Dorada program rules
- Program-specific customizations
- Specialized workflow modifications
- Program compliance updates

**Key Considerations:**
- Coordinate with ProgramManager for base rate factors
- Ensure program-specific rule consistency
- Validate against Aguila Dorada guidelines
- Consider cross-program impact

**Domain-Specific Queue:**
```bash
/app/workspace/requirements/processing-queues/program-traits/
```

### EntityIntegration Domain

**Typical Requirements:**
- External API integration updates
- DCS integration enhancements
- Third-party service connections
- Data verification workflows

**Key Considerations:**
- Review existing API integration patterns
- Ensure DCS architecture compliance (GR-53)
- Validate external service security requirements
- Consider impact on other domains using external data

**Domain-Specific Queue:**
```bash
/app/workspace/requirements/processing-queues/entity-integration/
```

### Reinstatement Domain

**Typical Requirements:**
- Policy reinstatement workflow updates
- Lapse processing enhancements
- Policy lifecycle modifications
- Reinstatement compliance updates

**Key Considerations:**
- Follow Policy Reinstatement Process guidelines (GR-64)
- Coordinate with Accounting for payment processing
- Ensure policy lifecycle consistency
- Validate against existing reinstatement patterns

**Domain-Specific Queue:**
```bash
/app/workspace/requirements/processing-queues/reinstatement/
```

### Sr22 Domain

**Typical Requirements:**
- SR22/SR26 filing enhancements
- Financial responsibility updates
- Compliance tracking modifications
- State filing system integration

**Key Considerations:**
- Follow SR22/SR26 Filing guidelines (GR-10)
- Coordinate with driver data from ProducerPortal
- Ensure compliance tracking accuracy
- Validate against state filing requirements

**Domain-Specific Queue:**
```bash
/app/workspace/requirements/processing-queues/sr22/
```

## Quality Checklist and Validation

### Pre-Submission Checklist

**Global Requirements Review:**
- [ ] **GR-52 (Universal Entity Management)**: Check if entities can be reused
- [ ] **GR-44 (Communication Architecture)**: Verify communication patterns
- [ ] **GR-41 (Database Standards)**: Ensure naming convention compliance
- [ ] **GR-38 (Microservice Architecture)**: Validate service boundaries
- [ ] **GR-53 (DCS Integration)**: Check external API patterns if applicable
- [ ] **GR-64 (Policy Reinstatement)**: Verify reinstatement process if applicable
- [ ] **GR-10 (SR22/SR26 Filing)**: Check financial responsibility requirements if applicable

**Domain-Specific Review:**
- [ ] **Check Approved Requirements**: Review domain's approved patterns
- [ ] **Entity Catalog Verification**: Ensure entity reuse where possible
- [ ] **Infrastructure Compatibility**: Validate against existing codebase
- [ ] **Cross-Domain Impact**: Identify shared entities and workflows

**Documentation Standards:**
- [ ] **Clear Requirement Description**: Unambiguous statement of needs
- [ ] **Complete Entity Analysis**: All entities identified and analyzed
- [ ] **Implementation Specifications**: Detailed technical requirements
- [ ] **Quality Validation Criteria**: Clear acceptance criteria

### Automatic Validation Process

The system performs progressive validation in these stages:

**Stage 1: Structure Validation (3 minutes)**
- Template compliance checking
- Required section verification
- Format standardization

**Stage 2: Domain Patterns (7 minutes)**
- Domain-specific business rule validation
- Entity pattern compliance
- Workflow consistency verification

**Stage 3: Cross-Domain (10 minutes)**
- Shared entity definition consistency
- Cross-domain relationship integrity
- Integration pattern validation

**Stage 4: Global Requirements (15 minutes)**
- Comprehensive GR compliance checking
- Universal entity management validation
- Communication architecture compliance
- Database standards verification

**Stage 5: Infrastructure (10 minutes)**
- Existing codebase pattern alignment
- Database schema compatibility
- API endpoint consistency
- Service layer integration verification

### Quality Gates

**Minimum Thresholds:**
- Global Requirements compliance: 95%
- Cross-domain consistency: 90%
- Infrastructure alignment: 85%
- Pattern reuse rate: 80%

**Common Validation Failures:**
- Missing Global Requirements references
- Entity duplication instead of reuse
- Inconsistent naming conventions
- Missing cross-domain coordination
- Infrastructure pattern misalignment

## Monitoring Progress

### Queue Status Monitoring

**Check Processing Status:**
```bash
# View current status of your requirements
ls -la /app/workspace/requirements/processing-queues/{domain}/in-progress/
ls -la /app/workspace/requirements/processing-queues/{domain}/completed/
```

**Monitor Cross-Domain Requirements:**
```bash
# Check multi-domain processing status
ls -la /app/workspace/requirements/processing-queues/multi-domain/in-progress/
```

### Progress Indicators

**File Locations Indicate Status:**
- `pending/`: Waiting for processing
- `in-progress/individual/`: Single requirement processing
- `in-progress/batch-{id}/`: Part of coordinated batch processing
- `completed/`: Processing finished
- `intelligence/`: Pre-processing analysis available

**Processing Artifacts:**
- `{requirement}-approach.md`: Processing approach and strategy
- `shared-entities.json`: Shared entity definitions within batch
- `cross-domain-links.json`: Links to related domain requirements
- `processing-metrics.json`: Performance and quality metrics

### Performance Tracking

**Individual Requirement Metrics:**
- Processing time from submission to completion
- Pattern reuse rate achieved
- Global Requirements compliance score
- Cross-domain coordination efficiency

**System-Wide Performance:**
- Average processing time across domains
- Pattern library growth rate
- First-pass approval rates
- Infrastructure alignment scores

## Troubleshooting Common Issues

### Validation Failures

**Global Requirements Non-Compliance**
- **Issue**: Requirement fails GR compliance validation
- **Solution**: Review applicable GRs and update requirement
- **Prevention**: Use pre-submission checklist

**Entity Duplication**
- **Issue**: Creating new entity when existing one should be reused
- **Solution**: Check Universal Entity Catalog and reuse existing patterns
- **Prevention**: Review entity catalog before creating new entities

**Cross-Domain Inconsistency**
- **Issue**: Shared entities defined differently across domains
- **Solution**: Coordinate entity definitions through shared context
- **Prevention**: Use multi-domain queue for cross-domain requirements

### Processing Delays

**Queue Congestion**
- **Issue**: Requirements stuck in pending queue
- **Solution**: Check for dependency conflicts and batch optimization
- **Prevention**: Submit related requirements together

**Agent Coordination Issues**
- **Issue**: Multi-domain processing taking longer than expected
- **Solution**: Check shared context synchronization
- **Prevention**: Ensure clear cross-domain dependency mapping

**Infrastructure Validation Delays**
- **Issue**: Extended validation time against codebase
- **Solution**: Verify requirement alignment with existing patterns
- **Prevention**: Review infrastructure patterns before submission

### Quality Issues

**Low Pattern Reuse**
- **Issue**: Requirement not leveraging existing patterns effectively
- **Solution**: Review pattern library and approved requirements
- **Prevention**: Conduct thorough pattern analysis pre-submission

**Infrastructure Misalignment**
- **Issue**: Requirement conflicts with existing codebase patterns
- **Solution**: Adjust requirement to align with established patterns
- **Prevention**: Validate against infrastructure patterns

## Best Practices

### Requirement Preparation

**Research Existing Patterns:**
- Review approved requirements in your domain
- Check Universal Entity Catalog for reusable entities
- Study Global Requirements for applicable standards
- Examine cross-domain patterns for shared workflows

**Clear Documentation:**
- Write unambiguous requirement descriptions
- Include complete entity analysis
- Specify all integration requirements
- Define clear acceptance criteria

**Cross-Domain Coordination:**
- Identify all affected domains early
- Map shared entities and dependencies
- Coordinate with domain experts
- Plan integration workflows

### Efficient Processing

**Batch Related Requirements:**
- Submit related requirements together
- Use cross-domain batches for coordinated processing
- Group requirements by shared entities
- Coordinate timing for dependent requirements

**Leverage Pattern Reuse:**
- Always check for existing patterns first
- Reuse entities whenever possible
- Follow established naming conventions
- Build on approved requirement patterns

**Quality Focus:**
- Use pre-submission checklists consistently
- Address validation feedback promptly
- Learn from successful requirement patterns
- Contribute to pattern library growth

### Continuous Improvement

**Learn from Metrics:**
- Review processing performance regularly
- Analyze pattern reuse effectiveness
- Study cross-domain coordination efficiency
- Track Global Requirements compliance trends

**Contribute to Knowledge Base:**
- Document new patterns discovered
- Share successful integration approaches
- Update entity catalog with new entities
- Contribute to Global Requirements evolution

**Collaborate Effectively:**
- Coordinate with other domain experts
- Share knowledge across domains
- Participate in pattern library development
- Provide feedback on system improvements

---

**Last Updated**: 2025-01-07  
**User Guide Version**: Phase 1 Implementation  
**Support**: Review documentation or submit questions through appropriate domain queue