#!/usr/bin/python

#Remap SDK module
from remapSDK import remapSDK
#from remapSDK import Sdk


print('##################################### ReMAP WP5 Model PoC #####################################')

remapSdk=remapSDK.Sdk()

start=remapSdk.getStartTime()
print(start)

end_date=remapSdk.getEndTime()
print(end_date)

tailno=remapSdk.getTailNumber()
print(tailno)

partNo=remapSdk.getParamPartNumber("param1")
print(partNo)

metadata=remapSdk.getMetadata()
print(metadata)

replacements=remapSdk.getReplacements()
print(replacements)

output=remapSdk.sendOutput( "rulUnit", 5, 44, 55)
print(output)