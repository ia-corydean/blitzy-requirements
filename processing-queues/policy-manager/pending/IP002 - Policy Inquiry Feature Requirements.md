# IP002 - Policy Inquiry Feature Requirements

## **A) WHY – Vision and Purpose**

The Policy Inquiry feature is the launch point for accessing policies within the system. It allows a user to: 

- Quickly and easily find policies within the system through a series of different search queries
- Customize data shown by configuring column preferences, allowing for more robust and comprehensive searching
- Export search results to utilize data in reporting

## **B) WHAT – Core Requirements**

### Search for Policy

- The default state of Policy Inquiry will be to list all policies
- The user can enter their query into search bar and complete search to narrow the results returned
    - The user can search by:
        - Policy Number
        - Producer Number
        - Producer Master Code
        - Producer Group Code
        - Insured Name
        - ZIP Code
        - City
        - VIN
        - Vehicle Plate
        - Phone Number
        - Address
- The user can narrow their options further using filtering and sorting options
    - Filter By:
        - Policy Status
            - ‘Reset’ will return all policy statuses to selected
            - ‘Cancel’ will dismiss the filter dropdown with no changes made
            - ‘Ok’ will refresh the search results with the filter applied
        - Effective Date
            - The user has the option to select a date range or single date value
            - ‘Reset’ will clear all dates selected
            - ‘Cancel’ will dismiss the filter dropdown with no changes made
            - ‘Ok’ will refresh the search results with the filter applied
        - Inception Date
            - The user has the option to select a date range or single date value
            - ‘Reset’ will clear all dates selected
            - ‘Cancel’ will dismiss the filter dropdown with no changes made
            - ‘Ok’ will refresh the search results with the filter applied
    - Sorting can be applied by selecting the header row per column
        - The column the data is sorted by will be indicated using the downward arrow
- The default set of columns returned for a search result will include:
    - Policy Number
    - Insured Name
    - Effective Date
    - Inception Date
    - Status
    - Producer Number
    - Primary Phone Number
- If no search results are returned based on the query, filters, or any combination, will show the no results found state

### Column Configuration

- The user will have the ability to configure the columns shown in the report by selecting the ‘Columns’ dropdown
- The user will have the option to:
    - Search for column labels using exact match
    - ‘Select All’ which will update all columns to checked
    - Scroll down the list of columns and manually select the columns they want to include
    - ‘Reset’, which would return the list of columns to default
    - ‘Cancel’, which will dismiss the columns dropdown
    - ‘Ok’, which will dismiss the columns dropdown and refresh the search results inclusive of the new columns selected
- The table will scroll horizontally to accommodate additional column width

### Export Report

- Export the report as CSV or PDF
- Export will defaut to include the columns currently selected in the search view
- The user can add additional columns by manually selecting or using ‘Select All’ before generating the export
- The export loading dialog will present showing the progression of the export generation
- Upon completion, user can download report

### Selecting a Policy

- To view a policy’s details, the user can select the appropriate row in the table to proceed to the next page (`IP288 - Policy View Feature Requirements`)

## **C) HOW – Planning & Implementation**

## **D) User Experience (UX) & Flows**

### Search for Policy

- Enter search query, and complete search
- Apply filters/sorting to narrow results
- Select relevant policy from the list

### Configure Columns

- Select ‘Columns’
- Select the relevant columns for inclusion in the search results and apply
- Results will refresh inclusive of the updated columns
- Select relevant policy from the list

### Export Report

- Select ‘Export’
- Choose Export by PDF or by CSV
- Review included columns, and add or remove columns as needed
- Generate export and download file

## **E) Master Schema Tables**