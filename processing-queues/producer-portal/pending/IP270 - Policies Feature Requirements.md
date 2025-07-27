# IP270 - Policies Feature Requirements

# #1 - Policy Search

## **A) WHY – Vision and Purpose**

The **policy search experience** is designed to allow producers to **quickly locate and review policy records** using powerful filters and keyword search. The goal is to:

- Improve **efficiency** in navigating large policy datasets.
- Enable **targeted search** by policy attributes (e.g., status, effective date).
- Support **range-based and single-date filtering** for flexible queries.
- Provide **responsive UI** for desktop and mobile use.

This experience empowers users to **manage and service policies more effectively** by reducing search time and minimizing the need for external queries.

---

## **B) WHAT – Core Requirements**

### 1. **Search Input**

- Keyword input that supports search by:
    - Policy number
    - Insured name
    - Phone number
    - Email address
    - Driver’s license number
    - Vehicle Identification Number (VIN)

### 2. **Filter Controls**

- **Status Filter**:
    - Multi-select checkboxes: `In Force`, `Pending Cancellation`, `Cancelled`, `Expired`
- **Effective Date Filter**:
    - Choose single date or date range
    - Calendar UI for selection
- **Expiration Date Filter**:
    - Same structure as effective date filter

### 3. **Policy Table Display**

- Columns:
    - Policy Number
    - Insured Name
    - Producer Number
    - Effective Date
    - Cancellation Date
    - Status (colored pill tag)
- Sorting:
    - Sortable by selecting column headers

### 4. **Mobile Version**

- Collapsed search bar and guiding text
- Search results horizontally scrolls

---

## **C) HOW – Planning & Implementation**

---

## **D) User Experience (UX) & Flows**

### 🧭 Flow Summary

1. **User opens Policies Search**
    - By default, displays policies in descending order by effective date
2. **User uses Search Bar**
    - Types a keyword to search, and hits enter to complete search
    - Partial matches return relevant records
3. **User applies Filters**
    - Status: Select one or multiple statuses
    - Effective or Expiration Date:
        - Select single date or range
        - Calendar UI supports smooth selection
    - Filters are shown using the selected filter states
4. **User reviews results**
    - Scans list of policy results
    - Clicks a policy to drill into details (next workflow)
5. **User clears/reset filters**
    - Clicking “X” on each filter clears that filter

---

### ✨ UX Notes

- Use **colored tags** for policy status to improve scannability
- Display **active filters** clearly and allow for individual removal
- Calendar date selectors default to today’s date for faster filtering
- Provide **loading indicator** while querying

---

### 🧪 Edge Cases & Validation

- No results → show “No policies found” message
- Invalid date ranges (end date before start date) → disable search
- Large datasets → enable pagination, showing 10 results on default with the user able to select the next page to view additional information

# #2 - Policy Details Tab

## **A) WHY – Vision and Purpose**

The **Policy Overview Page** provides a comprehensive and centralized snapshot of a customer's insurance policy. It is the **landing screen after selecting a policy** from the search results and serves as the user’s gateway into more detailed policy-related data and actions. The goals of this view are to:

- **Give users immediate visibility** into the most important policy information (e.g., next payment, coverages, insured details).
- Provide **structured and readable access** to policy metadata, financial details, and coverage breakdowns.
- Enable quick navigation to other key tabs such as **Drivers & Vehicles**, **Payment History**, **Documents**, **Claims**, and **Endorsements**.

This experience aims to streamline internal operations by reducing the need to jump between systems to view policy-level data.

---

## **B) WHAT – Core Requirements**

### 1. **Policy Header**

- Insured Name
- Policy Number
- Policy Status:
- Do Not Call (optional badge)
- Action Button: `More Actions` dropdown
    - Options: Payment, Endorsement, Claim, Suspense
- Cancel Policy button (with appropriate confirmation handling)

### 2. **Overview Panel (Right Rail)**

