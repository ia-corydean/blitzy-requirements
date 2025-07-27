# IP072 - Loss Inquiry Feature Requirements

# #1 - Search for Policy

## **A) WHY – Vision and Purpose**

The **Search for Policy** step is the **entry point** to capturing a First Notice of Loss (FNOL) or Loss Report. Before documenting a claim, the system must validate that the reported loss is associated with a known policy.

This step ensures:

- Losses are **accurately linked** to valid policies
- FNOLs are filed under the **correct insured party**
- The claims process proceeds with **verified information**
- Unnecessary or fraudulent FNOL entries are prevented

---

## **B) WHAT – Core Requirements**

### **1. Search Inputs**

The user must be able to search using any of the following:

- **Policy Number**
- **Insured Name**
- **License Plate**
- **Driver’s License**
- **Vehicle Identification Number (VIN)**

User must select **one field from the dropdown, which then needs to be populated** to perform a search.

### **2. Policy Lookup**

- System must query backend to find matching active policy records
- Matching policy data should include:
    - Policy Number
    - Policy Status
    - Insured Name
    - Date of Birth
    - Address
    - Driver’s License Number
    - Vehicles on Policy
        - Per Vehicle:
            - Vehicle Info (Make, Model, Year)
            - License Plate
    - Drivers on Policy
        - Per Driver:
            - Name
            - Included vs Excluded Status
            - Date of Birth
            - State of Identification Issuer
            - Identification Type
            - Identification Number
- The matched result format will remain the same regardless of the type of search the FNOL rep used (VIN, Policy Number, etc.)

### **3. Match Requirement**

- A **confirmed match** is required to proceed to the next step in the FNOL workflow
- Exact matches will be returned for Policy Number, License Plate, VIN, and Driver’s License
- If **no match** is found display inline alert

### 4. Partial Matches

- In the case of searching by Insured Name, there may be partial matches or multiple returned results
- These results will be presented in a table format with the Insured Name, Vehicle(s), Address, and Policy Number Listed
    - The user can hover over the relevant column in the search results to see the full set of information for that returned result

### **5. Error Handling**

- Search errors (API failures, invalid inputs, multiple ambiguous results) must be handled gracefully

---

## **C) HOW – Planning & Implementation**

### 

---

## **D) User Experience (UX) & Flows**

### **1. Initial State**

- The FNOL workflow opens with a search screen
- User sees a dropdown and search bar, with Policy Number selected by default

### **2. Search Interaction**

- User selects the value they wish to search by if different than Policy Number, and populates the search bar
- Presses **Search**
- If no input provided, search field shows inline validation

### **3. Match Found**

- A matching policy is displayed
- Display includes:
    - Policy Number
    - Policy Status
    - Insured Name
    - Date of Birth
    - Address
    - Driver’s License Number
    - Vehicles on Policy
        - Per Vehicle:
            - Vehicle Info (Make, Model, Year)
            - License Plate
    - Drivers on Policy
        - Per Driver:
            - Name
            - Included vs Excluded Status
            - Date of Birth
            - State of Identification Issuer
            - Identification Type
            - Identification Number
- **Action**: “Start Report” button appears

### **4. No Match Found**

- The relevant inline error will present based on the search query method selected
- User remains on search screen

### **5. Multiple Matches**

- If multiple matches are returned, the user must select the relevant policy from the list before proceeding

## E) Master Schema Tables

# #2 - FNOL Dashboard

## **A) WHY – Vision and Purpose**

The **Loss Inquiry Dashboard** is designed to serve as the primary interface for intake agents or support staff to capture full incident details once a policy has been selected. The goal is to simplify the process of creating a First Notice of Loss (FNOL) by organizing all relevant information into clearly defined, editable sections. The flexibility to complete the form in any order enhances operational efficiency and ensures critical details are not overlooked, regardless of the caller’s sequence of information.

---

## **B) WHAT – Core Requirements**

### **Functional Requirements**

1. **Policy Confirmation**
    - Display selected policy number and basic policy info (name, status).
2. **Reporter Info**
    - Identify who is reporting: the policyholder or someone else.
    - Provide options and guidance depending on selection.
