from flask import Flask, render_template, request, redirect, url_for
from db import get_connection

app = Flask(__name__)

@app.route('/')
def index():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM expenses ORDER BY expense_date DESC")
    expenses = cursor.fetchall()
    conn.close()
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['GET', 'POST'])
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def add_edit(id=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    expense = None

    if id:
        cursor.execute("SELECT * FROM expenses WHERE id = %s", (id,))
        expense = cursor.fetchone()

    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        amount = request.form['amount']
        description = request.form['description']
        if id:
            cursor.execute(
                "UPDATE expenses SET expense_date=%s, category=%s, amount=%s, description=%s WHERE id=%s",
                (date, category, amount, description, id)
            )
        else:
            cursor.execute(
                "INSERT INTO expenses (expense_date, category, amount, description) VALUES (%s, %s, %s, %s)",
                (date, category, amount, description)
            )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('add_edit.html', expense=expense)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/summary')
def monthly_summary():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT DATE_FORMAT(expense_date, '%%Y-%%m') AS month, SUM(amount) AS total
        FROM expenses
        GROUP BY month
        ORDER BY month DESC
    """)
    summary = cursor.fetchall()
    conn.close()
    return render_template('summary.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