- Billing Info
    - Amount Due
    - Remaining Payment
    - Billing Fee
    - Next Payment Date
    - Installment Payment Due Dates & Total Amounts
- **Important Dates**
    - Effective Date
    - Expiration Date
    - Inception Date

### 3. Upcoming Payment

- Show the following:
    - Upcoming Payment Value
    - Due Date
    - Make a Payment button, allowing the user to enter the make a payment flow

### 4. **Primary Insured Section**

- Primary Insured Name
- Date of Birth
- License Number
- Gender
- Marital Status
- Street Address
- Primary Phone Number
- Alternate Phone Number
- Notification Preference
- Email Address
- Policy Term
- Paperless Discount
- EFT Discount
- Prior Insurance Status
    - This will list one of three statuses: Prior Insurance, Verify, or Transfer, along with a number of months
- Eligible Discounts

### 5. **Coverages Table**

- Policy-Wide Coverage (e.g., Bodily Injury, PIP, Uninsured/Underinsured Motorist)
- Vehicle-Specific Coverage (grouped by vehicle, e.g., 2009 Toyota Tacoma)
- Display:
    - Coverage name
    - Coverage level/limit/type
    - Premium (per coverage line)
    - Total premium at bottom

### 6. **Navigation Tabs (Top Section)**

- `Policy Details` (active tab)
- `Drivers & Vehicles`
- `Payment History`
- `Documents`
- `Claims`
- `Endorsements`

---

## **C) HOW – Planning & Implementation**

### 

---

## **D) User Experience (UX) & Flows**

### 🧭 User Flow

1. **User clicks a policy from search results**
    - Redirected to Policy Overview tab
2. **User reviews top-level information**
    - Sees the Next Payment box with due date and CTA
3. **User reviews Primary Insured details**
    - Expands (if collapsed) to see name, contact, marital status, etc.
        - These sections will be expanded on default
4. **User views policy coverages**
    - Organized into: policy-wide and per-vehicle
    - Sees premium per coverage line and total
5. **User explores other policy areas**
    - Clicks other tabs (e.g., Drivers & Vehicles, Payment History)
6. **User takes actions**
    - Clicks “Make a Payment” or “Cancel Policy”
    - Accesses “More Actions” (e.g., Create Endorsement, Suspense, Payment or Claim)

---

### 📱 Mobile-Specific Adjustments

- Information will collapse to accommodate the reduction in screen space
- The additional tabs will be available by scrolling horizontally

---

# #3 - Drivers & Vehicles Tab

## **A) WHY – Vision and Purpose**

The **Drivers & Vehicles** tab allows users to view all individuals and vehicles associated with an insurance policy. This section ensures clarity around:

- Who is insured under the policy and in what capacity.
- Which vehicles are covered, including their associated coverage, limits, and premiums.

This section is critical for validation, servicing, endorsements, and customer inquiries. By structuring this information in a clearly grouped and expandable format, the system enhances operational efficiency and policy transparency.

---

## **B) WHAT – Core Requirements**

### 1. **Drivers Section**

- List of all drivers on the policy.
- For each driver:
    - Full Name
    - Label: `Primary` if applicable
    - Date of Birth
    - License Number
    - Violation Points
    - Status: `Included`, `Excluded`, etc.

### Expandable Driver Detail Panel (Drawer)

Upon click of a driver, a side panel will open from the right to show the following: 

- **Driver Info**
    - Full name
    - Primary status
    - Class
    - Gender
    - Date of birth
    - Age
    - Marital status
    - Relationship to Insured
    - Violation Points
- **Driver License Info**
    - License state
    - Country
    - Number
    - Years of experience
- **Employment Info**
    - Status (employed/unemployed)
    - Occupation title
    - Employer name

### 2. **Vehicles Section**

- List of all vehicles on the policy.
- For each vehicle:
    - Year, Make, and Model
    - VIN
    - Plate Number

