from app.migrations.seed import seed
from app import create_table

engine = create_table()

seed(engine)
