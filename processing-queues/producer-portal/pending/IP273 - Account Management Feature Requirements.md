# IP273 - Account Management: Feature Requirements

# #1: Sign In - Account Management

## **A) WHY - Vision and Purpose**

The **Sign-In Experience** is designed to provide users with a secure and seamless authentication process when accessing the **InsurePilot** platform. It ensures accessibility across different devices while handling authentication errors in a user-friendly manner. The goal is to enhance usability, security, and troubleshooting efficiency for users who may encounter login issues.

## **B) WHAT - Core Requirements**

1. **Sign-In Form**
    - Fields:
        - **Username** (freeform text field)
        - **Password** (freeform text field, masked input with a visibility toggle)
    - **Forgot Password Link** (Redirects users to the password recovery process)
    - **Sign-In Button** (Triggers authentication request)
2. **Error Handling**
    - Display an error message when incorrect credentials are entered:
        - "Incorrect Username or Password" in **red notification banner**.
    - Error messages should be clear and actionable.
3. **Responsive Design**
    - The **sign-in screen should be fully optimized** for both desktop and mobile devices.
4. **Help and Support**
    - Include **customer support contact information** for users who need assistance.

## **C) HOW - Planning & Implementation**

## **D) User Experience (UX) & Flows**

### **1. Default Sign-In Process**

- User enters their **username and password**.
- Clicks **Sign In**.
- If correct, the system authenticates the user and redirects them to the Producer Portal dashboard.

### **2. Handling Sign-In Errors**

- If credentials are incorrect:
    - A **red error message** appears: “Incorrect Username or Password.”
- If the user forgets their password:
    - Clicking “Forgot Password?” redirects them to the password reset flow.

### **3. Mobile Experience**

- On mobile, the form adapts to a **compact layout**.
- Text remains legible and touch-friendly.

## **E) Master Schema Tables**

# #2: Reset Password - Account Management

## **A) WHY - Vision and Purpose**

The **Password Reset Experience** ensures that users can securely and efficiently regain access to their accounts if they forget their password. The goal is to provide a **user-friendly, secure, and responsive** flow that minimizes frustration while maintaining high-security standards.

## **B) WHAT - Core Requirements**

1. **Forgot Password Flow**
    - A **“Forgot Password?”** link on the sign-in page.
    - Clicking the link opens the **password reset request form**.
    - Users must enter their **registered email or username**.
2. **Validation & Error Handling**
    - If the entered email/username is invalid, display an **error message**.
    - If the request is successful, show a **confirmation message** that an email has been sent.
3. **Reset Password Flow**
    - Users receive a **password reset email** with a secure link.
    - Clicking the link opens the **reset password form**.
    - Users must enter:
        - A **new password** (must meet security criteria).
        - **Confirm new password**.
    - If passwords don’t match or don’t meet security requirements, display **error messages**.
4. **Successful Reset Confirmation**
    - Upon successful reset, show a **success confirmation message**.
    - Provide a **“Return to Sign-In”** button.

## **C) HOW - Planning & Implementation**

## **D) User Experience (UX) & Flows**

### **1. Request Password Reset**

- User clicks **Forgot Password?**
- Enters their **email or username**.
- If valid, the system confirms that a reset email has been sent.

### **2. Reset Password Form**

- User clicks the **email link** and is redirected to the password reset page.
- They enter a **new password** and confirm it.
- If successful, a **confirmation message** appears.

### **3. Handling Errors**

- **Invalid email/username** → Show a red error message.
- **Password doesn’t meet security criteria** → Highlight the issue in red.
- **Expired or invalid reset link** → Redirect users to request a new reset link.

## **E) Master Schema Tables**

# #3: Sign Out - Account Management

## **A) WHY - Vision and Purpose**

The Sign Out Confirmation screen reassures users that their **log-out action was successful** and **provides a clear path back** to the login screen if they need to sign in again.

It improves trust, clarity, and experience by:

- Explicitly confirming that the user is securely signed out.
- Offering immediate re-login without navigating elsewhere manually.
- Maintaining brand consistency even during session end flows.

---

## **B) WHAT - Core Requirements**

### 1. **Confirmation Message**

- Display message:
    
    > "You successfully logged out."
    > 

### 2. **Sign In Button**

- A primary button labeled **"Sign In"** must be shown.
- Clicking the button should redirect the user to the login page.

### 3. **Responsive Layout**

- Experience must support both:
    - **Desktop** view (centered layout)
    - **Mobile** view (vertically optimized)