### Expandable Vehicle Detail Panel (Drawer)

Upon click of a vehicle, a side panel will open from the right to show the following: 

- **Vehicle Information**
    - Year, Make, Model
- **Vehicle Image**
    - Display if available
- **Limits & Deductibles**
    - Each coverage type (e.g., Comprehensive, Collision, Rental, Towing, etc.)
    - Deductible or status (declined or amount)
- **Premiums**
    - List all applicable coverages and associated premiums
    - Total Premium at bottom

### 3. **Applied Discounts**

- List all discounts applied to the policy due to drivers or vehicles (e.g., Multi-Car, Homeowner).

---

## **C) HOW – Planning & Implementation**

---

## **D) User Experience (UX) & Flows**

### 🧭 User Flow

1. **User selects “Drivers & Vehicles” tab** from the policy summary screen.
2. **Drivers list is shown**, each with status, role, and basic details.
3. User clicks a **driver name** → side panel opens with full info.
4. User closes the side panel, or clicks on the main screen behind the side panel to close it, and expands the **vehicles section**.
5. User clicks a **vehicle row** → side panel opens with coverages, deductibles, and premium details. User closes the side panel, or clicks on the main screen behind the side panel to close it.
6. **Applied Discounts** are shown in a short list at the bottom..

### 📱 Mobile Experience

- Section headers are stacked vertically.
- Tap to expand/collapse drivers or vehicles list.
- Modal-style drawer transitions for driver/vehicle detail.
- To navigate to other tabs, the user can swipe horizontally to access

### 🧪 Edge Case Handling

- If no vehicles are associated with the policy, the vehicles section will not show

# #4 - Payment History Tab

## **A) WHY – Vision and Purpose**

The **Payment History** tab provides a transparent and easily accessible record of all past and upcoming financial transactions related to the insurance policy. This section:

- Enables users to verify payment completion or failure.
- Allows tracking of payment schedules, methods, and associated adjustments (like policy changes or discounts).
- Surfaces failed transactions and prompts corrective action (e.g., reattempt payment).
- Supports service operations by detailing the financial lifecycle of a policy in one centralized view.

---

## **B) WHAT – Core Requirements**

### 1. **Payment History Table**

- Tabular listing of all financial transactions tied to the policy.
- **Columns:**
    - `Date`
    - `Transaction Type` (e.g., Installment, Billing Fee, Endorsement Fee)
    - `Payment Method` (e.g., E-Check, Card)
    - `Confirmation #`
    - `Amount`
    - `Balance`
    - `Status` (e.g., Paid, Upcoming, Failed, Cancelled)

### 2. **Filters and Search**

- **Filter by:**
    - Term: Current Term, Previous Term
    - Category: Installment, Billing Fee, Endorsement Fee
    - Status: Paid, Upcoming, Failed, Cancelled
- **Search** by confirmation number or dollar value (real-time filtering).

### 3. **Transaction Detail Drawer**

- Opens upon clicking a row in the table.
- Displays the following grouped data:

### General Info

- Transaction type
- Payment Status
- Date
- Description (if applicable)

### Payment Info

- Method (E-Check, Card, etc.)
- Confirmation number
- Amount
- Last 4 digits (for card), masked routing/account numbers (for e-check)

### Additional Info

- Billing Cycle
- EFT Autopay Enabled
- Billing Period
- Make a Payment button, if it is an upcoming payment

---

## **C) HOW – Planning & Implementation**

---

## **D) User Experience (UX) & Flows**

### 🧭 User Flow

1. User selects the **Payment History** tab from the policy overview.
2. The table loads all transactions.
3. User applies filters or searches for a transaction.
4. Clicking a transaction opens a **detail side panel**.
5. If transaction is:
    - **Upcoming** → Shows due date + “Make Payment” CTA.
    - **Failed** → Shows relevant status.
6. For refunds or voided payments, the drawer shows refund data.

