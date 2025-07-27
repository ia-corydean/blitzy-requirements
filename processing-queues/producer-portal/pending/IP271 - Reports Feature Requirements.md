# IP271 - Reports: Feature Requirements

# #1: Producer Performance Report

## **A) WHY - Vision and Purpose**

The **Producer Performance Reports** feature provides users with insights into **policy performance metrics**, allowing producers and administrators to track key business indicators such as new business, renewals, and endorsements. The goal is to **enhance decision-making and productivity** by offering a **clear, structured, and interactive** reporting system.

## **B) WHAT - Core Requirements**

1. **Report Dashboard & Summary View**
    - Display key metrics, including:
        - **New Business** (Policies issued within a set period).
        - **Renewals** (Policies successfully renewed).
        - **Endorsements** (Policies that have been modified).
        - **Expiring Policies** (Policies nearing expiration).
        - **Non-Renewals** (Policies that will not be renewed).
        - **Non-Pay Cancellation Notices** (Number of cancellation notices in the case where an Insured has not paid).
        - **Cash Payments** (Payments made by customers).
        - For each metric, the following is included:
            - Date
            - Number of Policies
            - Dollar Value per Date
2. **Report Export & Download**
    - Users can export reports in **PDF and CSV formats**.
    - Provide an **option to customize** which sections to include in the report.
3. **Loading & Status Updates**
    - Show a **loading screen** when reports are being generated.
    - Display an **error message** if the report cannot be presented.

## **C) HOW - Planning & Implementation**

## **D) User Experience (UX) & Flows**

### **1. Viewing Reports**

- Users navigate to **Producer Performance Reports** via the sidebar.
- Default view shows a **summary of key metrics**.

### **2. Modifying Reports**

- User navigates to the sections filter
- They can select checkboxes to chose which sections to present in the report
- Upon selecting “See Report”, the report will reload to reflect the chosen sections

### **3. Exporting Reports**

- User clicks **“Export Report”**.
- The user will have the option to Export by PDF or CSV, starting the download process

### **4. Report Processing & Loading**

- While the report generates, a **loading screen** is displayed.

## **E) Master Schema Tables**

# #2: Cancellations Report

## **A) WHY - Vision and Purpose**

The **Cancellations Report** provides a **centralized view** of all policy cancellations, including **policyholder details, policy status,** and **cancellation date**. This feature allows producers to **track trends, identify risks, and take proactive measures** to retain customers or address compliance requirements.

## **B) WHAT - Core Requirements**

1. **Report Filtering & Search**
    - Filters available:
        - **Cancellation Reasons**
        - **Search by Date (Cancellation Date or Expiration Date)**
        - **Date Range**
        - **Office Selection** (All Offices or specific offices)
    - Users must select their filters before generating reports.
2. **Cancellations Report Overview**
    - A dashboard displaying a list of canceled policies.
    - Key details include:
        - **Policy Number**
        - **Policyholder Name**
        - **Policy Status** (e.g. Cancelled - Non-Pay, Pending Cancellation, etc.)
        - **Payment Due Date**
        - **Cancellation Date**
        - **Amount Due**
3. **Cancellation Details View**
    - Clicking on a policy opens **detailed cancellation information** in a side panel fly-out.
    - Includes **contact details of the policyholder** for follow-ups.
    - Option to **make a payment** for outstanding payments.
4. **Report Generation & Export**
    - Ability to **generate reports in PDF or CSV format**.

## **C) HOW - Planning & Implementation**

## **D) User Experience (UX) & Flows**

### **1. Viewing Cancellation Reports**

- Users navigate to **Reports → Cancellations** in the sidebar.
- User will be presented with the filter screen, to apply their selections.
- Report will be generated based on selections.
- Clicking on a policy number expands **detailed view**.

### **2. Filtering & Searching**

- Users apply **filters** based on cancellation type, date, or office.
- The report updates **instantly** based on the selected filters.
- Users can sort by clicking on the heading of the report columns.
- Filters are presented across the top of the report, below the report title, and can be modified by selecting the “Edit” button.

### **3. Viewing Cancellation Details**

- Clicking a row opens **detailed policy information**.
- Users can view **customer contact details**..

### **4. Exporting Reports**