---

## **C) HOW - Planning & Implementation**

### 

---

## **D) User Experience (UX) & Flows**

### 1. **Logout Flow**

1. User clicks **Log Out** anywhere in the app.
2. User is redirected to **Signed Out** page.
3. Page loads:
    - Centered success card:
        - Success icon (✔️)
        - Text: "You successfully logged out."
        - Primary button: "Sign In"
4. If the user clicks **Sign In**:
    - Redirect to **Login** page.

### 2. **Mobile Flow**

- Same as desktop flow, but content is stacked vertically and scaled appropriately.
- Button easily reachable without horizontal scrolling.

## E) Master Schema Tables

# #4: Contact Info - Account Management

## **A) WHY - Vision and Purpose**

The purpose of this functionality is to provide a seamless user experience for managing contact information within the Producer Portal. Users should be able to view, edit, and save contact details efficiently across both desktop and mobile interfaces. The responsive design ensures that users can interact with the system effectively regardless of the device being used.

## **B) WHAT - Core Requirements**

The user can access the Account Management section of the platform by selecting the username in the side navigation, and navigating to the appropriate tab from the sub menu. The entirety of the Account Management section of the platform will only be available to users with Manager permissions. 

1. **Contact Information Management**
    - Users can view and update contact details, including website, email, phone number, and fax.
2. **Address Management**
    - Users can edit mailing and physical addresses.
    - Option to mark physical address as "Same as Mailing Address" for automatic population.
3. **Navigation and Layout**
    - Responsive UI that adapts to both desktop and mobile views.
    - Left sidebar navigation available on desktop but replaced with a collapsible menu on mobile.
4. **Editing & Validation**
    - Editable text fields for contact and address details.
    - "Save Changes" and "Cancel Edits" buttons for user control.
    - Validation for required fields before saving.
5. **Tabs for Additional Information**
    - Users can navigate between "Contact Info," "Profile," "Digital Signatures," "Roles & Permissions," “All Producers,” and "Documents" tabs.

## **C) HOW - Planning & Implementation**

## **D) User Experience (UX) & Flows**

### **1. Viewing Contact Information**

- The account presented will be the account the user has signed in with. This account is visible in the side navigation.
- Contact information is displayed in a structured form.

### **2. Editing Contact Details**

- User clicks on a field to edit contact or address details.
- Changes are reflected in real time.
- User clicks "Save Changes" to confirm edits or "Cancel Edits" to discard.

### **3. Managing Addresses**

- User edits mailing or physical address separately.
- If "Same as Mailing Address" is checked, physical address fields auto-populate.

### **4. Navigation Between Tabs**

- User selects a tab to switch between sections (Contact Info, Profile, etc.).
- The system dynamically loads relevant content.

## **E) Master Schema Tables**

# #5: Profile - Account Management

## **A) WHY - Vision and Purpose**

The Profile Management functionality enables users to view and update their account details, including email addresses and preferred language settings. Additionally, the password change feature provides a secure way for users to update their credentials while ensuring compliance with security policies. The goal is to offer a seamless and intuitive experience across desktop and mobile interfaces.

## **B) WHAT - Core Requirements**

The user can access the Account Management section of the platform by selecting the username in the side navigation, and navigating to the appropriate tab from the sub menu. The entirety of the Account Management section of the platform will only be available to users with Manager permissions. 

1. **Profile Management**
    - Users can view and update their preferred language.
    - Display of the user's email address.
    - Save and cancel buttons to confirm or discard changes.
2. **Change Password Functionality**
    - Users must enter their current password before setting a new one.
    - The new password must meet security requirements:
        - At least 10 characters
        - At least 1 letter
        - At least 1 number or special character
    - Confirmation field for re-entering the new password.
    - Validation messages to guide users in creating a secure password.
3. **Password Confirmation Message**
    - An informational dialog appears, reminding users to update passwords in external systems if necessary.
    - Users can cancel or proceed with updating their password.
4. **Success Confirmation**
    - Upon successful password change, a snackbar message appears confirming the update.
5. **Responsive Design**
    - Desktop and mobile views should maintain functional parity while adapting layouts appropriately.

## **C) HOW - Planning & Implementation**

## **D) User Experience (UX) & Flows**

### **1. Viewing & Updating Profile Information**

- User navigates to the Profile tab.
- Email and language preference fields are displayed.
- User can update the preferred language and save changes.

### **2. Changing Password**

