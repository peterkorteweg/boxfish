<img src="D:\Projects\Python\projects\boxfish\boxfish.svg" width="100%">

#Documentation

Boxfish, a lightweight tool for table extraction from HTML pages.

#Contents 

[Quick Start](#Quick Start)   
[Building a configuration](#Building a configuration)  
- [Get/set](#Get/set parameters)
- [Table](#Build a table configuration)
- [Next page](#Build a next page configuration)

[Extracting a table](#Extracting a table)  
[Examples](#Examples)


#Quick Start

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

#Building a configuration

A configuration is a dictionary which contains parameters for extracting a table. 
Parameters are divided into three keys: [driver](#Driver), [html](#Html) and [output](#output).

To build a configuration with default parameters use:

``` python
config = bf.build(url=aurl)
```

##Get/set parameters
Most parameters can be set directly as values in a dictionary. 

``` python
config['driver']['package'] = 'requests'
```
The keys below provide an overview of all sub-keys that can be set directly.
Keys that cannot be set directly, should be set with <code>build</code>. 

##Build a table configuration

TODO

##Build a next page configuration

TODO

##Driver
Driver contains parameters for the driver to access the HTML page. Boxfish supports the driver packages
`requests` and `selenium`. 

| Parameter     | Description                   |
| ------------- |:------------------------------|
| package       | Driver package                |
| sleep         | Sleep                         |
| requests      | Requests parameters           |
| selenium      | Selenium parameters           |

**package**  
The driver package. The choices are `requests` and `selenium`. If you choose `selenium`,  
make sure to install `selenium` first. See [Selenium](https://pypi.org/project/selenium/). 

``` python
config['driver']['package'] = 'requests'
```

**sleep**  
A dictionary with key-value pairs. Each key represents a number of calls, and each value
represents a number of seconds boxfish sleeps, after key driver calls.

``` python
config['driver']['sleep'] = {'1': 1, '200' : 3600}
```

###requests  

A dictionary with parameters for the `requests` driver.

| Parameter     | Description                   |
| ------------- |:------------------------------|
| headers       | HTTP headers                  |
| timeout       | Timeout                       |

**headers**  
A dictionary with HTTP headers. If no header is set boxfish uses a default header. 

``` python
config['driver']['headers'] = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "accept-language": "nl,en-US;q=0.7,en;q=0.3",
            "accept-encoding": "gzip, deflate, br"}
```

**timeout**   
Timeout for requests, in seconds. If no response is received before timeout, the
request is cancelled.

``` python
config['driver']['timeout'] = 10
```

###selenium  
A dictionary with parameters for the `selenium` driver.

| Parameter     | Description                   |
| ------------- |:------------------------------|
| filename      | Filename driver               |
| log           | Filename log                  |
| headless      | Browser mode                  |


**filename**    
Location of the selenium driver file. Boxfish supports the Chrome driver and Gecko driver. 

``` python
config['driver']['selenium']['filename'] = r'..\\..\\drivers\\geckodriver.exe'
```

**log**    
Location of the log file of the selenium driver.

``` python
config['driver']['selenium']['log'] = r'..\\..\\drivers\\geckodriver.log'
```

**headless**    
A boolean to determine if the browser window is visible (False) or not visible, 
i.e. headless (True).

``` python
config['driver']['selenium']['headless'] = True
```

##Html
Html contains parameters to access table data on an HTML page. 

| Parameter     | Description                   |
| ------------- |:------------------------------|
| url           | URL address                   |
| parser        | HTML parser                   |
| table         | Table layout                  |
| page          | Next page                     |

**url**  
The url which contains default page for table extraction.

``` python
config['html']['url'] = aurl
```

**parser**  
The html parser. The parser is required to access HTML via BeautifulSoup; see
[BS4 parsers](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser).

``` python
config['html']['parser'] = 'html.parser'
```

Parameters for table and page are set with <code>build</code>. 

##Output
Output contains parameters to save results to csv files. 

| Parameter     | Description                   |
| ------------- |:------------------------------|
| filename      | Filename table                |
| date_format   | Filename date format          |
| overwrite     | Overwrite existing file       |

``` python
config['output']['filename'] = 
config['output']['date_format'] = '%Y%m%d'
config['output']['overwrite'] = True
```


[Top](#Documentation)

#Extracting a table

[Top](#Documentation)

#Examples

[Top](#Documentation)