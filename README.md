# Exchange Rate Api

- This API returns calculation and updated exchange information for provider-based currencies.


- 2 providers are integrated in it.
  - http://fixer.io/
  - https://currencylayer.com/
  


### Requirements

-  Python version: 3.6

-  Django version : 3.2.0

-  DB : sqlite3

-  Cache: redis


### Endpoints
- In addition, for use the system, register and then login endpoints must be called.

```
   {{host}}/api/v1/account/register/
   {{host}}/api/v1/account/login/
```


- Exchange api endpoints:

```
   {{host}}/api/v1/exchange/list/
   {{host}}/api/v1/exchange/convert/
   {{host}}/api/v1/exchange/rates/
```


See [Swagger](http://localhost/) documented endpoints.

Download [Postman Collection](docs/Exchange API.postman_collection.json).
and [Postman Environment](docs/LOCAL.postman_environment.json).






### Quick Start

1. Download the latest docker.


2. Copy `env`:
   
        cp .env.example .env
 
3. API_KEYS need to be added in `env` files for two providers separately.

```
Example:
   FIXER_API_KEY=8g8aKfYY8rd0N3DwYNeH1uwf7OFmA50l
   CURRENCY_DATA_API_KEY=8g8aKfYY8rd0N3DwYNeH1uwf7OFmA50l
```

3. After these operations are done, the application can be installed using `Docker`:
   
        docker-compose up -d --build



### Notes

- If you want to fetch data from which provider, in the header section for the relevant endpoint;
  - `X-PROVIDER` parameter needs to be added.

   ``Note : 1: Fixer Api | 2: CurrencyData API``




