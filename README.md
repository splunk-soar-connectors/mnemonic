[comment]: # "Auto-generated SOAR connector documentation"
# Mnemonic

Publisher: Splunk  
Connector Version: 2.0.7  
Product Vendor: Mnemonic  
Product Name: Passive DNS  
Product Version Supported (regex): ".\*"  
Minimum Product Version: 5.1.0  

This app integrates with the Mnemonic Passive DNS API to implement investigative actions

### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a Passive DNS asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**domain** |  optional  | string | Domain to check connectivity (Default: phantom.us)

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
**range** |  optional  | Range (min_offset-max_offset), default is 0-100 | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.domain | string |  `domain`  `url`  |   https://test.us  test.us 
action_result.parameter.range | string |  |   1-1  0-17 
action_result.data.\*.answer | string |  `ip`  |   52.91.186.198 
action_result.data.\*.createdTimestamp | numeric |  |   0 
action_result.data.\*.customer | string |  |  
action_result.data.\*.firstSeenTimestamp | numeric |  |   1487193402522 
action_result.data.\*.firstSeenTimestampString | string |  |   2017-02-15 13:16:42 PST 
action_result.data.\*.lastSeenTimestamp | numeric |  |   1509969898297 
action_result.data.\*.lastSeenTimestampString | string |  |   2017-11-06 04:04:58 PST 
action_result.data.\*.lastUpdatedTimestamp | numeric |  |   0 
action_result.data.\*.maxTtl | numeric |  |   600 
action_result.data.\*.minTtl | numeric |  |   600 
action_result.data.\*.query | string |  |   test.us 
action_result.data.\*.rrclass | string |  |   in 
action_result.data.\*.rrtype | string |  |   a 
action_result.data.\*.times | numeric |  |   145 
action_result.data.\*.tlp | string |  |   white 
action_result.summary.items_returned | numeric |  |   3 
action_result.summary.total_items | numeric |  |   3 
action_result.message | string |  |   Items returned: 3, Total items: 3 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 