3. **Loss Info**
    - Capture incident date, time, location (city/state), and loss type.
    - Allow users to enter a brief narrative of what happened.
    - Flag whether the police were contacted, and capture report details if so.
4. **Named Insured**
    - Auto-populate from policy if available; editable fields for:
        - Driver Info
        - Injury & Attorney Representation
        - Vehicle Info
        - Passenger Info
5. **Claimants**
    - Add one or multiple claimants with:
        - Contact information
        - Injury and attorney info
        - Property damage flag
        - Vehicle details
6. **Witnesses**
    - Add one or more witnesses with:
        - Contact information
        - Statement text field
        - Language spoken
7. **Notes**
    - Add additional notes, if needed
8. **Navigation**
    - Users should be able to jump between sections via a left-side navigation menu by selecting a heading in the menu
    - Left-side navigation menu will be sticky on scroll and be persistently available, regardless of where on the dashboard the user is
    - The navigation will update to reflect additional claimants and witnesses
        - Default State: Claimant, Witness
        - If additional claimants or witnesses are added, it will update to reflect Claimant 001, Claimant 002, Witness 001, Witness 002, etc.
    - Submit option persistently available.
9. **Validation & Record Saving**
    - The report will be saved field by field, auto-saving the record
    - If the session is terminated unexpectedly without a user manually selecting “Submit Loss Report”, the report will be submitted automatically and added to the claims queue
10. **Audit Trail**
    - Timestamp for when the loss was created, inclusive of date, time, and timezone

---

## **C) HOW – Planning & Implementation**

### 

---

## **D) User Experience (UX) & Flows**

### **Flow Overview**

1. **Entry Point**:
    - User lands here after selecting a policy in Step 1.
2. **Section Flexibility**:
    - Users may complete any section in any order.
3. **Inline Expansion**:
    - Sections like “Add Witness” or “Add Claimant” expand inline rather than redirecting.
4. **Dynamic Additions**:
    - “+ Add Claimant”, “+ Add Witness”, and “+ Add Vehicle” buttons append dynamic fields.
    - Auto-numbered entries (e.g., “Claimant 001”, “Witness 002”).
5. **Responsive Design**:
    - Optimized for desktop view with scrollable layout and anchored section nav.
6. **Error Feedback**:
    - Real-time validation with contextual tooltips or red borders.
    - Final validation on submission attempt with scroll-to-error behavior.
7. **Save Draft/Submit**:.
    - “Submit” triggers final validation and submission to the claims queue.

## E) Master Schema Tables

# #3 - Reporter Info

## **A) WHY – Vision and Purpose**

The **Reporter Info** section ensures that the person initiating the FNOL process is clearly identified and their relationship to the policy is understood. Since the accuracy of the loss report depends on the reporter’s perspective and involvement, this step is critical for compliance, claim validation, and follow-up communication. Differentiating between policy-linked reporters and third-party reporters also tailors the data captured and prevents misinformation.

---

## **B) WHAT – Core Requirements**

### **Reporter Types**

1. **Someone on the Policy**
    - The reporter is the policyholder or a listed driver (included or excluded) to the policy.
    - Selectable from pre-populated options tied to the policy.
    - Fields are auto-filled
    - User can modify email address and phone number
2. **Someone Else**
    - A third party (Claimant, Attorney/Law Firm, Adverse Carrier, Friend/Family (Named Insured), Friend/Family (Claimant), Witness, or Lienholder)
    - Requires full manual entry of contact and relationship info.

### **Data Fields to Capture**

### **Shared Fields**

- Reporter Type:
    - Someone on the policy
    - Someone else

### **If “Someone on the Policy”:**

- Auto-suggested list of names from:
    - Named insured
    - Listed drivers
- Upon selection, autofill:
    - Name
    - Address
    - License Number
    - Phone Number
    - Email
    - Allow user to update/override email/phone number

### **If “Someone Else”:**

- Claimant
    - First Name
    - Last Name
    - Email
    - Phone Number
    - Relationship to Insured
