#!/bin/bash

./scripts/clean.sh
./scripts/build-lambdas.sh

aws cloudformation package \
   --template-file cfn-stack.yml \
   --s3-bucket "$STAGING_BUCKET" \
   --output-template-file build/cfn-stack.yml

aws cloudformation deploy \
    --template-file build/cfn-stack.yml \
    --stack-name classful-prod \
    --parameter-overrides ParamRecaptchaSecret=$RECAPTCHA_SECRET \
    --capabilities CAPABILITY_IAM