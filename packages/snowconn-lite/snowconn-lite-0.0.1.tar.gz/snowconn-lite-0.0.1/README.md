# SnowConn Lite

# Overview

This repository contains a lite version of snowconn package

# Why?

Because the current snowflake python package dependencies are too restrictive for automated deployments. A simple look at the [snowflake connector package](https://github.com/snowflakedb/snowflake-connector-python) shows that Snowflake's current package has grown due to the needs to support legacy customers with unique needs.

Currently, installing snowflake-connector (or snowflake-sqlalchemy or snowconn) on a new machine or any automatic deployment has a chance of failling due to snowflake-connector's requirements.


## Usage


###  Installation

```sh
$ pip install snowconn-lite
```


### Import

Usage of snowconn-lite mirrors the snowconn package

```Python
from snowconn import SnowConn
conn = SnowConn.credsman_connect('$CREDSMAN_KEY', db='$SNOWFLAKE_DB')
conn.read_df('SELECT * FROM TABLE').head()
```


## TODOs

This package is a WIP, feel free to submit a PR to reduce the dependencies even more!.


## License
----

This package has the same license as the original snowconn package (MIT License)
