# IP003 - Agent Inquiry Feature Requirements

# #1 - Producer Inquiry Experience (Producer Search)

## **A) WHY - Vision and Purpose**

The **Producer Inquiry Page** provides users with the ability to **search for, view, customize, and export** data on producers within the system. This tool supports operational efficiency by:

- Giving users quick access to producer information using intuitive filters.
- Empowering users to customize which data columns are shown based on their needs.
- Allowing users to export filtered and formatted producer data for offline review, audit, or sharing purposes.

This experience ensures transparency, usability, and task flexibility for producer-related inquiries.

---

## **B) WHAT - Core Requirements**

### 1. **Producer Search Table**

- Display list of producers including:
    - Status (colored pills: Active, Inactive, Suspended, Terminated)
    - Producer Number
    - Producer Name
    - Phone
    - Last Contact (date)
- Default columns visible:
    - Producer Number, Producer Name, Status, Phone, Last Contact
- User can search by keyword, filter, or sort the tables
    - Sorting functionality is accessed by selecting the column header
    - The downward pointing arrow will indicate which column the table is actively being sorted by

### 2. **Search Functionality**

- Global search input above the table that supports:
    - Keyword (Producer Name, Number, City, State, County, ZIP Code)
    - Filters: Status, State

### 3. **Filtering Capabilities**

- **Status Filter**
    - Checkbox list with statuses:
        - Active
        - Inactive
        - Suspended
        - Terminated
    - "Reset" and "OK" options
- **State Filter**
    - List of US states with checkboxes
    - Typeahead input for state names
    - "Reset", "OK", “Cancel” options
        - “Reset” will clear all selected checkboxes
        - “OK” will apply the filters selected
        - “Cancel” will close the filter dropdown with no modifications to filters selected/unselected
- Show active filters above the table with a **“Clear”** option

### 4. **Column Customization**

- "Columns" dropdown allows users to:
    - Select/Deselect columns to show in the table
    - Additional columns will expand the table horizontally, introducing a horizontal scroll to see all columns beyond the screen width
    - Use a typeahead interface for fast field discovery
    - "Reset", "OK", “Cancel” options
        - “Reset” will clear all selected checkboxes
        - “OK” will apply the columns selected
        - “Cancel” will close the column dropdown with no modifications to filters selected/unselected
- Column options include:
    - Default visible: Producer Number, Name, Status, Phone, Last Contact
    - Additional options (examples): City, County, State, ZIP, E&O Expiry Date, Net Written Premium, Renewal Count, etc.

### 5. **Export Producer Report**

- **Export Button** triggers modal with:
    - Export format selection: **CSV** or **PDF**
    - Column selection checklist
        - Export includes only visible/selected columns
        - The user can find additional columns by scrolling down the list of columns or using the typeahead interface for fast field discovery
        - The user can select additional columns by checking the appropriate boxes, or select all
    - "Generate" initiates file export
    - “Cancel” closes modal with no action taken

---

## **C) HOW - Planning & Implementation**

### 

---

## **D) User Experience (UX) & Flows**

### 1. **Search & Filter Flow**

1. User lands on Producer Inquiry Page
2. Enters keyword in search bar or applies filters (Status/State)
3. Table updates with number of results and filters shown above table
4. User can clear filters individually or all at once

### 2. **Column Customization Flow**

1. User clicks **“Columns”**
2. Modal opens with all available column fields
3. User selects/deselects columns, hits “OK”
4. Table updates immediately to reflect changes

### 3. **Export Flow**

1. User clicks **“Export”**
2. Modal opens prompting:
    - Format selection (CSV or PDF)
    - Column selection
3. User clicks **“Generate”**
4. File is generated with selected column structure

### 4. **Visual Behavior**

- **Status pills** use color codes:
    - Green = Active
    - Red = Inactive
    - Red = Suspended
    - Red = Terminated
- Columns maintain alignment and responsive spacing
- Empty state messaging if no producers match filters

## **E) Master Table Schemas**

# #2 - Producer Details: Overview Tab

## **A) WHY – Vision and Purpose**

The **Producer Overview Page** is the first screen users see after selecting a producer from the Producer Inquiry search results. Its purpose is to:

- Provide a **centralized, editable snapshot** of the producer’s business, licensing, and operational profile.
- Empower users to **review and update critical details** quickly and efficiently without navigating multiple pages.
- Display essential producer metadata in the **top navigation header** for quick at-a-glance access.

This experience improves operational efficiency, ensures data accuracy, and supports compliance requirements.

---

## **B) WHAT – Core Requirements**

### 1. **Header Metadata**

