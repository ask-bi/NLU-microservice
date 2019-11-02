# NLU MicroService

This micro service communicates with the NLU engine and responds with a standard JSON to generate a Query

## Prerequisites
- Python3
- Pip

## Setup:
- clone the repo
- cd into the directory
- pip install -r requirements.txt
- python app.py


## APIs:

- Command to json

 route: `/command-to-json`
 query param: `?command=<command here>`
 body payload: 

 ```
    {
        schema: [
            {
                db : <db-name>,
                tables : [
                    <table-1>,
                    <table-2>,
                    ...
                ]
            },
            .....
        ]
    }
 ```

 expected response:

 ```
 {
    type: <enum: as-is | query>,
    result: {
        body: <string | null>
        command_type: <string>,
        table_name: <string>,
        db_name: <string>,
        conditions: {

        }
    }
 }
 ```