- Attorney/Law Firm
    - First Name
    - Last Name
    - Email
    - Phone Number
    - Law Firm
    - Who are they representing?
        - If Insured, no additional information is required at this step, and the Named Insured’s Attorney Representation section will be pre-filled with the reporter’s information
        - If Claimant, user will be prompted to populate First and Last Name of Claimant, and the Claimant 001’s Attorney Representation section will be pre-filled with the reporter’s information
        - If the attorney is representing multiple claimants, the user will have the ability to select ‘Add Claimant’ to add another Claimant Name
        - Each additional claimant added at this step will be added as claimants in the claimant section, with their first and last name’s populated, and the Attorney Representation section pre-filled with the reporter’s information
- Adverse Carrier
    - First Name
    - Last Name
    - Insurance Company
    - Claim Number
    - Email
    - Phone Number
- Friend/Family (Named Insured)
    - First Name
    - Last Name
    - Email
    - Phone Number
    - Relationship to Insured
- Friend/Family (Claimant)
    - First Name
    - Last Name
    - Email
    - Phone Number
    - Relationship to Insured
- Witness
    - First Name
    - Last Name
    - Email
    - Phone Number
- Lienholder
    - First Name
    - Last Name
    - Email
    - Phone Number
    - Company Name

### **Validation Rules**

- First Name, Last Name, Phone Number are required

---

## **C) HOW – Planning & Implementation**

### 

---

## **D) User Experience (UX) & Flows**

### **General Flow**

1. **User enters the Reporter Info section** after policy selection.
2. Choose reporter type
    - “Someone on the policy” → show list of known people, select individual listed on policy, and verify email and phone number
    - “Someone else” → prompt user to select type of reporter and fill in relevant data for that reporter type

## E) Master Schema Tables

# #4 - Loss Information

## **A) WHY – Vision and Purpose**

The **Loss Info** section is a critical part of the FNOL workflow, as it captures factual and contextual information about what happened during the incident. This data not only sets the tone for the claim but also determines potential coverage, fault, and next steps in investigation and resolution. The structure must balance flexibility and completeness, while allowing for variability in how much is known at the time of reporting.

---

## **B) WHAT – Core Requirements**

### **Data Fields and Logic**

1. **Loss Date**
    - Required
    - Date picker
    - Cannot be in the future
2. **Loss Time**
    - Required
    - Time input field
    - Uses 12-hour format with AM/PM
3. **Time Zone**
    - Required
    - Dropdown list of U.S. time zones:
        - Eastern, Central, Mountain, Pacific, Atlantic, Hawaii, Alaska
4. **Loss Location**
    - Required
    - Free-text
5. **Loss Type**
    - Required
    - Dropdown with predefined options:
        - Fatality, Parking Lot, Intersection, Animal Hit, Single Vehicle, Chain Reaction, Rear End Loss, Windshield Loss, Vandalism, Theft, Fire
6. **Description**
    - Required
    - Free-text field
7. **Were authorities contacted?**
    - Required
    - Yes / No radio buttons
    - If **Yes**, reveal the following additional fields:
        - **Police Report Number** (text field)
        - **Responding City** (text field)
        - **State** (dropdown of U.S. states)
        - **Citations Issued** (multi-line text field)

### **Validation Rules**

- All required fields must be completed before the section is marked complete.
- Conditional logic must enforce that **Police Report**, **City**, **State**, and **Citations** fields are only required and visible when “Yes” is selected for authority involvement.
- Loss date must not be after today’s date.

---

## **C) HOW – Planning & Implementation**

### 

---

## **D) User Experience (UX) & Flows**

### **Interaction Flow**

1. **User enters Loss Info section** from the left-hand navigation.
2. Completes:
    - Loss Date (via date picker)
    - Loss Time (via time input)
    - Time Zone (dropdown)
3. Inputs Loss Location and selects Loss Type from dropdown
4. Describes the incident in the Description box
5. Chooses whether authorities were contacted:
    - If **No** is selected, section ends
    - If **Yes**, additional fields appear
6. User fills in police details
7. Section is validated and marked as complete in sidebar

### **UX Guidelines**

- **Progress Visibility**: Navigation sidebar shows status icon (✓) when section is complete

## E) Master Schema Tables

# #5 - Named Insured Information

## **A) WHY – Vision and Purpose**

The **Named Insured** section is designed to confirm and collect key information about the policyholder (the named insured) in the context of the reported incident. This section determines:

