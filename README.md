# transactions-alchemy-django
Django with Alchemy Mysql Pandas Rest Framework example

# Components

Users: handling with sqlite (default db with django)
Processors: handling with SQLAlchemy

# Authentication and Credentials
Please use these credentials to test

username: admin

password: admin

This project use Basic Auth (It won't be in production) please take in mind

# Considerations
for django and django rest it's easier handle users with django users system then
for practicality db.sqlite3 has been tracked to have a user to tests, although
for the processors system works with sqlalchemy.

### Prerequisites
 
to run this project you need:
* Docker and docker compose

### Run with docker
To run just run

```bash
docker-compose up
```
 
### Run tests
Tests don't have dependencies (They must not have) then you can run if you have 
python>=3.7 and requirements.txt dependencies with virtualenv

```console
pytest -s -v
```

or if you prefer docker 

TODO: tests with docker

# Curl Quickly Functional Tests

## Process File

It will relate transactions to user authenticated (i.e. admin)

Process File 

`POST http://localhost:8000/v1/processors/files`

You can use `transactions_example.csv` of this repository to test

**Auth required** : YES (Basic Auth)

**Response** `http status code 204`

**Example**

```console
curl --request POST \
  --url http://localhost:8000/v1/processors/files \
  --header 'authorization: Basic YWRtaW46YWRtaW4=' \
  --header 'content-type: multipart/form-data; boundary=---011000010111000001101001' \
  --form file=<path of your file>
```

## Get Transactions by User

It will retrieve transactions related to user authenticated (i.e. admin)
only supports search by transaction_id

Process File 

`GET http://localhost:8000/v1/processors/transactions?limit=10&page=1&order_by=id&search=52fba4fa`

**Auth required** : YES (Basic Auth)

**Response** Get Example

```json
{
  "count": 6,
  "page": 1,
  "next_page": 2,
  "transactions": [
    {
      "id": "0b6c0f19-3915-4fd7-93ca-c2be13b3939e",
      "transaction_id": "52fba4fa-3a01-4961-a809-e343dd4f9597",
      "transaction_date": "2020-06-01",
      "transaction_amount": 10000,
      "client_id": 1067,
      "client_name": "nombre cliente",
      "file_id": "d65c6de6-6423-4a97-a707-64382281c4a1",
      "user_id": 1
    }
  ]
}
```

**Example**

```console
curl --request GET \
  --url 'http://localhost:8000/v1/processors/transactions?limit=10&page=1&order_by=id&search=word' \
  --header 'authorization: Basic YWRtaW46YWRtaW4='
```

