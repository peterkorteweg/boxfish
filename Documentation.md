<img src="D:\Projects\Python\projects\boxfish\boxfish.svg" width="100%">

# Documentation

Boxfish, a lightweight tool for table extraction from HTML pages.

# Contents 

[Quick Start](#Quick Start)   
[Build a configuration](#Build a configuration)  
- [Get/set parameters](#Get/set parameters)
- [Build a table configuration](#Build a table configuration)
- [Build a next page configuration](#Build a next page configuration)

[Extract a table](#Extract a table)  
[Examples](#Examples)


# Quick Start

``` python
import boxfish as bf
import pandas as pd

# Define table layout of an url with strings from two rows.
aurl = ''
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

Boxfish uses a configuration to describe the parameters for table extraction. After building a configuration boxfish can extract tables for pages with the same HTML structure.

[Top](#Documentation)

# Build a configuration

<code>build(config=None, url='', rows=None, next_page=''))</code>

A configuration is a dictionary which contains parameters for extracting a table. 
Parameters are divided into three keys: [driver](#Driver), [html](#Html) and [output](#output).

To build a configuration with default parameters write:

``` python
aconfig = bf.build(url=aurl)
```

## Get/set parameters
Most parameters can be set directly as values in a dictionary. 

``` python
aconfig['driver']['package'] = 'requests'
```

Keys that cannot be set directly, should be set with <code>build</code>. See
[driver](#Driver), [html](#Html) and [output](#output) for a description of sub-keys that can be set directly.

## Driver
Driver contains parameters for the driver to access the HTML page. Boxfish supports the driver packages
`requests` and `selenium`. 

| Parameter     | Description                   |
|---------------|:------------------------------|
| package       | Driver package                |
| sleep         | Sleep                         |
| requests      | Requests parameters           |
| selenium      | Selenium parameters           |

**package : str**  
Driver package name. The options are `requests` and `selenium`. 

``` python
aconfig['driver']['package'] = 'requests'
```

**sleep : dict**   
A dictionary with key-value pairs. Each key represents a number of calls, and each value represents a number of seconds boxfish sleeps, after key driver calls.

``` python
aconfig['driver']['sleep'] = {'1': 1, '200' : 3600}
```

### requests : dict
A dictionary with parameters for the `requests` driver.

| Parameter      | Description                  |
|----------------|:-----------------------------|
| headers        | HTTP headers                 |
| timeout        | Timeout                      |

**headers: dict**  
A dictionary with HTTP headers. If no header is set boxfish uses a default header. 

``` python
aconfig['driver']['headers'] = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "accept-language": "nl,en-US;q=0.7,en;q=0.3",
            "accept-encoding": "gzip, deflate, br"}
```

**timeout: int**   
Timeout for requests, in seconds. If no response is received before timeout, the
request is cancelled.

``` python
aconfig['driver']['timeout'] = 10
```

### selenium  : dict
A dictionary with parameters for the `selenium` driver.

| Parameter      | Description                   |
|----------------|:------------------------------|
| filename       | Filename driver               |
| log            | Filename log                  |
| headless       | Browser mode                  |


**filename : str**    
Location of the selenium driver file. Boxfish supports the Chrome driver and Gecko driver. 

``` python
aconfig['driver']['selenium']['filename'] = r'..\\..\\drivers\\geckodriver.exe'
```

**log : str**    
Location of the log file of the selenium driver.

``` python
aconfig['driver']['selenium']['log'] = r'..\\..\\drivers\\geckodriver.log'
```

**headless : bool**    
If False, set Windows driver to visible.\
If True, set Windows driver to invisible (i.e. headless)

``` python
aconfig['driver']['selenium']['headless'] = True
```

## Html
Html contains parameters to access table data on an HTML page. 

| Parameter      | Description                   |
|----------------|:------------------------------|
| url            | URL address                   |
| parser         | HTML parser                   |
| table          | Table layout                  |
| page           | Next page                     |

**url : str**  
The url which contains a default page for table extraction.

``` python
aconfig['html']['url'] = aurl
```

**parser: str**  
The html parser. Boxfish uses a parser to access HTML with BeautifulSoup. For more information on parser options see [BS4 parsers](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser).

``` python
aconfig['html']['parser'] = 'html.parser'
```

Parameters for [table](#Build a table configuration) and [page](#Build a next page configuration) are set with <code>build</code>. 

## Output
Output contains parameters to save results to csv files. 

| Parameter     | Description                   |
|---------------|:------------------------------|
| filename      | Filename table                |
| date_format   | Filename date format          |
| overwrite     | Overwrite existing file       |

``` python
aconfig['output']['filename'] = 
aconfig['output']['date_format'] = '%Y%m%d'
aconfig['output']['overwrite'] = True
```

**filename : str**    
Filename of output csv file. If date_format is set, boxfish appends a timestamp to the filename.  

**date_format: str**    
Date format for timestamp. If date_format is set, boxfish appends a timestamp to the filename.  

**overwrite: bool**   
If False, append to existing file.
If True, overwrite existing file. 

## Build a table configuration
Use  <code>build</code> method to add a table configuration to a boxfish configuration.  

``` python
aconfig = bf.build(config=aconfig, url=aurl, rows=arows)
```

**config (optional): dict**  
If a config is provided, the table configuration is added to the configuration. Otherwise, the table configuration is added to a default configuration.

**url : str**  
The url to HTML page that contains the table that you want to extract.  

**rows : list**  
Rows should contain two strings with text from two different rows of the table that you want to extract.

## Build a next page configuration
Use <code>build</code> to add a next page configuration to a boxfish configuration.

``` python
aconfig = bf.build(config=aconfig, url=aurl, next_page=next_page)
```

**config (optional): dict**  
If a config is provided, the table configuration is added to the configuration. Otherwise, the table configuration is added to a default configuration.

**url (optional): str**  
The url to HTML page that contains the table that you want to extract. If no url is provided the method uses <code>config[html][url]</code>.

**next_page : str**  
An url that refers to the next page. The next page link must also be present on page provided by url.

 
[Top](#Documentation)

# Extract a table
Use <code>extract</code> method to extract a table from an HTML page. 

``` python
data = bf.extract(url=aurl, config=aconfig)
```

**url (optional): str**  
The url to HTML page that contains the table that you want to extract. If no url is provided the method uses <code>config[html][url]</code>. 

**config : dict**  
A configuration to extract a table.


[Top](#Documentation)

# Examples

Some examples using scrape test sites. For all examples first import boxfish and pandas.

``` python
import boxfish as bf
import pandas as pd
``` 

## Scrape This

### Single page 

``` python
aurl = 'https://www.scrapethissite.com/pages/simple/'
arows = ['Andorra', 'Antigua and Barbuda']

aconfig = bf.build(config=aconfig, url=aurl, rows=arows)

data = bf.extract(url=aurl, config=aconfig)
df = pd.DataFrame(data)
df.head()
```

### Multiple pages 

``` python
aurl = 'https://www.scrapethissite.com/pages/forms/?page_num=1'
arows = ['Boston Bruins', 'Buffalo Sabres']
aconfig = bf.build(config=aconfig, url=aurl, rows=arows)

next_page = 'https://www.scrapethissite.com/pages/forms/?page_num=2'
aconfig = bf.build(config=aconfig, next_page=next_page)

data = bf.extract(url=aurl, config=aconfig)
df = pd.DataFrame(data)
df.head()
```

## To Scrape

### Single page

``` python
# Use homepage to build configuration
aurl = 'https://books.toscrape.com/'
arows = ['A Light in the ...', 'Tipping the Velvet']

aconfig = bf.build(config=aconfig, url=aurl, rows=arows)

# Extract table from another page
aurl = 'https://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html' 

data = bf.extract(url=aurl, config=aconfig)
df = pd.DataFrame(data)
df.head()
```

## Wikipedia

Wikipedia offers free access to its content. See [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Copyrights) for more information on its copyright terms. 

``` python
# Use homepage to build configuration
aurl = 'https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3'
arows = ['ABW', 'AFG']

aconfig = bf.build(config=aconfig, url=aurl, rows=arows)

data = bf.extract(url=aurl, config=aconfig)
df = pd.DataFrame(data)
df.head()
```

[Top](#Documentation)