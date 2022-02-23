# SFNX: GeoSearch

## PyPi module local installation

```
$ pip install -t services/reverse_geoinfo requests
```

## AWS SAM : package & deploy

```
$ aws cloudformation package --profile simpleform --template-file template.yml --s3-bucket s3-simpleform-yamagishihrd-artifacts --output-template-file artifacts/packaged-template.yml
```

```
$ aws cloudformation deploy --profile simpleform --region ap-northeast-1 --template-file artifacts/packaged-template.yml --stack-name cfn-stack-sfnx-geo-search --capabilities CAPABILITY_IAM
```