- **Consistency:** Align detail drawer UI with other modules (Drivers, Vehicles).
- **Clarity:** Display monetary values with currency formatting.
- **Mobile Optimization:** user can horizontally scroll to see the payment history table.

### 🧪 Edge Case Handling

- **No Transactions:** Display message: “No payment activity for this policy term.”
- **All Failed Payments:** Include a sticky message on tab indicating issues.
- **Large Data Sets:** Paginate, showing 10 records on default, allowing the user to click to see the additional pages.

# #5 - Documents Tab

## **A) WHY – Vision and Purpose**

The **Documents** section enables users to **upload, manage, and review policy-related documents**. This ensures:

- All critical policy documentation is stored and organized in a single location.
- Users can upload compliance materials, such as licenses, endorsements, and forms.
- Documents are easily retrievable and viewable to support audits, service actions, or customer inquiries.
- Expiry and metadata tracking enables proactive compliance and follow-ups.

---

## **B) WHAT – Core Requirements**

### 1. **Document List View (Table)**

- Displays all documents linked to the selected policy.
- **Columns:**
    - Icon (file type)
    - Document Name
    - Date Added
    - Three dot menu, which will allow the user to delete the file if neeeded
- Search for documents by keying in document name or date added in the search bar
- The ID Card will be generated on demand

### 2. **Upload Document Modal**

- Allows file upload to the policy.
- Select from **document type dropdown** (configurable list).
- Drag-and-drop or file picker to upload file.

### 3. **Document Detail & View**

- Clicking a document row opens a **preview viewer** and **metadata panel**.
- **Details panel includes:**
    - Document Name
    - Policy Number
    - Loss Sequence (if applicable)
    - Description
    - Assigned to
    - Agent Number

### 4. **Document History**

- Accessible from the document detail panel.
- Logs actions (uploaded, viewed, deleted, restored) with timestamps and user.

### 5. **Delete (Trash) Document**

- Delete icon opens a confirmation modal:
    - Warns that file will move to trash.
    - Indicates it can be restored within X days.
    - Includes “Move to Trash” and “Cancel” actions.

---

## **C) HOW – Planning & Implementation**

---

## **D) User Experience (UX) & Flows**

### 🧭 User Flows

### 1. Viewing Documents

- User clicks **Documents** tab from the policy menu.
- Table displays list of uploaded files.
- User clicks a document → opens preview with metadata.

### 2. Uploading Documents

- User clicks “Upload Document”.
- Chooses document type
- Uploads file via drag/drop or picker.
- Clicks “Upload File” → confirmation & list refreshes.

### 3. Deleting a Document

- User clicks trash icon.
- Modal prompts for confirmation → upon confirmation, document is hidden/flagged as trashed.

### 4. Viewing Metadata / History

- Inside viewer panel, user can toggle to see:
    - `Document Info` (default)
    - `Document History` (user actions log)

### 📱 Mobile Considerations

- List of documents collapses to fit the width of the screen

# #6 - Claims Tab

## **A) WHY – Vision and Purpose**

The **Claims** section provides users with a centralized view of all claims associated with a specific insurance policy. This view supports:

- **Transparency** into past and ongoing claims.
- **Quick access** to relevant claim details like type, loss amount, adjuster, and description.
- The ability to identify and address open, unresolved, or complex claims.
- Support for customer service teams and agents to investigate or verify claim history efficiently.

---

## **B) WHAT – Core Requirements**

### 1. **Claims Table/List View**

- Shows all submitted claims for the policy.
- **Columns:**
    - Loss Number (unique identifier)
    - Loss Description (e.g., Car Accident - Insured operator at fault)
    - Loss Date
    - Assigned Adjuster

### 2. **Claim Flyout (Detail Panel)**

- When a row is clicked, opens a flyout with detailed information.
- **Fields Displayed:**
    - Loss Number
    - Description
    - Loss Date
    - Paid Out
    - Open Lines
    - Closed Lines
    - Adjuster