- User clicks "Change Password."
- A password change dialog appears, requiring:
    - Current password
    - New password with real-time validation
    - Confirm password field
- User clicks "Continue" to proceed.
- The user can toggle between viewing the masked text in the password fields by selecting the eye icon.

### **3. Password Confirmation Message**

- A dialog appears informing the user of potential external dependencies.
- User can cancel or proceed with updating the password.

### **4. Successful Password Update**

- If the password meets requirements and is correctly confirmed, the system updates it.
- A confirmation message appears as a snackbar notification.

## **E) Master Schema Tables**

# #6: Digital Signatures - Account Management

## **A) WHY - Vision and Purpose**

The Digital Signature Management feature allows users to create, store, and manage their electronic signatures for document signing. This ensures secure and legally binding transactions while streamlining business processes. The goal is to offer a seamless and intuitive experience for both desktop and mobile users.

## **B) WHAT - Core Requirements**

The user can access the Account Management section of the platform by selecting the username in the side navigation, and navigating to the appropriate tab from the sub menu. The entirety of the Account Management section of the platform will only be available to users with Manager permissions. 

1. **Creating a Digital Signature**
    - Users can create a new digital signature if one does not exist.
    - Users must enter their full name (Licensed Agent of Record Name).
    - Users must agree to adopt the signature for use.
    - The system generates a digital signature and initials based on the entered name.
2. **Managing an Existing Digital Signature**
    - The created signature and initials are displayed for user reference.
    - Users can change their signature by clicking the "Change Signature" button.
3. **Dialog Confirmation for Signature Creation**
    - A modal appears requesting users to enter their name for signature generation.
    - The user must check a box to confirm adoption of the signature.
    - The user can either cancel or confirm signature creation.
4. **Responsive Design**
    - The interface should adapt for both desktop and mobile screens while maintaining usability.

## **C) HOW - Planning & Implementation**

## **D) User Experience (UX) & Flows**

### **1. Creating a Digital Signature**

- User navigates to the "Digital Signatures" tab.
- If no signature exists, a prompt displays "Create a Signature."
- The user clicks the button to open the signature creation dialog.
- The user enters their name and agrees to adopt the signature.
- The system generates a signature and initials, then saves them.

### **2. Managing an Existing Signature**

- If a signature exists, it is displayed along with initials.
- User can click "Change Signature" to update their signature.

### **3. Mobile Adaptation**

- All dialogs and interactions must remain fully functional on smaller screens.

## **E) Master Schema Tables**

# #7: Roles & Permissions - Account Management

## **A) WHY - Vision and Purpose**

The **Roles & Permissions Management** feature allows users to view and manage role-based access control within an agency. This functionality provides transparency on permissions assigned to different roles, ensuring proper access control and compliance with organizational policies.

## **B) WHAT - Core Requirements**

The user can access the Account Management section of the platform by selecting the username in the side navigation, and navigating to the appropriate tab from the sub menu. The entirety of the Account Management section of the platform will only be available to users with Manager permissions. 

1. **Display User Roles & Assigned Permissions**
    - Show a list of roles such as **Manager** and **Customer Support**.
    - Display the number of members assigned to each role.
    - List permissions for each role (e.g., Commission Statements, Payment Posting, etc.).
2. **Master Permissions Notification**
    - If the user has **Master Permissions**, a notification banner should appear.
    - The banner should explain the benefits of Master Permissions.
3. **Responsive Design**
    - Ensure proper adaptation for both **desktop** and **mobile** views.

## **C) HOW - Planning & Implementation**

## **D) User Experience (UX) & Flows**

### **1. Viewing Roles & Permissions**

- User navigates to the **Roles & Permissions** tab.
- The system displays roles and their assigned members.
- Permissions for each role are listed with checkmarks indicating assigned access.

### **2. Master Permissions Notification**

- If the user has **Master Permissions**, a banner appears with an explanation.
- The banner remains visible unless permissions change.

### **3. Mobile Optimization**

- The UI should adjust for mobile views, ensuring readability and accessibility.

## **E) Master Schema Tables**

# #8: All Producers - Account Management

## **A) WHY - Vision and Purpose**

The **All Producers** feature enables users to view and manage a list of producers associated with an agency. It provides transparency into producer details, assigned roles, and permissions, ensuring efficient access control and role management. This feature supports business operations by allowing administrators to monitor and adjust producer access levels.

## **B) WHAT - Core Requirements**

The user can access the Account Management section of the platform by selecting the username in the side navigation, and navigating to the appropriate tab from the sub menu. The entirety of the Account Management section of the platform will only be available to users with Manager permissions. 

