import * as cdk from 'aws-cdk-lib';
import { aws_apigateway as apigateway } from 'aws-cdk-lib';
import { aws_iam as iam } from 'aws-cdk-lib';

declare const role: iam.Role;
declare const vpcLink: apigateway.VpcLink;

const httpIntegrationProps: apigateway.HttpIntegrationProps = {
  httpMethod: 'POST',
  options: {
    cacheKeyParameters: [],
    cacheNamespace: 'httpGatewayCacheNamespace',
    connectionType: apigateway.ConnectionType.INTERNET,
    contentHandling: apigateway.ContentHandling.CONVERT_TO_TEXT,
    credentialsPassthrough: false,
    credentialsRole: role,
    integrationResponses: [{
      statusCode: 'statusCode',

      // the properties below are optional
      contentHandling: apigateway.ContentHandling.CONVERT_TO_BINARY,
      responseParameters: {
        responseParametersKey: 'responseParameters',
      },
      responseTemplates: {
        responseTemplatesKey: 'responseTemplates',
      },
      selectionPattern: 'selectionPattern',
    }],
    passthroughBehavior: apigateway.PassthroughBehavior.WHEN_NO_MATCH,
    requestParameters: {
      requestParametersKey: 'requestParameters',
    },
    requestTemplates: {
      requestTemplatesKey: 'requestTemplates',
    },
    timeout: cdk.Duration.minutes(30),
    vpcLink: vpcLink,
  },
  proxy: false,
};