### 3. **Submit Claim Button**

- Prominent green button in desktop and mobile views.
- Navigates to a separate claim submission experience (out of scope for this view but should support routing to an external website)

### 4. **Empty State**

- If no claims exist on the policy, show a friendly message:
    
    > “This policy has no claims. When claims are submitted, they will appear here.”
    > 
- Disable or hide sorting/filtering tools when list is empty.

---

## **C) HOW – Planning & Implementation**

---

## **D) User Experience (UX) & Flows**

### 🧭 User Flows

### 1. Viewing Claims

- User navigates to a policy and clicks the **Claims** tab.
- If claims exist → list is displayed.
- If no claims exist → empty state message is shown.

### 2. Inspecting Claim Details

- User clicks a claim row.
- A flyout panel shows detailed claim information on right (desktop) or as full screen (mobile).

### 3. Submitting a Claim

- User clicks **Submit Claim** button.
- Redirects to external submission page.

# #7 - Endorsements Tab

## **A) WHY – Vision and Purpose**

The **Endorsements** section offers users a clear view into all **modifications** made to a policy **after issuance**. These include changes such as adding drivers, adjusting coverages, or removing discounts. The goals of this experience are:

- To give users and agents visibility into the **evolution of a policy** over time.
- To enable initiation of new endorsements with a **Submit Endorsement** button.
- To ensure traceability of all policy alterations in a clean, audit-friendly format.
- To maintain a consistent experience across desktop and mobile platforms.

---

## **B) WHAT – Core Requirements**

### 1. **Endorsements List View**

- Displays a chronological list of all endorsements associated with the policy.
- **Columns:**
    - **Endorsement #** (unique, sequential ID)
    - **Type** (e.g., Policy Change)
    - **Message** (brief explanation of the change)
    - **Effective Date**

### 2. **Submit Endorsement Button**

- Prominently displayed green button in both desktop and mobile views.
- Launches the workflow to start an endorsement request (this is out of scope for this epic, but must support internal routing to the endorsement workflow to follow).

### 3. **Empty State Handling**

- If no endorsements are present, show a friendly message:
    
    > “This policy has no endorsements. When endorsements are submitted, they will appear here.”
    > 
- Remove or disable sorting, interaction, and scroll regions when empty.

---

## **C) HOW – Planning & Implementation**

---

## **D) User Experience (UX) & Flows**

### 🧭 User Flows

### 1. Viewing Endorsements

- User selects the **Endorsements** tab under a policy.
- If endorsements exist → they are displayed in a table/list format.
- If no endorsements exist → empty state is shown.

### 2. Submitting a New Endorsement

- User clicks **Submit Endorsement**.
- Navigates to the endorsement workflow.

# #8 - Cancel Policy Workflow

## **A) WHY – Vision and Purpose**

The **Policy Cancellation** experience enables users to **initiate** a cancellation process, specify a **reason**, and confirm the action confidently. Once a cancellation is in progress or completed, users must clearly see the updated **status and context** of the policy directly from the **Policy Overview** screen.

This flow aims to:

- Provide a **controlled and guided process** for canceling a policy.
- Minimize user error by confirming intent and capturing rationale.
- Transparently **communicate the policy’s state** before, during, and after cancellation.
- Ensure consistency across both **desktop and mobile** views.

---

## **B) WHAT – Core Requirements**

### 1. **Cancel Policy Button**

- Appears in the top-right of the Policy Overview screen.
- Enabled only for **policies in force** (not already cancelled or pending cancel).

### 2. **Cancellation Workflow**

