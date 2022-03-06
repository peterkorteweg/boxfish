#Documentation

Boxfish, a lightweight tool for table extraction from HTML pages.

##Contents 

[Quick Start](#Quick Start)   
[Building a configuration](#Building a configuration)  
- [Get/set](#Get/Set parameters)
- [Table](#Build a table configuration)
- [Next page](#Build a next page configuration)

[Extracting a table](#Extracting a table)  
[Examples](#Examples)


##Quick Start

``` python
import boxfish as bf
import pandas as pd

# Define table layout of an url with strings from two rows.
aurl =  
row1 = ''
row2 = ''

# Build a configuration 
aconfig = bf.build(url=aurl, astr = [row1, row2])

# Extract a table
data = bf.extract(aconfig, url=aurl)

# View results
df = pd.DataFrame(data)
df.head() 
```

[Top](#Documentation)

##Building a configuration

A configuration is a dictionary which contains parameters for extracting a table. 
Parameters are divided into three keys: [driver](#Driver), [html](#Html) and [output](#output).

###Get/Set parameters

###Build a table configuration

###Build a next page configuration


###Driver
Driver contains parameters for the driver to access the HTML page. Boxfish supports the driver packages
**requests** and **selenium**. The parameters are:

| Parameter     | Description                   |
| ------------- |:------------------------------|
| package       | Driver package                |
| headers       | HTTP headers                  |
| timeout       | Timeout                       |
| sleep         | Sleep                         |
| filename      | Filename driver (selenium)    |
| log           | Filename log (selenium)       |
| headless      | Browser mode (selenium)       |

###Html
Html contains parameters to access table data on an HTML page. The parameters are: 

| Parameter     | Description                   |
| ------------- |:------------------------------|
| url           | URL address                   |
| parser        | HTML parser                   |
| id            | Page id                       |
| rows          | Table rows                    |
| columns       | Table columns                 |
| page          | Next page                     |

###Output
Output contains parameters to save results to disk. The parameters are:

| Parameter     | Description                   |
| ------------- |:------------------------------|
| filename      | Filename table                |
| date_format   | Filename date format          |
| overwrite     | Overwrite existing file       |

[Top](#Documentation)

##Extracting a table

[Top](#Documentation)

##Examples

[Top](#Documentation)