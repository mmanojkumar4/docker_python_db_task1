import psycopg2
import time

# Wait for PostgreSQL container to be ready
time.sleep(5)

def get_connection():
    conn = psycopg2.connect(
        host="postgres_db",
        database="testdb",
        user="postgres",
        password="password"
    )
    print("Connected to the database!")
    return conn

   

# Create table if not exists
def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50),
            batch INT,
            domain VARCHAR(20)
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

# 1. Add Employee
def add_employee():
    name = input("Enter Employee Name: ")
    batch = int(input("Enter Batch No: "))
    domain = input("Enter Domain (Java/AI/DevOps): ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO employees (name, batch, domain) VALUES (%s, %s, %s)",
        (name, batch, domain)
    )
    conn.commit()

    print("Employee Added Successfully!\n")
    cur.close()
    conn.close()

# 2. Update Employees
def update_employee():
    emp_id = int(input("Enter Employee ID to Update: "))
    new_name = input("New Name: ")
    new_batch = input("New Batch: ")
    new_domain = input("New Domain (Java/AI/DevOps): ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE employees
        SET name=%s, batch=%s, domain=%s
        WHERE id=%s
    """, (new_name, new_batch, new_domain, emp_id))

    conn.commit()
    print("Employee Updated Successfully!\n")
    cur.close()
    conn.close()

# 3. Delete Employee
def delete_employee():
    emp_id = int(input("Enter Employee ID to Delete: "))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM employees WHERE id=%s", (emp_id,))
    conn.commit()

    print("Employee Deleted Successfully!\n")
    cur.close()
    conn.close()

# 4. View All Employees
def view_employees():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM employees;")
    rows = cur.fetchall()

    print("\n===== EMPLOYEE LIST =====")
    for row in rows:
        print(row)
    print()

    cur.close()
    conn.close()

# Main Menu Loop
def main():
    create_table()

    while True:
        print("""
1. Add Employee
2. Update Employee
3. Delete Employee
4. View All Employees
5. Quit
""")
        choice = input("Select an option: ")

        if choice == "1":
            add_employee()
        elif choice == "2":
            update_employee()
        elif choice == "3":
            delete_employee()
        elif choice == "4":
            view_employees()
        elif choice == "5":
            print("Exiting program...")
            break
        else:
            print("Invalid choice! Try again.\n")

if __name__ == "__main__":
    main()

