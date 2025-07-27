# IP007 - Driver Alert Inquiry Feature Requirements

## **A) WHY – Vision and Purpose**

The Driver Alert Inquiry experience allows a user to view and create new driver alerts in the system. It enables: 

- Identifying drivers that should no longer be insured by the MGA
- Set temporary, or indefinite alerts with no expiration date
- Easily searching for driver alerts in the system

The goal of this functionality is to minimize risk to the MGA by preventing producers/MGAs from reinstating or renewing policies for specific drivers. 

## **B) WHAT – Core Requirements**

### 1. Searching for Driver Alerts

- Search will default to show all Driver Alerts in system prior to search
- Allow user to search by License Number, Policy Number, or Driver Name
- Allow user to filter search results by Entry Date, Expiration Date, and Never Expires
- Allow user to sort results by selecting the header column
    - Sorted by column will be indicated by downward pointing arrow as outlined in the designs
- Present search results with the following details:
    - License Number
    - Policy Number
    - Driver Name
    - State
    - Description
    - Entry Date
        - MM/DD/YYYY
    - Expiration Date
        - This will be a date in the MM/DD/YYYY format, or ‘Never Expires’ if no expiry was set
- If no results are returned, show empty state

### 2. Export Driver Alert Search Results

- User may export the search results as a PDF or CSV file

### 3. Create New Driver Alert

- Select ‘Create New’ CTA to open side panel flyout from the right side of the screen
- Populate alert with the following:
    - License Number (Required)
    - Policy Number (Required)
    - Driver Name (Required)
    - State (Required)
    - Description (select from dropdown) (Required)
    - Entry Date (Required)
        - This will be populated with the current date when the alert is being created
    - Expiration Date
        - If the user has selected “Never Expires” then the Expiration Date field will be disabled
        - If the user has entered a date in the Expiration Date field, then selects the “Never Expires” checkbox, the expiration date will be purged from the field
    - Message
    - Payment Authorization (Required)
    - Never Expires (checkbox)
    - Make Alert Visible to Producer (checkbox)
- If the user does not have a license number, they can select the ‘Create Policy Alert’ CTA
    - This will link the user to `IP010 - Policy Alert Inquiry Feature Requirements`

### 4. Modify Existing Driver Alert

- User may select an existing alert from the search results returned to modify an alert
    - Selecting an alert will open the alert with current information available in a sidepanel flyout
- If the user clicks outside of the side panel flyout prior to saving changes, clicks ‘Close’ prior to saving changes, or clicks ‘Save Changes’, confirmation dialog will be presented asking the user to confirm their changes prior to saving
- Once saved, the CTA will update to the ‘Saved’ state to indicate the change was made successfully
- Existing driver alerts will also have a ‘View History’ CTA, showing an audit log of changes made to this alert, including:
    - Last Edited Date/Time
    - Last Edited By (User)
    - Created Date/Time
    - Last Edited by (User)
    - Date/Time/User Stamps, alongside a description of the change made

### 5. Remove Driver Alert

- User may select an existing alert from the search results to remove an alert
    - Selecting an alert will open the alert with current information available in a sidepanel flyout
- Alerts can be removed by selecting the garbage can icon
- Upon selection, user will be presented confirmation dialog to confirm removal
    - ‘Cancel’ will dismiss the confirmation dialog, with no changes made to the alert
    - ‘Delete’ will dismiss the confirmation dialog, delete the alert, and show the user a success toast indicating the driver alert has been removed

## **C) HOW – Planning & Implementation**

## **D) User Experience (UX) & Flows**

### 1. Search for Alerts

- Open Driver Alert Inquiry experience, see all existing driver alerts in system
- Enter search query, and complete search
- Review returned results and;
    - Filter and/or sort results based on available filters/sorting options
    - Export results as a PDF or CSV
    - Create New alert
    - Select an existing alert

### 2. Create Alert

- Select ‘Create New’ and populate the information required for the Driver Alert
- ‘Save Changes’ and the alert will be created and available in the search results, as well as tied to the driver and their relevant policy

### 3. Modify Alert

- Select an existing alert from the search results
- Modify the alert as needed, and select ‘Save Changes’ to apply updates
    - Complete confirmation modal to apply changes
- Changes will be logged in the ‘View History’ section of the flyout

### 4. Delete Alert

- Select an existing alert from the search results
- Select trash icon to remove alert from this driver
    - Complete confirmation modal to apply changes
- Present success toast on Search Results page to indicate alert was removed successfully

## **E) Master Schema Tables**