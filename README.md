
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

## Example output using sample db3 file

The example db3 has tagged the NTP sources with the following group names:  
Devs, ITSupport, LinuxTeam, External, ADTEeam, Gladis
  
../ntp_checker_python# python3 twatch.py  
Current date & UTC time: 2022-03-30 15:13:50.055315+00:00  
Time offset from europe.pool: -0.11015892028808594 seconds, stratum: 2, LI: 0  
y europe.pool: 194.58.202.148  
  
---- Checking Devs group ----  
  
checking:  0.0.0.1 in group: Devs  
No external references were defined  
Socket time out for NTP request. No response received from 0.0.0.1. Ping:  no reply  
GroupAlert 1 Devs  
  
---- Checking ITSupport group ----  
  
checking:  10.20.74.141 in group: ITSupport  
No external references were defined  
Socket time out for NTP request. No response received from 10.20.74.141. Ping:  no reply  
GroupAlert 0 ITSupport  
  
---- Checking LinuxTeam group ----  
  
checking:  192.53.103.104 in group: LinuxTeam  
No external references were defined  
permissive references not checked. Offset Limits; lower, upper: -0.3 , 0.3  
offset: -0.11289691925048828 sec, Delay: 0.04291534423828125 sec, stratum: 1, LI: 0 no warning, Ref: European telephone modem, Ping: no reply  
  
---- Checking External group ----  
  
checking:  139.143.5.30 in group: External  
No external references were defined  
permissive references not checked. Offset Limits; lower, upper: -0.3 , 0.3  
offset: -0.1127932071685791 sec, Delay: 0.022999286651611328 sec, stratum: 2, LI: 0 no warning, Ref: 139.143.45.145, Ping: no reply  
  
checking:  139.143.5.31 in group: External  
No external references were defined  
permissive references not checked. Offset Limits; lower, upper: -0.3 , 0.3  
offset: -0.1127016544342041 sec, Delay: 0.022455692291259766 sec, stratum: 2, LI: 0 no warning, Ref: 139.143.45.145, Ping: no reply  
  
checking:  europe.pool.ntp.org in group: External  
No external references were defined  
permissive references not checked. Offset Limits; lower, upper: -0.3 , 0.3  
offset: -0.10941314697265625 sec, Delay: 0.044216156005859375 sec, stratum: 2, LI: 0 no warning, Ref: 194.58.202.148, Ping: 0.059770822525024414  
  
---- Checking ADTeam group ----  
  
checking:  192.53.103.108 in group: ADTeam  
No external references were defined  
permissive references not checked. Offset Limits; lower, upper: -0.3 , 0.3  
offset: -0.11337089538574219 sec, Delay: 0.043872833251953125 sec, stratum: 1, LI: 0 no warning, Ref: European telephone modem, Ping: no reply  
  
---- Checking Gladis group ----  
  
checking:  127.0.0.1 in group: Gladis  
No external references were defined  
permissive references not checked. Offset Limits; lower, upper: -0.3 , 0.3  
offset: -2.6226043701171875e-06 sec, Delay: 6.437301635742188e-05 sec, stratum: 3, LI: 0 no warning, Ref: 10.254.191.254, Ping: 0.00018548965454101562  
  
The following files containing the NTP output were created:
  
ADTeam_multiline.json  
ADTeam_pretty.json  
External_multiline.json  
External_pretty.json  
Gladis_multiline.json  
Gladis_pretty.json  
LinuxTeam_multiline.json  
LinuxTeam_pretty.json  

../ntp_checker_python# cat External_pretty.json
```
{
  "utp time": "2022-03-30 15:14:16",
  "host ip": "139.143.5.30",
  "group": "External",
  "offset": -0.1127932071685791,
  "lower offset limit": -0.3,
  "upper offset limit": 0.3,
  "offset status": "OK",
  "delay": 0.022999286651611328,
  "stratum": 2,
  "leap indicator": 0,
  "ref": "139.143.45.145",
  "ref status": "permissive references not checked.",
  "ping": "no reply",
  "alert status": "OK",
  "alert enabled": 1
}
{
  "utp time": "2022-03-30 15:14:20",
  "host ip": "139.143.5.31",
  "group": "External",
  "offset": -0.1127016544342041,
  "lower offset limit": -0.3,
  "upper offset limit": 0.3,
  "offset status": "OK",
  "delay": 0.022455692291259766,
  "stratum": 2,
  "leap indicator": 0,
  "ref": "139.143.45.145",
  "ref status": "permissive references not checked.",
  "ping": "no reply",
  "alert status": "OK",
  "alert enabled": 1
}
{
  "utp time": "2022-03-30 15:14:20",
  "host ip": "europe.pool.ntp.org",
  "group": "External",
  "offset": -0.10941314697265625,
  "lower offset limit": -0.3,
  "upper offset limit": 0.3,
  "offset status": "OK",
  "delay": 0.044216156005859375,
  "stratum": 2,
  "leap indicator": 0,
  "ref": "194.58.202.148",
  "ref status": "permissive references not checked.",
  "ping": 0.059770822525024414,
  "alert status": "OK",
  "alert enabled": 1
}
```


## Authors

- <fss1138@gmail.com>


## Installation

Install twatch.py along with the my_ntp_sqlite3.db file in the folder of your choice or create a venv including the modules ntplib and ping3

```
 pip install ntplib ping3
```
    
