from flask import Flask, request, render_template, jsonify
import re
import pdfplumber

app = Flask(__name__)

def parse_text(content):
    """Extract questions and options from raw text."""
    questions = []
    question_pattern = r'(\d+\..*?)(?:\n(A\..*?)\n(B\..*?)\n(C\..*?)\n(D\..*?))'
    matches = re.findall(question_pattern, content, re.DOTALL)

    for match in matches:
        question = {
            "question": match[0].strip(),
            "options": [match[1].strip(), match[2].strip(), match[3].strip(), match[4].strip()]
        }
        questions.append(question)
    return questions

@app.route('/')
def index():
    return render_template('index.html')  # Serve the HTML form

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    text_content = request.form.get('text')

    # Handle file upload
    if file and file.filename.endswith('.pdf'):
        with pdfplumber.open(file) as pdf:
            content = "\n".join(page.extract_text() for page in pdf.pages)
    elif text_content:
        content = text_content
    else:
        return "Please upload a file or paste content."

    # Parse MCQs
    parsed_data = parse_text(content)
    return jsonify(parsed_data)  # Return parsed MCQs as JSON

if __name__ == "__main__":
    app.run(debug=True)
