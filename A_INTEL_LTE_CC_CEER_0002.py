# @Scenario A_HL_Common_CC_CEER_0002.py
#
# @Dependencies
# Item    Module    HardType
# 1.     HL7518    200
# 2.    HL75xx    300
# 3.    HL7yyy    400
# 4.    HL7539  200
#
# @Test Cases
# Test Name                     Description
# A_HL_Common_CC_CEER_0002        Function test on command +CEER
#
# @History
# Date          Author       Modification
# 2015-04-02    rfa          Create file
# 2016-01-13    Cyuan        Update on HL7539
# 2017-03-15    pangoc       Correct the bahavior of +CEER error 
# 2017-04-14    NTSON        Modify to correct the behavior of +CEER error after making a voice call with DUMMY_NUMBER.
# 2017-12-27    ntcdung      Update for HL78xx
#------------------------------------------------------------------------------------

#print "Program Start:"

test_environment_ready = "Ready"

try:
    VarGlobal.statOfItem = "OK"

    # -------------------------- AutoTest Initialization --------------------------------
    # Variable Init
    #UART1_COM = 1
    SIM_Pin1 = get_ini_value( SIM_INI, 'Security', 'Pin1')
    VoiceNumber = get_ini_value( SIM_INI, 'Identification', 'VoiceNumber')[4:]
    HARD_TYPE = get_ini_value(HARD_INI, 'HardType', 'HardType')
    HARD_TYPE_LTE = get_ini_value(HARD_INI, 'HardType_LTE', 'HardType_LTE')
    H_AUDIO = get_ini_value(HARD_INI, 'Audio', 'H_AUDIO')
    DUMMY_NUMBER = 1234
    # 2017-12-27, ntcdung, Update for HL78xx.
    AT_CCID=int(get_ini_value( SOFT_INI, 'Features', 'AT_CCID'))
    AT_EXCEPT = int(get_ini_value( SOFT_INI, 'Features', 'AT_EXCEPT'))
    AT_percent_CCID = int(get_ini_value( SOFT_INI, 'Features', 'AT_percent_CCID'))
    short_waiting_time = 15000
    # -------------------------- Module Initialization ----------------------------------
    # UART Init
    #UART1 = SagOpen(UART1_COM, 115200, 8, "N", 1, "None")
    # 2017-12-27, ntcdung, Update to open UART with dynamic parameters
    Serial_BaudRate = get_ini_value(SERIAL_PORT_INI, 'Serial Port', 'Speed')
    Serial_Data = int(get_ini_value(SERIAL_PORT_INI, 'Serial Port', 'Data'))
    Serial_Stop = int(get_ini_value(SERIAL_PORT_INI, 'Serial Port', 'Stop'))
    Serial_Parity = get_ini_value(SERIAL_PORT_INI, 'Serial Port', 'Parity')
    rts_cts = get_ini_value(SERIAL_PORT_INI, 'Serial Port', 'rtscts')

    UART1 = SagOpen(UART1_COM, Serial_BaudRate, Serial_Data, Serial_Parity, Serial_Stop, rts_cts)

    # Module 1 Initialization
    # 2017-12-27, ntcdung, Update for HL78xx.
    SWI_Check_Module(UART1, AT_CMD_List_Check_Module, AT_Resp_List_Check_Module, AT_Timeout_List_Check_Module, AT_Restart_CMD, AT_Restart_Resp, Booting_Duration)

    if AT_CCID:    
        SagSendAT(UART1, 'AT+CCID\r')
        SagWaitnMatchResp(UART1, ['\r\n+CCID: *\r\n\r\nOK\r\n'], 4000)

    if AT_percent_CCID:
        SagSendAT(UART1, 'AT%CCID\r')
        SagWaitnMatchResp(UART1, ['\r\n%CCID: *\r\n\r\nOK\r\n'], 4000)

    # 2017-12-27, ntcdung, Update for HL78xx.
    if AT_EXCEPT:
        SagSendAT(UART1, 'AT+EXCEPT=255\r')
        SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 4000)
        SagSendAT(UART1, 'AT+EXCEPT\r')
        SagWaitnMatchResp(UART1, ['*\r\nOK\r\n'], 4000)

    SagSendAT(UART1, 'AT+CEREG=0\r\n')
    SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 4000)
    
    if not VarGlobal.Init_Status in ["AT_OK"]:
        test_environment_ready = "Not_Ready"
        
    #AUX_COM = 2
    if (H_AUDIO == "1"):
        AUX = SagOpen(AUX_COM, Serial_BaudRate, Serial_Data, Serial_Parity, Serial_Stop, rts_cts)
        AUX_SIM_Pin1 = get_ini_value( SIM_INI, 'Security', 'Pin1')
        AUX_VoiceNumber = get_ini_value( AUX_SIM_INI, 'Identification', 'VoiceNumber')[4:]

        # Module 2 Initialization
        SWI_Check_Module(AUX, AT_CMD_List_Check_Module, AT_Resp_List_Check_Module, AT_Timeout_List_Check_Module, AT_Restart_CMD, AT_Restart_Resp, Booting_Duration)

        SagSendAT(AUX, 'ATI9\r')
        SagWaitnMatchResp(AUX, ['\r\n*\r\n\r\nOK\r\n'], 4000)
        if AT_CCID:    
            SagSendAT(AUX, 'AT+CCID\r')
            SagWaitnMatchResp(AUX, ['\r\n+CCID: *\r\n\r\nOK\r\n'], 4000)

        if AT_percent_CCID:
            SagSendAT(AUX, 'AT%CCID\r')
            SagWaitnMatchResp(AUX, ['\r\n%CCID: *\r\n'], 4000)
            SagWaitnMatchResp(AUX, ['\r\nOK\r\n'], 4000)

        # 2017-12-27, ntcdung, Update for HL78xx.
        if AT_EXCEPT:
            SagSendAT(AUX, 'AT+EXCEPT=255\r')
            SagWaitnMatchResp(AUX, ['\r\nOK\r\n'], 4000)
            SagSendAT(AUX, 'AT+EXCEPT\r')
            SagWaitnMatchResp(AUX, ['*\r\nOK\r\n'], 4000)

        SagSendAT(AUX, 'AT+CEREG=0\r\n')
        SagWaitnMatchResp(AUX, ['\r\nOK\r\n'], 4000)

        SWI_Check_SIM_Ready(AUX, '"%s"'%AUX_SIM_Pin1, SIM_Check_CMD, SIM_Check_RESP, SIM_SET_PIN_CMD, AT_SET_SIM_RESP, UNSOLICITED_Notif, SIM_TimeOut)

        SWI_Check_Network_Coverage(AUX, AT_CMD_List_Net_Registration, AT_RESP_List_Net_Registration, Max_Try_Net_Registration)

        if not VarGlobal.Init_Status in ["AT_OK", "SIM_Ready", "Network_Registration_Ready"]:
            test_environment_ready = "Not_Ready"                
                    