- Users can select “Download” to see options for exporting as CSV or PDF.

## **E) Master Table Schemas**

# #3: Non-Renewals Report

## **A) WHY - Vision and Purpose**

The **Non-Renewals Report** provides a **comprehensive view of policies that will not be renewed**, helping producers and administrators track **potential client losses, understand reasons for non-renewals, and take proactive steps** to retain customers where possible. This feature ensures transparency in policy lifecycle management and supports decision-making for improving customer retention.

## **B) WHAT - Core Requirements**

1. **Report Filtering & Search**
    - Filters available:
        - **Date Range Selection** (Start Date, End Date).
        - **Included Categories** (e.g., Printed Non-Renewals).
        - **Office Selection** (All Offices or specific offices).
    - Users must select filter options before generating reports.
2. **Non-Renewals Report Overview**
    - Displays a **list of policies marked as non-renewing** based on the filters provided.
    - Key details include:
        - **Policy Number**
        - **Insured Name**
        - **Non-Renewal Date**
        - **Print Date**
        - **Message** (details as to why the policy has been set to non-renew)
3. **Report Generation & Export**
    - Users can generate **non-renewals reports in PDF or CSV format**.

## **C) HOW - Planning & Implementation**

### 

## **D) User Experience (UX) & Flows**

### **1. Viewing Non-Renewals Reports**

- Users navigate to **Reports → Non-Renewals** in the sidebar.
- Users apply **filters** based on date range, category, or office.
- Generate report to show data based on filters applied.

### **2. Filtering & Searching**

- Users apply **filters** based on date range, category, or office.
- The report updates **instantly** based on selected filters.
- Users can sort by clicking on the heading of the report columns.
- Filters are presented across the top of the report, below the report title, and can be modified by selecting the “Edit” button.

### **4. Exporting Reports**

- Users select “Download” for options to export as CSV or PDF.

## **E) Master Table Schemas**

# #4: Policy Suspenses Report

## **A) WHY - Vision and Purpose**

The **Policy Suspenses Report** provides insights into suspenses that must be addressed. Suspenses are an ‘action item’ requiring action from a producer to resolve. This report helps to identify actions to be taken, to ensure they are resolved in a timely fashion, reducing the risk of policy lapses. 

## **B) WHAT - Core Requirements**

1. **Report Filtering & Search**
    - Filters available:
        - **Date Range Selection** (Start Date, End Date).
        - **Show Processed** (Yes or No)
    - Search functionality allows users to look up policies by **policy number**
    - Filters or search criteria must be applied before generating the report.
2. **Policy Suspenses Report Overview**
    - Displays a **list of policies currently with an active suspense**
    - Key details include:
        - **Policy Number**
        - **Insured Name**
        - **Status**
        - **Producer Number**
        - **Due Date**
        - **Message**
        - **Open or Submit Button**
3. **Policy Suspense Details View**
    - Clicking on a policy opens a **detailed suspense flyout panel** showing:
        - Policy Number
        - Due Date
        - Insured Name
        - Producer Number
        - Details on what must be addressed in the suspense, which could include any combination of:
            - Notes
            - Documents to be uploaded
            - Photos to be uploaded
            - CTAs to collect signature, or resend digital link, in the case of suspenses open for documents needing to be signed
4. **Report Generation & Export**
    - Users can generate **policy suspense reports in PDF or CSV format**.
5. **Suspense Resolution Workflow**
    - Users can update suspense status directly from the report.
    - Attachments can be uploaded to resolve suspense cases.
    - Confirmation modal before closing a suspense item.

## **C) HOW - Planning & Implementation**

### 

## **D) User Experience (UX) & Flows**

### **1. Viewing Policy Suspenses Report**

- Users navigate to **Reports → Policy Suspenses** in the sidebar.
- The user will input the appropriate information in the filter section before generating the report.
- Clicking on a policy opens the **suspense flyout panel where the user can take remediating action on the suspense.**

### **2. Filtering & Searching**

- Users apply **filters** to find specific suspenses.
- The report updates based on selected filters when generated again.

### **3. Viewing & Managing Suspense Details**

- Clicking a row opens the **detailed suspense flyout panel**.
- Users can view **status, required actions, and supporting documents**.
- They can **upload new documents** or **update suspense status**.

