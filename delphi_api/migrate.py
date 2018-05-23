from app.migrations.migrate import migrate
from app import create_table

engine = create_table()

migrate(engine)
