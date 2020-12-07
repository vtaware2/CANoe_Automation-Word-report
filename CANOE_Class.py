# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 13:09:03 2020

@author: Vikas
"""

## Canoe Class details with all the functionalities to be explored
## Note:- Create the .cfg file first with the details ready such as dbc file, 
# CAPL script for excution. Panel if required for any work before starting the 
# automation of CANoe with pythons.
# win 32com.client important for real time data gathering and accessing the 
# CANoe enviornmrnt
import win32com.client as win32
import os 
import subprocess
import time

# Check all the processes running currently on the PC with subprocess and 
# if CANoe is running close the current application 
class CANoe:
    ## for class initialization __init__ is an important syntax
    def __init__(self):
        # Checking the tasks runnign in the background and closing the CANoe
        # tasks runnning in the background
        self.application = None
        output = subprocess.check_output('tasklist', shell=True)
        ## printing out the list of tasks to have a look if required
        #print(output)
        ## Closing the CANoe 64 bit version                                              
        if ("CANoe64.exe" in str(output)) :
            os.system("taskkill /im CANoe64.exe /f 2>nul >nul")
            print('Previous CANoe application Terminated')
        ## closing the CANoe 32 bit version
        elif("CANoe32.exe" in str(output)):
            os.system("taskkill /im CANoe32.exe /f 2>nul >nul")
            print('Previous CANoe application Terminated')
        else:
            print('No Previously running application available.')
        
        ## Opeinign the CANoe application once the ystsem is initialised
        # to open the CANoe application
        self.application = win32.DispatchEx('CANoe.Application')                 
        ## second command to open CANoe using the win32com
        # self.application = win32.gencache.EnsureDispatch('CANoe.Application')
        
        ## Checking the version of the loaded CANoe
        self.sof_ver = self.application.Version
        print('Loaded software version is ', str(self.sof_ver)) 
        
        ## Clarifying the measurement running status
        self.Measurement = self.application.Measurement.Running
        print('Measurement running status is', str(self.Measurement))
            
    def open_cfg(self,cfgname):
        "@ cfg name required in text format for the system to perform"
        try:
            cfgname_check = cfgname.split('.')
            # print(cfgname_check)
            if (cfgname_check[len(cfgname_check)-1]) == 'cfg':
                if os.path.isfile(cfgname):
                    f_path = os.path.abspath(cfgname)
                    # print(f_path)
                    self.open_cfg = self.application.Open(f_path)
            else:
                cfgname = cfgname + '.cfg'
                # print(cfgname)
                if os.path.isfile(cfgname):
                    f_path = os.path.abspath(cfgname)
                    self.open_cfg = self.application.Open(f_path)
        except:
            raise RuntimeWarning("File with mentioned name not available")
           
    ## Start the CANoe Simulation
    def start_measure(self):
        if (self.application != None):
            if self.application.Measurement.Running is False:
                self.application.Measurement.Start()
            else:
                raise RuntimeWarning('System already in simulation mode.')
        else: 
            raise RuntimeWarning('CANoe application is not on.')
    
    ## Stop the CANoe Simulation
    def stop_measure(self):
        if (self.application != None):
            if self.application.Measurement.Running is True:
                self.application.Measurement.Stop()
            else:
                raise RuntimeWarning('No simulation on')
        else:
            raise RuntimeWarning('CANoe application is not on.')
            
    ## Getting the system variable value
    def get_sysVar(self, name_space, var_name):
        if (self.application != None):
            CANsystem = self.application.System.Namespaces
            system_namespace = CANsystem(name_space)
            system_value = system_namespace.Variables(var_name)
            return system_value.Value
        else:
            raise RuntimeWarning('CANoe application is not on')
    
    ## Getting the all the system variable value
    def get_allsysVar(self, name_space):
        if (self.application != None):
            CANsystem = self.application.System.Namespaces
            system_namespace = CANsystem(name_space)
            system_info = system_namespace.Variables
            sys_var_detail = []
            for i in system_info:
                sys_var_detail.append((i.Name,i.Value))
            return sys_var_detail
        else:
            raise RuntimeWarning('CANoe application is not on')
            
    ## Setting system variable to a particular value
    def set_sysVar(self, name_space, var_name,var):
        if (self.application != None):
            CANsystem = self.application.System.Namespaces
            system_namespace = CANsystem(name_space)
            system_value = system_namespace.Variables(var_name)
            system_value.Value = var
            check = 0
            while check == 0:
                CANsystem = self.application.System.Namespaces
                system_namespace = CANsystem(name_space)
                system_valueC = system_namespace.Variables(var_name)
                if system_valueC.Value == var:
                    check = 1
                else:
                    check = 0
        else:
            raise RuntimeWarning('CANoe application is not on')
    
    ## Getting the system variable value
    def get_envVar(self, var_name):
        if (self.application != None):
            env_value = self.application.Environment.GetVariable(var_name)
            return env_value.Value
        else:
            raise RuntimeWarning('CANoe application is not on')
    
    ## Setting Enviornment variable to a particular value
    def set_envVar(self, var_name, var):
        if (self.application != None):
            env_value = self.application.Environment.GetVariable(var_name)
            env_value.Value = var
            check = 0
            while check == 0:
                env_valueC = self.application.Environment.GetVariable(var_name)
                if env_valueC.Value != var:
                    check = 0
                else:
                    check = 1
        else:
            raise RuntimeWarning('CANoe application is not on')
    
    ## Get signal value from the CAN bus
    def get_signal(self, chanel, msg_name, sig_name, bustype = "CAN"):
        if (self.application != None):
            CANsignal = self.application.GetBus(bustype).GetSignal(chanel,msg_name,sig_name)
            return CANsignal.Value
        else:
            raise RuntimeWarning('CANoe application is not open')
    
    ## Set signal value from the CAN bus
    def set_signal(self, chanel, msg_name, sig_name, var, bustype = "CAN"):
        if (self.application != None):
            CANsignal = self.application.GetBus(bustype).GetSignal(chanel,msg_name,sig_name)
            CANsignal.Value = var
            print('Check if the value chnaged might be issue of transmitter not avaialable')
        else:
            raise RuntimeWarning('CANoe application is not open')
    
    ##Get list of all test enviornments available
    def get_list_tes_env(self):
        if (self.application != None):    
            temp_test_env = self.application.Configuration.TestSetup.TestEnvironments
            test_env = []
            for i in temp_test_env:
                test_env.append(i.Name)
            return test_env
        else:
            raise RuntimeWarning('CANoe application is not on')
        
    ## Getting list of all test modules in a test enviornment
    def list_test_module(self,test_env_name):
        if (self.application != None):
            temp_mod_list = self.application.Configuration.TestSetup.TestEnvironments.Item(test_env_name)
            temp_mod_list = win32.CastTo(temp_mod_list, "ITestEnvironment2")
            modules = temp_mod_list.TestModules
            list_module = []
            for i in modules:
                list_module.append(i.Name)
            return list_module
        else:
            raise RuntimeWarning("CANoe application is not open.")
    
    ## running a particular test module
    def test_module_run(self, test_env_name, test_module_name):
        if (self.application != None):
            if self.application.Measurement.Running is True:
                test_env = self.application.Configuration.TestSetup.TestEnvironments.Item(test_env_name)
                test_env = win32.CastTo(test_env, "ITestEnvironment2")
                test_module = test_env.TestModules.Item(test_module_name)
                # seq = test_module.Sequence
                # print(seq.Count)
                test_module.Start()
                seq = test_module.Sequence
                # print(seq.Count)
                while seq.Count < 1:
                    seq = test_module.Sequence
                    # print(seq.Count)
                tc_result = []
                tc_status = [] 
                for i in range(1,seq.Count+1):
                    tc_check = win32.CastTo(seq.Item(i), "ITestCase")
                    tc_result.append(tc_check.Verdict)
                    tc_status.append(tc_check.Enabled)
                return tc_result,tc_status  
            else:
                raise RuntimeWarning('CANoe application is not simulating, cannot run the test enviornment')
        else:
            raise RuntimeWarning('CANoe application is not open')
    ## Close the application CANoe
    def Close(self):
        ## closing the application after running all the operations as desired 
        if (self.application != None):
            self.Close = self.application.Quit()
        else:
            raise RuntimeWarning('CANoe application is not on')

## Command details to use the above class
# app = CANoe()                                               # Open the CANoe
# file_name = 'pr1_test_automation'                           # Provide the configuration file name to open
# app.open_cfg(file_name)                                     # to open the particular cfg file
# # temp = app.test_module_run('test1', 'test_1')
# namespace = 'TestCase'
# var_name = 'TestCase1'
# check_all = app.get_allsysVar(namespace)
# for i in check_all:
#     print(i)
# check = app.get_sysVar(namespace, var_name)                 # get value of the system variable
# print(check)
# app.start_measure()                                         # command to start simulation
# var = 250
# app.set_sysVar(namespace, var_name,var)
# check2 = app.get_sysVar(namespace, var_name)
# print(check2)
# time.sleep(5)
# temp1 = app.test_module_run('test1', 'test_1')
# print(temp1)
# temp2 = app.test_module_run('test1', 'test_2')
# print(temp2)
# # app.set_signal(1, 'EngineData', 'EngineRPM')
# time.sleep(2)
# sig_RPM1 = app.get_signal(1, 'EngineData', 'EngineRPM')
# print(sig_RPM1)
# temp3 = app.test_module_run('test1', 'test_3')
# print(temp3)
# sig2 = app.get_signal(1, 'EngineData', 'EngineRPM')
# print(sig2)
# app.stop_measure()                                          # command to stop simulation
# # # app.Close()                                             # Closing the CANoe