# This software is licenced under the same terms a Python 3.9
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted.  DEEV March2022

import sqlite3 # core module
import json # core module
import ntplib # pip install ntplib
from ping3 import ping # pip install ping3; ping for python3 (not pyping)
from time import ctime
from datetime import datetime, timezone


''' Test script for Timewatch4 '''

# read the NTP client database
db = sqlite3.connect('file:my_ntp_sources.db3?mode=ro', uri=True) # open db read only
c = db.cursor() # create a cursor object
# extract all the IPs (these are the primary key so no need to deduplicate)
c.execute("SELECT IP FROM ntp_sources WHERE NTPCheck = 1") # execute sql to extract active IPs
ips = c.fetchall() # fetchall rows from the result set
# extract all the groups and deduplicate
c.execute("SELECT MonitorGroup FROM ntp_sources WHERE NTPCheck = 1") # extract active groups
groups = c.fetchall() # fetchall rows from the result set
ddgroups = set(groups) # deduplicate the groups 

def pingme (pingip):
    try: 
        presult = ping(*ip) 
        if presult == None:
            return ('no reply')
        elif presult == False:
            return ('test could not resolve address')
        elif presult  >= 0:
            return (presult)
    except OSError as e: # OSError if A socket operation was attempted to an unreachable network
            return (e)

def alert_check (cur, hostip):
    cur.execute("SELECT SendGroupAlert FROM ntp_sources WHERE IP = ?", hostip)
    alert = cur.fetchone()
    # print ('alert check:',*alert) # this is a tuple list (1,) so needs unpacking
    if alert[0] == 1:
        return (1)
    else:
        return(0)

# To also select the MonitorGroup: SELECT IP, MonitorGroup FROM ntp_sources WHERE NTPCheck = 1
# To find ExtRefs for ip variable: "SELECT ExtRefs FROM ntp_sources WHERE IP = ?, ip"

# setup NTP client and test access to europe.pool.ntp.org
client = ntplib.NTPClient() # create NTP client object
try:
    req = client.request('europe.pool.ntp.org', version=3) # make ntp request
except:
	print('Failed request for time from europe.pool.ntp.org')
else:
    print ('Current date & UTC time:',datetime.fromtimestamp(req.tx_time, timezone.utc))
    print(f'Time offset from europe.pool: {req.offset} seconds, stratum: {req.stratum}, LI: {req.leap}')
    ref = ntplib.ref_id_to_text(req.ref_id, req.stratum) # ref_id needs converting to readable text
    print(f'Reference used by europe.pool: {ref}')

for gp in ddgroups: # for each (deduplicated) group, check the IP
    # print (*gp, ' ', end ='')
    # created filename based on group for json output
    outfile = gp[0] + '_multiline.json'
    outfile_pretty = gp[0] + '_pretty.json'
    
    c.execute("SELECT IP FROM ntp_sources WHERE NTPCheck = 1 AND MonitorGroup =?",gp)
    group_ips = c.fetchall()
    # print ('IPs for group ', gp, 'are: ', *group_ips)
    print ('\n---- Checking', *gp, 'group ----')
    # ref_status = 'invalid' # refernce check, set to valid if match found
    for ip in group_ips:
        alert_status = 'OK' # or replace with error
        alert_enabled = alert_check(c, ip) # query database for SendGroupAlert state
        print('\nchecking: ', *ip, 'in group:', *gp)
        # extract permissive references from database
        c.execute("SELECT ExtRefs FROM ntp_sources WHERE ExtRefCheck = 1 AND IP = ?",ip)
        
        extrefs = c.fetchone()
        if extrefs == None:
            print ('No external references were defined')
           
        else:
            print('External references permitted are: ', end='')
            for r in extrefs:
                print(r,end=' ')
            print('')
        # extract upper and lower offset limit from databse
        c.execute("SELECT LowerLimit, UpperLimit FROM ntp_sources WHERE IP = ?",ip)
        limits = c.fetchone()
        pingtime = pingme(*ip)
        try:
            req = client.request( *ip, version=3)
        except ntplib.NTPException as e:
            print('Socket time out for NTP request.', e, 'Ping: ', pingtime)
            alert_status = 'Socket time out for NTP request.' + str(e)
            print('GroupAlert', alert_check(c, ip), *gp)
        except OSError as e: # OSError if A socket operation was attempted to an unreachable network
            print('NTP request failed: ', e) # if network unreachable no point in ping test
            alert_status = 'NTP request failed: ' + str(e)
            print('GroupAlert', alert_check(c, ip), *gp)

    
        else: # print the NTP and ping stats
            # convert ref ip to text.  Stratum 1 string found containing null so nulls removed.
            ref = ntplib.ref_id_to_text(req.ref_id, req.stratum).replace('\x00', '') 
            if extrefs == None:
                 ref_status = 'permissive references not checked.'
            else:
                for extr in extrefs:
                    if ref in extr or extr in ref: 
                        # has to work both ways so premissive ref such as 'MRS' can be found within "Unidentified reference source 'MRS '"
                        ref_status = f'{ref} is a permitted reference.'
                    else:
                        ref_status = f'Warning! {ref} is not a permitted reference source.'
            # stratum 1 response will be looked up and identified by libntp if listed
            # Meinbergs Multi Reference Source is not in the table and shows as
            #  Unidentified reference source MRS
            # stratum 2 and higher is decoded as an IP by libntp. 'stratum =' not required if always >= 2
            # leap indicator table decodes indicator into english: ntplib.NTP.LEAP_TABLE[req.leap]
            print(ref_status, 'Offset Limits; lower, upper:', limits[0], ',', limits[1])
            if not limits[0] < req.offset < limits[1]:
                print('Offset outside specified limits')
                print('GroupAlert', alert_check(c, ip), *gp)
                offset_status = 'FAILED - outside limits'
                alert_status = 'FAILED - outside offset limits'
                
            else:
                offset_status = 'OK'
                
            print(f'offset: {req.offset} sec, Delay: {req.delay} sec, stratum: {req.stratum}, LI: {req.leap} {ntplib.NTP.LEAP_TABLE[req.leap]}, Ref: {ref}, Ping: {pingtime}')
            
            # put the required stats into this dictionary
            logtime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

            ntp_stats = {
                'utp time': logtime,
                'host ip': ip[0],
                'group': gp[0],
                'offset': req.offset,
                'lower offset limit': limits[0],
                'upper offset limit': limits[1],
                'offset status':offset_status,
                'delay': req.delay,
                'stratum': req.stratum,
                'leap indicator': req.leap,
                'ref': ref,
                'ref status': ref_status,
                'ping': pingtime,
                'alert status': alert_status,
                'alert enabled': alert_enabled
            }
            # print(ntp_stats)
            
            # dump dict as json to file
            with open(outfile, 'a') as jsout, open(outfile_pretty, 'a') as jsoutp:
                json.dump(ntp_stats, jsout)
                jsout.write('\n') # add a new line between each json entry
                jsout.close()
                # same as above but an indented file for humans
                json.dump(ntp_stats, jsoutp, indent=2)
                jsoutp.write('\n')
                jsoutp.close()
                #TODO may need to create one big json file with a single root entry 
                
            
