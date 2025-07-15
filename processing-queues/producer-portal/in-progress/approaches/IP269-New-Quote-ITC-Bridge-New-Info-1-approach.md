# IP269-New-Quote-ITC-Bridge-New-Info-1 - Implementation Approach

## Requirement Understanding

This feature handles the scenario where external data enrichment (ITC Bridge/DCS integration) discovers additional drivers not initially declared in the quote. The system must:

- Display alerts for newly discovered drivers in the quote review
- Automatically set discovered drivers as excluded
- Allow producers to modify driver status (excluded → included)
- Collect additional required information for included drivers
- Update premium calculations based on driver changes
- Provide seamless navigation back to driver editing
- Maintain all changes when returning to review

This ensures compliance by capturing all household members while giving producers control over inclusion decisions.

## Domain Classification
- Primary Domain: ProducerPortal
- Cross-Domain Impact: No
- Complexity Level: Medium

## Pattern Analysis

### Reusable Patterns Identified

**From Infrastructure Codebase:**
- **DCS Integration (GR-53)**: Household driver discovery patterns
- **Driver Management**: Existing driver models and relationships
- **Premium Calculation**: Dynamic premium update patterns
- **Alert/Banner Components**: UI notification patterns

**From Global Requirements:**
- **[GR-53 - DCS Integration]**: External data enrichment architecture
- **[GR-52 - Universal Entity Management]**: External entity handling
- **[GR-07 - Reusable Components]**: Alert and banner patterns
- **[GR-18 - Workflow Requirements]**: Navigation and state management

**From Approved ProducerPortal Requirements:**
- **[IP269-New-Quote-Step-2-Drivers]**: Driver management patterns
- **[IP269-New-Quote-Step-6-Quote-Review]**: Review screen structure
- Navigation patterns from previous steps

### Domain-Specific Needs
- **Bridge Alert Display**: Visual indication of discovered data
- **Driver Status Toggle**: Excluded/Included management
- **Conditional Data Collection**: Additional fields for included drivers
- **Premium Recalculation**: Real-time updates on status change
- **State Preservation**: Maintain changes across navigation

## Proposed Implementation

### Simplification Approach
- **Current Complexity**: External data integration, dynamic UI updates, conditional fields, premium recalculation
- **Simplified Solution**: 
  - Use existing DCS integration patterns
  - Simple alert banners in driver section
  - Leverage existing driver edit side panel
  - Reuse premium calculation service
  - Session-based state management
- **Trade-offs**: 
  - Gain: Consistent patterns, maintainable code, proven UI components
  - Lose: Complex inline editing (use existing side panel instead)

### Technical Approach

#### Phase 1: DCS Integration Enhancement
- [ ] Extend DCS Household Drivers integration for discovery
- [ ] Create `BridgedDriverService` to handle discovered drivers
- [ ] Add `is_bridged` flag to driver data
- [ ] Implement discovery result storage
- [ ] Create audit trail for bridged data

#### Phase 2: Backend Services
- [ ] Create API endpoint for bridged driver retrieval
- [ ] Implement driver status update logic
- [ ] Add validation for included driver requirements
- [ ] Create premium recalculation trigger
- [ ] Handle state preservation during edits

#### Phase 3: Frontend Alert System
- [ ] Create `BridgedDataAlert` component showing:
  - Number of discovered drivers
  - Default excluded status
  - Edit action link
- [ ] Add alert integration to Quote Review
- [ ] Implement visual highlighting for bridged sections
- [ ] Create dismissible information banners

#### Phase 4: Driver Management Flow
- [ ] Modify driver edit panel to handle bridged drivers
- [ ] Add status toggle (excluded/included)
- [ ] Show conditional fields for included drivers
- [ ] Implement validation for required fields
- [ ] Create return navigation to review

#### Phase 5: Premium Updates
- [ ] Integrate premium recalculation on status change
- [ ] Display premium impact clearly
- [ ] Update review summary automatically
- [ ] Show before/after premium comparison
- [ ] Add loading states during calculation

## Risk Assessment

- **Risk 1**: DCS API failures → Mitigation: Graceful degradation, cached results
- **Risk 2**: Data conflicts → Mitigation: Clear source indicators, manual override
- **Risk 3**: Premium accuracy → Mitigation: Server-side validation, audit logging
- **Risk 4**: User confusion → Mitigation: Clear messaging, help tooltips

## Context Preservation

- **Key Decisions**: 
  - Default discovered drivers to excluded
  - Use existing edit panels vs inline editing
  - Leverage DCS integration patterns
  - Simple alert/banner approach
  - Server-side premium calculation
  
- **Dependencies**: 
  - Requires DCS integration (GR-53)
  - Uses existing driver management
  - Builds on quote review structure
  - Integrates with premium service
  
- **Future Impact**: 
  - Foundation for other bridged data (vehicles)
  - Supports automated underwriting
  - Enables household discovery features
  - Template for external data integration

## Approval Section
**Status**: PENDING APPROVAL
**Reviewer Comments**: [Space for feedback]
**Decision**: [ ] APPROVED [ ] REVISE [ ] REJECT [ ] DEFER