# Snowflake Connector Lite

# Overview

This repository contains a lite version of snowflake-sqlalchemy python package

# Why?

Because the current snowflake python package dependencies are too restrictive for automated deployments. A simple look at the [snowflake connector package](https://github.com/snowflakedb/snowflake-connector-python) shows that Snowflake's current package has grown due to the needs to support legacy customers with unique needs.

Currently, installing snowflake-connector (or snowflake-sqlalchemy) on a new machine or any automatic deployment has a chance of failling due to snowflake-connector's requirements.

This package aims to reduce the dependencies. You get a connection, thats all


## Usage


###  Installation

```sh
$ pip install snowflake-connector-lite
```

### Import

Usage of snowflake-sqlalchemy-lite mirrors the official snowflake-sqlalchemy package, **except** it does not support the most advanced features of that package (like cloud integrations)

```Python
from sqlalchemy import create_engine
engine = create_engine('snowflake://$SNOWFLAKE_USER:$SNOWFLAKE_PWD@$SNOWFLAKE_ACCOUNT/')
connection = engine.connect()
results = connection.execute('select current_version()').fetchone()
print(results[0])
```


## TODOs

This package is a WIP, feel free to submit a PR to reduce the dependencies even more!.


## License
----

This package has the same license as the original snowflake-sqlalchemy package (Apache License Version 2.0, January 2004)