### **4. Resolving Suspense Cases**

- Users click **“Resolve Suspense”** and select a resolution reason.
- A **confirmation modal** appears before finalizing the action.

### **5. Suspenses Requiring Signatures**

- If a suspense requires a signature, the ‘Collect Signature’ and ‘Resend Digital Link’ CTAs will be available
    - Select ‘Collect Signature’
        - User will be presented with Sign Documentation modal, with ‘Sign in Person’ selected
            - The user will present the screen to the Insured, where they will adopt their signature and complete signing of the documents
            - The Insured will be presented with a success modal indicating the action is complete
            - The user may download a copy of the PDF, or select close, dismissing the modal
            - The suspense will be automatically closed upon completion
        - Note: this is a delta of `IP269 - Quotes: Bind - Step 3 & 4: Sign Documents In Person & Make Payment` with UI modifications
    - Select ‘Resend Digital Link’
        - User will be presented with Sign Documentation modal, with ‘Sign Remotely’ selected
            - The user will be able to select the language the message will be sent in, as well as to send it by email, SMS, or both
            - The user can preview the message by selecting the preview CTA
            - An email and/or SMS will be sent to the Insured based on the user’s selection, with a link to sign the document
            - The user will enter their birthdate to access the portal, prior to adopting their signature, and proceeding to sign the document
            - Upon completion, the user will be shown a success state
                - Download Copy (PDF) will generate a download of the signed form
            - The suspense will be automatically closed upon completion
        - Note: this is a delta of `IP269 - Quotes: Bind - Step 3 & 4: Sign Remotely & Make Payment` with UI modifications

### **6. Exporting Reports**

- The report can be exported in PDF or CSV.

## **E) Master Table Schemas**

# #5: Requotable Policies Report

## **A) WHY - Vision and Purpose**

The **Requotable Policies Report** provides visibility into policies that are eligible for requoting. This feature enables **insurance producers and administrators** to efficiently manage policy renewals, improve customer retention, and maximize revenue opportunities.

## **B) WHAT - Core Requirements**

1. **Requotable Policies Report Overview**
    - Displays a **list of policies eligible for requoting**.
    - Key details include:
        - **Policy Number**
        - **Insured Name**
        - **Cancellation Date**
2. **Report Filtering & Search**
    - Filters available:
        - **Office Selection** (All Offices or Specific Office).
3. **Policy Details View**
    - Clicking on a policy opens a **details flyout panel** showing:
        - **Policyholder contact information**
        - **Cancellation Date**
        - **Policy Number, with link to policy**
4. **Report Generation & Export**
    - Users can generate **Requotable Policies reports in PDF or CSV format**.

## **C) HOW - Planning & Implementation**

## **D) User Experience (UX) & Flows**

### **1. Viewing Requotable Policies Report**

- Users navigate to **Reports → Requotable Policies** in the sidebar.
- The default view shows a **summary of all requotable policies**.
- Clicking on a policy opens the **policy details flyout panel**.

### **2. Filtering & Searching**

- Users apply **filters** to refine the list.
- The report updates **instantly** based on selected filters.
- Users can sort by clicking on the heading of the report columns.
- Filters are presented across the top of the report, below the report title, and can be modified by selecting the “Edit” button.

### **3. Viewing Policy Details**

- Clicking a row opens the **policy details flyout panel**.

### **4. Exporting Reports**

- Users select “Download” for options to export as CSV or PDF.

## **E) Master Table Schema**

# #6: Unsigned E-Signature Endorsements

## **A) WHY - Vision and Purpose**

The **Unsigned E-Sig Endorsements Report** provides visibility into policy endorsements that have been issued but not yet signed by policyholders. This feature helps **insurance producers, administrators, and compliance teams** track pending signatures, follow up with clients, and ensure endorsements are legally binding before policies are finalized.

## **B) WHAT - Core Requirements**

1. **Unsigned E-Sig Endorsements Report Overview**
    - Displays a **list of policy endorsements that remain unsigned**.
    - Key details include:
        - **Policy Number**
        - **Insured Name**
        - **Endorsement Creation Date**
        - **Effective Date**
2. **Empty State Handling**
    - If no unsigned endorsements exist, show a **“No unsigned endorsements”** message.
