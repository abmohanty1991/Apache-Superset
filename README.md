
# Business Intelligence Capability inclusion using Apache Superset into an existing Grails OLTP web application

Business Intelligence capabilities are crucial for echelons to take informed decisions and draw insights about the various facets of business. This project enumerates steps and nuances of incorporating Business Intelligence capabilities using Apache Superset and embed the same into an existing OLTP application built using Grails.



## Tech Stack

**OLAP Application:** Apache Superset 

**OLAP Database:** PostgreSQL

**OLTP Application:** Grails

**OLTP Database:** Oracle

**OLTP-OLAP Replication:** ReplicaDB

**OS:** Cent OS 9 / RHEL Distribution




## Documentation

[Apache Superset](https://superset.apache.org/docs/)

[ReplicaDB](https://osalvador.github.io/ReplicaDB/docs/docs.html)




## Architecture

![arch](https://user-images.githubusercontent.com/108822178/227702453-ac2be4c2-147e-429f-93b0-6418a326435f.png)


## Installation

Install Dependencies

```bash
  sudo dnf install gcc gcc-c++ libffi-devel python3-devel python3-pip python3-wheel openssl-devel cyrus-sasl-devel openldap-devel
```

Install & activate virtualenv

```bash
  pip install virtualenv
  . venv/bin/activate
```
Install Apache Superset

```bash
  pip install apache-superset
```
Set environment variable

```bash
  export FLASK_APP=superset
```

Upgrade db, create admin, load examples and initiate

```bash
  superset db Upgrade
  superset fab create-admin
  superset load_examples
  superset init
```

Run the Development server to check installation (this is just the development server, process to run in production using wsgi server is mentioned later)

```bash
  superset run -p 8088 -h 0.0.0.0
```


## DB driver installation

PostgreSQL database has been utilised here as the OLAP database (the user is free to choose any database as Superset supports a wide range of databases)

```bash
  pip install psycopg2
```

## Synchronisation between the OLTP and the OLAP database using ReplicaDB

As OLAP does notnecessarily require latest data, the synchronisation can be set up as a job that runs every 2 hours(or as per the convinient periodicity) using replicadb. To install ReplicaDB download the file and unzip it

```bash
   curl -o ReplicaDB-0.15.0.tar.gz -L "https://github.com/osalvador/ReplicaDB/releases/download/v0.15.0/ReplicaDB-0.15.0.tar.gz"
   tar -xvzf ReplicaDB-0.15.0.tar.gz
   ./bin/replicadb --help
```

ReplicaDB can take the source and sink table along with the connection string in the command line itself or optionally we can make use of a replicadb.conf file which holds the necessary source and sink table and connection properties. An example of a replicadb.conf file to undertake replication from a Oracle table to a PostgreSQL table is as follows:-

```bash
######################## ReplicadB General Options ########################
mode=complete
jobs=1
############################# Soruce Options ##############################
source.connect=jdbc:oracle:thin:@${ORAHOST}:${ORAPORT}:${ORASID}
source.user=${ORAUSER}
source.password=${ORAPASS}
source.table=orders
############################# Sink Options ################################
sink.connect=jdbc:postgresql://${PGHOST}/osalvador
sink.table=orders
```

Finally we pass the name of the conf file as follows
```bash
replicadb --options-file replicadb.conf  
```


## Bypassing the login mechanism for embedding Superset charts and dashboards into the web app

Superset renders its own authentication system wherein users can login and utilise the app. However, for the users utilising the OLTP application, the charts built using Superset are required to be embedded inside the web app. For this, the access to charts and graphs needs to be provided (without the option to edit/create the chart or access the dataset/SQL lab). 

The behaviour of Superset is configured using the parameters in the config.py file in the installation directory of superset. The parameters that need to be altered are mentioned as follows.

## Enabling CORS

For the web application to access the SUperset charts which is hosted at a different location, the Cross-Origin Resource Sharing is required to be set up. For this set the following parameter in config.py

`ENABLE_CORS = True`

```Bash
CORS_OPTIONS = {
'supports_credentials' : True,
'allow_headers' : ['*'], ## Customize this as per the requirements
'resources' : ['*'],
'origins' : [''address of the OLTP web app']
}
```
Fire the command ```superset init``` and ```superset run -h 0.0.0.0 -p 8088``` after making changes to the config file.


## Using <iframe> for embedding the dashboards
After logging in to Superset, either we can use the Embed chart/dashboard option to generate the iframe code block or we can just copy the URL and append standalone=true in the end to make it work. Also we would like to hide the top navigation pane, and for that filterPaneEnabled will have to be set to false as follows:

```
http://localhost:8088/superset/dashboard/12/?standalone=true&filterPaneEnabled=false
```

The iframe tag example can be as follows:

```
<iframe 
src="http://localhost:8088/superset/dashboard/12/?standalone=true&filterPaneEnabled=false" 
height="200" 
width="300">
</iframe>
```

## Deployng in Production using Gunicorn WSGI Server
The known configuration of Gunicorn known to be running fine, as mentioned in Official SUperset documentation is as follows :

```
      gunicorn
      -w 10 \
      -k gevent \
      --worker-connections 1000 \
      --timeout 120 \
      -b  0.0.0.0:6666 \
      --limit-request-line 0 \
      --limit-request-field_size 0 \
      --statsd-host localhost:8125 \
      "superset.app:create_app()"
```

## Caution

In previous vulnerability reportsof Apache SUperset, enabling the ``` ENABLE_TEMPLATE_PROCESSING = True ``` has been known to be open to SQL Injection. SO be aware while using this option.

## Conclusion

And there you have it, Apache Superset dashboards fully integrated with the GRails Web application. The users will have a fully responsive dashboard presented to them, without any access to edit or create a dashboard. However, users with admin priviledge can log into superset and create/edit charts/dashboards.

If this project was helpful, please send me a coffee !!!!






