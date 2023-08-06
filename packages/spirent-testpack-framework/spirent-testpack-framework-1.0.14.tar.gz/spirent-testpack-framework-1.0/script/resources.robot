*** Settings ***
Library     Process
Library     OperatingSystem
Library     test_framework.testbase.gen_testbed_config
Library     Collections

*** Variables ***
${TESTBED_FILE}      testbed.yaml
${validate}         0
${set_dut}  False

*** Keywords ***
TestInit
    [Arguments]         ${TESTCASE_FILE}
    Set Test Variable   ${TEST_DIR}     ${OUTPUT DIR}${/}${TEST NAME}
    Create Directory    ${TEST_DIR}
    Import Variables    ${TESTCASE_FILE}
    Should Be Equal     ${TEST NAME}    ${testcase.id}  Testcase id mismatch, mapping incorrect!
    ${flag} =  Run Keyword And Return Status  Dictionary Should Contain Key  ${TESTCASE_TESTBEDS}  ${TEST NAME}
    Should Be Equal     ${flag}    ${TRUE}  ${TEST NAME} is not in testbed mapping file!
    Generate            ${testbed_config}  ${EXECDIR}/${testcase.run_info.testbed}  ${TESTCASE_TESTBEDS}[${TEST NAME}]  ${TEST_DIR}/${TESTBED_FILE}
    Set Test Variable   &{TEST_INP}    &{testcase.run_info}    testbed=${TESTBED_FILE}    outdir=${TEST_DIR}    testcase_id=${TEST NAME}    set_dut=${set_dut}
    Set Test Variable   ${TEST_CLASS}   ${TEST_INP.script_class}
    Import Library      test_framework.script.test_wrapper.TestWrapper  ${TEST_INP.script_module}  ${TEST_CLASS}  ${TEST_INP}  WITH NAME  ${TEST_CLASS}
TestRun
    [Timeout]           ${TEST_INP.timeout}
    Pass Execution If   ${validate}==1      Done
    Log To Console      \nRunning ${TEST_CLASS}.setup...
    Run Keyword         ${TEST_CLASS}.setup
    Log To Console      Running ${TEST_CLASS}.setup done
    Log To Console      \nRunning ${TEST_CLASS}.run...
    ${RC} =     Run Keyword     ${TEST_CLASS}.run
    Set Test Message    ${RC}
    Log To Console      Running ${TEST_CLASS}.run done

TestFinish
    Pass Execution If   ${validate}==1      ${TEST MESSAGE}
    Log To Console      \nRunning ${TEST_CLASS}.cleanup...
    Run Keyword         ${TEST_CLASS}.cleanup
    Log To Console      Running ${TEST_CLASS}.cleanup done
