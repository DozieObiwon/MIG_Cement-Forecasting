import sqlite3
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_cement_data(db_path=None):
    if db_path is None:
        db_path = PROJECT_ROOT / "data" / "raw" / "MIG_Cement_Records.db"
    else:
        db_path = Path(db_path)
        if not db_path.is_absolute():
            candidates = [
                PROJECT_ROOT / db_path,
                Path.cwd() / db_path,
            ]
            db_path = next((candidate for candidate in candidates if candidate.exists()), candidates[0])

    if not db_path.exists():
        raise FileNotFoundError(f"Database file not found: {db_path}")

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    query = """         
    SELECT
        o.date, o.site_id, s.region, s.behavior, o.cement_type, 
        o.planned_pour_tonnes, o.consumed_tonnes, o.opening_inventory_tonnes, 
        o.deliveries_tonnes, o.closing_inventory_tonnes, o.rain_mm, 
        o.avg_temp_c, o.silo_capacity
    FROM
        operations o
    JOIN sites s ON o.site_id = s.site_id
    """

    df = pd.read_sql_query(query, conn)
    conn.close()
    df['date'] = pd.to_datetime(df['date'])

    return df