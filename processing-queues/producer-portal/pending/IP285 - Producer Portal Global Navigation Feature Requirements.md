# IP285 - Producer Portal Global Navigation Feature Requirements

# #1 - Search Field

## **A) WHY - Vision and Purpose**

The goal of this global search experience is to empower producers to rapidly locate and access specific policy or quote records across the platform. Instead of navigating manually, users can type a policyholder name, policy number, or related keyword and instantly surface the relevant record. This improves efficiency, reduces friction in high-volume workflows, and aligns with modern usability standards for enterprise tools.

---

## **B) WHAT - Core Requirements**

### 1. **Search Entry Point**

- A **search bar** is present in the **global header** (side navigation)
- Can be activated via clicking the search bar

### 2. **Search Modal/Dialog**

- Opens an overlay modal with:
    - Input field for query
    - Loading state while fetching results
    - Dynamic dropdown of results as user types

### 3. **Search Result Types**

- Results returned in a simple list format
- Supported search types:
    - Policy number
    - Insured Name
    - Insured Email
    - Insured Phone Number
    - Insured Drivers License Number
    - VIN

### 4. **Interaction States**

- **Initial State**: Placeholder text suggests what the user can search (e.g., “Search for a policy…”)
- **Typing State**: Query string is processed after 3 characters or debounce timeout (300–500ms)
- **Loading State**: Spinner while results are being fetched
- **Success State**: List of results matching input string
- **No Results**: Message when no matches are found
- **Error State**: Message when the search fails due to system error

### 5. **Search Result Behavior**

- Clicking a result will navigate to the corresponding policy detail page
- Each result displays:
    - Insured Name
    - Policy or Quote Indicator
    - Policy Number
    - Effective Date

---

## **C) HOW - Planning & Implementation**

---

## **D) User Experience (UX) & Flows**

### 1. **Global Search Flow**

1. User clicks on the search bar or triggers via shortcut
2. Modal overlay opens with input field
3. User starts typing (e.g., "Smith" or "ABC123")
4. After 3 characters, results are fetched and displayed
5. The query is overlaid on the search results to show the match between the characters queried and the information returned in the results, using a green highlight
6. User selects a result → navigates to policy overview
7. User selects ‘View All Results’ → navigates to the full list of search results 

### 2. **Edge Cases**

- **Empty Input**: No action until minimum characters are entered
- **Loading**: Spinner shown after typing before results return
- **No Matches**: Message like “No policies found for ‘Smith’”
- **Backend Error**: Message like “Something went wrong. Try again.”
- **Fuzzy Search:** Show related results based on fuzzy search matching

### 3. **Visual & Accessibility Notes**

- Keyboard navigation support:
    - Use arrows to navigate between results
    - Enter to select
- Close modal with Esc key or click outside
- Loading and error states must be screen-reader accessible

# #2 - Search Results

## **A) WHY - Vision and Purpose**

The goal of this interface is to **deliver a rich, actionable search results page** that supports multiple types of user queries (by name, policy number, email, partial text, etc.), enhances discoverability through fuzzy logic, and provides efficient tools for **sorting and filtering**. These features ensure that producers can quickly access and evaluate relevant policies or quotes across various search methods.

This is a continuation of the **global search** functionality and acts as the second step after entering a query when the user opts to view all search results.

---

## **B) WHAT - Core Requirements**

### 1. **Search Results Page**

- Shows after a query is entered from the global search bar, results are returned, and the user chooses to view all results
- Includes:
    - Query confirmation (e.g., “Search results for ‘Jane Smith’”)
    - Count of results (if applicable)
    - Display of key fields for each result

### 2. **Supported Search Inputs**

- **Exact Match**
- **Partial Match**
- **Fuzzy Match**
    - Misspelled names or variations (e.g., “Smth” → “Smith”)
    - Shows “Did you mean?” prompt with corrected results

### 3. **Sort and Filter Capabilities**

- Filter By:
    - Policy or Quote Status
    - Effective Date
    - Inception Date
- Sort by:
    - All column headings
- UI includes:
    - Dropdown for filter options
    - Calendar picker for date-based sorting

### 4. **Search Result Items**

Each result should display:

- Policy Number or Quote Indicator
- Insured Name
- Policy Status (colored indicator tags)
- Type
- Effective Date
- Insured Phone Number
- Insured Email (if searched via email)

### 5. **Behavior**

- Click on a result opens a summary view in a side panel from the right of the screen
- The side panel will include the following information:
    - Policy Number, which will link the user to the full policy
    - Policy Effective Date
    - Policy Status
    - Primary Phone Number
    - Alternate Phone Number (if applicable)
    - Email Address
    - Communication Preference
    - Address
    - Vehicles, with the following information per vehicle
        - Vehicle Number on the policy
        - Year
        - Make
        - Model
        - VIN
    - Drivers, with the following information per driver
        - Driver number on the policy
        - Driver Name
        - Included or Excluded Status
        - Date of Birth
        - Identification Number
    - Coverage, including:
        - Policy Wide Coverages
            - Coverage Line
            - Coverage Limit
        - Vehicle Specific Coverages
            - Coverage Line
            - Coverage Limit

---

## **C) HOW - Planning & Implementation**

---

## **D) User Experience (UX) & Flows**

### 1. **Flow: Direct Search**

1. User searches “AB12345678” → exact match found
2. User chooses to ‘View All Results’
3. User selects appropriate result from search results, side panel summary opens
4. User clicks to navigate to full policy page

### 2. **Flow: Partial or Fuzzy Match**