- Clicking "Cancel Policy" opens a **confirmation flow**:
    - **Cancellation Effective Date**
        - Specify the date the cancellation would go into effect
    - **Cancellation Reason Dropdown**
        - Options include:
            - Found a better rate
            - Got coverage elsewhere
            - No longer needs coverage
            - Moving out of state
            - Vehicle sold
            - Financial hardship
            - Dissatisfied with service
            - Other
    - **Additional Notes**
        - If the producer wants to capture any additional information to submit with the cancellation request, they can populate that information here.
    - **Confirm Cancellation**
        - Summary screen showing policy number and confirmation text:
            
            > “Are you sure you want to cancel this policy?”
            > 
        - Buttons: **Cancel** and **Yes, Cancel Policy**

### 3. **Post-Cancellation State Handling**

- Once cancellation is initiated, the Policy Overview screen must reflect the new state:
    - **Warning or Error Banners** based on status and billing
    - **Updated Labels**: "Cancellation Pending" or "Cancelled"
    - Visual color changes (e.g., yellow for pending, red for cancelled)
    - Payment summary updates (e.g., refund owed, balance due)

---

## **C) HOW – Planning & Implementation**

### 

---

## **D) User Experience (UX) & Flows**

### 🧭 User Flows

### 1. Cancel a Policy

1. User clicks **Cancel Policy**.
2. Cancellation effective date must be filled in. 
3. User proceedes to reason dropdown and selects a reason, as well as any additional notes to communicate to the underwriting team. 
4. Confirmation screen appears.
5. On confirmation, the policy state updates to “Pending Cancellation”.

### 2. View Cancelled or Pending Cancellation State

- On returning to Policy Overview:
    - Banner at top of page (color-coded)
    - Status pill changes to "Pending Cancellation" or "Cancelled"
    - Payment area displays refund or balance owed
- There are four possible states supported for policies in the cancellation workflow:
    - Cancelled upon customer request, policy reinstatement is available
    - Cancelled due to non-payment, policy reinstatement is available
    - Pending cancellation
    - The policy has been cancelled and is eligible to be requoted (this will enter the requoting flow within the platform)

# #9 - Make a Payment Workflow

## **A) WHY - Vision and Purpose**

The purpose of this experience is to provide users with a streamlined and flexible way to submit policy payments through various methods—E-Check (Insured & Producer) and Credit Card—while ensuring robust validation, clear feedback, and error handling. This experience is designed to support payment submission, reduce user friction, and handle edge cases like invalid inputs or processing failures.

---

## **B) WHAT - Core Requirements**

1. **Payment Methods Supported**
    - Insured E-Check
    - Producer E-Check
    - Credit Card
2. **Form Fields by Method**
    - **Producer E-Check:**
        - No additional information is required if selected
    - **Insured E-Check:**
        - Routing number
        - Account number
    - **Credit Card:**
        - Cardholder name
        - Card number
        - Expiration date (MM/YY)
        - CVV
        - Billing Address
3. **Convenience Fee**
    1. The Insurance Company may optionally implement a convenience fee on credit card transactions. If applicable, the user will be presented an alert when selecting credit card as their payment method, and the convenience fee will be listed as an additional line item in the transaction prior to completing payment. 
    2. The fee value is configurable and may vary from insurance company to insurance company. 
4. **Payment Method Fields**
    - Payment due date is presented to provide helpful context to the user
    - The user has the following options:
        - To Pay in Full, with the full payment listed
        - Pay the Minimum Amount, with the minimum amount listed
        - An Other Amount, to be populated by the user
5. **Validation Requirements**
    - Required fields must be filled
    - Numeric fields (routing, account, card) must be valid
    - Card expiration must be in the future
    - Other Amount must be greater than $0.00 and not greater than the full payment amount if selected
6. **Error Handling**
    - Field-level error indicators (red text + borders)
    - Inline messages for form validation
    - Full-screen error pages for payment processing failures
7. **Success and Confirmation**
    - Loading indicator while processing
    - Confirmation screen upon successful payment
    - Error screen with retry option if processing fails

---

## **C) HOW - Planning & Implementation**

### 

---

