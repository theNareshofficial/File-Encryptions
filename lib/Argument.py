#!/bin/python

class Argument:
    def __init__(self, args):
        self.command = []           # without ifen(-) commands
        self.options = []           # single ifen(-)  like -h
        self.optionValue = {}       # using set & Dictnory{} for unique value
        self.args = args
        print(args)

        for arg in self.args:       # Remove () here
            if "-" in arg:          # if ifen in arg that means options or optionValue
                if "=" in arg:      # Checking if equal sign is present in options arg
                    pair = arg.split('=')     # splitting ifen and equal
                    self.optionValue[pair[0]] = pair[1]     # corrected assignment
                    self.options.append(pair[0])            # corrected usage of append
                else:
                    self.options.append(arg)
            else:
                self.command.append(arg)

    def hashOptions(self, options: list):                # Checking User given options are there or not
        userOptions = set(options)                       # User given Options
        reqOptions = set(self.options)                   # reqOptions = requiredOptions (My options)
        return list(reqOptions & userOptions)            # checking user options and my options if any match, return value
    
    def hashOption(hash, option):                              # Checking hashOptions in value is thir or not
        return option in self.hashOptions([option])            # if options it's avaliable return True or not
    
    def hashCommands(self, commands):
        userCommands = set(commands)
        reqCommands = set(self.commands)
        return list(reqCommands & userCommands)
    
    def hashCommand(self, command):
        return command in self.hashCommands(command)
    
    def getOptionsValue(self, options, default=None):         # if I pass option this func provide value eg : -h value : This is help message
        if options in self.optionValues:        # Checking key value is there or not
            return self.optionValues[options]   # if key is there it's return key value options
        else:
            return default                      # if conditions not woriking then return default, default mean None



# Testing the class
# a = Argument(['hello', '-f'])
# print(a.hashOptions(['-f']))