1. **Producer List View**
    - Display a table listing all producers with the following columns:
        - **Login**
        - **Email**
        - **Producer ID**
        - **Access Level**
        - **User Level (Role Assignment - e.g., Manager, Customer Success, etc.)**
    - Implement **search functionality** to filter producers by name, email, or role.
    - Provide an **export option** to download producer data in PDF or CSV.
2. **Role and Permissions Visibility**
    - Clicking on a user’s **role (e.g., Manager, Customer Success)** opens a modal showing the **permissions assigned** to that role.
3. **Producer Details View**
    - Clicking on a producer opens a detailed view showing:
        - **Email**
        - **Agent ID**
        - **Access Level**
        - **Assigned Permissions**
4. **Mobile Optimization**
    - Ensure responsiveness for mobile views, maintaining the same core functionality.

## **C) HOW - Planning & Implementation**

## **D) User Experience (UX) & Flows**

### **1. Viewing Producer List**

- User navigates to the **All Producers** tab.
- The system displays a **list of producers** with key details.
- Users can **search** or **export** the list for further processing.

### **2. Viewing Role Permissions**

- Clicking on the **role name (e.g., Manager, Customer Success)** opens a modal.
- The modal displays a **list of assigned permissions**.

### **3. Viewing Producer Details**

- Clicking on a **producer** opens the detailed view.
- The page displays **email, agent ID, access level, and assigned permissions**.

### **4. Mobile Experience**

- The UI adapts to a **responsive layout** ensuring smooth navigation.

## **E) Master Schema Tables**

# #9: Documents - Account Management

## A) WHY - Vision and Purpose

The purpose of this functionality is to enhance document management within the system. Users should be able to view, manage, and delete documents efficiently while maintaining a history of changes. This functionality ensures better document control, security, and user experience.

## B) WHAT - Core Requirements

The user can access the Account Management section of the platform by selecting the username in the side navigation, and navigating to the appropriate tab from the sub menu. The entirety of the Account Management section of the platform will only be available to users with Manager permissions. 

- **Document Viewing**: Users should be able to open and view documents within the system.
- **Document Metadata**: Display key information such as document name, license number, expiry date, and upload date.
- **Document History**: Users should be able to track edits, including last modified date, who edited it, and creation details.
- **Document Management Options**:
    - View document information
    - View document history
    - Delete a document with confirmation
    - Search for documents by exact match
- **Error Handling & Validation**:
    - Show error messages when required fields are missing
    - Provide validation for incorrect inputs
    - Display success messages upon successful actions

## C) HOW - Planning & Implementation

## D) User Experience (UX) & Flows

### **Primary User Flows:**

1. **Viewing a Document:**
    - User opens a document from the list.
    - The document is displayed with metadata and actions available, using the “Document View” functionality.
2. **Viewing Document Info & History:**
    - User clicks on the menu and selects "Document Info" or "Document History."
    - The system displays relevant information with a back button to return.
3. **Deleting a Document:**
    - User selects "Delete File" from the menu.
    - A confirmation dialog appears asking for user confirmation.
    - If confirmed, the document moves to the "Recently Deleted" folder for 90 days.
4. **Uploading a Document:** 
    - User clicks “Upload Document” to initiate document upload process.
    - A modal will be presented, where the user will select the type of document they are uploading (i.e. License Document, or E&O”.)
    - The user will then upload the file from their desktop or mobile device.
    - If the user has selected E&O as their file type, they must populate the Policy Coverage Limit (i.e. $1,000,000, $2,000,000, or $5,000,000, which will be available in a dropdown) and the expiration date, before completing their upload.
    - If the user has selected License Document as their file type, they must populate the License Number and the expiration date, before completing their upload.
5. **Error Handling & Validation:**
    - If required fields are missing, the system displays an appropriate message.
    - If a user attempts an invalid action, an error prompt appears.
    - Successful operations provide confirmation messages.

## E) Master Schema Tables

# #11: References

1. **Development-Ready Designs:**
    1. Development-ready, annotated UI designs can be found [HERE](https://www.figma.com/design/wZy88tHbSjEicvzgzVqZH2/Insure-Pilot---MVP-Designs?node-id=2107-2) to guide front-end and back-end implementation efforts. The password to view the file is `insurepilot2025` . These designs include specifications for component states, interactions, and data mappings, ensuring that developers have a clear visual reference for building the Account Management feature.