# IP272 - Resources: Feature Requirements

### **TABLE OF CONTENTS**

### **#1: WHY - VISION & PURPOSE**

**Purpose:**
The "Resources" section provides a centralized area within the Insure Pilot platform where users can quickly access categorized external links and informational resources. This feature ensures that users have an efficient and intuitive interface for navigating essential forms, government links, insurance-related resources, and other tools, enhancing productivity and accessibility.

**Users (for context only):**

- **Manager and Customer Support Representative Accounts:** Users who need quick access to forms, government links, and informational sites to manage claims or policies efficiently.

---

### **#2: WHAT - CORE REQUIREMENTS**

**Functional Requirements**

1. **Resource List Layout & Categorization**
    - Display resource categories as visually distinct sections.
    - Each category displays a header with the category name and a list of linked items underneath.
    - A prioritized ranking will be used to determine the order in which to present the resource groups.
    - Include a visual divider between categories to improve scannability.
2. **Resource Items**
    - Each resource item must display:
        - **Name** of the resource as a clickable link.
        - **External link icon** (indicating the link opens in a new tab or window).
    - When hovering over the link, a hover state is present.
    - A prioritized ranking will be used to determine the order in which to present the resources within the groups.
    - Resource links must be responsive and accessible, adapting to different screen sizes.
3. **Responsiveness**
    - The design must support both desktop and mobile views:
        - **Desktop View:** Display categories in two columns, maintaining alignment and consistency.
        - **Mobile View:** Collapse categories into a single column to fit smaller screens.
    - Ensure proper spacing and readability in all views.
4. **User Roles and Permissions**
    - All users with access to the Insure Pilot platform must be able to view the "Resources" section.
    - The feature does not require role-based restrictions; all links are available to all users.

---

### **#3: HOW - Planning & Implementation**

**Technical Considerations:**

1. Full Mapping of Front-End Fields to Database Fields
    - Resource Group Name → `map_resource_group` to get resource id and `resource_group` id
    - Resource Group Ranking → `map_resource_group_order`
    - Resource Name → `map_resource_group` to get resource id -> `resource.name`
    - Resource URL → `map_resource_group` to get resource id -> `resource.url`
    - Resource Ranking → `map_resource_group` -> order alpha
    - External vs Internal Status → `map_resource_group` -> resource id -> `resource.resource_type_id` of External or Internal or anything
2. **Responsiveness:**
    - Use media queries to switch between desktop and mobile layouts.
    - Test designs across multiple devices to ensure consistent functionality and appearance.
3. **Accessibility Standards:**
    - Ensure resource links have appropriate ARIA labels and keyboard navigation support.
    - Contrast ratios and font sizes must comply with WCAG guidelines.

---

### **#4: USER EXPERIENCE (UX) & FLOWS**

**Flow: Viewing Resources**

1. **Accessing the Resources Section:**
    - Users navigate to the "Resources" section from the main navigation menu.
    - The "Resources" page loads, displaying all categories and their corresponding links.
2. **Browsing Categories and Links:**
    - Users scroll through the list of categorized resources.
    - For links with the external indicator icon, the resource will be opened in a new tab.
    - For links without the external indicator icon, the user will navigate to another page within the Producer Portal.

**Flow: Responsive Navigation**

1. **Desktop Experience:**
    - Categories appear side-by-side in a two-column layout.
    - Clicking a link does not disrupt the layout.
2. **Mobile Experience:**
    - Categories stack vertically for single-column navigation.
    - The first column will take priority, with the second column stacking certically underneath.
    - Links remain fully functional, and spacing ensures readability.

---

### **#5: BUSINESS REQUIREMENTS**

**Access & Authentication:**

- All authenticated users can view the "Resources" section.
- No role-based restrictions are necessary for this feature.

**Data Validation & Integrity:**

- Resource links must be validated to ensure they point to live, secure URLs.
- Categories and resource names must be updated periodically to maintain relevance.

**Operational Requirements:**

- Any updates to the resource list (e.g., adding/removing links) must not disrupt user access.

---

### **#6: REFERENCES & ATTACHMENTS**

1. **Development Ready Designs:** 
    - Development-ready, annotated UI designs can be found [HERE](https://www.figma.com/design/wZy88tHbSjEicvzgzVqZH2/Insure-Pilot---MVP-Designs?node-id=362-1744) to guide front-end and back-end implementation efforts. The password to view the file is `insurepilot2025`. These designs include specifications for component states, interactions, and data mappings, ensuring that developers have a clear visual reference for building the Reources feature.