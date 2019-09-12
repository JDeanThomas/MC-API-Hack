#!/bin/bash

az login

echo ""
printf "Enter name for resource group:\n"
printf "(Suggested: member-central-api)\n"
echo ""
read -p "Resource Group: " resource_group
echo ""

printf "Enter name for data container:\n"
printf "(Suggested: oajustice)\n"
echo ""
read -p "Container Name: " container_name
echo ""

printf "Enter name for member data Blob:\n"
printf "(Suggested: members)\n"
echo ""
read -p "Blob Name: " member_blob_name
echo ""


echo "Deleting previous resource group instance..."
az group delete --name member-central-api

echo ""

echo "creating resource group..."
az group create \
    --name $resource_group \
    --location southcentralus

echo "Creting storage account..."
AZURE_STORAGE_ACCOUNT=$(az storage account create \
    --name $container_name \
    --resource-group $resource_group \
    --location southcentralus \
    --sku Standard_LRS \
    --encryption blob \
    --query "name" | tr -d '"')

export AZURE_STORAGE_ACCOUNT

echo "Grabbing account key..."
AZURE_STORAGE_KEY=$(az storage account keys list \
    --resource-group $resource_group\
    --account-name $AZURE_STORAGE_ACCOUNT \
    --query "[0].value" | tr -d '"')

export AZURE_STORAGE_KEY

echo ""
echo $AZURE_STORAGE_ACCOUNT
echo $AZURE_STORAGE_KEY
echo ""

echo "Creating the container..."
az storage container create --name $container_name

echo "Extracting member index and creating CSV of full member data..."
python3 member_API.py

echo ""

echo "Uploading the the index and member file to Blob storage..."
az storage blob upload \
    --container-name $container_name \
    --file ./Members.csv \
    --name $member_blob_name \
    --auth-mode key

echo "Listing the blobs..."
az storage blob list --container-name $container_name --output table

echo "Done"