#!/bin/bash

az login

#!/bin/bash

az login

echo "Creating storage acount updatemcmembers for app..."
echo ""
az storage account create \
--name updatemcmembers \
--location southcentralus \
--resource-group member-central-api \
--sku Standard_LRS

echo ""
echo "Creating function environment in Azure..."
echo ""
az functionapp create \
--resource-group member-central-api \
--os-type Linux \
--consumption-plan-location eastus  \
--runtime python \
--name MC-API-Update \
--storage-account  updatemcmembers

echo ""
echo "Publishing app to Azure"
echo ""
func azure functionapp publish MC-API-Update --build remote