3. **Pagination & Sorting**
    - Data should be paginated for performance optimization.
    - Users can sort by **clicking on the heading of the column.**
4. **Report Download & Export**
    - Users can **download the report in CSV or PDF format**.

## **C) HOW - Planning & Implementation**

### 

## **D) User Experience (UX) & Flows**

### **1. Viewing Unsigned E-Sig Endorsements Report**

- Users navigate to **Reports → Unsigned E-Sig Endorsements** in the sidebar.
- If unsigned endorsements exist, they are displayed in a **sortable table**.
- If no unsigned endorsements exist, an **empty state UI** appears.

### **2. Sorting**

- Users can sort by clicking on the heading of the report columns.

### **3. Exporting Reports**

- Users click the **“Download”** button to generate a PDF or CSV report.

## **E) Master Table Schemas**

# #7: Payment Due Report

## **A) WHY - Vision and Purpose**

The **Payment Due Report** helps insurance teams track and manage **pending premium payments** from policyholders. This feature ensures timely payment follow-ups, reduces policy cancellations due to non-payment, and improves revenue collection efficiency.

## **B) WHAT - Core Requirements**

1. **Payment Due Report Overview**
    - Displays a **list of policies with pending payments**.
    - Key details include:
        - **Policy Number**
        - **Insured Name**
        - **Status** (e.g., "In Force," "Canceled – Non-Pay")
        - **Phone Number(s)** (Primary and Alternate)
        - **Cancellation Date** (if applicable)
        - **Payment Due Date**
        - **Payment Due**
2. **Report Filtering & Search**
    - Users can filter by:
        - **Date Range (Payment Due Date, Cancellation Date)**
3. **Pagination & Sorting**
    - Data is **paginated for performance optimization**.
    - Users can sort by selecting the column headers.
4. **Report Download & Export**
    - Users can **download the report as a CSV or PDF**.

## **C) HOW - Planning & Implementation**

### 

## **D) User Experience (UX) & Flows**

### **1. Viewing Payment Due Report**

- Users navigate to **Reports → Payment Due** in the sidebar.
- If payment due records exist, they appear in a **sortable, filterable table**.
- If no records exist, an **empty state UI** is shown.

### **2. Filtering & Searching**

- Users apply **filters** (Date Range).
- Filters are presented across the top of the report, below the report title, and can be modified by selecting the “Edit” button.

### **3. Generating & Exporting Reports**

- Users click **“Download”** to generate a PDF or CSV.

## **E) Master Table Schema**

# #8: Claims Report

## **A) WHY - Vision and Purpose**

The **Claims Report** provides insurance teams with a detailed overview of **filed claims**, their statuses, and key financial details. This feature improves claims management, helps track outstanding liabilities, and enhances decision-making.

## **B) WHAT - Core Requirements**

1. **Report Filtering & Search**
    - Users can filter claims by:
        - **Status (Open, Closed)**
        - **Date Range (Loss Date, Report Date)**
        - User must apply filters first to generate report.
2. **Claims Report Overview**
    - Displays a **list of claims** within a selected date range.
    - Key details include:
        - **Policy Number**
        - **Insured Name**
        - **Claim Status**
        - **Loss Sequence Number**
        - **Loss Date**
        - **Report Date**
        - **Loss Paid**
3. **Pagination & Sorting**
    - Data is **paginated for performance**.
    - Sorting can be done by clicking on any column header.
4. **Report Download & Export**
    - Users can **export claims data in CSV or PDF formats.**

## **C) HOW - Planning & Implementation**

### 

## **D) User Experience (UX) & Flows**

### **1. Viewing Claims Report**

- Users navigate to **Reports → Claims** in the sidebar.
- User selects appropriate filters and generates report.
- If claims exist, they appear in a **sortable, filterable table**.
- If no records exist, an **empty state UI** is displayed.

### **2. Filtering & Searching**

- Users can apply **filters** based on date range or status.
- Filters are presented across the top of the report, below the report title, and can be modified by selecting the “Edit” button.

### **3. Generating & Exporting Reports**

- Users click **“Download”** to generate a PDF or CSV.

## **E) Master Table Schemas**

# #9: Transmittal Report

