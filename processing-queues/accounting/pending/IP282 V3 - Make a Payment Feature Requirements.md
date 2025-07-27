# IP282 V3 - Make a Payment Feature Requirements (Late Fee Definition)

## **A) WHY - Vision and Purpose**

The **Make a Payment / Credit Card** feature allows users to securely pay their insurance premiums using a credit card. This provides a **fast, convenient, and widely accepted payment option**, reducing the risk of late payments and improving the user experience. 

This document is an amendment to the initial Make a Payment requirements, focusing on late fees. Insurance companies will have the option to assess a late fee for missed payments, which will be processed as a part of the next payment made. This is payment method agnostic, and will not overwrite the existing workflows for Make a Payment.

## **B) WHAT - Core Requirements**

- Prerequisites:
    - User has been invoiced for a payment, and failed to satisfy the payment by the defined due date
    - User access the ‘Make a Payment’ page in the Insured Portal
- User will be presented an alert indicating a late fee has been assessed and will be charged with their next payment
- This alert will include two configurable elements for the dollar value of the late fee, and the due date associated to the missed payment
- In addition to the alert, the late fee will be listed in the ‘Order Summary’, and included in the calculation for the total dollar value of the payment

## **C) HOW - Planning & Implementation**