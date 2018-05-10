# Testing



### Start API independent of front end for testing

1. Spin up docker containers for the database and api
'''
docker-compose up db
docker-compose up delphi_api
'''

2. In the delphi_api container run the migration
'''
docker exec -it delphiapi_delphi_api_1 bash
python migration.py
'''

3. Check that data was seeded into the database
'''
docker exec -it delphi_api_db_1 bash
psql -U postgres
\c delphi
\x auto
slect * from stake;
'''