## **D) User Experience (UX) & Flows**

### 1. **Initial State**

- User clicks “Make a Payment”
- Chooses between: Insured E-Check, Producer E-Check, or Credit Card
- Corresponding form displays based on selection

### 2. **Form Entry Flow**

- User fills in all required payment info
- Submit button remains disabled until all validations pass

### 3. **Submission**

- Upon clicking “Submit Payment,” the user is pushed to a loading state, followed by a confirmation screen

### 4. **Outcome States**

- **Success:**
    - User is directed to a confirmation page with success status and confirmation number
- **Failure:**
    - Full-screen error with explanation

### 5. **Error States**

- Field-level errors show if inputs are invalid
- All validations triggered on “submit” click
- Red borders and messages for fields like invalid routing, blank fields, etc.

---

# #10 - Right Panel Navigation

## **A) WHY - Vision and Purpose**

The **Right Panel** serves as a quick-access, context-aware navigation hub for managing key policy functions without leaving the current view. It is designed to reduce user effort and improve efficiency by consolidating core policy actions into an easily accessible panel on the right side of the policy overview.

This workflow empowers users to **act on policies faster**, **stay oriented**, and **reduce page navigations**, enhancing both usability and task completion speed.

---

## **B) WHAT - Core Requirements**

There are four sections within the Right Panel: 

- Overview (already covered in this document)
- Activity
- Notes
- Settings

The user can keep this side panel open as they navigate between tabs, or collapse the side panel by clicking the “X”. It can be re-expanded on click of the side panel. 

**Activity**

- This is an activity log of changes on the policy, along with date and timestamps for record (e.g. new suspenses being created, endorsements being created, payments made)

**Notes**

- This captures notes recorded on the policy by the producer
- This section also allows the producer to add additional notes

**Settings**

- This is where we can manage key details on the insured

---

## **C) HOW - Planning & Implementation**

---

## **D) User Experience (UX) & Flows**

### 1. **Panel Launch**

- Panel is open on default, and can be closed by clcking the “X” button
- Click action (e.g., Overview, Activity, Notes, Settings) opens panel
- Panel slides over the right side of screen
- Current context remains visible (policy overview stays in background)

### 2. **Navigation in Panel**

- Actions shown as selectable icons

### 3. Viewing Activities

- The user can view activites on the policy, including paymentse, notes, documents, suspenses, and endorsements

### 4. Viewing & Adding Notes

- User navigates to Notes
- User can see prior notes, including the author, date, and content of the note
- The user can add additional notes by populating the text field and selecting “Post”
- Notes will be shown in descending order, with the most recent note at the top

### 5. Updating Settings

- General and Payment Settings can be modified by selecting the pencil icon to edit
- General Settings
    - When entering edit mode, a modal will present with the following information
    - Here the user can update the email address and phone number of the named insured, as well as their notification preferences and enrollment in paperless delivery
    - If an insured needs to be marked as “Do Not Call”, this flag can also be set here
    - When an email and/or phone number are updated, the user will receive an email or SMS to verify their contact information, which will then show the verified flag in the General Settings section
    - Here the producer can also resend verification emails/SMS if needed
    - When changes are saved, the modal will close and the user will see the relevant updates reflected in the general settings section
- Payment Settings
    - If the insured wants to modify their payment method, the user can do so by selecting e-check or credit card, and populating the relevant information
        - E-Check: Rounting number, account number
        - Credit Card: card number, expiration date, CVV, name of cardholder, and billing address
            - If the Insurance Company has opted in to levying the convenience fee on credit card transactions, an alert will be presented to the user indicating the fee will be charged on future transactions. This fee will be a dynamic value.
    - Upon selection of a payment method and proceeding, the user will be presented the signature workflow to sign their documents as defined in `IP269 - Quotes: Bind - Step 3: Sign Documents` with the user having the option to sign in person or remotely

# E) Master Schema Tables