Aime/workspace/requirements/processing-queues/entity-integration/in-progress/approaches/entity-catalog-extension-plan-v2.md
- Migration Complexity is not an issue in this case (greenfield)
- We need to cross reference the existing catalogue for
  - anything to migrate into the this plan that may not be defined
  - if there are existing entites that will end up transformaing into another/other tables, which ones?
  - Essitionally I want to know the difference of what we have and what we will end up having for entities, without losing whats already defined.

From your response:
4. Entities Being Split/Reorganized:                                       
  - communication_hub → communication + communication_preference + template
    - remember that communication is where all api requests are sent from, not just for sms/email/etc..
  - universal_entity → entity (enhanced with better patterns)
    - entities can have types like body shop, inegration vendor, lienholder, mga, carrier, vehicle owner, system, etc..
      - things that are important but not quite relevant enough for it's own table/model
6. Missing from v2 Plan (need to preserve):                                
  - billing_cycle (exists in current, not in prompt4.md) - remove for now. Accounting requirements are coming soon.                  
  - payment_method (referenced but not defined) - keep for now                           
  - ach_transaction (referenced but not defined) - remove for now                          
  - underwriting_rule (exists but not in prompt4.md) - remove for now                      
  - program_config (exists but replaced by program)  - this should be in configuration with the _type.id for Program                      
  - lapse_record (exists for reinstatement)    - remove for now.                            
  - sr22_filing (exists for sr22 domain)  - remove for now.                                 
  - dcs_api (integration pattern, not a table)  - this should be accounted for with entity and communication

Add transaction, transaction_type, transaction_line, transaction_line_type