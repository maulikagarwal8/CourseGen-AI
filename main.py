#importing all the necessary libraries.
import openai
import os
from flask import Flask, render_template_string, request

openai.api_key = os.environ['OPENAI_API_KEY']

#Creating a function to get the response from the openai api.
def generate_tutorial(course):
     response = openai.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "system","content": "You are a helpful assistant"}, 
        {"role":"user","content":f"Give a concise statement that describes the purpose and goals of the {course}. Also, include a detailed syllabus outline that covers the main topics and modules to be taught throughout the {course}.List specific, measurable learning outcomes categorized according to Bloom's Taxonomy levels: Knowledge, Comprehension, and Application.Give suggestions on how to evaluate the learning outcomes through various forms of assessment.Give a list of resources, including books, articles, and other materials relevant to the {course} content.In the end give a motivational quote related to {course}."}
        ])
     return response['choices'][0]['message']['content']

# Create a Flask web application object named 'app' and define a route for the root('/') URL that responds to GET and POST requests.
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

# Defining a function that generates the data based on user input obtained through a POST request.
def hello():
     output = ""
     if request.method == 'POST':
          course_name = request.form['course_name']
          output = generate_tutorial(course_name)
    # This is a HTML template for a Custom Educational Course Content Generator web page. It includes a form for users to input the course title, and two JavaScript functions for generating a details of course based on the input and copying the output to the clipboard. The template uses the Bootstrap CSS framework for styling.
     return render_template_string('''
     
     <!DOCTYPE html >
     <html >
     <head >
      <title >Educational Course Content Generator </title >
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css"
        rel="stylesheet">
      <script >
    
      async function generateTutorial() {
       const course_name = document.querySelector('#course_name').value;
       const output = document.querySelector('#output');
       output.textContent = 'Finding all the details about the course...';
       const response = await fetch('/generate', {
        method: 'POST',
        body: new FormData(document.querySelector('#tutorial-form'))
       });
       const newOutput = await response.text();
       output.textContent = newOutput;
      }
      function copyToClipboard() {
       const output = document.querySelector('#output');
       const textarea = document.createElement('textarea');
       textarea.value = output.textContent;
       document.body.appendChild(textarea);
       textarea.select();
       document.execCommand('copy');
       document.body.removeChild(textarea);
       alert('Copied to clipboard');
      }
    
      </script >
     </head >
     <body >
      <div class="container">
       <h1 class="my-4">Educational Course Content Generator</h1 >
       <form id="tutorial-form" onsubmit="event.preventDefault(); generateTutorial();" class="mb-3">
        <div class="mb-3">
         <label for="course_name" class="form-label"><b>Name of the Course :</b></label >
         <input type="text" class="form-control" id="course_name" name="course_name" placeholder="Enter the course name to generate data related to it." required >
        </div >
        <button type="submit" class="btn btn-primary">Generate the content </button >
       </form >
       <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
         <b>Output:</b>
         <button class="btn btn-secondary btn-default" onclick="copyToClipboard()">Copy </button >
        </div >
        <div class="card-body">
         <pre id="output" class="mb-0" style="white-space: pre-wrap;">{{ output }}</pre >
        </div >
       </div >
      </div >
     </body >
     </html >
    
    ''',output=output)

# This code defines a route for the URL '/generate' that only accepts POST requests.
@app.route('/generate', methods=['POST'])

# Defining a function 'generate' that takes a POST request containing a 'course_name' field and returns the result of calling the 'generate_tutorial' function with the provided course_name as input.
def generate():
     course_name = request.form['course_name']
     return generate_tutorial(course_name)

# This code snippet starts the Flask application if the script is being run directly as the main program, running on the IP address '0.0.0.0' and port number '8080'.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
