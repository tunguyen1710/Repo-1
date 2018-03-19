# @Scenario A_HL_Common_GPRS_CGSMS_0002.PY
#
# @Dependencies
# Item    Module    HardType
# 1.     HL7518    200
# 2.    HL75xx    300
# 3.    HL7yyy    400
#
# @Test Cases
# Test Name                            Description
# A_HL_Common_GPRS_CGSMS_0002        Check behaviour of AT+CGSMS command to select GPRS service for MO SMS 
#
# @History
# Date            Author        Modification
# 2014-12-01    TKW            Create file
# 2016-01-19    AMarto         Delete if(HardType_LTE) to make the script generic to all HL7
# 2016-04-26    tye            Behavior update only for HL7528 SKT SMS over SGs). Keep unchanged for others based on ANO79447 and ANO77731.
# 2016-05-03    tye            Behavior update only for HL7528 SKT SMS over SGs) based on ANO91114: CMS ERROR: 38 -> CMS ERROR: 513
# 2016-05-17    Jlee           +CGSMS=* reponse change for ANO90836 HL7539, HL7549
# 2016-11-07    Cyuan          Add for HL7648
# 2017-03-20    NTSON (TMA)    Add HardType_LTE == "13" for HL7650. Add check current FW
# 2017-08-09    ntcdung        Add KSRAT=5 for HL7650, update for Oneclick
# 2017-12-13    vtquyen        Update for HL7800 (AT+EXCEPT and AT+CCID are not supported but AT%CCID is supported base on ALT1250-416; Update to open UART with dynamic parameters; Update HardType_LTE==13,16 by HardType_LTE in Generic_Behaviour_Product_List)
#----------------------------------------------------------------------------------------

print "Program start:"

test_environment_ready = "Ready"

try:
    VarGlobal.statOfItem = "OK"
    # -------------------------- AutoTest Initialization --------------------------------

    # Variable Init
    #UART1_COM = 98
    SIM_Pin1 = get_ini_value( SIM_INI, 'Security', 'Pin1')
    VoiceNumber = get_ini_value( SIM_INI, 'Identification', 'VoiceNumber')
    PARAM_GPRS_APN = get_ini_value( SIM_INI, 'gprs', 'APN')
    HARD_TYPE = get_ini_value(HARD_INI, 'HardType', 'HardType')
    HardType_LTE = get_ini_value(HARD_INI, 'HardType_LTE', 'HardType_LTE')
    Soft_version = get_ini_value( SOFT_INI, 'Soft', 'Version')
    operator = get_ini_value(NETWORK_INI, 'Network', 'Short_name')
    # 2017-12-13, vtquyen, Update for HL7800
    AT_EXCEPT = int(get_ini_value( SOFT_INI, 'Features', 'AT_EXCEPT'))
    AT_CCID = int(get_ini_value( SOFT_INI, 'Features', 'AT_CCID'))
    AT_percent_CCID=int(get_ini_value( SOFT_INI, 'Features', 'AT_percent_CCID'))
    AT_CGCLASS = int(get_ini_value( SOFT_INI, 'Features', 'AT_CGCLASS'))

    short_waiting_time = 15000
    
    # -------------------------- Module Initialization ----------------------------------

    # UART Init
    # 2017-12-11, vtquyen, Update to open UART with dynamic parameters
    Serial_BaudRate = get_ini_value(SERIAL_PORT_INI, 'Serial Port', 'Speed')
    Serial_Data = int(get_ini_value(SERIAL_PORT_INI, 'Serial Port', 'Data'))
    Serial_Stop = int(get_ini_value(SERIAL_PORT_INI, 'Serial Port', 'Stop'))
    Serial_Parity = get_ini_value(SERIAL_PORT_INI, 'Serial Port', 'Parity')
    rts_cts = get_ini_value(SERIAL_PORT_INI, 'Serial Port', 'rtscts')
    UART1 = SagOpen(UART1_COM, Serial_BaudRate, Serial_Data, Serial_Parity, Serial_Stop, rts_cts)


    # Module 1 Initialization
    SWI_Check_Module(UART1, AT_CMD_List_Check_Module, AT_Resp_List_Check_Module, AT_Timeout_List_Check_Module, AT_Restart_CMD, AT_Restart_Resp, Booting_Duration)

    SagSendAT(UART1, 'ATI9\r')
    SagWaitnMatchResp(UART1, ['\r\n*\r\n\r\nOK\r\n'], 4000)

    # 2017-12-13, vtquyen, Update for HL7800
    if AT_CCID:
        SagSendAT(UART1, 'AT+CCID\r')
        SagWaitnMatchResp(UART1, ['\r\n+CCID: *\r\n'], 4000)
        SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 4000)

    if AT_percent_CCID:
        SagSendAT(UART1, 'AT%CCID\r')
        SagWaitnMatchResp(UART1, ['\r\n%CCID: *\r\n'], 4000)
        SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 4000)

    # 2017-12-13, vtquyen, Update for HL7800
    if AT_EXCEPT:
        SagSendAT(UART1, 'AT+EXCEPT=255\r')
        SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 4000)

        SagSendAT(UART1, 'AT+EXCEPT\r')
        SagWaitnMatchResp(UART1, ['*\r\nOK\r\n'], 4000)

    SagSendAT(UART1, 'AT+CEREG=0\r\n')
    SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 4000)
            
    SWI_Check_SIM_Ready(UART1, '"%s"'%SIM_Pin1, SIM_Check_CMD, SIM_Check_RESP, SIM_SET_PIN_CMD, AT_SET_SIM_RESP, UNSOLICITED_Notif, SIM_TimeOut)

    SWI_Check_Network_Coverage(UART1, AT_CMD_List_Net_Registration, AT_RESP_List_Net_Registration, Max_Try_Net_Registration)
    
    if not VarGlobal.Init_Status in ["AT_OK", "SIM_Ready", "Network_Registration_Ready"]:
        test_environment_ready = "Not_Ready"
    SagSleep(5000)

