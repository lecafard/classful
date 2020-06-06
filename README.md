Classful
========

```sh
./scripts/build-lambdas.sh
aws cloudformation package --template-file cfn-stack.yml --s3-bucket <cloudformation bucket> --output-template-file build/cfn-stack.yml
aws cloudformation deploy --template-file build/cfn-stack.yml --stack-name classful-prod --capabilities CAPABILITY_IAM --parameter-overrides ParamRecaptchaSecret=<recaptcha secret>
```

Inside frontend
```sh
REACT_APP_RECAPTCHA_KEY="<recaptcha-public>" REACT_APP_API_URL="<api url>" yarn build
```

There are some issues with CORS so you do need to enable it manually.