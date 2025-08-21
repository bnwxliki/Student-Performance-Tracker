from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# loading data
students = pd.read_csv("data/students.csv")  # Use the updated CSV with extra columns
subjects = pd.read_csv("data/subjects.csv")
marks = pd.read_csv("data/marks.csv")

# merging data
df = marks.merge(students, on="student_id").merge(subjects, on="subject_id")

@app.route("/", methods=["GET", "POST"])
def index():
    student_list = students.to_dict(orient="records")
    selected_student = None
    student_data = None
    avg_marks = None
    chart = None

    if request.method == "POST":
        student_id = int(request.form["student_id"])
        student_df = students[students["student_id"] == student_id]
        if not student_df.empty:
            selected_student = student_df.iloc[0].to_dict()
            student_data = df[df["student_id"] == student_id]
            avg_marks = round(student_data["marks_obtained"].mean(), 2)

            # Create bar chart of marks
            plt.figure(figsize=(8,4))
            plt.bar(student_data["subject_name"], student_data["marks_obtained"], color='skyblue')
            plt.title(f'Marks for {selected_student["student_name"]}')
            plt.xlabel('Subject')
            plt.ylabel('Marks')
            plt.ylim(0, 100)
            plt.tight_layout()

            # Save plot to PNG image in a buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            chart = base64.b64encode(buf.getvalue()).decode()
            plt.close()

    return render_template(
        "index.html",
        students=student_list,
        selected_student=selected_student,
        student_data=student_data,
        avg_marks=avg_marks,
        chart=chart
    )

if __name__ == "__main__":
    app.run(debug=True)
