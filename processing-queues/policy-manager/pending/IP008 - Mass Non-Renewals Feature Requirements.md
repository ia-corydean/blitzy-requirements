# IP008 - Mass Non-Renewals Feature Requirements

## **A) WHY – Vision and Purpose**

The Mass Non-Renewals experience allows a user to set a group of policies to non-renew, meaning the MGA will no longer service this policy past their expiration date. It enables the MGA to: 

- Non-renew by program (i.e. the insurance product offering)
- Non-renew by producer (i.e. the insurance agent selling the insurance product)

This provides the MGA flexibility to discontinue certain programs, or customer groups tied to specific producers. 

## **B) WHAT – Core Requirements**

### Select Non-Renewal Type

- To begin this workflow, the user must first select the non-renewal type they will proceed with
    - Non-Renew by Program
    - Non-Renew by Producer

### Non-Renew by Program

- To initiate a non-renewal by program, the user must populate:
    - Notice Wording (dropdown)
        - Program No Longer Available
        - MGA No Longer Represents the Company
    - Insurance Companies (dropdown)
        - All Companies (default selection)
        - Additional dropdown options will be available depending on the insurance carriers associated with the MGA - this dropdown will need to accommodate this flexibility
    - Policy Prefix
        - All Policy Prefixes (default selection)
        - Additional dropdown options will be available depending on the programs the MGA offers - this dropdown will need to accommodate this flexibility
    - Inception Date Month
        - All Months (default selection)
        - The other options will be the months of the year
- Following population of these fields, the user will select submit to initiate the non-renewal
    - Prior to completion, a confirmation modal will be presented
- Upon selecting proceed, the user will be redirected to a success state, showcasing a summary of the change made
- The user may then start another mass non-renewal, which would redirect them to the initial screen

### Non-Renew by Producer

- To initiate a non-renewal by producer, the user must populate:
    - Notice Wording (dropdown)
        - Producer No Longer Represents the Company
    - Insurance Companies (dropdown)
        - All Companies (default selection)
        - Additional dropdown options will be available depending on the insurance carriers associated with the MGA - this dropdown will need to accommodate this flexibility
    - Policy Prefix
        - All Policy Prefixes (default selection)
        - Additional dropdown options will be available depending on the programs the MGA offers - this dropdown will need to accommodate this flexibility
    - Inception Date Month
        - All Months (default selection)
        - The other options will be the months of the year
- Following completion of these fields, the user must then add Producers for non-renewal
- To identify a producer, the user will search by Producer Name or Producer Number using the search bar provided
    - Upon completion of search, the returned results will be presented
    - The user may add the producer by selecting the ‘Add’ CTA
    - Once added, the user will have the option to ‘Remove’ the producer if required before submission
    - Note: only Producers in an inactive status will be eligible for non-renewal - if the user searches for an active producer, they will be unable to set them to non-renewal
- Following population of these fields, the user will select submit to initiate the non-renewal
    - Prior to completion, a confirmation modal will be presented
- Upon selecting proceed, the user will be redirected to a success state, showcasing a summary of the change made
- The user may then start another mass non-renewal, which would redirect them to the initial screen

## **C) HOW – Planning & Implementation**

## **D) User Experience (UX) & Flows**

### Non-Renew by Program

- Select ‘Non-Renew by Program’
- Complete the Notice Wording, Insurance Comopanies, Policy Prefix and Inception Date Month fields
- Submit non-renewal and confirm using the confirmation modal
- Present success state indicating completion

### Non-Renew by Producer

- Select ‘Non Renew by Producer’
- Complete the Notice Wording, Insurance Comopanies, Policy Prefix and Inception Date Month fields
- Search for Producer(s) using Producer Name or Producer Number
- Add relevant producer(s) to non-renewal
    - Producers must be inactive to be eligible for inclusion in this workflow
- Submit non-renewal and confirm using the confirmation modal
- Present success state indicating completion

## **E) Master Schema Tables**