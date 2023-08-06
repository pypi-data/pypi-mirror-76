from swagger_integration_tests.api.src.service import SwaggerTestRunner
from python_selenium_helper import SeleniumHelper
from python_helper import SettingHelper, log

INTEGRATION = 'integration'

KW_AUTHORIZATION = 'authorization'
KW_MAIN_SWAGGER_URL = 'main-swagger-url'
KW_AUTHORIZATION_ADMIN = f'{KW_AUTHORIZATION}-admin'
KW_AUTHORIZATION_USER = f'{KW_AUTHORIZATION}-user'

TEST_CASE = 'test-case'
URL = 'url'
TAG = 'tag'
METHOD = 'method'
VERB = 'verb'
AUTHORIZATION = KW_AUTHORIZATION
PROCESSING_TIME = 'processing-time'
PATH_VARIABLE_SET = 'query-param-set'
PATH_VARIABLE_SET = 'path-variable-set'
REQUEST = 'request'
RESPONSE = 'response'
EXPECTED_RESPONSE = f'expected-{RESPONSE}'
IGNORE_KEY_VALUE_LIST = 'ignore-key-value-list'

GET = 'GET'
POST = 'POST'
PUT = 'PUT'
PATCH = 'PATCH'
DELETE = 'DELETE'

SUCCESS_MESSAGE = 'Success'

