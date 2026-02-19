from app import app, db, User

def check_db():
    print("Checking Database Connection...")
    try:
        with app.app_context():
            # Check if User table exists by querying count
            user_count = User.query.count()
            print(f"PASS: Connected to DB. Users count: {user_count}")
    except Exception as e:
        print(f"FAIL: Database error: {e}")

if __name__ == "__main__":
    check_db()