## **A) WHY - Vision and Purpose**

The **Transmittal Report** provides a financial summary of transactions, payments, and receipts related to insurance policies. It helps insurers and agents track collected premiums, ensuring transparency and financial accuracy.

## **B) WHAT - Core Requirements**

1. **Report Filtering & Search**
    - Users can filter transactions by:
        - **Date Range (Start Date, End Date)**
        - **Producer E-Check Items Only**
    - User must apply their relevant filters to generate the report.
2. **Summary & Detailed View**
    - The report consists of:
        - **Transmittal Report Summary**
            - Key Data Includes:
                - Type
                - New Business
                - Payment
                - Endorsement
                - Requote
                - Total
        - **Transmittal Detailed Report** (Itemized breakdown of transactions).
            - Key Data Includes:
                - Type
                - Office
                - Policy Number
                - Insured Name
                - Method
                - Submit
                - E-Check Number
                - Accepted
                - Confirmation Number
                - Amount
                - Other
                - Total
3. **Report Download & Export**
    - Users can **export the report in CSV or PDF format**.

## **C) HOW - Planning & Implementation**

## **D) User Experience (UX) & Flows**

### **1. Viewing Transmittal Report**

- Users navigate to **Reports → Transmittal** in the sidebar.
- User must select the relevant filters and generate the report.
- If transactions exist, they appear in a **sortable, filterable table**.
- If no records exist, an **empty state UI** is displayed.

### **2. Filtering & Searching**

- Users can apply **filters** based on date range and payment type.
- Filters are presented across the top of the report, below the report title, and can be modified by selecting the “Edit” button.

### **3. Generating & Exporting Reports**

- Users click **“Download”** to generate a PDF or CSV.

## **E) Master Table Schemas**

# #10: Retention Report

## **A) WHY - Vision and Purpose**

The **Retention Report** helps insurers track customer retention trends, policy renewals, and overall business performance. By providing insights into retention rates across different time periods, the report allows businesses to make data-driven decisions to improve customer engagement and renewal strategies.

## **B) WHAT - Core Requirements**

1. **Report Generation & Ordering**
    - Users can generate reports based on:
        - **Order By:**
            - **Date/Program**
            - **Program/Date**
2. **Retention Report Overview**
    - Displays **policy retention metrics** based on selected criteria.
    - Key data includes:
        - **Year**
        - **Month**
        - **Policies**
        - **Program Name**
        - **Progress Metrics** (e.g., % Retained, % Lapsed)
        - **Renewal Rates**
3. **Report Download & Export**
    - Users can **export the report in CSV or PDF format**.

## **C) HOW - Planning & Implementation**

## **D) User Experience (UX) & Flows**

### **1. Viewing Retention Report**

- Users navigate to **Reports → Retention** in the sidebar.
- User must select their ordering preference and then generate the report.
- If data exists, it appears in a **sortable, filterable table**.
- If no records exist, an **empty state UI** is displayed.

### **2. Filtering & Ordering Reports**

- Users select their preferred **ordering method** (Date/Program vs. Program/Date).
- Filters are presented across the top of the report, below the report title, and can be modified by selecting the “Edit” button.

### **3. Generating & Exporting Reports**

- Users click **“Download”** to generate a PDF or CSV.

## **E) Master Table Schemas**

# #11: Producer Summary Report

## **A) WHY - Vision and Purpose**

The **Producer Summary** report provides a comprehensive overview of an insurance producer’s performance. It consolidates **policy sales, premium amounts, and other key financial metrics** for producers as of a specified timeframe. This report helps management analyze productivity and support strategic decision-making.

## **B) WHAT - Core Requirements**

1. **Report Generation & Filtering**
    - Users select a **specific end date** to generate the summary report.
    - The system fetches **producer data as of the date entered** and the report is generated.
2. **Producer Summary Report Overview**
    - Displays aggregated financial and performance data per producer/agent, including:
        - Transaction Counts, Premiums, Cancellation Counts by Reason, Earned Premiums & Incurred Losses, Inforce Policy Counts, Renewals, etc.
        - This report will be presented as a PDF within the Reporting experience
3. **Data Presentation & Export**
    - The generated report is displayed in a **tabular format (PDF preview)**.
    - Users can **download the report in CSV format** for further analysis.