Displayed at the top of the screen:

- Producer Name
- Producer Number
- City/State
- Phone Number
- Email Address
- Status indicator (e.g., Active / Inactive / Suspended / Terminated)
- Back Arrow to return to the search results experience

### 2. **Overview Tab Sections**

Each section displays data in a collapsed format with an **Edit** button and supports in-place editing per section. Modifications will be saved upon selection of the **Save** button when in the edit state. If the user wants to purge their edits without saving, they can click **cancel**, or exit the page.

### a. **Insurance Details**

- Group Code
- Master Code
- Producer Name
- Doing Business As Name
- Email
- Website
- Error & Omissions Limit
    - When editing this field, a dropdown will be available with the following values:
        - $5,000,000
        - $2,000,000
        - $1,000,000
- Error & Omissions Expiration Date
    - When editing this field, a date picker will be presented up on selection, allowing the user to select the appropriate date

### b. **Tax Details**

- Tax Name
- Tax ID/SSN
- Tax Code
    - When editing this field, a dropdown will be available with the following values:
        - Corporation
        - Individual
        - Partnership
- Tax ID Type
    - When editing this field, a dropdown will be available with the following values:
        - EIN/TIN
        - SSN
        - This field will be defaulted based on the tax code
            - Tax Code: Individual = Tax ID Type: SSN
            - Tax Code: Corporation or Partnership = Tax ID Type: EIN/TIN
- Tax Address
- Tax City
- Tax State
    - When editing this field, a dropdown will be available with a list of US states to select from
- Tax Zip

### c. **Advanced Settings**

- Use Digital Signatures
    - This field cannot be edited and is locked down by default
- Criminal Search
    - When editing this field, a dropdown will be available with the following values:
        - Yes
        - No
        - This controls whether or not the criminal search process is run during underwriting.
- Distribution Channel
    - When editing this field, a dropdown will be available with the following values:
        - Retail
        - Other Independent Agents
        - Controlled Agent
        - This is the rating factor that is used as a part of the Rate, Quote, Bind flow. This is an easy way for the MGA to change the rating factor, allowing for discounts, or surcharges based on these definitions.
- Remote Signature Default
    - When editing this field, a dropdown will be available with the following values:
        - Opt-In
        - Opt-Out
        - This setting controls whether or not the agent can input an email/phone number to gather the e-signature. If the agent is opted out, the insured would need to come physically into the office to sign.
        - This will default to opt-in for all new producers created, but can be overridden.
- Homeowner Verification
    - When editing this field, this can be turned on or off using the relevant toggle.
- Notify Method
    - This field cannot be edited and is locked down by default.
- Loss Experience
    - When editing this field, a dropdown will be available with the following values:
        - Off
        - On
- Liability Only
    - When editing this field, this can be turned on or off using the relevant toggle.
- Rater
    - The comparative rater used by the agency. This will be a read only field and set globally. There is an edge case where an agency may use multiple raters.

### **d. Suspension**

- 

### e. Page History

- This section acts as the audit history for this tab, reflecting any interactions with the page sections
- Each row in the table will be comprised of the following attributes:
    - Date and Time Stamp of when the interaction with the page occurred
    - The action, which may include:
        - Page Created
        - Page Viewed
        - Page Edited: [Section Name] (i.e. Insurance Details, Tax Details, Advanced Settings)
            - This will only include one section per row, as the user is not able to edit multiple sections at once
        - User
            - This will be the system username for this user

### 3. **Edit Functionality**

Each section supports an edit mode:

- Inline or modal editing
- Cancel/save actions
- Real-time update of overview data upon save

### 5. **Quick Info Panel (Right Sidebar)**

The right sidebar will be expanded on default when the page loads, showing the Quick Info section. This section includes: 

- Marketing Rep
- Contact Information
- Mailing Address
- Physical Address
    - In the Physical Address section, a search will be run in the background for the latitude and longitude of this producer, with a status confirming if it was found. If the latitude/longitude is not found, the status will be updated to reflect that, and the latitude/longitude fields will be left empty.

Each section can be edited by selecting the **Edit** button, and a modal will be presented allowing the user to modify, save, or cancel changes per section. 

---

## **C) HOW – Planning & Implementation**

### 

---

## **D) User Experience (UX) & Flows**

### 1. **Landing on the Overview Tab**

- Trigger: User clicks a producer from search results
- Page loads:
    - Top header with producer metadata
    - Overview tab is open by default
    - Each detail section (Insurance, Tax, Advanced) shown in read-only mode
    - Right side panel expanded, showing Quick Info section

### 2. **Editing a Section**

