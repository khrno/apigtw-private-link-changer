import boto3
import argparse
import pprint

parser = argparse.ArgumentParser()
parser.add_argument('--profile',
                    action="store",
                    required=True)
parser.add_argument('--apiId',
                    action="store",
                    required=True)
parser.add_argument('--connId',
                    action="store",
                    required=True)
parser.add_argument('--debug',
                    action="store_true",
                    default=False)
args = parser.parse_args()


session = boto3.Session(profile_name=args.profile)
apigateway = session.client('apigateway')


paginator = apigateway.get_paginator('get_resources')
iterator = paginator.paginate(restApiId=args.apiId)
total = 0
for page in iterator:
    for item in page['items']:
        try:
            verbs = list(item['resourceMethods'].keys())
            for verb in verbs:
                if verb != 'OPTIONS':
                    integration = apigateway.get_integration(
                        restApiId = args.apiId,
                        resourceId = item['id'],
                        httpMethod = verb
                    )
                    
                    if integration['connectionType'] == 'VPC_LINK' and integration['connectionId'] != args.connId:
                        total += 1
                        print(integration['connectionType'],integration['connectionId'])
                        print("Fixing,",item['path'],integration['connectionId'],integration['type'],verb)
                        apigateway.update_integration(
                            restApiId = args.apiId,
                            resourceId = item['id'],
                            httpMethod = verb,
                            patchOperations = [
                                {
                                    'op': 'replace',
                                    'path': '/connectionId',
                                    'value': args.connId
                                } 
                            ]
                        )

        except KeyError:
            if args.debug:
                print("KeyError exception found")
            pass
    if args.debug:
        print("Running on debug mode")
        break

print(total,"resources fixed")
        