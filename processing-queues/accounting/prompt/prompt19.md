Added my responses to Aime/workspace/requirements/processing-queues/accounting/in-progress/approaches/accounting-schema-revised-final.md
- All data that is suggested in JSON format needs to be uniform and structured in nature for maintainablity.
  - JSON fields are okay and can be beneficial in certain aspects. Do not remove all of them for the sake of structure.
  - You should still be able to have structured JSON formats within the fields.
- Please analyze and provide suggestions, questions, feedback, updates to approach, etc..
- Notice how everything that could potentially grow at scale, i'm breaking out into their own tables with types. Although when doing this too much may cause complex queries, it keeps data organized and relational. In the end, it will be humans maintaining this so organization that is intuitive for humans is key.
- put the output in a new file for review.