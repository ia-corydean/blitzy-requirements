**Make A Payment Workflow** 

The make a payment workflow should be the same as making a payment in producer portal.  The back-office user should have the following options for processing a payment; credit card, ACH (insured e-check) and Agent E-Check (Sweep). 

When physical checks/money orders are received to process there should be an additional option on the make a payment screen with the payment types noted above labeled Mailed in Payment.  

When this is selected the side panel should require the following fields. 

Postmarked Date   
Payment Type   
Check Number   
Check Amount 

**Rule Requirements:** Payment should apply to the billed unsatisfied invoice.  If the payment exceeds the amount due on the billed invoice the balance should apply to the policy balance and all future bills should be recalculated. 

If the payment is less than the billed unsatisfied invoice, the system should determine if there is enough premium to carry the policy to the next due date \+11/12 days for cancellation.  

* If there is enough the bill should be satisfied. The shortage should apply to the policy balance and all future bills should be recalculated.   
* If there is NOT enough money the payment should be applied to the bill and the difference should remain as an open invoice and if cancellation is not already pending, then the system should determine days paid and process the cancellation based on the paid to date to prevent unnecessary refunds. 

**Batch Payments** 

Batch Payments should be a separate function under Policy. This function will allow you to process multiple payments received via mail at one time. 

* The system should create a batch number automatically when the user starts the process.    
* These fields should be required, Once the policy number is entered the side panel or batch should display a portion of the policy view so the user can validate the following: 

**Required Fields**   
Policy Number   
Postmarked Date   
Payment Type   
Check Number   
Check Amount 

**System Field Auto Processed**   
        Batch Number   
        Batch Total – System should run a tally of all checks entered for reconciliation.   
        Show Report View of Posted Items with the required fields noted above.   
	   
       **Policy Data to Display**  
       Name of Insured   
       Address   
       Policy Status – Active, Pending or Cancelled  
       Payment Due Date  
       Payment Amount  

Day 2 – some MGA’s may have a check reader from the bank and want to process via the scan and imaging machine via manual entry. 

![A screenshot of a computerAI-generated content may be incorrect.][image1] 

[image1]: <data:image/png;base64,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>