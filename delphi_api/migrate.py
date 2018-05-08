from app.migrations.seed import seed
from app import create_table

env = 'dev' # hardcoded to dev to prevent production migration

engine = create_table()

seed(engine)
