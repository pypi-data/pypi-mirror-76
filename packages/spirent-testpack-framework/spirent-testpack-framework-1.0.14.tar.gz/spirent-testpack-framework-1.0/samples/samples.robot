*** Settings ***
Resource        ${EXECDIR}/test_framework/script/resources.robot

Test Setup      TestInit    TESTCASE_FILE=${CURDIR}${/}${TESTCASE_FILES}[${TEST NAME}]
Test Teardown   TestFinish

*** Variables ***
&{TESTCASE_FILES}   samples.router.001=router_forwarding.yaml
...                 samples.router.002=router_bgp.yaml
...                 samples.bgp.001=bgp_routes_stability.yaml

*** Test Cases ***
samples.router.001
    [Tags]      priority=1
    TestRun

samples.router.002
    [Tags]      priority=2
    TestRun

samples.bgp.001
    [Tags]      priority=2
    TestRun
