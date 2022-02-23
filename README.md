# SFNX: GeoSearch

## PyPi module local installation

```
$ pip install -t services/reverse_geoinfo requests
```

## AWS SAM commands

```
$ aws cloudformation --profile simpleform package --template-file template.yml --s3-bucket s3-simpleform-yamagishihrd-artifacts --output-template-file artifacts/packaged-template.yml
```

```
$ aws cloudformation --profile simpleform --region ap-northeast-1 deploy --template-file artifacts/packaged-template.yml --capabilities CAPABILITY_IAM --stack-name cfn-stack-sfnx-function-geosearch
```

```
$ aws cloudformation --profile simpleform --region ap-northeast-1 delete-stack --stack-name cfn-stack-sfnx-function-geosearch
```

```
$ aws cloudformation --profile simpleform --region ap-northeast-1 list-stacks
```

---
EOF