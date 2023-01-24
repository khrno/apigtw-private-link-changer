# apigtw-private-link-changer

### How to execute

```
docker build -t apigtw-changer .

docker run  -v ~/.aws:/root/.aws -it apigtw-changer --profile Mifel --apiId <API_ID> --connId <CONN_ID>
```

### Parameters

1. `profile` (required): AWS Profile on your local machine

2. `apiId` (required): Rest API Gateway ID

3. `connId` (required): VPC Private Link to homologate

4. `debug` (optional): First page only and don't made changes.