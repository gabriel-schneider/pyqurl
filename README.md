Simple query string parser for LHS filtering, sorting and pagination. This project is directly based on Qurl by Hector Carballo (https://github.com/hector-co/Qurl).

# Installing 
```
$ pip install pyqurl
```

# Usage

```python

from pyqurl import create_query_from_string

# Name contains "john"
create_query_from_string("name[ct]=john")

# Price is greater than 20
create_query_from_string("price[gt]=20")

# Disabled_at is not null
create_query_from_string("disabled_at[nn]=true")

# Year is between 2020 and 2022
create_query_from_string("year[rng]=2020,2022")

# Color is equal to yellow
create_query_from_string("color[eq]=yellow")
# Same result if the operator is not present
create_query_from_string("color=yellow")

# Category is drama, romance or comecy
create_query_from_string("category[in]=drama,romance,comedy")

# Category is not horror or action
create_query_from_string("category[nin]=horror,action")


```