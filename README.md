# retail-inventory-manager
A simple inventory manager based on Python and SQL

## Objective
Demonstrate Python and SQL skills by building a simple manager.

## Manager's capabilities
With a Console based User Interface users can track product, stock and transactions of a retail store

### Menu
Users will get to choose from the following options once they run the program:
![Image](https://github.com/sowmyatdm/retail-inventory-manager/blob/main/Choices.PNG)



## Components
The manager was built using Postgres as the database. Python script connects to the database using psycopg2 python library. *database.ini* file defines the db configuration parameters. A sample file is provided. Three tables are necessary for the manager's functionality. Their schema is as follows: 

```
product

  Column  |     Type      |
----------+---------------+
 id       | character(10) |
 name     | character(20) |
 category | character(20) |
 
```

```
transaction

   Column   |         Type          |
------------+-----------------------+
 dt         | date                  |
 c_id       | character varying(10) |
 id         | character varying(10) |
 sold_price | numeric(20,0)         |
 units_sold | integer               |
 
 ```
 
 ```
 
 stock
 
     Column     |     Type      |
----------------+---------------+
 id             | character(10) |
 purchase_price | numeric(10,0) |
 selling_price  | numeric(10,0) |
 units          | integer       |

```