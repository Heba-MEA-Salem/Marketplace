- git clone the-repo-link
- cd your-repo-name

- create .gitignore file and add to it:
.venv/
.idea/
__pycache__

  # Python virtual environment
  env/
  venv/
    
  # Python cache files
  __pycache__/
  *.pyc
    
  # IDE/editor files
  .vscode/
  .idea/
    
  # Environment variables
  .env


- python -m venv marketplace-venv
- marketplace-venv\Scripts\activate.bat  or marketplace-venv\Scripts\activate    for windows
- source venv/bin/activate   for mac
- pip install -r requirements.txt
- uvicorn main:app --reload