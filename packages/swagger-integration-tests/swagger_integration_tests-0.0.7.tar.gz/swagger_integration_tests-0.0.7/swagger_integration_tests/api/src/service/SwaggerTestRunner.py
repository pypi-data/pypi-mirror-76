import json
from swagger_integration_tests.api.src.service import SwaggerIntegrationTests
from python_helper import ObjectHelper

integration = SwaggerIntegrationTests

def runTestSet(swagger,testSet) :
    for tagSet in testSet.keys() :
        for testName in testSet[tagSet] :
            testCase = swagger.getTestCase(tagSet,testName)
            for testCaseKey,testCaseValues in testCase.items() :
                runTestCase(swagger,tagSet,testCaseKey,testCaseValues)

def runTestCase(swagger,tagSet,testCaseKey,testCaseValues) :
    url = getUrl(swagger,testCaseValues)
    tag = getTag(swagger,testCaseValues,tagSet)
    method = swagger.getFilteredSetting(integration.METHOD,testCaseValues)
    verb = swagger.getFilteredSetting(integration.VERB,testCaseValues)
    authorizaton = getAuthoization(swagger,testCaseValues)
    processingTime = swagger.getFilteredSetting(integration.PROCESSING_TIME,testCaseValues)
    pathVariableSet = swagger.getFilteredSetting(integration.PATH_VARIABLE_SET,testCaseValues)
    payload = swagger.getFilteredSetting(integration.REQUEST,testCaseValues)
    expectedResponse = swagger.getFilteredSetting(integration.EXPECTED_RESPONSE,testCaseValues)
    ignoreKeyList = getIgnoreKeyList(swagger,testCaseValues)
    response = swagger.runTest(url,tag,method,verb,authorizaton,processingTime,pathVariableSet,payload,expectedResponse)

    filteredExpectedResponseAsDict = ObjectHelper.filterIgnoreKeyList(getObjectAsJson(swagger,expectedResponse),ignoreKeyList)
    filteredResponseAsDict = ObjectHelper.filterIgnoreKeyList(getObjectAsJson(swagger,response),ignoreKeyList)
    success = ObjectHelper.equal(filteredResponseAsDict,filteredExpectedResponseAsDict)
    print(f'''
        {testCaseKey}
        ''')
    if success :
        logContent = f'''
        {integration.SUCCESS_MESSAGE}'''
    else :
        logContent = f'''Test-failed :
        {integration.URL} ==> {url}
        {integration.TAG} ==> {tag}
        {integration.METHOD} ==> {method}
        {integration.VERB} ==> {verb}
        {integration.PROCESSING_TIME} ==> {processingTime}
        {integration.PATH_VARIABLE_SET} ==> {pathVariableSet}
        {integration.REQUEST} ==> {payload}
        {integration.EXPECTED_RESPONSE} ==> {expectedResponse}
        {integration.RESPONSE} ==> {response}'''
    print(logContent + '\n\n')
    return persistLog(swagger,testCaseKey,logContent)

def getUrl(swagger,testCaseValues) :
    url = swagger.getFilteredSetting(integration.URL,testCaseValues)
    if not url :
        return swagger.mainUrl
    return url

def getAuthoization(swagger,testCaseValues) :
    authorizaton = swagger.getFilteredSetting(integration.AUTHORIZATION,testCaseValues)
    if not authorizaton :
        return swagger.authorizationAdmin
    return authorizaton

def getTag(swagger,testCaseValues,tagSet) :
    tag = swagger.getFilteredSetting(integration.TAG,testCaseValues)
    if not tag :
        return tagSet
    return tag

def getIgnoreKeyList(swagger,testCaseValues) :
    ignoreKeyList = swagger.getFilteredSetting(integration.IGNORE_KEY_VALUE_LIST,testCaseValues)
    if ignoreKeyList :
        return ignoreKeyList
    return []

def getObjectAsJson(swagger,objectAsString) :
    try :
        return json.loads(objectAsString)
    except Exception as exception :
        swagger.globals.error(swagger.__class__,'error in Json converion',exception)

def persistLog(swagger,testCaseKey,logContent) :
    try :
        if 'Test-failed' in logContent :
            return swagger.repository(testCaseKey,logContent)
    except Exception as exception :
        swagger.globals.error(swagger.__class__,f'''couldn't persist {testCaseKey} log content''',exception)
