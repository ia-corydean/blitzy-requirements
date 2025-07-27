# IP279 - Endorsements Feature Requirements

## **A) WHY – Vision and Purpose**

The purpose of this workflow is to allow authorized users to **modify an in-force insurance policy**. These changes (known as endorsements) may involve:

- Updating driver information
- Adding or removing vehicles
- Modifying coverage options or limits

This functionality supports:

- Real-time policy servicing
- Accurate premium recalculation

The endorsement process must ensure that **all changes are reviewed and priced before being finalized**, with clear transparency into impact on cost and coverage.

---

## **B) WHAT – Core Requirements**

### 1. **Entry Point: Policy Summary**

- This workflow is initiated by clicking the “Submit Endorsement” CTA as defined in `IP270 - Policies`.
- Define the effective date of the endorsement (i.e. when this change will come into effect)
- Display of all current policy data:
    - Active drivers (both included and excluded)
    - Covered vehicles
    - Associated coverages (per-vehicle and policy-wide)
    - Premium Summary

### 2. **Editable Sections**

- Users can:
    - Edit Drivers
        - The user will be routed to the `IP269 - Quotes: New Quote - Step 2: Drivers` experience to modify drivers on the policy.
        - The CTA to take the user to the next step will be modified to return the user to the Policy Summary screen with the modification reflected.
    - Edit Vehicles
        - The user will be routed to the `IP269 - Quotes: New Quote - Step 3: Vehicle Information` experience to modify vehicles on the policy.
        - The CTA to take the user to the next step will be modified to return the user to the Policy Summary screen with the modification reflected.
    - Edit Coverages
        - The user will be routed to the `IP269 - Quotes: New Quote - Step 5: Coverage Selection` experience to modify vehicles on the policy.
        - The CTA to take the user to the next step will be modified to return the user to the Policy Summary screen with the modification reflected.

### 4. **Summary of Changes**

- **Change Indicator:**
    - Drivers, vehicles, or coverages modified through the endorsement will be identified using a blue dot indicator, as well as modifying the colour of the appropriate row in the table where the change was made
    - This allows the user to quickly scan to see where changes have been made
- **Summary of Changes**:
    - High-level note of what has changed (e.g., “1 driver added” or “Coverage updated”)
- **Endorsement Premium Summary**:
    - This section will reflect the:
        - Premium Change, with an arrow indicator to show if the premium has increased, or decreased
        - Down Payment Due Today, meaning the payment the insured will make today to process this endorsement
            - If there is no premium change as a part of the endorsement, this field will be hidden
        - Their remaining monthly payments, with the appropriate due dates and dollar values
        - The updated total premium + policy fees

### 5. **Next Step: Continue to Document Signing**

- “Continue” button becomes active once a valid configuration is reached
- Changes are locked in and user proceeds to bind the endorsement
- The user will then be navigated to the following steps in the workflow:
    - `IP269 - Quotes: Bind - Step 1: Vehicle Photo Upload`
        - This step will only be required if there has been a change to an existing vehicle, or addition of a new vehicle to the policy.
        - The steps to be completed will be updated to reflect the endorsement designs, not the steps as defined in the Quotes experience.
    - `IP269 - Quotes: Bind - Step 2: Document Upload`
        - This step will only be required if the user has to provide additional documentation to support their endorsement.
        - The steps to be completed will be updated to reflect the endorsement designs, not the steps as defined in the Quotes experience.
    - `IP269 - Quotes: Bind - Step 3: Sign Documents`
        - This step will only be required if signatures are required for the endorsements made to the policy.
        - The steps to be completed will be updated to reflect the endorsement designs, not the steps as defined in the Quotes experience.
    - `IP269 - Quotes: Bind - Step 3 & 4: Sign Documents In Person & Make Payment`
        - This step will only be required if signatures are required and/or the user has to make a payment to reflect the endorsement on the policy.
        - The steps to be completed will be updated to reflect the endorsement designs, not the steps as defined in the Quotes experience.
    - `IP269 - Quotes: Bind - Step 3 & 4: Sign Remotely & Make Payment`
        - This step will only be required if signatures are required and/or the user has to make a payment to reflect the endorsement on the policy.
        - The steps to be completed will be updated to reflect the endorsement designs, not the steps as defined in the Quotes experience.

---

## **C) HOW – Planning & Implementation**

---

## **D) User Experience (UX) & Flows**

### 🧭 Flow Overview

1. **View Existing Policy (Policy Summary)**
    - Driver(s), vehicle(s), and coverages shown
    - Edit actions available inline
2. **Make Changes**
    - Edit driver modal: Add/remove/update driver details
    - Edit vehicle modal: VIN, Year/Make/Model, etc.
    - Edit coverage modal: Adjust per-vehicle and policy-level options
3. **Review Updated Summary**
    - System recalculates premium in real-time
    - “Summary of Changes” displays a list of modifications made
4. **Premium Summary**
    - Itemized breakdown of total premium
    - Shows down payment and updated monthly payments
    - Clear green callout showing amount due or saved
5. **Continue to Next Step**
    - Once changes are complete, user clicks “Continue”
    - System locks in changes and proceeds to document generation & payment (next step)

---

### E) Master Schema Tables