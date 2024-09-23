from flask import Flask, render_template_string, request

app = Flask(__name__)

# HTML Template with embedded CSS
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grade Calculator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #429E9D;
            margin: 0;
            padding: 0;
        }
        .container {
            width: 80%;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #B6D0E2;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            color: 	#9002a8;
        }
        form {
            display: flex;
            flex-direction: column;
        }
        label {
            margin-bottom: 5px;
            font-size: 1.1em;
            color: #000000;
        }
        input[type="number"] {
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button {
            padding: 10px 20px;
            background-color: #9002a8;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #ce03f0;
        }
        .result {
            margin-top: 20px;
            padding: 10px;
            background-color: #E3BEB4;
            border-radius: 4px;
        }
        .error {
            color: red;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Grade Calculator</h1>
        <form method="POST">
            <label for="absences">Absences:</label>
            <input type="number" id="absences" name="absences" min="0" required>

            <label for="prelimExam">Prelim Exam Grade (0-100):</label>
            <input type="number" id="prelimExam" name="prelim_exam" step="0.01" min="0" max="100" required>

            <label for="quizzes">Quizzes Grade (0-100):</label>
            <input type="number" id="quizzes" name="quizzes" step="0.01" min="0" max="100" required>

            <label for="requirements">Requirements Grade (0-100):</label>
            <input type="number" id="requirements" name="requirements" step="0.01" min="0" max="100" required>

            <label for="recitation">Recitation Grade (0-100):</label>
            <input type="number" id="recitation" name="recitation" step="0.01" min="0" max="100" required>

            <button type="submit">Calculate</button>
        </form>

        {% if error_message %}
        <p class="error">{{ error_message }}</p>
        {% endif %}

        {% if prelim_grade %}
        <div class="result">
            <p>Prelim Grade: {{ prelim_grade }}%</p>
            <p>To pass with 75%, you need a  Midterm grade of: {{ required_midterm_and_final }}% and a Final grade of : {{ required_midterm_and_final }}%.</p>
            <p>To achieve 90%, you need a Midterm grade of : {{ required_midterm_and_final2 }}% and a Final Grade of : {{ required_midterm_and_final2 }}%.</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def calculate_grade():
    error_message = None
    prelim_grade = None
    required_midterm_and_final = None
    required_midterm_and_final2 = None

    if request.method == 'POST':
        try:
            # Retrieve form data
            absences = int(request.form['absences'].strip())
            prelim_exam = float(request.form['prelim_exam'].strip())
            quizzes = float(request.form['quizzes'].strip())
            requirements = float(request.form['requirements'].strip())
            recitation = float(request.form['recitation'].strip())

            # Validate inputs
            if absences < 0:
                raise ValueError("Absences cannot be negative.")
            if not (0 <= prelim_exam <= 100):
                raise ValueError("Prelim Exam Grade must be between 0 and 100.")
            if not (0 <= quizzes <= 100):
                raise ValueError("Quizzes Grade must be between 0 and 100.")
            if not (0 <= requirements <= 100):
                raise ValueError("Requirements Grade must be between 0 and 100.")
            if not (0 <= recitation <= 100):
                raise ValueError("Recitation Grade must be between 0 and 100.")

            # Attendance Calculation
            attendance = 100 - (absences * 10)
            if absences >= 4:
                raise ValueError("FAILED due to absences.")

            # Class Standing Calculation
            class_standing = (0.40 * quizzes) + (0.30 * requirements) + (0.30 * recitation)

            # Prelim Grade Calculation
            prelim_grade = (0.60 * prelim_exam) + (0.10 * attendance) + (0.30 * class_standing)

            # Required Midterm and Final Grades
            prelim_percent = 0.20
            midterm_percent = 0.30
            final_percent = 0.50

            passing_grade = 75
            deans_lister_grade = 90

            current_total = prelim_grade * prelim_percent
            required_total = passing_grade - current_total
            required_total2 = deans_lister_grade - current_total

            # Midterm/Final Grades for 75 Passing
            if required_total > 0:
                required_midterm_and_final = required_total / (midterm_percent + final_percent)
            else:
                required_midterm_and_final = 0

            # Midterm/Final Grades for 90 Passing (Dean's Lister)
            if required_total2 > 0:
                required_midterm_and_final2 = required_total2 / (midterm_percent + final_percent)
            else:
                required_midterm_and_final2 = 0

        except ValueError as e:
            error_message = str(e)

    return render_template_string(HTML_TEMPLATE,
                                  error_message=error_message,
                                  prelim_grade=f"{prelim_grade:.2f}" if prelim_grade else None,
                                  required_midterm_and_final=f"{required_midterm_and_final:.2f}" if required_midterm_and_final else None,
                                  required_midterm_and_final2=f"{required_midterm_and_final2:.2f}" if required_midterm_and_final2 else None)


if __name__ == '__main__':
    app.run(debug=True)