class SwaggerIntegrationTests(SeleniumHelper.SeleniumHelper):

    def __init__(self,globals,**kwargs):
        SeleniumHelper.SeleniumHelper.__init__(self,globals,**kwargs)
        self.integrationPath = f'{globals.apiPath}{globals.baseApiPath}{INTEGRATION}{globals.OS_SEPARATOR}'
        self.mainSwaggerUrlFilePath = f'{self.integrationPath}{INTEGRATION}.{self.globals.extension}'
        self.mainUrl = self.getFilteredSetting(KW_MAIN_SWAGGER_URL,globals.getSettingTree(settingFilePath=self.mainSwaggerUrlFilePath))
        self.authorizationAdmin = self.getFilteredSetting(KW_AUTHORIZATION_ADMIN,globals.getSettingTree(settingFilePath=self.mainSwaggerUrlFilePath))
        self.authorizationUser = self.getFilteredSetting(KW_AUTHORIZATION_USER,globals.getSettingTree(settingFilePath=self.mainSwaggerUrlFilePath))

    def runTestSet(self,testSet):
        try :
            self.newDriver()
            try :
                SwaggerTestRunner.runTestSet(self,testSet)
            except Exception as exception :
                log.error(self.__class__, 'Error runing SwaggerTestRunner.runTestSet() method', exception)
            self.closeDriver()
        except Exception as exception :
            log.error(self.__class__, 'Error runing test set. Most likely related to web_driver', exception)

    def runTest(self,url,tag,method,verb,authorization,processingTime,pathVariableSet,payload,expectedResponse) :
        self.resetValues(url,tag,method,verb,authorization,processingTime,pathVariableSet,payload,expectedResponse)
        swaggerUrl = self.accessSwaggerUrl()
        swaggerTag = self.accessSwaggerTag(swaggerUrl)
        swaggerMethod = self.accessSwaggerMethod(swaggerTag)
        self.hitTryOut(swaggerMethod)
        self.typeAuthorizaton(swaggerMethod)
        self.hitPathVariableSet(swaggerMethod)
        self.typePayload(verb,swaggerMethod)
        self.hitExecute(swaggerMethod)
        self.waitProcessingTime()
        response = self.getResponse(swaggerMethod)
        return response

    def resetValues(self,url,tag,method,verb,authorization,processingTime,pathVariableSet,payload,expectedResponse):
        globals = self.globals
        self.url = url
        self.tag = tag
        self.method = method
        self.verb = verb
        self.authorization = authorization
        self.processingTime = processingTime
        self.pathVariableSet = pathVariableSet
        self.payload = payload
        self.expectedResponse = expectedResponse
        self.findByIdRequest = f'{SwaggerKeyWord.OPERATION_TAG_DASH}{self.tag.replace(globals.SPACE,globals.UNDERSCORE)}'
        self.accessIdRequest = f'{SwaggerKeyWord.OPERATIONS_DASH}{self.tag}-{self.method}{SwaggerKeyWord.USING}{self.verb}'

    def accessSwaggerUrl(self):
        return self.accessUrl(self.url)

    def accessSwaggerTag(self,swaggerUrl):
        return self.accessClass(SwaggerKeyWord.EXPAND_OPERATION,self.findById(self.findByIdRequest,swaggerUrl))

    def accessSwaggerMethod(self,swaggerTag):
        return self.accessId(self.accessIdRequest,swaggerTag)

    def hitTryOut(self,swaggerMethod):
        self.accessButton(self.findByClass(SwaggerKeyWord.TRY_OUT,swaggerMethod))

    def typeAuthorizaton(self,swaggerMethod):
        self.typeInSwagger(self.authorization,self.findBySelector(SwaggerKeyWord.SELECTOR_AUTHORIZATION,swaggerMethod))

    def hitPathVariableSet(self,swaggerMethod):
        if self.pathVariableSet :
            for pathParamKey,pathParamValue in self.pathVariableSet.items() :
                self.hitPathVariable(pathParamKey,pathParamValue,swaggerMethod)

    def hitPathVariable(self,pathParamKey,pathParamValue,swaggerMethod):
        htmlParamList = self.findAllBySelector(SwaggerKeyWord.SELECTOR_TBODY,swaggerMethod)
        for htmlParam in htmlParamList :
            if self.findByClass(SwaggerKeyWord.MARKDOWN,htmlParam).text == pathParamKey :
                self.accessTag(self.TAG_SELECT,htmlParam)
                optionList = self.findAllByTag(self.TAG_OPTION,htmlParam)
                for option in optionList :
                    if option.text == pathParamValue :
                        self.clickElement(option)

    def typePayload(self,verb,swaggerMethod):
        if self.payload :
            if not GET == verb :
                self.typeInSwagger(self.payload,self.findByClass(SwaggerKeyWord.BODY_PARAM,swaggerMethod))
            else :
                self.globals.error(self.__class__,"GET method do not support payload.",None)

    def hitExecute(self,swaggerMethod):
        self.accessButton(self.findByClass(SwaggerKeyWord.EXECUTE_WRAPPER,swaggerMethod))

    def getResponse(self,swaggerMethod):

        return self.getTextBySelector(SwaggerKeyWord.SELECTOR_RESPONSE,swaggerMethod)

    def waitProcessingTime(self):
        self.wait(processingTime=self.processingTime)

    def getFilteredSetting(self,keySetting,testCase):
        return SettingHelper.getFilteredSetting(self.globals.getSetting(keySetting,settingTree=testCase),self.globals)

    def getTestCase(self,tag,testName):
        settingTree = self.globals.getSettingTree(settingFilePath=f'{self.integrationPath}{tag}{self.globals.BACK_SLASH}{testName}.{self.globals.extension}')
        if TEST_CASE in settingTree.keys() :
            newSettingTree = {}
            for settingTreeKey, settingTreeValue in settingTree[TEST_CASE].items() :
                newSettingTree[f'{testName}.{settingTreeKey}'] = settingTreeValue
            return newSettingTree
        return {testName : settingTree}


class SwaggerKeyWord:

    SELECTOR_TBODY = '//div//div//table//tbody//tr//td[@class="col parameters-col_description"]'
    SELECTOR_AUTHORIZATION = '//tbody//tr//td//input[@placeholder="Authorization - Access Token"]'
    SELECTOR_RESPONSE = '//tbody//tr//td//div//div//pre[@class=" microlight"]'

    EXPAND_OPERATION = 'expand-operation'
    TRY_OUT = 'try-out'
    BODY_PARAM = 'body-param__text'
    EXECUTE_WRAPPER = 'execute-wrapper'
    HIGHLIGHT_CODE = 'highlight-code'
    MICROLIGHT = 'microlight'
    MARKDOWN = "markdown"

    ###- this seccion is used only as part of the full swagger html class or ir or whatever
    OPERATIONS_DASH = 'operations-'
    OPERATION_TAG_DASH = 'operations-tag-'
    USING = 'Using'
