[IP269-Bind-Document-Signatures-approach.md](../in-progress/approaches/IP269-Bind-Document-Signatures-approach.md)
- updates added
- create a -v2 file
[IP269-Bind-Document-Upload-approach.md](../in-progress/approaches/IP269-Bind-Document-Upload-approach.md)
- if no other changes in this document affect this requirement, this is approved. if there are changes in here that affect this requirement, outline a -v file.
  - use the process outlined in Aime/workspace/requirements/README.md to generate the completed requirements if approved.
[IP269-Bind-Local-Signatures-Payment-approach.md](../in-progress/approaches/IP269-Bind-Local-Signatures-Payment-approach.md)
- outline the cost benefit of useing docusign for digital signatures vs the followoing in a -v2 file
- Frontend:
    - Blade Templates: Templates are used to render user-friendly PDF previews.
    - Tailwind CSS: Provides modern styling for forms and signature displays.
- PDF Rendering/Generation:
- Barryvdh/Laravel-Snappy
    - Converts HTML Blade templates to PDFs using wkhtmltopdf.
    - Blade templates are styled to ensure clarity and proper dimensions.
    - Two PDFs are generated: one for initials and another for the full signature.
    - PDFs are stored accordingly.
[IP269-Bind-Photo-Upload-approach.md](../in-progress/approaches/IP269-Bind-Photo-Upload-approach.md)
- we should have a photo and photo_type table
- we should have a map_vehicle_photo
- create a -v2 file with these in place.
[IP269-Bind-Remote-Signatures-Payment-approach.md](../in-progress/approaches/IP269-Bind-Remote-Signatures-Payment-approach.md)
- portal_session (For Remote Access Tracking)
- this should be in session and session_type
- create a -v2 file with these in place.
[IP269-ITC-Bridge-New-Info-1-approach.md](../in-progress/approaches/IP269-ITC-Bridge-New-Info-1-approach.md)
- Recommended: Set driver.lookup_source = 'ITC_BRIDGE'
  - use driver.source_entity_id
- create a -v2 file with these in place.
[IP269-ITC-Bridge-New-Info-2-approach.md](../in-progress/approaches/IP269-ITC-Bridge-New-Info-2-approach.md)
- create a -v2 of this file with all the other comments above in mind.
[IP269-New-Quote-Step-1-Primary-Insured-approach.md](../in-progress/approaches/IP269-New-Quote-Step-1-Primary-Insured-approach.md)
- license (Needs Additional Fields)
  - create these fields in the docker database
  - update the entity catalogue to reference this addition.
- create a -v2 with this in place.
[IP269-New-Quote-Step-2-Drivers-approach.md](../in-progress/approaches/IP269-New-Quote-Step-2-Drivers-approach.md)
- driver (Need Employment Fields)
  - create employment and employment_type table and reference the employment_id
  - create occupation and occupation_type table and reference the occupation_id
  - remove income_source
  - driver_type should account for excluded or included
  - remove removal_reason
- create a -v2 file with these updates
[IP269-New-Quote-Step-3-Vehicles-approach.md](../in-progress/approaches/IP269-New-Quote-Step-3-Vehicles-approach.md)
- vehicle (Need License Plate Fields)
  - registered_owner_driver_id
    - the registered owner can either be an entity or a driver, how can we make this better and simpler?
- create a -v2 file with these updates
[IP269-New-Quote-Step-4-UW-Questions-approach.md](../in-progress/approaches/IP269-New-Quote-Step-4-UW-Questions-approach.md)
- if no other changes in this document affect this requirement, this is approved. if there are changes in here that affect this requirement, outline a -v file.
  - use the process outlined in Aime/workspace/requirements/README.md to generate the completed requirements if approved.
[IP269-New-Quote-Step-5-Coverages-approach.md](../in-progress/approaches/IP269-New-Quote-Step-5-Coverages-approach.md)
- If not storing equipment in separate table:
  - we need a special_equipment and _type
- create a -v2 file with these updates
[IP269-New-Quote-Step-6-Quote-Review-approach.md](../in-progress/approaches/IP269-New-Quote-Step-6-Quote-Review-approach.md)
- if no other changes in this document affect this requirement, this is approved. if there are changes in here that affect this requirement, outline a -v file.
  - use the process outlined in Aime/workspace/requirements/README.md to generate the completed requirements if approved.
[IP270-Policies-approach.md](../in-progress/approaches/IP270-Policies-approach.md)
- if no other changes in this document affect this requirement, this is approved. if there are changes in here that affect this requirement, outline a -v file.
  - use the process outlined in Aime/workspace/requirements/README.md to generate the completed requirements if approved.
[IP279-Endorsements-approach.md](../in-progress/approaches/IP279-Endorsements-approach.md)
- what if we considered endorsements as transaction_types? essentially endorsements and re-quotes and renewals are types of transactions/changes to the policy.
  - does this make for an easier approach?
  - what are your thoughts?
- create a -v2 file with these updates
[IP286-Re-Quoting-approach.md](../in-progress/approaches/IP286-Re-Quoting-approach.md)
- if no other changes in this document affect this requirement, this is approved. if there are changes in here that affect this requirement, outline a -v file.
  - use the process outlined in Aime/workspace/requirements/README.md to generate the completed requirements if approved.