except:
    print "***** Test environment check fails !!!*****"
    test_environment_ready = "Not_Ready"

print "\\n----- Testing Start -----\\n"

# -----------------------------------------------------------------------------------
# A_HL_Common_GPRS_CGSMS_0002. Testing command AT
# -----------------------------------------------------------------------------------
test_nb=""
test_ID = "A_HL_Common_GPRS_CGSMS_0002"
PRINT_START_FUNC(test_nb + test_ID)

try:
    if test_environment_ready == "Not_Ready":
        VarGlobal.statOfItem="NOK"
        raise Exception("---->Problem: Test environment Is Not Ready !!!")

    if (HARD_TYPE == "200"):
        print "\r\n HardType_LTE=%s operator=%s \r\n" %(HardType_LTE, operator)
        #tye, behavior updated for HL7528 SKT. Keep unchanged for others.
        if ( HardType_LTE in ['5'] and operator in ['SKT']):
            VarGlobal.statOfItem="OK"
            print "\r\nHL7528 SKT\r\n"
            # 6. UART1 AT+CCID<CR>
            SagSendAT(UART1, 'AT+CCID\r')
            SagWaitnMatchResp(UART1, ['\r\n+CCID: *\r\n'], 2000)
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            SagSendAT(UART1, 'AT+CNMI=1,1\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            print "\r\n--------------------------------CLASS B------------------------------------\r\n"
            #TYE, remove +CGCLASS        
            # 16. UART1 AT+CGCLASS?<CR>
            # SagSendAT(UART1, 'AT+CGCLASS="B"\r')
            # SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 10000)

            # 17. UART1 AT+CGSMS=?<CR>
            SagSendAT(UART1, 'AT+CGSMS=?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGSMS: (0-3)\r\n\r\nOK\r\n'], 2000)

            # 18. UART1 AT+CGSMS?<CR>
            SagSendAT(UART1, 'AT+CGSMS?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGSMS: 1\r\n\r\nOK\r\n'], 2000)

            SagSendAT(UART1, 'AT+CGATT=0\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 5000)
            
            #TYE, add message storage settings      
            # 19. UART1 AT+CPMS="SM","SM","SM"<CR>
            SagSendAT(UART1, 'AT+CPMS="SM","SM","SM"\r')
            SagWaitnMatchResp(UART1, ['\r\n+CPMS: *\r\n\r\nOK\r\n'], 40000)
            
            # 19. UART1 AT+CMGD=1,4<CR>
            SagSendAT(UART1, 'AT+CMGD=1,4\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 20000)

            SagSendAT(UART1, 'AT+CMGF=1\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 5000)

            SagSendAT(UART1, 'AT+CMGW="'+VoiceNumber+'"\r')
            SagWaitnMatchResp(UART1, ['\r\n> '], 2000)
            SagSendAT(UART1, 'TEST SMS\x1A')
            SagWaitnMatchResp(UART1, ['\r\n+CMGW: *\r\n\r\nOK\r\n'], 5000)

            print "\r\n----------------------------CGATT = 0, CGSMS = 0------------------------------------\r\n"

            # 22. UART1 AT+CGSMS=0<CR>
            SagSendAT(UART1, 'AT+CGSMS=0\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            # 23. UART1 AT+CGSMS?<CR>
            SagSendAT(UART1, 'AT+CGSMS?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGSMS: 0\r\n'], 2000)
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            SagSendAT(UART1, 'AT+CMSS=1\r')
            SagWaitnMatchResp(UART1, ['\r\n+CMS ERROR: 38\r\n'], 8000)

            print "\r\n----------------------------CGATT = 0, CGSMS = 1------------------------------------\r\n"

            # 25. UART1 AT+CGSMS=1<CR>
            SagSendAT(UART1, 'AT+CGSMS=1\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            # 26. UART1 AT+CGSMS?<CR>
            SagSendAT(UART1, 'AT+CGSMS?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGSMS: 1\r\n\r\nOK\r\n'], 2000)

            # 27. UART1 AT+CMSS=1<CR>
            SagSendAT(UART1, 'AT+CMSS=1\r')
            #SagWaitnMatchResp(UART1, ['\r\n+CMSS: *\r\n\r\nOK\r\n'], 8000)
            #SagWaitnMatchResp(UART1, ['\r\n+CMTI: "SM",2\r\n'], 30000)
            SagWaitnMatchResp(UART1, ['\r\n+CMS ERROR: 38\r\n'], 8000)

            print "\r\n----------------------------CGATT = 0, CGSMS = 2------------------------------------\r\n"

            # 28. UART1 AT+CGSMS=2<CR>
            SagSendAT(UART1, 'AT+CGSMS=2\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            # 29. UART1 AT+CGSMS?<CR>
            SagSendAT(UART1, 'AT+CGSMS?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGSMS: 2\r\n\r\nOK\r\n'], 2000)

            # 30. UART1 AT+CMSS=1<CR>
            SagSendAT(UART1, 'AT+CMSS=1\r')
            #SagWaitnMatchResp(UART1, ['\r\n+CMSS: *\r\n\r\nOK\r\n'], 8000)
            #SagWaitnMatchResp(UART1, ['\r\n+CMTI: "SM",3\r\n'], 30000)
            SagWaitnMatchResp(UART1, ['\r\n+CMS ERROR: 38\r\n'], 8000)

            print "\r\n----------------------------CGATT = 0, CGSMS = 3------------------------------------\r\n"

            # 31. UART1 AT+CGSMS=3<CR>
            SagSendAT(UART1, 'AT+CGSMS=3\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            # 32. UART1 AT+CGSMS?<CR>
            SagSendAT(UART1, 'AT+CGSMS?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGSMS: 3\r\n\r\nOK\r\n'], 2000)

            # 33. UART1 AT+CMSS=1<CR>
            SagSendAT(UART1, 'AT+CMSS=1\r')
            #SagWaitnMatchResp(UART1, ['\r\n+CMSS: *\r\n\r\nOK\r\n'], 8000)
            #SagWaitnMatchResp(UART1, ['\r\n+CMTI: "SM",4\r\n'], 30000)
            SagWaitnMatchResp(UART1, ['\r\n+CMS ERROR: 38\r\n'], 8000)

            # 34. UART1 AT+CGATT=1<CR>
            SagSendAT(UART1, 'AT+CGATT=1\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 5000)

            # 35. UART1 AT+CGATT?<CR>
            SagSendAT(UART1, 'AT+CGATT?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGATT: 1\r\n\r\nOK\r\n'], 2000)

            print "\r\n----------------------------CGATT = 1, CGSMS = 0------------------------------------\r\n"

            SagSendAT(UART1, 'AT+CGSMS=0\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            SagSendAT(UART1, 'AT+CGSMS?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGSMS: 0\r\n\r\nOK\r\n'], 2000)
            #SagSleep(60000)
            SagSendAT(UART1, 'AT+CMSS=1\r')
            #tye, CMS error code updated based on ANO91114
            #tye, correct for LTE sms over SGs
            # SagWaitnMatchResp(UART1, ['\r\n+CMS ERROR: 38\r\n'], 8000)
            SagWaitnMatchResp(UART1, ['\r\n+CMS ERROR: 513\r\n'], 60000)
            # SagWaitnMatchResp(UART1, ['\r\n+CMSS: *\r\n\r\nOK\r\n'], 60000)
            # SagWaitnMatchResp(UART1, ['\r\n+CMTI: "SM",2\r\n'], 30000)

            print "\r\n----------------------------CGATT = 1, CGSMS = 1------------------------------------\r\n"

            # 36. UART1 AT+CGSMS=1<CR>
            SagSendAT(UART1, 'AT+CGSMS=1\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            # 37. UART1 AT+CGSMS?<CR>
            SagSendAT(UART1, 'AT+CGSMS?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGSMS: 1\r\n\r\nOK\r\n'], 2000)

            # 38. UART1 AT+CMSS=1<CR>
            SagSendAT(UART1, 'AT+CMSS=1\r')
            #SagWaitnMatchResp(UART1, ['\r\n+CMSS: *\r\n\r\nOK\r\n'], 8000)
            #SagWaitnMatchResp(UART1, ['\r\n+CMTI: "SM",6\r\n'], 30000)
            #tye, correct for LTE SMS over SGs
            # SagWaitnMatchResp(UART1, ['\r\n+CMS ERROR: 38\r\n'], 8000)
            SagWaitnMatchResp(UART1, ['\r\n+CMSS: *\r\n\r\nOK\r\n'], 60000)
            SagWaitnMatchResp(UART1, ['\r\n+CMTI: "SM",2\r\n'], 30000)
            
            print "\r\n----------------------------CGATT = 1, CGSMS = 2------------------------------------\r\n"

            SagSendAT(UART1, 'AT+CGSMS=2\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            SagSendAT(UART1, 'AT+CGSMS?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGSMS: 2\r\n\r\nOK\r\n'], 2000)

            SagSendAT(UART1, 'AT+CMSS=1\r')
            SagWaitnMatchResp(UART1, ['\r\n+CMSS: *\r\n\r\nOK\r\n'], 60000)
            SagWaitnMatchResp(UART1, ['\r\n+CMTI: "SM",3\r\n'], 30000)
            
            print "\r\n----------------------------CGATT = 1, CGSMS = 3------------------------------------\r\n"

            SagSendAT(UART1, 'AT+CGSMS=3\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            SagSendAT(UART1, 'AT+CGSMS?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGSMS: 3\r\n\r\nOK\r\n'], 2000)

            SagSendAT(UART1, 'AT+CMSS=1\r')
            SagWaitnMatchResp(UART1, ['\r\n+CMSS: *\r\n\r\nOK\r\n'], 60000)
            SagWaitnMatchResp(UART1, ['\r\n+CMTI: "SM",4\r\n'], 30000)
            #tye, remove +CGCLASS        
            # 41. UART1 AT+CGCLASS="B"<CR>
            # SagSendAT(UART1, 'AT+CGCLASS="B"\r')
            # SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 5000)

            SagSendAT(UART1, 'AT+CMGD=1,4\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 20000)    
        #for other product
        # 2017-03-20 NTSON (TMA) Add HardType_LTE == "13" for HL7650
        #elif (HardType_LTE in ['6','8','12', '13']):
        #2017-12-13, vtquyen, Update for HL7800:HardType_LTE==13,16 by HardType_LTE in Generic_Behaviour_Product_List)
        elif (HardType_LTE in ['6','8','12'] or HardType_LTE in Generic_Behaviour_Product_List):
            VarGlobal.statOfItem="OK"
            # 2017-08-09   ntcdung  Add KSRAT=5 for HL7650, update for Oneclick
            #if HardType_LTE == "13":
            #2017-12-13, vtquyen, Update for HL7800
            #SagSendAT(UART1, 'AT+KSRAT=5\r')
            #SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 10000)
            if RAT_Param=="RAT_2G":
                SagSendAT(UART1, RAT_2G_CMD  + '\r\n')
                SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 4000)
            elif RAT_Param=="RAT_3G":
                SagSendAT(UART1, RAT_3G_CMD  + '\r\n')
                SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 4000)
            elif RAT_Param=="RAT_4G":
                SagSendAT(UART1, RAT_4G_CMD  + '\r\n')
                SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 4000)
            
            # Wait for network registration
            SagSleep(10000) 

            # 6. UART1 AT+CCID<CR>
            # 2017-12-13, vtquyen, Update for HL7800
            if AT_CCID:
                SagSendAT(UART1, 'AT+CCID\r')
                SagWaitnMatchResp(UART1, ['\r\n+CCID: *\r\n'], 2000)
                SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            if AT_percent_CCID:
                SagSendAT(UART1, 'AT%CCID\r')
                SagWaitnMatchResp(UART1, ['\r\n%CCID: *\r\n'], 2000)
                SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            SagSendAT(UART1, 'AT+CNMI=1,1\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            print "\r\n--------------------------------CLASS B------------------------------------\r\n"
            # 16. UART1 AT+CGCLASS?<CR>
            if AT_CGCLASS:
                SagSendAT(UART1, 'AT+CGCLASS="B"\r')
                SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 10000)

            # 17. UART1 AT+CGSMS=?<CR>
            # 2017-12-13, vtquyen, Update for HL7800
            if HardType_LTE in Specific_Behaviour_Product_List:
                SagSendAT(UART1, "AT+CGSMS=?\r")
                SagWaitnMatchResp(UART1, ["\r\n+CGSMS: (0,1)\r\n\r\nOK\r\n"], C_TIMER_LOW)
            else:
                SagSendAT(UART1, "AT+CGSMS=?\r")
                SagWaitnMatchResp(UART1, ["\r\n+CGSMS: (0-3)\r\n\r\nOK\r\n"], C_TIMER_LOW)

            # 18. UART1 AT+CGSMS?<CR>
            SagSendAT(UART1, 'AT+CGSMS?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGSMS: 1\r\n\r\nOK\r\n'], 2000)

            SagSendAT(UART1, 'AT+CGATT=0\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 5000)

            # 19. UART1 AT+CMGD=1,4<CR>
            SagSendAT(UART1, 'AT+CMGD=1,4\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 20000)

            SagSendAT(UART1, 'AT+CMGF=1\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 5000)

            SagSendAT(UART1, 'AT+CMGW="'+VoiceNumber+'"\r')
            SagWaitnMatchResp(UART1, ['\r\n> '], 2000)
            SagSendAT(UART1, 'TEST SMS\x1A')
            SagWaitnMatchResp(UART1, ['\r\n+CMGW: *\r\n\r\nOK\r\n'], 5000)

            print "\r\n----------------------------CGATT = 0, CGSMS = 0------------------------------------\r\n"

            # 22. UART1 AT+CGSMS=0<CR>
            SagSendAT(UART1, 'AT+CGSMS=0\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            # 23. UART1 AT+CGSMS?<CR>
            SagSendAT(UART1, 'AT+CGSMS?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGSMS: 0\r\n'], 2000)
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            SagSendAT(UART1, 'AT+CMSS=1\r')
            SagWaitnMatchResp(UART1, ['\r\n+CMS ERROR: 38\r\n'], 8000)

            print "\r\n----------------------------CGATT = 0, CGSMS = 1------------------------------------\r\n"

            # 25. UART1 AT+CGSMS=1<CR>
            SagSendAT(UART1, 'AT+CGSMS=1\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            # 26. UART1 AT+CGSMS?<CR>
            SagSendAT(UART1, 'AT+CGSMS?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGSMS: 1\r\n\r\nOK\r\n'], 2000)

            # 27. UART1 AT+CMSS=1<CR>
            SagSendAT(UART1, 'AT+CMSS=1\r')
            #SagWaitnMatchResp(UART1, ['\r\n+CMSS: *\r\n\r\nOK\r\n'], 8000)
            #SagWaitnMatchResp(UART1, ['\r\n+CMTI: "SM",2\r\n'], 30000)
            SagWaitnMatchResp(UART1, ['\r\n+CMS ERROR: 38\r\n'], 8000)

            print "\r\n----------------------------CGATT = 0, CGSMS = 2------------------------------------\r\n"

            # 28. UART1 AT+CGSMS=2<CR>
            # 2017-12-13, vtquyen, Update for HL7800
            if HardType_LTE in Specific_Behaviour_Product_List:
                pass
            else:
                SagSendAT(UART1, 'AT+CGSMS=2\r')
                SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

                # 29. UART1 AT+CGSMS?<CR>
                SagSendAT(UART1, 'AT+CGSMS?\r')
                SagWaitnMatchResp(UART1, ['\r\n+CGSMS: 2\r\n\r\nOK\r\n'], 2000)

                # 30. UART1 AT+CMSS=1<CR>
                SagSendAT(UART1, 'AT+CMSS=1\r')
                #SagWaitnMatchResp(UART1, ['\r\n+CMSS: *\r\n\r\nOK\r\n'], 8000)
                #SagWaitnMatchResp(UART1, ['\r\n+CMTI: "SM",3\r\n'], 30000)
                SagWaitnMatchResp(UART1, ['\r\n+CMS ERROR: 38\r\n'], 8000)

            print "\r\n----------------------------CGATT = 0, CGSMS = 3------------------------------------\r\n"

            # 31. UART1 AT+CGSMS=3<CR>
            # 2017-12-13, vtquyen, Update for HL7800
            if HardType_LTE in Specific_Behaviour_Product_List:
                pass
            else:
                SagSendAT(UART1, 'AT+CGSMS=3\r')
                SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

                # 32. UART1 AT+CGSMS?<CR>
                SagSendAT(UART1, 'AT+CGSMS?\r')
                SagWaitnMatchResp(UART1, ['\r\n+CGSMS: 3\r\n\r\nOK\r\n'], 2000)

                # 33. UART1 AT+CMSS=1<CR>
                SagSendAT(UART1, 'AT+CMSS=1\r')
                #SagWaitnMatchResp(UART1, ['\r\n+CMSS: *\r\n\r\nOK\r\n'], 8000)
                #SagWaitnMatchResp(UART1, ['\r\n+CMTI: "SM",4\r\n'], 30000)
                SagWaitnMatchResp(UART1, ['\r\n+CMS ERROR: 38\r\n'], 8000)

            # 34. UART1 AT+CGATT=1<CR>
            SagSendAT(UART1, 'AT+CGATT=1\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 5000)

            # 35. UART1 AT+CGATT?<CR>
            SagSendAT(UART1, 'AT+CGATT?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGATT: 1\r\n\r\nOK\r\n'], 2000)

            print "\r\n----------------------------CGATT = 1, CGSMS = 0------------------------------------\r\n"

            SagSendAT(UART1, 'AT+CGSMS=0\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            SagSendAT(UART1, 'AT+CGSMS?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGSMS: 0\r\n\r\nOK\r\n'], 2000)
            #SagSleep(60000)
            SagSendAT(UART1, 'AT+CMSS=1\r')
            #Jlee, CMS error code updated based on ANO90836
            #Jlee, correct for LTE sms over SGs
            SagWaitnMatchResp(UART1, ['\r\n+CMS ERROR: 513\r\n'], 60000)
            #SagWaitnMatchResp(UART1, ['\r\n+CMSS: *\r\n\r\nOK\r\n'], 60000)
            #SagWaitnMatchResp(UART1, ['\r\n+CMTI: "SM",2\r\n'], 30000)

            print "\r\n----------------------------CGATT = 1, CGSMS = 1------------------------------------\r\n"

            # 36. UART1 AT+CGSMS=1<CR>
            SagSendAT(UART1, 'AT+CGSMS=1\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            # 37. UART1 AT+CGSMS?<CR>
            SagSendAT(UART1, 'AT+CGSMS?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGSMS: 1\r\n\r\nOK\r\n'], 2000)

            # 38. UART1 AT+CMSS=1<CR>
            SagSendAT(UART1, 'AT+CMSS=1\r')
            #Jlee, correct for LTE sms over SGs
            SagWaitnMatchResp(UART1, ['\r\n+CMSS: *\r\n\r\nOK\r\n'], 8000)
            SagWaitnMatchResp(UART1, ['\r\n+CMTI: "SM",2\r\n'], 60000)
            #SagWaitnMatchResp(UART1, ['\r\n+CMTI: "SM",6\r\n'], 30000)
            #SagWaitnMatchResp(UART1, ['\r\n+CMS ERROR: 38\r\n'], 8000)
            
            print "\r\n----------------------------CGATT = 1, CGSMS = 2------------------------------------\r\n"

            # 2017-12-13, vtquyen, Update for HL7800
            if HardType_LTE in Specific_Behaviour_Product_List:
                pass
            else:
                SagSendAT(UART1, 'AT+CGSMS=2\r')
                SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

                SagSendAT(UART1, 'AT+CGSMS?\r')
                SagWaitnMatchResp(UART1, ['\r\n+CGSMS: 2\r\n\r\nOK\r\n'], 2000)

                SagSendAT(UART1, 'AT+CMSS=1\r')
                SagWaitnMatchResp(UART1, ['\r\n+CMSS: *\r\n\r\nOK\r\n'], 60000)
                SagWaitnMatchResp(UART1, ['\r\n+CMTI: "SM",3\r\n'], 60000)
            
            print "\r\n----------------------------CGATT = 1, CGSMS = 3------------------------------------\r\n"

            # 2017-12-13, vtquyen, Update for HL7800
            if HardType_LTE in Specific_Behaviour_Product_List:
                pass
            else:
                SagSendAT(UART1, 'AT+CGSMS=3\r')
                SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

                SagSendAT(UART1, 'AT+CGSMS?\r')
                SagWaitnMatchResp(UART1, ['\r\n+CGSMS: 3\r\n\r\nOK\r\n'], 2000)

                SagSendAT(UART1, 'AT+CMSS=1\r')
                SagWaitnMatchResp(UART1, ['\r\n+CMSS: *\r\n\r\nOK\r\n'], 60000)
                SagWaitnMatchResp(UART1, ['\r\n+CMTI: "SM",4\r\n'], 60000)
            
            # 41. UART1 AT+CGCLASS="B"<CR>
            if AT_CGCLASS:
                SagSendAT(UART1, 'AT+CGCLASS="B"\r')
                SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 5000)

            SagSendAT(UART1, 'AT+CMGD=1,4\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 20000)
        else:
            VarGlobal.statOfItem="OK"
            
            # 6. UART1 AT+CCID<CR>
            SagSendAT(UART1, 'AT+CCID\r')
            SagWaitnMatchResp(UART1, ['\r\n+CCID: *\r\n'], 2000)
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            SagSendAT(UART1, 'AT+CNMI=1,1\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            print "\r\n--------------------------------CLASS B------------------------------------\r\n"
            # 16. UART1 AT+CGCLASS?<CR>
            SagSendAT(UART1, 'AT+CGCLASS="B"\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 10000)

            # 17. UART1 AT+CGSMS=?<CR>
            SagSendAT(UART1, 'AT+CGSMS=?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGSMS: (0-3)\r\n\r\nOK\r\n'], 2000)

            # 18. UART1 AT+CGSMS?<CR>
            SagSendAT(UART1, 'AT+CGSMS?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGSMS: 1\r\n\r\nOK\r\n'], 2000)

            SagSendAT(UART1, 'AT+CGATT=0\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 5000)

            # 19. UART1 AT+CMGD=1,4<CR>
            SagSendAT(UART1, 'AT+CMGD=1,4\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 20000)

            SagSendAT(UART1, 'AT+CMGF=1\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 5000)

            SagSendAT(UART1, 'AT+CMGW="'+VoiceNumber+'"\r')
            SagWaitnMatchResp(UART1, ['\r\n> '], 2000)
            SagSendAT(UART1, 'TEST SMS\x1A')
            SagWaitnMatchResp(UART1, ['\r\n+CMGW: *\r\n\r\nOK\r\n'], 5000)

            print "\r\n----------------------------CGATT = 0, CGSMS = 0------------------------------------\r\n"

            # 22. UART1 AT+CGSMS=0<CR>
            SagSendAT(UART1, 'AT+CGSMS=0\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            # 23. UART1 AT+CGSMS?<CR>
            SagSendAT(UART1, 'AT+CGSMS?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGSMS: 0\r\n'], 2000)
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            SagSendAT(UART1, 'AT+CMSS=1\r')
            SagWaitnMatchResp(UART1, ['\r\n+CMS ERROR: 38\r\n'], 8000)

            print "\r\n----------------------------CGATT = 0, CGSMS = 1------------------------------------\r\n"

            # 25. UART1 AT+CGSMS=1<CR>
            SagSendAT(UART1, 'AT+CGSMS=1\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            # 26. UART1 AT+CGSMS?<CR>
            SagSendAT(UART1, 'AT+CGSMS?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGSMS: 1\r\n\r\nOK\r\n'], 2000)

            # 27. UART1 AT+CMSS=1<CR>
            SagSendAT(UART1, 'AT+CMSS=1\r')
            #SagWaitnMatchResp(UART1, ['\r\n+CMSS: *\r\n\r\nOK\r\n'], 8000)
            #SagWaitnMatchResp(UART1, ['\r\n+CMTI: "SM",2\r\n'], 30000)
            SagWaitnMatchResp(UART1, ['\r\n+CMS ERROR: 38\r\n'], 8000)

            print "\r\n----------------------------CGATT = 0, CGSMS = 2------------------------------------\r\n"

            # 28. UART1 AT+CGSMS=2<CR>
            SagSendAT(UART1, 'AT+CGSMS=2\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            # 29. UART1 AT+CGSMS?<CR>
            SagSendAT(UART1, 'AT+CGSMS?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGSMS: 2\r\n\r\nOK\r\n'], 2000)

            # 30. UART1 AT+CMSS=1<CR>
            SagSendAT(UART1, 'AT+CMSS=1\r')
            #SagWaitnMatchResp(UART1, ['\r\n+CMSS: *\r\n\r\nOK\r\n'], 8000)
            #SagWaitnMatchResp(UART1, ['\r\n+CMTI: "SM",3\r\n'], 30000)
            SagWaitnMatchResp(UART1, ['\r\n+CMS ERROR: 38\r\n'], 8000)

            print "\r\n----------------------------CGATT = 0, CGSMS = 3------------------------------------\r\n"

            # 31. UART1 AT+CGSMS=3<CR>
            SagSendAT(UART1, 'AT+CGSMS=3\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            # 32. UART1 AT+CGSMS?<CR>
            SagSendAT(UART1, 'AT+CGSMS?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGSMS: 3\r\n\r\nOK\r\n'], 2000)

            # 33. UART1 AT+CMSS=1<CR>
            SagSendAT(UART1, 'AT+CMSS=1\r')
            #SagWaitnMatchResp(UART1, ['\r\n+CMSS: *\r\n\r\nOK\r\n'], 8000)
            #SagWaitnMatchResp(UART1, ['\r\n+CMTI: "SM",4\r\n'], 30000)
            SagWaitnMatchResp(UART1, ['\r\n+CMS ERROR: 38\r\n'], 8000)

            # 34. UART1 AT+CGATT=1<CR>
            SagSendAT(UART1, 'AT+CGATT=1\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 5000)

            # 35. UART1 AT+CGATT?<CR>
            SagSendAT(UART1, 'AT+CGATT?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGATT: 1\r\n\r\nOK\r\n'], 2000)

            print "\r\n----------------------------CGATT = 1, CGSMS = 0------------------------------------\r\n"

            SagSendAT(UART1, 'AT+CGSMS=0\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            SagSendAT(UART1, 'AT+CGSMS?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGSMS: 0\r\n\r\nOK\r\n'], 2000)
            #SagSleep(60000)
            SagSendAT(UART1, 'AT+CMSS=1\r')
            SagWaitnMatchResp(UART1, ['\r\n+CMSS: *\r\n\r\nOK\r\n'], 60000)
            SagWaitnMatchResp(UART1, ['\r\n+CMTI: "SM",2\r\n'], 30000)

            print "\r\n----------------------------CGATT = 1, CGSMS = 1------------------------------------\r\n"

            # 36. UART1 AT+CGSMS=1<CR>
            SagSendAT(UART1, 'AT+CGSMS=1\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            # 37. UART1 AT+CGSMS?<CR>
            SagSendAT(UART1, 'AT+CGSMS?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGSMS: 1\r\n\r\nOK\r\n'], 2000)

            # 38. UART1 AT+CMSS=1<CR>
            SagSendAT(UART1, 'AT+CMSS=1\r')
            #SagWaitnMatchResp(UART1, ['\r\n+CMSS: *\r\n\r\nOK\r\n'], 8000)
            #SagWaitnMatchResp(UART1, ['\r\n+CMTI: "SM",6\r\n'], 30000)
            SagWaitnMatchResp(UART1, ['\r\n+CMS ERROR: 38\r\n'], 8000)
            
            print "\r\n----------------------------CGATT = 1, CGSMS = 2------------------------------------\r\n"

            SagSendAT(UART1, 'AT+CGSMS=2\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            SagSendAT(UART1, 'AT+CGSMS?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGSMS: 2\r\n\r\nOK\r\n'], 2000)

            SagSendAT(UART1, 'AT+CMSS=1\r')
            SagWaitnMatchResp(UART1, ['\r\n+CMSS: *\r\n\r\nOK\r\n'], 60000)
            SagWaitnMatchResp(UART1, ['\r\n+CMTI: "SM",3\r\n'], 30000)
            
            print "\r\n----------------------------CGATT = 1, CGSMS = 3------------------------------------\r\n"

            SagSendAT(UART1, 'AT+CGSMS=3\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

            SagSendAT(UART1, 'AT+CGSMS?\r')
            SagWaitnMatchResp(UART1, ['\r\n+CGSMS: 3\r\n\r\nOK\r\n'], 2000)

            SagSendAT(UART1, 'AT+CMSS=1\r')
            SagWaitnMatchResp(UART1, ['\r\n+CMSS: *\r\n\r\nOK\r\n'], 60000)
            SagWaitnMatchResp(UART1, ['\r\n+CMTI: "SM",4\r\n'], 30000)
            
            # 41. UART1 AT+CGCLASS="B"<CR>
            SagSendAT(UART1, 'AT+CGCLASS="B"\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 5000)

            SagSendAT(UART1, 'AT+CMGD=1,4\r')
            SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 20000)
            
except Exception, err_msg :
    VarGlobal.statOfItem = "NOK"
    print Exception, err_msg
PRINT_TEST_RESULT(test_ID, VarGlobal.statOfItem)

# -----------------------------------------------------------------------------------

print "\n----- Testing End -----\n"

# Restore Module
#restore_module( UART1,"Intel",["AT&F AT&W CFUN=1,1<60 DELAY:30"] )
SagSendAT(UART1, 'AT+CGSMS=1\r')
SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 2000)

# 2017-12-13, vtquyen, Update for HL7800
if AT_EXCEPT:
    SagSendAT(UART1, 'AT+EXCEPT\r')
    SagWaitnMatchResp(UART1, ['*\r\nOK\r\n'], 6000)
# Close UART
SagClose(UART1)

#SagClose(AUX)

