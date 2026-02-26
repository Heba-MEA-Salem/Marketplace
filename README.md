- git clone the-repo-link
- cd your-repo-name
- python -m venv marketplace-venv
- marketplace-venv\Scripts\activate.bat  or marketplace-venv\Scripts\activate    for windows
- source venv/bin/activate   for mac
- pip install -r requirements.txt
- uvicorn main:app --reloapip install uvicorn



db/          Folder for database-related code
routes/      Folder for API endpoints
schemas/     Folder for request/response validation
main.py      FastAPI app, includes routers, runs server