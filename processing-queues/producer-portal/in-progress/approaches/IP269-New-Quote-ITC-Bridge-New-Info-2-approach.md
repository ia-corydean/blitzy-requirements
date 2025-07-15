# IP269-New-Quote-ITC-Bridge-New-Info-2 - Implementation Approach

## Requirement Understanding

This is an enhanced version of the bridged data handling that requires mandatory resolution before proceeding. When external data enrichment discovers undisclosed drivers, the system must:

- Display prominent warning-style alerts for discovered drivers
- Show "Missing Info" badges on each bridged driver
- Block quote progression until all drivers are addressed
- Provide bulk "Exclude All" functionality
- Enable individual driver management via side panel
- Collect required fields (gender, marital status, relationship)
- Update premiums dynamically based on inclusion decisions
- Remove alerts once all entities are resolved

This ensures complete and accurate underwriting data by enforcing producer action on discovered information.

## Domain Classification
- Primary Domain: ProducerPortal
- Cross-Domain Impact: No
- Complexity Level: Medium

## Pattern Analysis

### Reusable Patterns Identified

**From Infrastructure Codebase:**
- **Alert Components**: Warning-style UI patterns
- **Badge System**: Status indicators on entities
- **Side Panel**: Existing driver edit panel
- **Validation Blocking**: Form progression control

**From Global Requirements:**
- **[GR-53 - DCS Integration]**: External data discovery
- **[GR-04 - Validation]**: Mandatory field validation
- **[GR-07 - Reusable Components]**: Alert and badge patterns
- **[GR-11 - Accessibility]**: WCAG compliant warnings

**From Approved ProducerPortal Requirements:**
- **[IP269-New-Quote-ITC-Bridge-New-Info-1]**: Basic bridged data patterns
- **[IP269-New-Quote-Step-2-Drivers]**: Driver management
- Quote review and navigation patterns

### Domain-Specific Needs
- **Mandatory Resolution**: Block progression until addressed
- **Bulk Actions**: Exclude all discovered drivers at once
- **Visual Prominence**: Warning-style alerts for urgency
- **Missing Info Tracking**: Badge-based status indicators
- **Dynamic Premium Updates**: Real-time recalculation

## Proposed Implementation

### Simplification Approach
- **Current Complexity**: Blocking validation, bulk actions, dynamic badges, real-time updates
- **Simplified Solution**: 
  - Reuse alert card patterns with warning styling
  - Simple blocking validation on Continue button
  - Leverage existing side panel for edits
  - Badge system using existing status patterns
  - Bulk action as simple API call
- **Trade-offs**: 
  - Gain: Clear user guidance, enforced compliance, consistent UI
  - Lose: Inline quick actions (use side panel for all edits)

### Technical Approach

#### Phase 1: Enhanced Alert System
- [ ] Create `BridgedDataWarningCard` with:
  - Yellow/orange warning styling
  - Clear explanation text
  - "Exclude All" action button
  - Dismissible only when resolved
- [ ] Add to driver section of quote review
- [ ] Implement alert visibility logic

#### Phase 2: Badge Status System
- [ ] Create `DriverStatusBadge` component showing:
  - "Missing Info" for incomplete bridged drivers
  - "Included" for reviewed and included
  - "Excluded" for reviewed and excluded
- [ ] Add badge logic to driver list items
- [ ] Update badges dynamically on changes

#### Phase 3: Blocking Validation
- [ ] Implement `hasPendingBridgedDrivers` validation
- [ ] Disable Continue button when true
- [ ] Show tooltip explaining block reason
- [ ] Add visual indicators on blocked button
- [ ] Clear block when all resolved

#### Phase 4: Driver Resolution Flow
- [ ] Enhance side panel for bridged drivers:
  - Pre-populate known data
  - Highlight required fields
  - Show inclusion/exclusion toggle
- [ ] Implement bulk exclude functionality
- [ ] Add progress tracking
- [ ] Update alerts/badges on save

#### Phase 5: Premium Recalculation
- [ ] Trigger recalculation on driver status change
- [ ] Show loading state during calculation
- [ ] Display before/after premium
- [ ] Update summary section
- [ ] Add calculation audit trail

## Risk Assessment

- **Risk 1**: User frustration with blocking → Mitigation: Clear messaging, bulk actions
- **Risk 2**: Complex validation states → Mitigation: Simple binary resolved/unresolved
- **Risk 3**: Performance with many drivers → Mitigation: Efficient badge updates
- **Risk 4**: Accidental exclusions → Mitigation: Confirmation dialogs, undo capability

## Context Preservation

- **Key Decisions**: 
  - Mandatory resolution before progression
  - Warning-style visual treatment
  - Bulk exclude for convenience
  - Reuse existing side panel
  - Simple badge-based status tracking
  
- **Dependencies**: 
  - Builds on ITC Bridge Option 1
  - Uses existing driver management
  - Requires DCS integration
  - Leverages alert/badge patterns
  
- **Future Impact**: 
  - Pattern for other mandatory validations
  - Foundation for compliance workflows
  - Supports automated underwriting rules
  - Template for data quality enforcement

## Approval Section
**Status**: PENDING APPROVAL
**Reviewer Comments**: [Space for feedback]
**Decision**: [ ] APPROVED [ ] REVISE [ ] REJECT [ ] DEFER