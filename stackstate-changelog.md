# StackState Agent Integrations v2 releases

## 1.20.1 / 2022-04-20

* [Fixed] vSphere collection_level setting documentation update [(STAC-14671)](https://stackstate.atlassian.net/browse/STAC-14671)

## 1.20.0 / 2022-04-12
* [Added] Add Dynatrace support for synthetic checks [(STAC-14511)](https://stackstate.atlassian.net/browse/STAC-14511)

## 1.19.0 / 2022-04-08

* [Improvement] Added support for topology element deletes.

## 1.18.0 / 2022-03-01

* [Fixed] AWS topology, Swapped the SQS & Lambda relation to show Lambda as a SQS dependency/child not the other way around

## 1.17.1 / 2022-01-31

* [Fixed] A dependency for vsphere was updated to a version that is not compatible with the version (3.4.6) of py3 cryptography library, updated to 35.0.0.  

## 1.17.0 / 2021-12-17

* [Added] Add support for Raw Metrics in line with the current v2/v3 api format. [(STAC-12434)](https://stackstate.atlassian.net/browse/STAC-12434)
* [Improvement] AWS topology check got support for custom FlowLogs S3 bucket. [(STAC-14622)](https://stackstate.atlassian.net/browse/STAC-14622)
* [Improvement] AWS topology check processes malformed StepFunction definitions. [(STAC-14622)](https://stackstate.atlassian.net/browse/STAC-14622)  
* [Fixed] AWS topology check supports Elastic Load Balancer for Application that targets lambda and has no VPC. [(STAC-14546)](https://stackstate.atlassian.net/browse/STAC-14546)
* [Improvement] Rename `min_collection_interval` to `collection_interval` to communicate that's the expected run time of the check.[(STAC-14364)](https://stackstate.atlassian.net/browse/STAC-14364)
* [Fixed] Dropped default expiry value for health checks when using a main stream as expiry is optional in that case. [(STAC-14364)](https://stackstate.atlassian.net/browse/STAC-14364)

## 1.16.1 / 2021-10-21

* [Fixed] Dynatrace - Added `relativeTime` to all topology API calls [(STAC-14569)](https://stackstate.atlassian.net/browse/STAC-14569)

## 1.16.0 / 2021-10-15

* [Fixed] Fix the type for azureHostNames attribute of Dynatrace component [(STAC-14048)](https://stackstate.atlassian.net/browse/STAC-14048)
* [Improved] Custom Devices support for Dynatrace integration [(STAC-13274)](https://stackstate.atlassian.net/browse/STAC-13274)
* [Fixed] Fixed unwanted merging of hosts on a zabbix instance [(STAC-13977)](https://stackstate.atlassian.net/browse/STAC-13977)
* [Improved] Support StackState common tags in Zabbix [(STAC-13984)](https://stackstate.atlassian.net/browse/STAC-13984)
* [Improved] AWS experimental flowlogs support [(STAC-12981)](https://stackstate.atlassian.net/browse/STAC-12981)
* [Improved] Dynatrace check was split in topology and health checks. [(STAC-14104)](https://stackstate.atlassian.net/browse/STAC-14104)
* [Fixed] SolarWinds Create interface components with MAC address and no IP address [(STAC-14057)](https://stackstate.atlassian.net/browse/STAC-14057) 
* [Added] ServiceNow send Topology Event to StackState before the scheduled Planned Start Date of the Change Request. [(STAC-13256)](https://stackstate.atlassian.net/browse/STAC-13256)
* [Fixed] Cleanup of event payload fields [(STAC-12986)](https://stackstate.atlassian.net/browse/STAC-12986)

## 1.15.0 / 2021-08-02
* [Fixed] SolarWinds Component has multiple health statuses. [(STAC-13796)](https://stackstate.atlassian.net/browse/STAC-13796)
* [Improvement] AWS x-ray integration performance improvements when fetching historic data, as well as schema validation using Schematics.  [(STAC-13551)](https://stackstate.atlassian.net/browse/STAC-13551)
* [Fixed] Unable to load Splunk Topology on Stackstate UI. [(STAC-13564)](https://stackstate.atlassian.net/browse/STAC-13564)
* [Added] Splunk http helper base library. [(STAC-13089)](https://stackstate.atlassian.net/browse/STAC-13089)
* [Added] Health synchronization splunk check to synchronize health states from Splunk into StackState. [(STAC-13174)](https://stackstate.atlassian.net/browse/STAC-13174)
* [Added] SolarWinds integrations that monitors your network landscape and reports it to StackState. [(STAC-13240)](https://stackstate.atlassian.net/browse/STAC-13240)
* [Fixed] AWS Topology ResourceMethodIntegration validation for API Gateway resources.  [(STAC-13604)](https://stackstate.atlassian.net/browse/STAC-13604)
* [Added] Add instance url as an identifier for zabbix integration. [(STAC-13621)](https://stackstate.atlassian.net/browse/STAC-13621)
* [Added] Validation to ensure all lists produced by integrations are homogeneous and all dictionaries contain only string keys.

## 1.14.0 / 2021-07-09

* [Fixed] AWS x-ray check error when `role_arn` is not defined in `conf.yaml`.
* [Fixed] AWS x-ray check memory leak caused by `trace_ids` and `arns`.
* [Fixed] AWS x-ray integration spans produce a span kind to allow StackState to correctly calculate metrics.
* [Added] AWS x-ray integration spans are interpreted to get http response codes.
* [Added] Hostname identifiers for Zabbix hosts.
* [Added] `get_hostname` to AgentCheck base class.
* [Fixed] `event_type` is used as the Event Type in StackState for normal events.
* [Added] SCOM check now support two operation modes, api-based or powershell-based. 
  The operation mode can be switched using `integration_mode` in `conf.yaml`.
* [Fixed] Removed `lastSeenTimestamp` from DynaTrace components to avoid sporadic updates in StackState.
* [Added] AWS Topology integration that monitors your AWS landscape and reports it to StackState.

## 1.13.2 / 2021-04-19

* [Fixed] Fixed out-of-box AWS x-ray check instance error.

## 1.13.1 / 2021-04-14

* [Fixed] Fix out-of-box VSphere check settings to support the Vsphere StackPack.

## 1.13.0 / 2021-03-30

* [Added] Dynatrace - Gathers Dynatrace events for determining health state of Dynatrace components is StackState. 

## 1.12.0 / 2021-03-30

* [Added] Make the check state location configurable in the `conf.d` of the check. See [#123](https://github.com/StackVista/stackstate-agent-integrations/pull/123).

## 1.11.0 / 2021-03-24

* [Added] ServiceNow - Implement query param change for retrieving tags from ServiceNow.

## 1.10.1 / 2021-03-11

* [Fixed] Remove `stackstate-identifier`, `stackstate-environment`, `stackstate-layer`, `stackstate-domain` and `stackstate-identifiers` from the tags object if it has been mapped to the data object.

## 1.10.0 / 2021-03-09

* [Added] Added support to map user defined `stackstate-environment` tags or config to the `environments` object
* [Added] Added support to map user defined `stackstate-layer` tags or config to the `layer` object
* [Added] Added support to map user defined `stackstate-domain` tags or config to the `domain` object
* [Added] Added support to map user defined `stackstate-identifiers` tags or config to the `identifiers` array
* [Added] Added support to map user defined `stackstate-identifier` tag or config to the `identifiers` array
