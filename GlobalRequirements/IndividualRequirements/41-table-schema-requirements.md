# 41.0 Table Schema Requirements

To systematically outline and standardize table schema requirements, we must use a structured and hierarchical approach.

- Understand Table Relationships – Primary keys, foreign keys, and associations.
- Maintain Consistency – Follow a predefined naming convention.
- Ensure Completeness – Include required constraints, descriptions, and references.
- Follow Best Practices – Adhere to database standards (e.g., /MariaDB/ best practices).
1. Structured Table Schema Explanation
    1. General Table Structure
        1. Each table follows a consistent format, containing:
            - Primary Key (id) – Uniquely identifies each record.
            - Foreign Keys – References related entities.
            - Status Tracking – Uses a status_id column for record state management.
            - Audit Fields – Tracks user interactions (created_by, updated_by) and timestamps (created_at, updated_at).
            - Description Column (if applicable) – Stores additional details about the record.
    2. Naming Conventions
        - Tables: Use singular nouns (e.g., user, policy, producer).
        - Join Tables (Mapping Tables): Prefixed with map_ and use singular nouns (e.g., map_user_group, map_producer_signature).
        - Status Tables: Single status table and status_type table. status.id referred to in each map_ table.
        - Reference Tables: Use _type suffix (e.g., user_type, producer_type).
        - Timestamps: Always include created_at, updated_at for record lifecycle tracking.
    3. Standardized Table Types
        1. Each table falls into one of the following categories:
            - Core Entity Tables
                - Store primary records in the system.
                - Example: user, policy, producer.
            - Reference Tables
                - Define categories for entity classification.
                - Example: user_type, producer_type, document_type.
            - Mapping Tables (map_*)
                - Define many-to-many relationships.
                - Example: map_user_group, map_producer_user.
            - Status & Lifecycle Tracking
                - Track entity state (e.g., active, inactive).
                - Example: status, policy.status_id.
2. Conclusion
    - Tables use singular nouns.
    - Join tables use map_ prefix.
    - Each table includes a primary key (id), status tracking (status_id), and audit fields (created_by, updated_by, created_at, updated_at).
    - Use BIGINT for IDs, VARCHAR(255) for names, and TEXT for descriptions.
    - Ensure foreign keys reference appropriate parent tables.
    - Ensure timestamps track data changes.