- Whether the policyholder was the driver or present at the scene,
- Whether they were injured,
- If they are represented by an attorney,
- Which vehicle they were in, and
- Who else (passengers) was in the vehicle.

This data is foundational for evaluating liability, verifying coverages, and ensuring accurate claims processing.

---

## **B) WHAT – Core Requirements**

### **1. Driver Info**

- **Who was driving?**
    - Dropdown selection of:
        - Named Insured
        - Listed Drivers on Policy (both included and excluded drivers)
        - Someone Not on Policy
            - If the driver was someone not on the policy, the user must populate:
                - First Name
                - Last Name
                - Phone Number
                - Alternate Phone Number (optional)
                - Email
                - Date of Birth
                - Driver’s License Number
                - Languages Spoken (English, Spanish, Other)
                - Street Address, City, State, ZIP Code
        - Unknown

### **2. Injury Information**

- Add Injury Info
    - Expandable section if selected
    - Were you injured in the accident? Yes/No
        - If yes, additional fields are presented
            - Injury Description (text field)
            - Were you transported by ambulance for medical care? Yes/No
            - Are you currently being treated? Yes/No
                - If yes, show treatment location and treatment date
        - If no, the additional injury related fields will remain hidden

### **3. Attorney Representation**

- Add Attorney Info
    - Expandable section if selected
        - First Name
        - Last Name
        - Email
        - Phone Number
        - Law Firm
    - This will default to expanded and pre-populated if the reporter was an attorney and confirmed they represented the insured in the Reporter Info step

### **4. Vehicle Info**

- Ability to **Add Vehicle** via flyout panel
- Vehicle Info
    - Is the vehicle listed on the policy?
        - If yes, select a vehicle from the dropdown, which includes year, make, model and VIN per vehicle
        - If no, manually populate year, make, model, color, VIN, license plate number, and license plate state
    - Is there a lienholder for this vehicle?
        - If yes, populate Lienholder Name, Address, Loan Number and Phone Number
- Damage Info
    - Is the vehicle damaged? Yes/No/Unknown
    - Is the vehicle driveable? Yes/No/Unknown
    - Was the vehicle towed? Yes/No/Unknown
    - Current Location of Vehicle (text field)
    - Damage Location (multi-select checkboxes)
    - Damage Description
        - Notes (text field)
        - Estimated Repair Cost if known (numerical field)
- The user can “Save & Close” to add this vehicle to the report, if not all information is available
- This vehicle can be removed by selecting the garbage can icon

### **5. Passengers**

- Ability to **Add Passengers**
- For each passenger:
    - Is this person listed on the policy?
        - If yes, show listed individuals on policy and allow user to select one from list
        - If no, populate first name, last name, phone number, alternate phone number (optional), email, date of birth, languages spoken, and address
    - Were you injured in the accident?
        - If yes, populate injury descriptions, details relating to ambulance and treatment
        - If yes, this passenger will be listed as a claimant, and all information captured for the passenger will be pre-populated in the claimant section of the report
- The user can “Save & Close” to add this passenger to the report, if not all information is available
- This passenger can be removed by selecting the garbage can icon

---

## **C) HOW – Planning & Implementation**

### 

---

## **D) User Experience (UX) & Flows**

### **General Flow**

1. **Driver Confirmation**
    - User selects whether the named insured was the driver
    - If not, user chooses from listed drivers or enters a new one manually
2. **Injury Status**
    - Expand to add injury information, if applicable
3. **Attorney Representation**
    - Expand to add representation information, if applicable
4. **Add Vehicle**
    - Opens a flyout with:
        - Vehicle selection (from policy or manual entry)
        - Damage type, drivable toggle, tow info
    - Save to add to vehicle list view
    - Flyout will close when vehicle is saved, and the vehicle will be listed in the vehicle info section
5. **Add Passenger**
    - Opens a flyout for each passenger:
        - General info
        - Injury/treatment
        - Attorney representation
    - Flyout will close when passenger is saved, and they will be listed in the passenger section

### **UX Details**

- **Visual Cues**:
    - “No Vehicles Added” and “No Passengers Added” placeholders disappear once entries exist
- **Progress Indicator**:
    - Navigation sidebar updates with checkmark once driver, injury status, and vehicle are recorded

