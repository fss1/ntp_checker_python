
# Project Title

NTP Checker in Python 


## Run Locally

Clone the project

```bash
  git clone https://fss1/ntp_checker_python
```

Go to the project directory

```bash
  cd ntp_checker_python
```

Install dependencies

```bash
pip install ntplib ping3
```

run the script

```bash
  python3 twatch.py
```


## Appendix

twatch.py is a test script in Python to replace the old ntp_checker Timewatch script 

Instead of Net::NTP for Perl, Python's ntplib is used.  Sources to be tested are defined in the SQLite3 my_ntp_sources.db3 file stored in the same directory as this script.  Check out the example using <https://sqlitebrowser.org/>

Each group name in the database will create a JSON blob in a file containing the query results 
Currently the \<group_name\>.json files 

The database has the following columns:
- IP: For the NTP source to be checked.  This can also be a hostname.
- Hostname: Optional text name of NTP server
- Description: Optional text description of NTP server
- NTPCheck:  1 to be checked, 0 to be skipped (intended to disable test without removing server from database)
- MonitorGroup: Group name for all the NTP servers to be included in the MonitorGroup-name.json file
- SendGroupAlert: 1 to send, 0 to stay silent 
- UpperLimit: Upper alert threshold in seconds between ref time and measured time
- LowerLimit: Lower alert threshold in seconds between ref time and measured time
- ExtRefs:  IP or hostname of acceptable references (upstream NTP servers).  NULL if not to be checked
- ErrorsBeforeAlert: How many successive errors need to exist before an alert is generated
- Status:  Text note
- Owner:  Text note
- Comment:  Text note

The Python version of NTP Checker was intended to replace or supplement the previous Graphana screen by importing the JSON NTP data into Splunk.  
Currently it only produces json files.

Alerting has not yet been implemented

This is work in progress...


## Authors

- <fss1138@gmail.com>


## Installation

Install twatch.py along with the my_ntp_sqlite3.db file in the folder of your choice or create a venv including the modules ntplib and ping3

```
 pip install ntplib ping3
```
    