1. User clicks **Edit** in a section
2. Section becomes editable (inline or modal)
3. User modifies values and clicks **Save**
4. Validations run
5. If valid, data is updated, and section returns to read-only with new values shown

### **E) Master Table Schemas**

---

# #3 - Producer Details: Banking Info Tab

## **A) WHY – Vision and Purpose**

The **Banking Info** tab provides authorized users with a dedicated view to **review and manage critical financial and banking data** for a producer. These banking details directly affect how commissions and e-check payments are processed.

This centralized experience:

- Ensures producers’ banking information is accurate, secure, and compliant.
- Reduces friction in payment operations by allowing quick updates to account details.
- Provides transparency via a clear audit trail of changes.

---

## **B) WHAT – Core Requirements**

### 1. **Top Navigation Context**

Persistent top header showing:

- Producer name
- Status (e.g., Active)
- Producer Number
- City/State
- Phone Number
- Email Address
- Back button to return to the Producer Inquiry experience

### 2. **Tabs Navigation**

Secondary nav bar with access to:

- Overview
- Banking Info (current)
- License & Contact Info
- Appointments
- Users
- Commissions
- Documents
- All Activity

### 3. **Banking & Info Section**

Two primary account panels:

### a. **E-Check Account**

Fields:

- Name of Account Holder
- Bank Name
- Bank Address (Street, City, State, ZIP)
- Bank Routing Number
- Bank Account Number
- E-Check Option (Yes/No)

### b. **Commission Account**

Fields:

- Name of Account Holder
- Bank Name
- Bank Address (Street, City, State, ZIP)
- Bank Routing Number
- Bank Account Number
- Commission Pay Method
    - The only option available in the dropdown when editing will be Deposits
- Process Commissions (Yes/No)

Each section:

- Is read-only by default
- Has an **Edit** button that opens inline or modal editing
- Allows Save/Cancel with validation

### 4. Page History

- This section acts as the audit history for this tab, reflecting any interactions with the page sections
- Each row in the table will be comprised of the following attributes:
    - Date and Time Stamp of when the interaction with the page occurred
    - The action, which may include:
        - Page Created
        - Page Viewed
        - Page Edited: [Section Name] (i.e. Insurance Details, Tax Details, Advanced Settings)
            - This will only include one section per row, as the user is not able to edit multiple sections at once
        - User
            - This will be the system username for this user

### 5. **Quick Info Sidebar (Right Panel)**

Persistent on the right side. 

---

## **C) HOW – Planning & Implementation**

---

## **D) User Experience (UX) & Flows**

### 1. **Viewing Banking Information**

- User lands on tab and sees:
    - E-Check Account
    - Commission Account
    - Page History
    - Quick Info Sidebar

### 2. **Editing a Banking Section**

1. User clicks **Edit**
2. Fields become editable inline or in a modal
3. User modifies data
4. User clicks **Save**
5. Validation checks run
6. If successful:
    - Section returns to read-only
    - Page History logs the change

### 3. **Viewing Page History**

- User scrolls to Page History
- Can view a chronological log:
    - When the page was created
    - Any edits made
    - By whom

### 4. **Quick Info Sidebar Use**

- Available across all tabs for context
- User can:
    - Update contact details
    - Edit addresses
    - Change marketing rep
- Changes update in real time without leaving the tab

## **E) Master Table Schemas**

# #4 - Producer Details: License & Contact Info Tab

## **A) WHY – Vision and Purpose**

The **License & Contact Info** tab serves as the central place to manage a producer's licensing and contact information. It ensures that all producer-related legal, regulatory, and operational contact data is:

- Up to date
- Easily accessible
- Editable by authorized users
- Logged for auditing

This functionality helps ensure producers are authorized to sell insurance products in relevant jurisdictions and remain compliant with state-specific regulations.

---

## **B) WHAT – Core Requirements**

### 1. **Contact Information Section**

- Displays list of contact entries for the producer
- Each contact includes:
    - Name
    - Title
    - Email
    - Primary Phone Number
    - Comments
- Users can:
    - **Add New Contact**
    - **Edit existing contact**

### 2. **Agent License Information**

- Each license entry includes:
    - Name
    - Producer SSN
    - License Number
    - Expiry Date
    - State License Type
    - National Producer Number
- Users can:
    - **Add Agent License**
    - **Edit existing license entries**

### 3. **Errors & Omissions (E&O) Coverage**

- Displays
    - Coverage Limit
    - Expiry Date
    - Attached documentation
    - Document name

### 4. **Page History**

- Table format showing:
    - Date & Time
    - Action (e.g., Contact Added, License Edited)
    - User who performed action

