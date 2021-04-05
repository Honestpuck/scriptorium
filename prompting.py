#!/usr/bin/env python3

# prompting test

print("Script details")


<?xml version="1.0" encoding="UTF-8"?>
  <script>
    <id>78</id>
    <name>admin-1.1.sh</name>
    <category>Security</category>
    <filename>admin-1.1.sh</filename>
    <info/>
    <notes>Creates an admin account with random name and password then saves the details in extension attributes
v1.1 - Added code to delete existing secret admin</notes>
    <priority>After</priority>
    <parameters/>
    <os_requirements/>
    <script_contents>#!/bin/bash
#
# admin.sh
# v 1.0 ARW 09/01/2020
# create an admin account with random name and password
# v 1.1 - Added code to delete existing secret admin 10/01/2020 (ARW)
# v 1.2 - Improved method of getting current admin 13/01/202 (ARW)

# Jamf Pro details
api_name='api_computers'
api_pass='changeit!'
api_base='https://suncorp.jamfcloud.com/JSSResource/computers'

# get a random name and password
name=$(openssl rand -base64 32 | tr -cd '[:lower:]' | head -c 6 ; echo '')
passwd=$(openssl rand -base64 64 | tr -cd '[:alnum:]' | tr -d '1l0O' | head -c 8 ; echo '')

# get the record of this computer
url="${api_base}/name/$(hostname)"
rec=$(curl -su ${api_name}:${api_pass} -X GET $url)
# get the ID
id=$(echo $rec | xmllint --xpath 'string(/computer/general/id)' -)

# get the admin_name
current_admin=$(echo $rec | xmllint -xpath "//extension_attributes/extension_attribute[./name = 'admin_name']/value/text()" - )

# create the data to be sent to Jamf