## E) Master Schema Tables

# #6 - Claimants

## **A) WHY – Vision and Purpose**

The **Claimant** section captures detailed information about any party making a claim as a result of the loss incident. These individuals may be drivers, passengers, pedestrians, or property owners impacted by the event. Collecting this information systematically supports liability determination, coverage evaluation, and efficient claim setup.

The design allows for multiple claimants to be added and managed independently, reflecting the often complex and multi-party nature of real-world incidents.

---

## **B) WHAT – Core Requirements**

### **Claimant Management**

- **Add Claimant** button to append new claimants.
- Sequential labeling: Claimant 001, Claimant 002, etc. which will be present in the left-side panel navigation as more claimants are added
- Auto-add logic: Any passenger marked as **Injured** becomes a claimant automatically, and any claimant identified at the Reporter step by an attorney will be added as a claimant automatically.

### **1. General Info**

- **First Name / Last Name** (Required)
- **Primary Phone Number** (Required)
- **Alternate Phone Number** (Optional)
- **Preferred Language**: English, Spanish, Other
- **Address**: Street, City, State, ZIP Code
- Was this person driving a vehicle involved in the incident?
    - If no, populate where the individual was located at the time of the incident
    - If yes, proceed to next section

### **2. Injury Information**

- Select ‘Add Injury Info’ to expand injury section, if applicable
- Were you injured in the accident? Yes/No
    - If yes, additional fields are presented
        - Injury Description (text field)
        - Were you transported by ambulance for medical care? Yes/No
        - Are you currently being treated? Yes/No
            - If yes, show treatment location and treatment date
    - If no, the additional injury related fields will remain hidden

### **3. Attorney Representation**

- Select ‘Add Attorney Info’ to expand attorney representation section, if applicable
- Add Attorney Info
    - First Name
    - Last Name
    - Email
    - Phone Number
    - Law Firm
    - This will default to expanded and pre-populated if the reporter was an attorney and confirmed they represented this claimant in the Reporter Info step

### **4. Non-Vehicle Property Damage**

- Select ‘Add Non-Vehicle Property Damage’ to expand section, if applicable
    - Are you the owner of the damaged property? Yes/No
    - Property Type (Dropdown): Building/Structure, Fence/Gate, Personal Property (belongings, equipment), Landscaping/Yard Features, Other Property
    - Free-text for description of damage
    - Estimated Value
    - Property Location (text field)

### **5. Vehicle Info**

- Add Vehicle via Flyout
- Vehicle Info
    - Vehicle Info: Make, Model, Year, Color, License Plate
    - Is there a lienholder for this vehicle? Yes/No
        - If yes, show Lienholder Name, Lienholder Address, Loan Number, Phone number fields
    - Is the driver the owner of the vehicle? Yes/No/Unknown
        - Owner First Name, Owner Last Name, Owner Phone Number, Insurance Company, Policy Number, Claim Number
- Damage Info
    - Is the vehicle damaged? Yes/No/Unknown
    - Is the vehicle driveable? Yes/No/Unknown
    - Was the vehicle towed? Yes/No/Unknown
    - Current Location of Vehicle (text field)
    - Damage Location (multi-select checkboxes)
    - Damage Description
        - Notes (text field)
        - Estimated Repair Cost if known (numerical field)
- The user can “Save & Close” to add this vehicle to the report, if not all information is available
- This vehicle can be removed by selecting the garbage can icon

### **6. Passengers**

- Add passengers via flyout:
    - First Name
    - Last Name
    - Phone Number
    - Alternate Phone Number
    - Email
    - Date of Birth
    - Languages Spoken
    - Street Address, City, State, ZIP

---

## **C) HOW – Planning & Implementation**

### 

---

## **D) User Experience (UX) & Flows**

### **Main Flow**

1. User clicks **Add Claimant**
2. Sidebar updates (Claimant 001, 002…)
3. Complete General Info, Injury, Attorney, Property, Vehicle, and Passenger sections
4. Repeat as needed for all involved claimants

### **Interaction Details**

- **Flyouts** for adding:
    - Vehicles (with damage tagging and tow info)
    - Passengers

## E) Master Schema Tables

# #7 - Witnesses

## **A) WHY – Vision and Purpose**