### 4. Page History

- This section acts as the audit history for this tab, reflecting any interactions with the page sections
- Each row in the table will be comprised of the following attributes:
    - Date and Time Stamp of when the interaction with the page occurred
    - The action, which may include:
        - Page Created
        - Page Viewed
        - Page Edited: [Section Name] (i.e. Insurance Details, Tax Details, Advanced Settings)
            - This will only include one section per row, as the user is not able to edit multiple sections at once
        - User
            - This will be the system username for this user

### 5. **Quick Info Sidebar (Right Column)**

Persistent module. 

---

## **C) HOW – Planning & Implementation**

---

## **D) User Experience (UX) & Flows**

### 1. **Viewing Contact Info**

- View one or more contact entries upon load of tab
- Contacts presented in cards with Edit buttons
- If no contact exists: show empty state with “Add Contact” CTA

### 2. **Adding a Contact**

1. Click **Add Contact**
2. Modal opens with input fields
3. User fills out required info
4. Click **Save**
5. Contact appears in list
6. Page History updated

### 3. **Editing a Contact**

- Click **Edit** → Modal opens pre-filled
- Make changes → Click **Save**
- Contact card updates + audit log entry created
- “Delete” removes contact after confirmation prompt

### 4. **Viewing & Managing Agent License**

- License cards are displayed similarly to contact cards
- “Edit” opens modal for changes
- “Add Agent License” opens blank form modal

### 5. **E&O Coverage**

- Presented as read-only view with:
    - Coverage Limit
    - Expiry Date
    - Thumbnail of uploaded document
        - Document can be viewed in the document viewer upon selection
    - Document name

## **E) Master Table Schemas**

# #5 - Producer Details: Appointments Tab

## **A) WHY – Vision and Purpose**

The **Appointments** tab is a critical control panel for assigning insurance programs to producers. A producer must be formally *appointed* to a specific program before they are allowed to quote or sell it. This functionality ensures:

- Legal and contractual compliance with carrier/program requirements
- Clear visibility into a producer's program participation
- An auditable record of all appointment changes

This feature directly supports business enablement and regulatory adherence.

---

## **B) WHAT – Core Requirements**

### 1. **View Existing Appointments**

- Appointments are grouped by Program Name (e.g., “ADG 6 Month”)
- Each appointment card includes:
    - Prefix
    - New Business status
    - Appointment Date
    - Termination Date
    - Appointment Fee and Fee Date
    - Appointment Expiry Date
    - Insurance Company
- A collapsible card format is used

### 2. **Add New Appointment**

- Accessed via the **“+ Add Program”** button
- Opens a side panel with the following fields:
    - Program (dropdown)
    - Insurance Carrier (auto-filled based on program)
    - Appointment Date (calendar input)
    - Termination Date (optional, calendar input)
    - Appointment Fee
        - This will be populated by the program manager if applicable
    - Appointment Fee Date (optional)
    - Appointment Expiry Date (optional)
    - Notes (optional)

### 3. **Edit Existing Appointment**

- Accessed by clicking the **Edit** button on a program card
- Side panel will open, reflecting the existing values populated
- The user can modify the details of the appoitment, and then **Save Changes**
    - All fields will be editable except Appointment Fee

### 4. Page History

- This section acts as the audit history for this tab, reflecting any interactions with the page sections
- Each row in the table will be comprised of the following attributes:
    - Date and Time Stamp of when the interaction with the page occurred
    - The action, which may include:
        - Page Created
        - Page Viewed
        - Page Edited: [Section Name] (i.e. Insurance Details, Tax Details, Advanced Settings)
            - This will only include one section per row, as the user is not able to edit multiple sections at once
        - User
            - This will be the system username for this user

---

## **C) HOW – Planning & Implementation**

### 

---

## **D) User Experience (UX) & Flows**

### 1. **Viewing Appointments**

- Producer visits the **Appointments** tab
- All current appointments are listed in collapsible cards
- Default: all cards expanded

### 2. **Adding an Appointment**

1. User clicks **“+ Add Program”**
2. Side panel opens with empty form
3. User selects program → carrier auto-fills
4. User completes required fields (Appointment Date)
    1. Error presents if user attempts to save without selecting the program and appointment date
5. Clicks **Save**
6. New card appears in appointment list
7. Page History updated with timestamped log

### 3. **Editing an Appointment**

1. User clicks **Edit** on an existing card
2. Side panel opens with pre-filled data
3. User modifies any editable field
4. Clicks **Save Changes**
5. Card updates in place
6. Page History updated

