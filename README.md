# QRCat

Application for a Cat Charity Fund. 

### Description:

The Fund gathers donations for various targeted projects: for medical care of poor cats, for setting up a cat colony, for food for abandoned cats - for any purpose related to the support of the cat population.

Each user can make a donation and include a comment with it. Donations are not targeted: they are made to a fund, not to a specific project. Each donation received is automatically added to the first open project that has not yet reached the required amount. If the donation is more than the required amount or there are no open projects in the Fund, the remaining money is waiting for the next project to be opened. When a new project is created, all uninvested donations are automatically invested in the new project.

Access to the application is provided via API.

The application has the feature of generating a report in Google Sheets. The table displays closed projects sorted by the speed of fundraising - from those that closed the fastest to those that took a long time to raise the required amount.


### How to launch the project

Clone the repository and access it on the command line:

```
git clone 
```

```
cd cat_charity_fund
```

Create and activate the virtual environment:

```
python3 -m venv venv
```

* For Linux/macOS

    ```
    source venv/bin/activate
    ```

* For Windows

    ```
    source venv/scripts/activate
    ```

Install dependencies from the requirements.txt file:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Create and fill in the .env configuration file using the template provided:  
```  
APP_TITLE=Application name
DESCRIPTION=Application description
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=Your secret key for generating passwords
```  

Create migration files and apply them:  
```  
alembic revision --autogenerate
```
```  
alembic upgrade head
```  

Use the command line to start the project:  
```  
uvicorn app.main:app --reload 
```  

### Technologies

- Python 3.9
- SQLAlchemy 1.4
- FastAPI
- Alembic 1.7
- Google API

### Author
Vladimir Maksimov 
