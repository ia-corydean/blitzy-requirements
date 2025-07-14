This is in response to Aime/workspace/requirements/processing-queues/accounting/pending/accounting-global-requirements-generation-v6.md
- please put all revisions in a -v7 file.
- remove all table specific references in the requirments
- remove all laravel / service code from the requirements.
- Use the process defined in Aime/workspace/requirements/README.md to
  - re-evaluate the remaining requirements that were not stripped out of accounting-global-requirements-generation-v6.md and placed in accounting-global-requirements-generation-v7.md
  - scan the project for existing requirements that would provide context on coming up with tables, schemas, infra to support our accounting requirements.
- the main tables for accounting should be transaction and transaction_line
- ensure that we are not over-complicating the accounting foundation.