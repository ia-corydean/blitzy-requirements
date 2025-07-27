We are going to update our existing Global Requirements to reflect our current database
- we need to make sure we are only updating the database sections and ensuring that any other part of the file that depends on the database is reflective of that.
- there was existing work done, but understand the following
  - the existing work isn't entirely reflective of the new database. With this said:
    - take the concepts out of these that are suggestions for the global requirement updates.
    - use our existing docker container as the source of truth and the requirements should be reflective of that.
      - there may be additions to our existing databsse we'll need to make. these need to be outlined in an approach file for approval.
- creat new appraoch files for each existing global requirements on how to get it in line with our databse.

GlobalRequirements/IndividualRequirements
- existing global requirements.

GlobalRequirements/IndividualRequirements/approaches
- existing approach files to consider

Aime/workspace/requirements/README.md
- for context on our overall process and how these fit in.

/blitzy-requirements
- do not reference this while looking for existing tables and configuration.
- this is a seperate repo.

docker database variables

# Database Configuration
DB_ROOT_PASSWORD=very_secure_root_password
DB_NAME=claude_db
DB_USER=claude_user
DB_PASSWORD=secure_claude_password