except:
    print "***** Test environment check fails !!!*****"
    test_environment_ready = "Not_Ready"

print "\\n----- Testing Start -----\\n"    
# -----------------------------------------------------------------------------------
# A_HL_Common_CC_CEER_0002
# -----------------------------------------------------------------------------------
test_nb=""
test_ID = "A_HL_Common_CC_CEER_0002"
PRINT_START_FUNC(test_nb + test_ID)

VarGlobal.statOfItem = "OK"

#######################################################################################
#    START: Module HL7518    Hard Type: 200
#           Moudle HL7xxx    Hard Type: 400
#######################################################################################
try:
    if test_environment_ready == "Not_Ready":
        VarGlobal.statOfItem="NOK"
        raise Exception("---->Problem: Test environment Is Not Ready !!!")

    if (HARD_TYPE_LTE == "xxx"):
        print "*********************************************"
        print "This test case is running on hard type: %s " % str(HARD_TYPE_LTE)
        print "*********************************************"

        print "***************************************************************************************************************"
        print "%s: <Test case description in QC>" % test_ID
        print "***************************************************************************************************************"

        # ......
        # ......
        # ......

    elif (HARD_TYPE == "200") or (HARD_TYPE == "400"):
        print "*********************************************"
        print "This test case is running on hard type: %s " % str(HARD_TYPE)
        print "*********************************************"

        print "***************************************************************************************************************"
        print "%s: <Test case description in QC>" % test_ID
        print "***************************************************************************************************************"

        # ------------------------------------------------------------------------------------
        # Test function
        # ------------------------------------------------------------------------------------
        #AT+CRC=0
        SagSendAT(UART1, "AT+CRC=0\r\n")
        SagWaitnMatchResp(UART1, ['*OK\r\n'], 2000)

        #Check Extended Error Report is ready    
        SagSendAT(UART1, "AT+CEER\r\n")
        SagWaitnMatchResp(UART1, ['\r\n+CEER: "No report available"\r\n\r\nOK\r\n'], 2000)
        
        #Check if the module hasn't been register
        if RAT_Param=="RAT_2G":
            SagSendAT(UART1, "AT+CREG?\r\n")
            SagWaitnMatchResp(UART1, ['\r\n+CREG: 0,0\r\n'], 2000)        
        elif RAT_Param=="RAT_4G":        
            SagSendAT(UART1, "AT+CEREG?\r\n")
            SagWaitnMatchResp(UART1, ['\r\n+CEREG: 0,0\r\n'], 2000)
    
        #Make a outgoing call
        if (H_AUDIO == "1"):    
            #Voice call support
            SagSendAT(UART1, "ATD" + AUX_VoiceNumber + ";\r\n")
        else:
            #Voice call not support
            SagSendAT(UART1, "ATD" + str(DUMMY_NUMBER) + ";\r\n")        
            SagWaitnMatchResp(UART1, ['*OK\r\n'], 2000)
            
        SagWaitnMatchResp(UART1, ['*OK\r\n'], 2000)
        SagWaitnMatchResp(UART1, ['*NO CARRIER\r\n'], 36000)

        #Check ERROR Report for call rejection
        time.sleep(5)
        SagSendAT(UART1, "AT+CEER\r\n")
        # 2017-03-15, pangoc, Correct the bahavior of +CEER error         
        SagWaitnMatchResp(UART1, ['\r\n+CEER: "CC setup error",288,"MM no service"\r\n\r\nOK\r\n'], 2000)        
        # SagWaitnMatchResp(UART1, ['*\r\n+CEER: *\r\n\r\nOK\r\n'], 2000)
        #Make Moudle 1 connect to the network

        SagSendAT(UART1, 'AT+CPIN="%s"\r\n' % SIM_Pin1)
        SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 4000)
        #SagWaitnMatchResp(UART1, ['\r\n+PBREADY\r\n'], 30000, update_result="not_critical")
        
        time.sleep(100)
        SagSendAT(UART1, "AT+COPS=0\r\n")
        SagWaitnMatchResp(UART1, ['*\r\nOK\r\n'], 60000)
                
        if RAT_Param=="RAT_2G":
            for i in range(24):
                print "Loop: ", str(i+1)
                SagSendAT(UART1, "AT+CREG?\r")
                match_result = SagWaitnMatchResp(UART1, ["\r\n+CREG: 0,1\r\n\r\nOK\r\n"], 5000, update_result="not_critical")
                if match_result == 1:
                    break
                if i == 23:
                    print "-------->Problem: Fail to register network !!!"
                    test_environment_ready = "Not_Ready" 
        elif RAT_Param=="RAT_4G":
            for i in range(24):
                print "Loop: ", str(i+1)
                SagSendAT(UART1, "AT+CEREG?\r")
                match_result = SagWaitnMatchResp(UART1, ["\r\n+CEREG: 0,1\r\n\r\nOK\r\n"], 5000, update_result="not_critical")
                if match_result == 1:
                    break
                if i == 23:
                    print "-------->Problem: Fail to register network !!!"
                    test_environment_ready = "Not_Ready"    
                
        SagSleep(20000)
        SagSendAT(UART1, "AT\r\n")
        SagWaitnMatchResp(UART1, ['*OK\r\n'], 60000, update_result="not_critical")        
        
        #Make a outgoing call
        if (H_AUDIO == "1"):
            #Outgoing call was rejected
            SagSendAT(UART1, "ATD" + AUX_VoiceNumber + ";\r\n")
            SagWaitnMatchResp(UART1, ['*OK\r\n'], 2000)
            
            SagWaitnMatchResp(AUX, ['*RING\r\n'], 10000)
            
            SagSendAT(AUX, 'ATH\r\n')
            SagWaitnMatchResp(AUX, ['*OK\r\n'], 6000)
            SagWaitnMatchResp(UART1, ['*NO CARRIER\r\n'], 4000)

            #Check ERROR Report    for call rejection
            time.sleep(5)
            SagSendAT(UART1, "AT+CEER\r\n")
            SagWaitnMatchResp(UART1, ['\r\n+CEER: "CC setup error",21,"Call rejected"\r\n\r\nOK\r\n'], 2000)
        else:
            #Voice call not support
            SagSendAT(UART1, "ATD" + str(DUMMY_NUMBER) + ";\r\n")
            SagWaitnMatchResp(UART1, ['*OK\r\n'], 2000)
            SagWaitnMatchResp(UART1, ['*NO CARRIER\r\n'], 60000)

            #Check ERROR Report    for call rejection
            time.sleep(5)
            SagSendAT(UART1, "AT+CEER\r\n")
            # 2017-03-15, pangoc, Correct the bahavior of +CEER error 
            #2017-04-14, NTSON Modifided to correct the behavior of +CEER error after making a voice call.
            #SagWaitnMatchResp(UART1, ['\r\n+CEER: "CC setup error",288,"MM no service"\r\n\r\nOK\r\n'], 2000)
            SagWaitnMatchResp(UART1, ['\r\n+CEER: "CC setup error",1,"Unassigned (unallocated) number"\r\n\r\nOK\r\n'], 2000)
            # SagWaitnMatchResp(UART1, ['\r\n+CEER: *\r\n\r\nOK\r\n'], 2000)

        # 2017-03-15, pangoc, Correct the bahavior of +CEER error 
        #Set a incorrect APN for internet
        SagSendAT(UART1, 'AT+CGDCONT=2,"IP","aaa.aaa"\r\n')
        SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 5000)

        SagSendAT(UART1, "AT+CGACT=1,2\r\n")
        SagWaitnMatchResp(UART1, ['\r\n+CME ERROR:*\r\n'], 60000)

        #Check ERROR Report    for call rejection
        SagSendAT(UART1, "AT+CEER\r\n")
        #Test with KTF_SIM3,HL7539
        # 2017-03-15, pangoc, Correct the bahavior of +CEER error 
        SagWaitnMatchResp(UART1, ['\r\n+CEER: "SM activation error",133,"Requested service option not subscribed"\r\n\r\nOK\r\n'], 2000)
                #SagWaitnMatchResp(UART1, ['\r\n+CEER: *\r\n\r\nOK\r\n'], 2000)
        #Clear the CGDCONT 2
        SagSendAT(UART1, 'AT+CGDCONT=2\r\n')
        SagWaitnMatchResp(UART1, ['\r\nOK\r\n'], 5000)        
        
        # Check point 2
        if VarGlobal.statOfItem != "OK":
            raise Exception("Check point failed")

    if (H_AUDIO == "1"):
        if AT_EXCEPT:
            SagSendAT(AUX, 'AT+EXCEPT\r')
            SagWaitnMatchResp(AUX, ['*\r\nOK\r\n'], 6000)

        # Close AUX
        SagClose(AUX)

except Exception, err_msg :
    VarGlobal.statOfItem = "NOK"
    print Exception, err_msg

PRINT_TEST_RESULT(test_ID, VarGlobal.statOfItem)

# -----------------------------------------------------------------------------------

print "\n----- Testing End -----\n"

print "\n************************************************************************************************"
if AT_EXCEPT:
    SagSendAT(UART1, 'AT+EXCEPT\r')
    SagWaitnMatchResp(UART1, ['*\r\nOK\r\n'], 6000)

# Close UART
SagClose(UART1)
