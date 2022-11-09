#!/usr/bin/env python

import os

# Bin directory
BIN_DIR = "./bin/"

# Cloud Foundry Environment
CF_APP_NAME       = "PUT_HERE: APPLICATION_NAME"
CF_ORG            = "PUT HERE: ORG NAME"
CF_SPACE_PROD     = "Production"
CF_SPACE_DEV      = "Development"
CF_SPACE_TEST     = "Test"
CF_ENTRYPOINT     = "https://api.apps1-or-int.icloud.intel.com"
CF_DOMAIN         = "apps1-or-int.icloud.intel.com"
CF_IAP_ID         = 99999
CF_INSTANCES_PROD = 3
CF_MANIFEST       = "./manifest.yml"
CF_PROD_MEM       = "4096M"
CF_PROD_DISK      = "4096M"
CF_NON_PROD_MEM   = "4096M"
CF_NON_PROD_DISK  = "4096M"
CF_USERNAME       = os.environ.get('CF_USERNAME')
CF_PASSWORD       = os.environ.get('CF_PASSWORD')