### **E) Master Table Schemas**

# #6 - Producer Details: Users Tab

## **A) WHY – Vision and Purpose**

The **Users** tab enables management of web credentials for producers. Each producer is assigned login credentials—typically a **Manager** and **Customer Service Representative (CSR)**—to access the Producer Portal. These credentials control access to specific features and data visibility in the portal.

The purpose of this feature is to:

- Allow system administrators to provision and manage user access.
- Ensure role-based permissions are enforced at the producer level.
- Provide a clear audit trail of changes to credentials.

---

## **B) WHAT – Core Requirements**

### 1. **User List Display**

- Table view of all active users associated with a producer.
- Columns include:
    - Web User ID
    - Producer Number
    - Group Access (e.g., Master)
    - Access Level (e.g., CSR, MGR)
    - Commission Report Access (checkbox)
    - Loss Ratio Access (checkbox)
    - Account Management (checkbox)
    - This table will scroll horizontally as required
- An alert will be presented if the user accounts have been suspended or terminated
    - If the producer’s profile status is suspended or terminated, the associated user accounts will be suspended or terminated accordingly, an alert will be shown in this tab to indicate to the user why they will no longer be able to login using the provided credentials

### 2. **Create New User**

- Show empty state initially prior to the first user for this Producer being created.
- Accessed via **"+ Add User"** button.
- Opens a flyout panel with fields:
    - Producer Number (pre-populated)
    - Login (pre-populated)
    - Email Address
    - Verify Email Address
    - New Password
    - Verify Password
    - Temporary Password Suggestion
        - This will be auto-generated each time the page loads
        - This can be provided to the user as a temporary password, so they can modify their password separately in the Producer Portal experience
    - Group Access (dropdown)
    - Access Level (dropdown)
    - Permissions (checkboxes):
        - Commission Report
        - Loss Ratio
        - Account Management

### 3. **Edit Existing User**

- Opens a flyout with:
    - Display:
        - Producer Number
        - Login
        - Email Address
        - Permissions
            - Group Access
            - Access Level
            - Permissions Checkboxes
    - Option to:
        - **Change Email**
        - **Reset/Change Password**

### 4. **Dialogs**

- **Change Email Dialog**
    - User will populate email address, and verify email address, before saving or cancelling to purge changes
- **Change Password Dialog**
    - User will populate new password, and verify password, before saving or cancelling to purge changes
    - Alternatively, they can use the temporary password suggestion and provide this to the user to login to the Producer Portal where they can then change the password themselves

### 5. Page History

- This section acts as the audit history for this tab, reflecting any interactions with the page sections
- Each row in the table will be comprised of the following attributes:
    - Date and Time Stamp of when the interaction with the page occurred
    - The action, which may include:
        - Page Created
        - Page Viewed
        - Page Edited: [Section Name] (i.e. Insurance Details, Tax Details, Advanced Settings)
            - This will only include one section per row, as the user is not able to edit multiple sections at once
        - User
            - This will be the system username for this user

---

## **C) HOW – Planning & Implementation**

---

## **D) User Experience (UX) & Flows**

### 1. **Viewing Users**

- User navigates to **Users** tab
- Table shows current users for this producer
- Columns are sortable by selecting the appropriate header column
    - Sorting will be indicated by the downwards arrow, indicating which column the table is sorted by
- Quick Info remains visible in right sidebar

### 2. **Adding a New User**

1. Click **"+ Add User"**
2. Fill in all required fields in flyout
3. Select permissions
4. Click **Save**
5. User added to table; audit log updated

### 3. **Editing an Existing User**

1. Click on a user row or "Edit"
2. Modify email, password, group access, or permissions in the flyout
3. Confirm changes
4. Updates reflected in table and audit log

## **E) Master Table Schemas**

# #7 - Producer Details: Commissions Tab

## **A) WHY – Vision and Purpose**

The **Commissions tab** is designed to manage and track a producer’s compensation for selling insurance programs. This section is essential for:

- Assigning commission structures based on appointment status.
- Ensuring accurate payout rates for different transaction types.
- Maintaining an audit history of commission payments for financial transparency and compliance.

This ensures producers are fairly compensated, appointments are financially governed, and support/admin teams can view and update commission-related data effectively.

---

## **B) WHAT – Core Requirements**

### 1. **Commission Type Display**

- A list of commission types currently assigned to the producer, each entry includes:
    - **Program**
    - **Transaction Type** (e.g., New Business, Renewals)
    - **Paid On** (e.g., Collected)
    - **Rate** (e.g., 17.00%)
    - The table will be sortable by selecting the column header; the downward arrow will indicate which column it is sorted by