The **Witnesses** section is intended to capture critical third-party perspectives on the incident being reported. Witness statements can be instrumental in determining fault, validating claims, and resolving disputes. Collecting their information early in the FNOL process ensures the accuracy and integrity of the investigation, while allowing insurers to follow up directly if needed.

The system should support collecting details for **multiple witnesses**, each with their own contact information and personal statement, and track their willingness to be contacted.

---

## **B) WHAT – Core Requirements**

### **Witness Management**

- Add unlimited witnesses using the “+ Add Witness” button.
- Each witness is labeled sequentially: *Witness 001*, *Witness 002*, etc.

### **1. General Info (Required unless otherwise noted)**

- **First Name** *(Required)*
- **Last Name** *(Required)*
- **Phone Number** *(Required)*
- **Alternate Phone Number** *(Optional)*
- **Email** *(Optional)*
- **Date of Birth** *(Optional, Date Picker)*
- **Languages Spoken** *(At least one must be selected)*:
    - English
    - Spanish
    - Other

### **2. Address Info**

### **(Optional but encouraged)**

- **Street Address**
- **City**
- **State** *(Dropdown of U.S. states)*
- **ZIP Code**

### **3. Witness Statement**

- **Location at Time of Accident** *(Text area)* – Describe where the witness was located when the incident occurred.
- **Witness Statement** *(Text area)* – Freeform statement from the witness regarding what they saw or heard.

### **4. Contact Permission**

- **Is the witness willing to be contacted again?** *(Dropdown: Yes / No / Unknown)*

---

## **C) HOW – Planning & Implementation**

### 

---

## **D) User Experience (UX) & Flows**

### **Main Flow**

1. User selects **“Add Witness”**
2. A new witness form appears labeled “Witness 00X”
3. User completes:
    - Contact info
    - Address (optional)
    - Location and statement
    - Contact permission
4. Validation ensures required fields are completed
5. Repeat steps to add additional witnesses

### **UX Considerations**

- **Progressive Disclosure**:
    - Fields are logically grouped and clearly labeled
    - Contact permission dropdown placed at the bottom to match user reading flow
- **Sidebar Nav Updates**:
    - “Witnesses” section marked complete once at least one valid entry is saved

## E) Master Schema Tables

# #8 - Notes

## **A) WHY – Vision and Purpose**

The **Notes** section provides a flexible place for users to record **any relevant information** that doesn’t fit neatly into the structured fields of the FNOL workflow. This could include observations, quotes from the caller, or context that may be useful for adjusters or investigators later.

Critically, **notes are immutable**—once saved, they cannot be edited or deleted. This enforces audit integrity, allowing claims teams to trust the historical accuracy of each loss report’s note trail.

---

## **B) WHAT – Core Requirements**

### **1. Add Note**

- **“Add Note”** button opens a flyout
- **Note content** input (Required, free text)
- Automatically populates:
    - **Policy number** (read-only)
    - **Author name** (pre-filled from user context)
    - **Timestamp** (assigned upon save)

### **2. Display of Notes**

- Notes are shown in reverse chronological order (most recent at top)
- Each note card includes:
    - Author name
    - Timestamp (date and time)
    - Full note text
- Notes **cannot be edited or deleted**

### **3. Data Rules**

- Blank notes or whitespace-only submissions must be prevented

---

## **C) HOW – Planning & Implementation**

### 

---

## **D) User Experience (UX) & Flows**

### **Main Flow**

1. User clicks **“Add Note”**
2. Flyout appears on right side of screen
3. User enters note in free text area
4. Clicks “Add Note” to submit
    - Note appears instantly in list
    - Flyout closes if “Save & Close” is used
5. Notes display with:
    - Most recent first
    - Author and timestamp always visible
    - No ability to modify or remove

### **UX Considerations**

- **Empty State**
    - “No Notes Added” placeholder with light gray background until first note is added

## E) Master Schema Tables

# #9 - Review & Summary

## **A) WHY – Vision and Purpose**

The **Review** section is the final step in the FNOL process. It serves as a structured, read-only summary of all collected data, with particular focus on:

- Incident summary,
- Involved parties and vehicles,
- Passenger and claimant relationships.

