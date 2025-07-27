# IP286 - Re-Quoting Feature Requirements

## **A) WHY - Vision and Purpose**

The *Requote* feature enables users to efficiently generate a **new quote** by leveraging data from an **existing policy**. This is designed to:

- **Speed up the quoting process** by reusing validated data (e.g., drivers, vehicles, coverages).
- **Improve accuracy** by automatically flagging outdated or changed information.
- **Enhance flexibility** by allowing edits to key data before generating the new quote.

This tool is particularly valuable for scenarios like policy renewal comparisons, post-cancellation re-engagement, or quote revision based on life changes.

---

## **B) WHAT - Core Requirements**

### 1. **Requote Entry Points**

- **From policy detail pages**
- Triggered by a **"Requote" button**, which launches a dialog

### 2. **Requote Kickoff Dialog**

- Dialog presents:
    - Effective Date
        - This date will default to today, but can be manually modified by the user
    - Call to action: **Start Requote**
- Includes option to start or cancel

### 3. **Requote Workflow**

This section will be a variant of `IP269 - Quotes: New Quote - Step 6: Review Quote`. This section will describe the delta between the initial implementation as referenced in the `IP269 - Quotes: New Quote - Step 6: Review Quote` document, and what must be modified for the Re-Quoting experience. 

- User will arrive at the Review Quote screen, which includes:
    - Notification for **newly flagged items**
        - If a new address has been returned for the primary insured, a modal will present showing the original address and new address, and the user must select one address to proceed with requoting
            - The address information will be highlighted in yellow, to visually indicate the change
            - The user can revert to the original address using the CTA if required
        - If additional drivers have been identified in the household, the user must choose to exclude all drivers, or select the individual driver to open the side panel, where they can set to include or exclude the driver, along with the additional information required (as implemented in `IP269 - Quotes: Bridged In - New Info Found Option 2`)
    - Sections for:
        - Primary Insured
        - Drivers
        - Vehicles
        - Coverages
        - Discounts
        - Premium Summary

### 4. **Editable Sections**

Each section is editable, allowing the user to return to the appropriate section of the workflow to modify. 

- **Drivers** – Add, edit, or remove
- **Vehicles** – VIN, use type, coverage per vehicle
- **Coverages** – Bodily injury, property damage, PIP, comp/collision
- **Discounts**
- **Premium Summary**

### 5. **Validation & Flagging**

- Flag items that are:
    - Recently changed
- Use visual indicators (e.g., yellow highlight)

### 6. **Final Actions**

- Start Binding, and proceed to bind
    - The user will proceed through the workflows as implemented in:
        - `IP269 - Quotes: Bind - Step 1: Vehicle Photo Upload`
        - `IP269 - Quotes: Bind - Step 2: Document Upload`
        - `IP269 - Quotes: Bind - Step 3: Sign Documents`
        - `IP269 - Quotes: Bind - Step 3 & 4: Sign Documents In Person & Make Payment`
        - `IP269 - Quotes: Bind - Step 3 & 4: Sign Remotely & Make Payment`
- Option to return to previous step or cancel

---

## **C) HOW - Planning & Implementation**

---

## **D) User Experience (UX) & Flows**

### 1. **Flow: Starting a Requote**

1. User selects **Requote** from a policy
2. Dialog appears → user must confirm effective date for new policy
3. Clicks **Start Requote**

### 2. **Flow: Reviewing and Editing**

1. Pre-filled data appears in requote view
2. Warnings display for new information or changes from previously provided information
3. User edits drivers, coverage, etc.
4. Premium recalculates live
5. User can proceed to the binding step

### 3. **Flow: Exit or Cancel**

- At any point, users can:
    - Save draft
    - Cancel and return to policy details

---

## E) Master Table Schemas