### 2. **Add Commission Type**

- Available only **if a program appointment exists**.
- Fields required:
    - Program (dropdown)
    - Paid On (dropdown: Collected, Earned, Written)
    - Transaction Type (dropdown: New Business, Renewal)
    - Rate (dropdown: % input, which will be populated by the Program Manager)

### 3. **Guardrail if No Appointment Exists**

- If user tries to add a commission but the producer is not yet appointed to a program:
    - Prevents access to commission form.
    - Displays an inline warning and a CTA: **"Go to Appointments"**.

### 4. **Commission History Table**

- Paginated log of all commissions issued to the producer.
- Each row shows:
    - Entry Date
    - Type (e.g., Monthly Commissions)
    - Amount
    - Comments (e.g., “ACH #001234 to Account #001234567”)
    - Last User
    - Last Date

### 5. **Agent Commission Details**

- View mode showing details of a particular commission payment:
    - Producer Number
    - Type
    - Date
    - Time
    - Comments
    - Collected Premium
    - Commission Paid
    - Date Commission Paid

### 6. **Add Adjustment**

- Allows manual override of a commission payout.
- Fields:
    - Entry Date
    - Entry Amount
    - Comments
    - Ending amount auto-calculated/displayed
- Upon ‘Add’, this adjustment will be added to the Commission History

### 7. Page History

- This section acts as the audit history for this tab, reflecting any interactions with the page sections
- Each row in the table will be comprised of the following attributes:
    - Date and Time Stamp of when the interaction with the page occurred
    - The action, which may include:
        - Page Created
        - Page Viewed
        - Page Edited: [Section Name] (i.e. Commission Types, Commission History)
            - This will only include one section per row, as the user is not able to edit multiple sections at once
        - User
            - This will be the system username for this user

---

## **C) HOW – Planning & Implementation**

### 

---

## **D) User Experience (UX) & Flows**

### 1. **View Assigned Commission Types**

- User lands on the Commissions tab.
- Top section displays a list of assigned commission types.
- Bottom section displays historical payouts.

### 2. **Add a New Commission Type**

1. Click **"+ Add Commission"**
2. If appointment exists:
    - Side panel opens with form
    - User selects Program, Paid On, Transaction Type, and Rate
    - Click **Save**
3. If appointment does **not** exist:
    - Side panel shows warning with **“Go to Appointments”** button

### 3. **Review Commission History**

- Scroll down to Commission History section.
- View rows with full audit metadata.

### 4. **View Agent Commission Detail**

- Click into any commission row
- Opens flyout with complete agent and commission data

### 5. **Add Adjustment**

1. Click **“Add Adjustment”**
2. Fill Entry Date, Amount, and Comment
3. See **Ending Amount** calculated dynamically
4. Click **Add**

# #8 - Producer Details: Documents Tab

## **A) WHY – Vision and Purpose**

The **Documents** tab provides a centralized, structured way to manage files associated with a producer's profile. Its purpose is to:

- Enable uploading, organizing, and accessing critical documents (e.g., forms, agreements, commission statements).
- Streamline review and auditing with proper file tagging and history.
- Support document merging and processing for compliance and internal workflows.

This tab supports operational efficiency, audit readiness, and a more unified producer file experience.

---

## **B) WHAT – Core Requirements**

### 1. **Upload Documents**

- Users can upload multiple documents at once.
- Each document must be associated with:
    - **Producer Number** (auto-filled)
    - **Original Document Date**
    - **Description** (dropdown)
        - Producer Commission Deposit Authorization Form
        - Producer Contract
        - Producer E and O
        - Producer EFT Form
        - Producer License
        - Producer W-9 Form
    - **Assigned To** (dropdown of users in the system)
- Optional: checkbox for **“Mark as Processed”**
    - If marked as processed, the document will not be assigned to a queue to be worked by another user
- Uploading state will be presented
- Once complete, the modal will close and the user will remain on the Documents tab

### 2. **Document Listing Table**

- Displays all documents associated with the producer.
- Columns:
    - Checkbox (for multi-select)
    - File Name (clickable for viewing)
    - Date Added
    - Added By (user name)

### 3. **Document Viewer**

- Opens in the document viewer.
- Shows PDF preview with controls (zoom, download, etc.)
- Right panel: **File Details** editable metadata:
    - File Name
    - Date Received
    - Description
    - Assigned to
    - Producer Number
    - CTA: Mark as Processed
    - The user can also view the document history, as previously implemented

### 4. **Merge Documents**

- User can select multiple files and click **“Merge Files”**
- Prompt asks for new file name
- New merged file is added to document list
- Confirmation toast on success

### 5. **Delete Documents**

- Multiple selection and deletion supported
- Confirmation modal appears before deletion

### 6. **Upload Progress**

- Upload dialog displays visual upload progress
- Individual file success or error indicators
- Uploaded files appear immediately in the list

---

## **C) HOW – Planning & Implementation**

### 

---

## **D) User Experience (UX) & Flows**

### 1. **Upload Document(s)**

1. Click **Upload Document(s)**
2. Select files from computer 
3. Fill metadata (description, original document date, assign to)
4. Click **Upload Docs**
5. Files upload, status indicators shown
6. Files appear in the list with entered metadata

### 2. **View and Edit Document**

1. Click file name in list
2. Viewer opens in document viewer
3. Right panel shows editable metadata
4. Change details if needed, and click **“Mark as Processed”**
5. Close viewer

### 3. **Merge Files**

1. Multi-select 2+ files using checkboxes
2. Click **“Merge Files”**
3. Enter merged file name in modal
4. Click **Merge Files**
5. Confirmation shown and new file appears in list

### 4. **Delete Files**

1. Multi-select files
2. Click **Delete**
3. Confirm in modal
4. Files are removed and page refreshes with updated list

### 5. **Upload Status Flow**

- **Uploading:** Progress bar visible
- **Success:** Green checkmarks on each file
- **Failure:** Red X with option to retry or remove

# #9 - Producer Details: All Activity Tab

# #10 - Producer Suspension Workflow

## **A) WHY – Vision and Purpose**

The **Suspend Producer** feature allows platform administrators to temporarily deactivate a producer profile without fully terminating their account. This is useful in scenarios such as:

- Compliance issues or investigations
- Incomplete or expired licensing or E&O insurance
- Business inactivity or violations

**Lifting a suspension** reinstates the producer’s ability to quote, sell, and manage business. This feature ensures that access and privileges are managed cleanly and safely without loss of history.

---

## **B) WHAT – Core Requirements**

### 1. **Suspend Producer**

- Accessible via **Actions → Suspend Producer**
- User must enter:
    - **Suspension Date** (date picker)
    - **Reason for Suspension** (dropdown)
- A secondary **confirmation modal** alerts:
    
    > “This producer profile will be suspended on [DATE]. They will no longer be able to bind business, and all associated policies will need to be reassigned.”
    > 
- After confirmation:
    - Suspension is saved
    - Status badge updates to **“Suspended”**
    - Overview displays an alert:
        
        *“This producer was suspended on [DATE] due to [reason].”*
        
    - All downstream systems should enforce the suspension (e.g., disable quoting/selling)

---

### 2. **Lift Suspension**

- Accessed via **Lift Suspension** button in Overview tab (visible only when profile is suspended)
- User must enter:
    - **Reason for lifting suspension** (dropdown)
- Upon confirmation:
    - Status badge updates back to **“Active”**
    - Overview alert is removed
    - Success toast appears:
        
        *“Producer’s suspension has been lifted”*
        

---

### 3. **Audit Trail**

- All actions logged in the **Page History**:
    - Action: “Producer Suspended” / “Suspension Lifted”
    - Timestamp
    - User

---

## **C) HOW – Planning & Implementation**

### 

---

## **D) User Experience (UX) & Flows**

### **1. Suspension Flow**

1. User clicks **Actions → Suspend Producer**
2. Modal appears:
    - Select Suspension Date
    - Input Reason
    - Click **Suspend Producer**
3. Confirmation dialog appears:
    - “Are you sure?” with reminder of the consequence
    - Click **Yes, Continue**
4. Producer status updates to **Suspended**
5. Suspension alert banner appears on Overview
6. **Lift Suspension** button becomes visible

### **2. Lift Suspension Flow**

1. User clicks **Lift Suspension**
2. Modal appears with text field for Reason
3. User submits → Status changes to **Active**
4. Overview page alert is removed
5. Toast appears: *“Producer’s suspension has been lifted”*

### **3. System-wide Impact**

- Prevent new policy creation by this producer
- All tabs remain visible, but interactions are read-only where appropriate

# #11 - Producer Termination Workflow

## **A) WHY – Vision and Purpose**

The **Termination** workflow allows administrators to permanently deactivate a producer’s ability to conduct business within the system. This action is typically taken when:

- A producer exits the program entirely
- A licensing or compliance issue renders them ineligible
- The producer business is no longer operational or contracted

**Reinstatement** exists to reverse terminations that may have been done in error or due to corrected conditions, restoring the producer’s active status and system access.

This functionality ensures clean cutoffs in quoting, selling, and access, while preserving the producer’s record and history for audit purposes.

---

## **B) WHAT – Core Requirements**

### 1. **Terminate Producer**

- **Access Point**: Via `Actions → Terminate Producer`
- **User must input**:
    - **Termination Date** (calendar picker)
    - **Termination Reason** (dropdown)
- **Confirmation modal** before finalizing:
    
    > “This producer profile will be terminated on [DATE]. They will no longer be able to bind business, and all associated policies will need to be reassigned.”
    > 
- Upon confirmation:
    - Producer status updates to **Terminated**
    - Red **Terminated** status badge displayed next to name
    - Overview tab shows alert:
        
        *“This producer was terminated on [DATE] due to [reason].”*
        
    - **Reinstate Producer** button appears in Overview tab

---

### 2. **Reinstate Producer**

- **Access Point**: Only visible in Overview when producer is terminated
- **User must input**:
    - **Reason for reinstatement** (dropdown)
- Upon confirmation:
    - Producer status updates back to **Active**
    - Termination alert is removed
    - Green success toast:
        
        *“Producer has been reinstated”*
        

---

### 3. **System Effects**

- When **Terminated**:
    - Producer cannot:
        - Quote or sell policies
        - Be appointed to new programs
        - Be paid commissions
        - Log into the Producer Portal
    - All existing appointments and commission types should be locked
- When **Reinstated**:
    - Existing configuration is retained
    - System-level restrictions are lifted
    - Appointments, users, documents, etc. remain viewable

---

## **C) HOW – Planning & Implementation**

### 

---

## **D) User Experience (UX) & Flows**

### **1. Termination Flow**

1. User opens `Actions → Terminate Producer`
2. Modal appears prompting for:
    - Termination Date
    - Reason
3. Upon clicking **Terminate Producer**, confirmation modal appears
4. Click **Yes, Continue**
5. UI updates:
    - Badge changes to **Terminated**
    - Alert appears in Overview tab
    - `Reinstate Producer` button is shown

---

### **2. Reinstatement Flow**

1. User clicks **Reinstate Producer** from Overview tab
2. Modal prompts for reinstatement reason
3. On confirmation:
    - Producer status returns to **Active**
    - Alert and `Reinstate` button disappear
    - Toast appears: “Producer has been reinstated”

---

# #12 - Notes Side Panel

# #13 - Change Producer Number Workflow

## **A) WHY – Vision and Purpose**

In certain business scenarios such as mergers, acquisitions, or restructurings, a producer may need to have their **agent (producer) number updated**. This action ensures all **new business is credited to the correct entity** going forward.

This workflow:

- Provides a controlled and auditable way to reassign producer identifiers.
- Ensures that the **new agent number** becomes the reference point for **future transactions**.
- Preserves historical activity while clearly documenting the reassignment.

---

## **B) WHAT – Core Requirements**

### 1. **Accessing the Function**

- Users access this function via the **Actions menu** on the Producer Details page, which is persistently available throughout the Details experience.
- Option: **“Change Agent Number”**

### 2. **Change Agent Number Modal**

- Fields:
    - **Old Agent Number** (auto-filled with current agent number)
    - **New Agent Number** (dropdown list)
- Buttons:
    - Cancel
    - **Submit Change**

### 3. **Confirmation Modal**

- Modal warns:
    
    **“Are you sure? By making this change, all future business will be written against the new producer number.”**
    
- Options:
    - Cancel
    - **Yes, Continue**

### 4. **Impact Scope**

- All **future quoting, policy writing, commissions, reporting, and logins** should reference the new agent number.
- Past data should remain tied to the old agent number, but visually traceable from this profile.

### 5. **Page History**

- Record the agent number change with:
    - Timestamp
    - User who made the change
    - Description of the action (e.g., “Changed Agent Number: 000001 → 000099”)

---

## **C) HOW – Planning & Implementation**

### 

---

## **D) User Experience (UX) & Flows**

### 1. **Change Flow**

1. User clicks **Actions > Change Agent Number**
2. Modal opens with Old Agent Number (auto-filled) and New Agent Number dropdown
3. User selects a valid new number and clicks **Submit Change**
4. A second modal opens:
    
    “Are you sure? All future business will be written against the new producer number.”
    
5. User clicks **Yes, Continue**
6. System updates the profile and shows a success toast
7. Page refreshes with updated agent number in the header
8. Page History updates with the change event

### 2. **Failure Scenarios**

- If system error occurs:
    
    → Show alert with: “Something went wrong. Please try again or contact support.”