This view provides clarity and confidence before submission and ensures that all inputs can be validated visually by the reporting user. It also aids adjusters by presenting a consolidated view of the incident without needing to comb through individual sections.

---

## **B) WHAT – Core Requirements**

### **1. Loss Summary Section**

- Read-only display of core incident details:
    - **Loss Date & Time**
    - **Loss Location**
    - **Loss Type**
    - **Description**
- Display collapsible, expanded by default (expand/collapse toggle)

### **2. Vehicle Overview**

For each vehicle (Vehicle 001, Vehicle 002, etc.):

- **Vehicle Info**: Year, Make, Model
- **Occupants**, grouped visually:
    - Each person’s:
        - Name
        - Role (e.g., Driver, Passenger – with seat position)
        - Relationship Tags:
            - **Named Insured**
            - **Claimant**
            - **Included**
            - **Excluded**
            - **Not on Policy**
            - **Third Party**

### **3. Witness Section**

- List of all recorded witnesses
- For each:
    - Name
    - Relationship Tag (e.g., **Third Party**)

### **4. Submission**

- **Submit Loss Report** button at bottom of screen
    - Submits the complete FNOL report to backend
    - Once submitted, disables editing and displays confirmation

---

## **C) HOW – Planning & Implementation**

### 

---

## **D) User Experience (UX) & Flows**

### **Primary User Flow**

1. User reaches **Review** section from the left-side navigation or by scrolling to the bottom of the page.
2. Reviews the **Loss Summary** at top (Date/Time, Location, Description).
3. Scrolls through each **Vehicle** section:
    - Views driver, passengers, and tags
4. Views **Witness** list at bottom
5. If satisfied, clicks **Submit Loss Report**
6. On submit:
    - System locks editing
    - Redirect to start of FNOL workflow

### **UX Details**

- **Submission Feedback**:
    - Real-time validation before submission (e.g., prevent submit if required data missing)
    - Toast: “Loss Report successfully submitted” on success

## E) Master Schema Tables

# #10 - Request Appraisals

## **A) WHY – Vision and Purpose**

The **Request Appraisals** function is designed to streamline the collection of appraisal documents (such as damage estimates, receipts, or medical documentation) from claimants immediately after a loss report is submitted. This step provides a configurable option for insurers to choose how claimants will submit appraisal materials—either through an **internal link** (e.g., secure portal) or **external link** (e.g., third-party platform).

By surfacing this at the moment of submission, the workflow encourages early follow-up and claimant engagement, while allowing flexibility to delay if more information is needed.

---

## **B) WHAT – Core Requirements**

### **Modal Trigger & Display**

- The **Request Appraisals modal** appears **after clicking “Submit Loss Report”**.
- Only visible if at least one **claimant** is present in the FNOL report.

### **Modal Content**

### **1. Claimant List Table**

- Displays each **claimant’s**:
    - **Name**
    - **Email**
    - **Phone Number**
    - **Delivery Method Selection**:
        - **Internal Link** (radio button)
        - **External Link** (radio button)
        - One must be selected for each claimant
        - If only one method is available per configuration, hide the other

### **2. Action Buttons**

- **Send Requests**:
    - Sends the appraisal request to all listed claimants via the selected delivery method (email or SMS).
    - Submits the loss report at the same time.
- **Skip for Now**:
    - Bypasses the request step.
    - Proceeds to loss report submission only.
- **Cancel**:
    - Closes the modal with no action taken.

---

## **C) HOW – Planning & Implementation**

---

## **D) User Experience (UX) & Flows**

### **Standard Flow**

1. User completes all required FNOL sections and clicks **Submit Loss Report**.
2. **Request Appraisals modal** appears.
3. User selects **Internal Link** or **External Link** per claimant.
4. User clicks **Send Requests**.
5. Appraisal requests are sent → Success message appears → Report is submitted.

### **Alternate Flow – Skip**

1. User clicks **Skip for Now**.
2. Modal closes and loss report is submitted without appraisal requests.

### **UX Guidelines**

- **Auto-Select**: If only one delivery option is available for all claimants, preselect and hide the other.
- **Error Prevention**: “Send Requests” is disabled if no delivery method is selected (when both options are available).

## E) Master Schema Tables