## **C) HOW - Planning & Implementation**

## **D) User Experience (UX) & Flows**

### **1. Generating a Producer Summary Report**

- Users navigate to **Reports → Producer Summary**.
- They select a **specific end date** from the date picker.
- Clicking **"Generate Report"** fetches and displays the producer summary.
- Filters are presented across the top of the report, below the report title, and can be modified by selecting the “Edit” button.

### **2. Viewing & Downloading Reports**

- Users review **detailed performance metrics** in a **PDF preview**.
- They can **download the report in CSV format** for further analysis.

## **E) Master Table Schemas**

# #12: Commission Statement Report

## **A) WHY - Vision and Purpose**

The **Commission Statement** feature provides detailed insights into commission earnings across different offices and time periods. It enables insurance professionals to track and manage commission payments efficiently. The report helps stakeholders analyze revenue distribution, identify discrepancies, and ensure accurate payouts.

## **B) WHAT - Core Requirements**

1. **Commission Statement Overview**
    - Displays commission data categorized into:
        - **Global Commission Statements**
        - **Commission Statements by Office**
    - Each entry includes:
        - **Date & Time**
        - **Master Code**
        - Description
        - Link to PDF and CSV
            - Upon click;
                - The PDF will be presented in the Document View
                - The CSV will download
2. **Filtering**
    - Users can specify all offices, or specific offices, to receive commission statements for.
3. **Report Download & Export**
    - Users can **export reports in CSV or PDF format**.
4. **Report Access**
    - This report will only be accessible to users with a Manager profile - this means Customer Service Representative (CSR) accounts will not see this report or have access to it

## **C) HOW - Planning & Implementation**

## **D) User Experience (UX) & Flows**

### **1. Viewing Commission Statements**

- Users navigate to **Reports → Commission Statements**.
- The screen displays commission records categorized as:
    - **Global Commission Statements**
    - **Commission Statements by Office**
- All office commission statements available to the user profile will be presented on default

### **2. Filtering & Sorting Data**

- Users select an **office filter** from a dropdown.
- Filters are presented across the top of the report, below the report title, and can be modified by selecting the “Edit” button.

### **3. Generating & Exporting Reports**

- Users select an office and click **“Generate Report”**.
- A **loading state** appears while processing.
- Users download the report as **CSV or PDF**.

## **E) Master Table Schema**

# #13: Sweep Balance Report

## **A) WHY - Vision and Purpose**

The **Sweep Balance** feature provides a detailed breakdown of check transactions processed within a given period. It enables insurance professionals and finance teams to track **swept funds**, verify transactions, and ensure financial reconciliation. This report ensures **accuracy in fund transfers and payment tracking** while helping stakeholders manage cash flow effectively.

## **B) WHAT - Core Requirements**

1. **Report Generation & Filtering**
    - Users must generate a report for a **specific date range**.
    - Start and end dates must be selected before generating the report.
2. **Sweep Balance Report Overview**
    - Displays financial transaction details, including:
        - **Type**
        - **Office Number**
        - **Policy Number**
        - **Insured Name**
        - **Payment Date & Time**
        - **Submit**
        - **E-Check #**
        - **Accepted**
        - **Sweep Date**
        - **Amount Paid**
        - Total Checks for Date, Office, Dollar Amount
    - This page will paginate, showing 10 results on default with the option for the user to click to additional pages or change the default number of rows per page.
3. **Data Sorting & Filtering**
    - Users can sort transactions by clicking the header columns
4. **Download & Export Options**
    - Users can **export reports as CSV or PDF** while retaining selected filters.

## **C) HOW - Planning & Implementation**

## **D) User Experience (UX) & Flows**

### **1. Generating a Sweep Balance Report**

- Users navigate to **Reports → Sweep Balance**.
- They select a **start and end date** from the date picker.
- Clicking **"Generate Report"** fetches and displays transaction data.

### **2. Viewing & Sorting Transactions**

- Users review **transaction details**, including **policy number, e-check info, and sweep date**.
- They sort transactions by clicking the column headers.

### **3. Exporting Data**

- Users click the **Download** button to export the report as CSV or PDF.

## **E) Master Table Schemas**