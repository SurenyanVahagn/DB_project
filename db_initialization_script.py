import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

# Configuration
DB_NAME = '' 
DB_OWNER = 'SurenyanVahagn'
DB_URI = f'postgresql:///{DB_NAME}'

# Create engine (Note: this assumes you have a PostgreSQL service running and accessible)
engine = create_engine(DB_URI)

# Create the database if it doesn't exist
if not database_exists(engine.url):
    create_database(engine.url)
    print(f'Database {DB_NAME} created.')
else:
    print(f'Database {DB_NAME} already exists.')

# Set the owner of the database
with engine.connect() as conn:
    conn.execute(f'ALTER DATABASE {DB_NAME} OWNER TO {DB_OWNER}')
    print(f'Owner of database {DB_NAME} set to {DB_OWNER}.')
