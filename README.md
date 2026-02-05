# ETL Pipeline: API data to PostgreSQL & Google Sheets & Email


A full-fledged ETL pipeline for collecting statistical data from an external API, transforming it, deduplicating it, and uploading it to a relational database with an analytical report in Google Sheets and via email.

```mermaid
graph LR
    A(API Extract) --> B(Pandas Transform)
    B --> C[(PostgreSQL)]
    B --> D(Google Sheets)
    B --> E(Email Report)
    
    style A fill:#fff,stroke:#333,stroke-width:2px
    style B fill:#fff,stroke:#333,stroke-width:2px
    style C fill:#ADD8E6,stroke:#333,stroke-width:2px
    style D fill:#dfd,stroke:#333,stroke-width:2px
    style E fill:#F0F8FF,stroke:#333,stroke-width:2px
  ```

## Features

-  Getting data from the API with timeouts and network error handling.

- Data processing using Pandas.

- Deployment of nested JSON structures.

- Idempotence: generation of a SHA-256 hash for each row of data (protection against duplicates).

- High-speed upload to a PostgreSQL database.

- Automatic generation of a small analytical dashboard.

- Advanced logging with file rotation (storage for the last 3 days).

- Email distribution of HTML reports with the results of the pipeline.

  


## How to run


1.  **Install dependencies**:

>```pip install -r requirements.txt```


2.  **Fill an `.env` file**:

>Create an `.env` file in the root folder of the project using an .env.example:

3.  **Add Google Credentials file**:

>Put credentials.json (Service Account Key) in the root folder of the project .

4. **Run `main.py`**


## .env file content
|                |                       |
|----------------|-------------------------------|
|**PG_HOST**					|`Your DB host`            |
|**PG_PORT**          			|`Your DB port`            |
|**PG_DB**          			|`Your DB name`|
|**PG_USER**          			|`Your DB login`|
|**PG_PASSWORD**          		|`Your DB password`|
|-------------------------|-----------------------------------------|
|**API_URL**          			|`Endpoint`|
|**CLIENT**          			|`Api login`|
|**CLIENT_KEY**          		|`Api password`|
|-------------------------|-----------------------------------------|
|**EMAIL_USER**          		|`Sender Email`|
|**EMAIL_PASSWORD**          	|`Sender email service password`|
|**EMAIL_RECEIVER**          	|`Receiver email`|
|               			|                       |
## 



