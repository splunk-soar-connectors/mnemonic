[comment]: # "Auto-generated SOAR connector documentation"
# Mnemonic

Publisher: Splunk  
Connector Version: 2\.0\.6  
Product Vendor: Mnemonic  
Product Name: Passive DNS  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 5\.1\.0  

This app integrates with the Mnemonic Passive DNS API to implement investigative actions

### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a Passive DNS asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**domain** |  optional  | string | Domain to check connectivity \(Default\: phantom\.us\)

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[lookup domain](#action-lookup-domain) - Check for the presence of a domain in a threat intelligence feed  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'lookup domain'
Check for the presence of a domain in a threat intelligence feed

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**domain** |  required  | Domain to lookup | string |  `domain`  `url` 
**range** |  optional  | Range \(min\_offset\-max\_offset\), default is 0\-100 | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.domain | string |  `domain`  `url` 
action\_result\.parameter\.range | string | 
action\_result\.data\.\*\.answer | string |  `ip` 
action\_result\.data\.\*\.createdTimestamp | numeric | 
action\_result\.data\.\*\.customer | string | 
action\_result\.data\.\*\.firstSeenTimestamp | numeric | 
action\_result\.data\.\*\.firstSeenTimestampString | string | 
action\_result\.data\.\*\.lastSeenTimestamp | numeric | 
action\_result\.data\.\*\.lastSeenTimestampString | string | 
action\_result\.data\.\*\.lastUpdatedTimestamp | numeric | 
action\_result\.data\.\*\.maxTtl | numeric | 
action\_result\.data\.\*\.minTtl | numeric | 
action\_result\.data\.\*\.query | string | 
action\_result\.data\.\*\.rrclass | string | 
action\_result\.data\.\*\.rrtype | string | 
action\_result\.data\.\*\.times | numeric | 
action\_result\.data\.\*\.tlp | string | 
action\_result\.summary\.items\_returned | numeric | 
action\_result\.summary\.total\_items | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 