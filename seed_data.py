# seed_data.py
# Run this ONCE to fill MySQL with 240 realistic historical
# sales records (2020-2024) and train the model automatically.
#
# Usage:
#   python seed_data.py

import random
import sys
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
from models import SalesData
from ml_model import train_model

REGIONS    = ["North", "South", "East", "West"]
CATEGORIES = ["Electronics", "Clothing", "Food", "Software", "Home Appliances"]

random.seed(42)


def generate_record(month: int, year: int, region: str, category: str) -> dict:
    """Generate one realistic sales record with correlated features."""

    base_sales = {
        "Electronics":     80000,
        "Clothing":        45000,
        "Food":            30000,
        "Software":        65000,
        "Home Appliances": 55000
    }

    # Q4 is peak sales season (+30%), Q3 slight boost (+10%)
    seasonal   = 1.0 + (0.30 if month in [11, 12] else 0.10 if month in [7, 8] else 0.0)

    # ~8% year-over-year growth
    growth     = 1.0 + (year - 2020) * 0.08

    # Regional variation
    region_f   = {"North": 1.10, "South": 0.95, "East": 1.05, "West": 1.00}[region]

    expected   = base_sales[category] * seasonal * growth * region_f
    mkt_spend  = round(expected * random.uniform(0.10, 0.20), 2)
    employees  = random.randint(20, 150)

    # Actual sales = expected + marketing boost + employee contribution + noise
    actual = (expected + mkt_spend * 1.5 + employees * 100) * random.uniform(0.90, 1.10)

    return {
        "month":            month,
        "year":             year,
        "sales":            round(actual, 2),
        "marketing_spend":  mkt_spend,
        "num_employees":    employees,
        "region":           region,
        "product_category": category
    }


def seed():
    print("🌱 Starting database seed...")

    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    try:
        # Clear old data
        deleted = db.query(SalesData).delete()
        db.commit()
        if deleted:
            print(f"🗑️  Cleared {deleted} existing records.")

        # Generate 5 years × 12 months × 4 regions = 240 records
        records     = []
        orm_objects = []

        for year in range(2020, 2025):
            for month in range(1, 13):
                for region in REGIONS:
                    category = random.choice(CATEGORIES)
                    rec      = generate_record(month, year, region, category)
                    records.append(rec)
                    orm_objects.append(SalesData(**rec))

        db.bulk_save_objects(orm_objects)
        db.commit()
        print(f"✅ Inserted {len(records)} records into MySQL → sales_data table.")

        # Train model immediately after seeding
        print("🤖 Training Linear Regression model...")
        metrics = train_model(records)
        print(f"   R² Score            : {metrics['r2_score']}")
        print(f"   Mean Absolute Error : {metrics['mean_absolute_error']}")
        print(f"   Records used        : {metrics['records_used']}")
        print("\n🎉 Done! You can now start the server: uvicorn main:app --reload")

    except Exception as e:
        db.rollback()
        print(f"❌ Error during seeding: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    seed()