1. User searches “Smth”
2. UI shows message: “Did you mean ‘Smith’?”
3. Results populate below suggestion
4. User chooses to ‘View All Results’
5. User selects appropriate result from search results, side panel summary opens
6. User clicks to navigate to full policy page

### 3. **Flow: Filtering & Sorting**

1. User applies the Policy Status, Effective Date, and/or Inception Date filter
2. Results are reduced based on the filter applied
3. User clicks on column heading to sort by that field 
4. Results reorganize based on sorting option selected

### 4. **Empty or Error States**

- If no results:
    - Message: “No results found for ‘xyz’”
    - Suggest alternate query or spelling
- If system error:
    - “Something went wrong. Please try again later.”

---

## **Visual & Accessibility Notes**

- Highlight matching terms in results (e.g., green highlight)
- Use contrasting tags for policy statuses
- Keyboard navigation support:
    - Tab through rows
    - Enter to select result
- Screen-reader support for:
    - Results count
    - Sort option labels
    - “Did you mean” prompts

# #3 - Global Navigation

## **A) WHY - Vision and Purpose**

The purpose of the global navigation is to be persistently available throughout the experience, allowing the user to navigate to key sections within the platform as needed. 

## **B) WHAT - Core Requirements**

**Expanded vs. Collapsed State**

The user can click on the border of the global navigation to collapse the view, showing the icons and names of the individual sections. They can click on the border of the global navigation to expand it again as needed. The global navigation will default to the expanded state. 

**Navigation Paths** 

The user can navigate to the following locations from the global navigation: 

- Alerts
- Home (IP268 - Dashboard (Producer Portal): Feature Requirements)
- Quotes (IP269 - Quotes Feature Requirements)
- Policies (IP270 - Policies Feature Requirements)
- Reports (IP271 - Reports: Feature Requirements)
- Resources (IP272 - Resources: Feature Requirements)
- Account Management (IP273 - Account Management: Feature Requirements)
    - The user can access the account management experience by clicking on the Producer Username in the bottom left corner (e.g. 500127-MGR)
    - Upon selection of the username, the user will have the following additional options, which will shortcut them to the appropriate tab in the Account Management screens:
        - Contact Info
        - Profile
        - Digital Signatures
        - Roles
        - Producers
        - Documents
        - Log Out
        - These options become a part of the side navigation on mobile, removing the secondary menu user flow
- Contact Us (External Link)
- Privacy Policy (External Link)

## **C) HOW - Planning & Implementation**

# #4 - Alerts

## **A) WHY - Vision and Purpose**

The Alerts experience is designed to **proactively notify users** (producers/agents) about **important account actions** that require their attention, such as expiring licenses, missing documents, or pending tasks.

It provides:

- Immediate visibility into urgent issues via the dashboard.
- A central place to review, manage, and resolve outstanding alerts.
- Direct navigation to specific actions needed to clear each alert.

The goal is to **reduce user oversight** and **increase operational efficiency** by highlighting time-sensitive activities directly in their workflow.

---

## **B) WHAT - Core Requirements**

### 1. **Dashboard Alerts Banner**

- **Single Alert Mode**:
    - If there is exactly one open alert, display a single banner.
    - Banner shows short alert message and Update button.
- **Multiple Alerts Mode**:
    - If there are multiple open alerts, display a generic banner:
        - "You have X important tasks that need your attention."
        - **Review Now** button that directs to the Alerts center.

### 2. **Alerts Center (Navigation > Alerts)**

- Dedicated "Alerts" page in global nav
- List of active alerts with:
    - Alert title
    - Short description
    - Status indicator (e.g., New, In Progress, Resolved)
    - Timestamp
- Alerts will be listed in descending order, with the most recent alert at the top of the screen based on the timestamp
- Each alert must have a clear "Resolve" action that links to the relevant part of the platform (e.g., Licensing, Payments, Documents).

### 3. **Document-Related Alerts**

- Specific document alerts (e.g., missing uploads) must:
    - Display both in Alerts center and in the **Documents** section.
    - Highlight the required documents with status "Action Required."

### 4. **Alert Management**

- Alert can be:
    - **Resolved**: Alert disappears from active alerts.
    - **Dismissed** (if allowed by type): Alert removed without resolution (optional feature).
- System must track when an alert is resolved/dismissed for audit purposes.

### 5. **Empty State**

- When there are no active alerts:
    - Display friendly empty state (illustration + "No new alerts").
    - No error or loading message.

---

## **C) HOW - Planning & Implementation**

---

## **D) User Experience (UX) & Flows**

### 1. **Dashboard Single Alert Flow**

1. User logs in
2. Sees **single alert** banner on dashboard
3. Clicks **Resolve**
4. Redirected to the relevant action page
5. Completes action
6. Alert removed automatically

### 2. **Dashboard Multiple Alerts Flow**

1. User logs in
2. Sees **multiple alerts** banner
3. Clicks **Review Alerts**
4. Directed to Alerts page
5. Selects alert → clicks **Resolve** → navigates to appropriate page

### 3. **Alerts Center Flow**

1. User opens navigation → selects **Alerts**
2. Views all active alerts
3. Clicks an alert to resolve
4. Action page loads
5. Completing task clears the alert from the list

### 4. **Empty State Flow**

- No active alerts:
    - Dashboard shows no banner
    - Alerts page shows empty illustration and message: "You're all caught up!"

---

## **Visual & Accessibility Notes**

- Dashboard banners must be **high-contrast** (e.g., red for critical alerts).
- Alerts in list must have:
    - Clear hierarchy (title > detail)
    - Timestamp (date issued)
- Buttons labeled appropriately ("Resolve", "View Details").
- Screen reader labels for all interactive elements.