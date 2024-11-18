# Code Analyzer using Gemini API
## About:
I have made a tool that can analyze code and if needed, translate to these languages:
1. Python
2. JavaScript
3. Java
4. C++
5. C#
6. Ruby
7. Go

**To make this:**
* _Gemini 1.5 Flash_ is used for the generation of code report, vulnerabilities and potential improvements, translated language.
* Tkinter is used for interface
* Regular expression (re) is used for finding patterns and formatting text for easier readibility.

## Working:
The below image is the starting interface of the tool:
![Starting interface](https://github.com/user-attachments/assets/8d07b1e8-4edd-4ce5-b458-ce9a3c8a3691)

We enter our code(no need of mentioning the language of the code, the tool detects it by its own) and select the language we want to translate in _(optional)_. If needed, click *Reset* to erase everything *(In this case, it's python language and we translate it to C++)*:
![Select language](https://github.com/user-attachments/assets/674cdbdc-d37b-407b-a7f2-0f5fe32863f9)

After we click Analyze, it will analyze and generate results after a while.

When done analyzing, we can select any tab for the result:

### Analysis Result
Here, the model explains the working of the code the user has uploaded:
![Analysis Result](https://github.com/user-attachments/assets/ca1a0346-6ef0-43d6-b85a-4121ef0c48b8)

### Vulnerabilities and Suggestions
Here, the model generates a report on vulnerabilities on the code and also gives some suggestions to tackle them:
![Vulnerabilities   Suggestions](https://github.com/user-attachments/assets/58bf5204-f709-4280-a545-4930f0a3d4ce)

### Translated Code
Here, the model translates our code to the language we select *(It's empty if we don't select any language)*:
![Translated Code](https://github.com/user-attachments/assets/04f2e7bc-aa8d-458d-9032-a5fdf8b092a1)


## Note:
* It only works on codes, nothing else
* In **'Translated Code'** section, only translation is given, no explaination
