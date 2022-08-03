/* eslint-disable import/no-extraneous-dependencies */
import {
  CorsHttpMethod,
  HttpApi,
  HttpMethod,
} from '@aws-cdk/aws-apigatewayv2-alpha';
import {HttpLambdaIntegration} from '@aws-cdk/aws-apigatewayv2-integrations-alpha';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as cdk from 'aws-cdk-lib';
import * as path from 'path';
// import { config } from "dotenv";


type Environment = { [key: string]: string };

const environment: Environment = {};  // config({ path: ".env" }).parsed as Environment;

export class DiscordDicebotAppStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // 👇 create our HTTP Api
    const httpApi = new HttpApi(this, 'dicebot-http-api', {
      description: 'HTTP API example',
      corsPreflight: {
        allowHeaders: [
          'Content-Type',
          'X-Amz-Date',
          'Authorization',
          'X-Api-Key',
        ],
        allowMethods: [
          // CorsHttpMethod.OPTIONS,
          // CorsHttpMethod.GET,
          CorsHttpMethod.POST,
          // CorsHttpMethod.PUT,
          // CorsHttpMethod.PATCH,
          // CorsHttpMethod.DELETE,
        ],
        allowCredentials: true,
        allowOrigins: ['http://localhost:3000'],
      },
    });

    const lambdaLayer = new lambda.LayerVersion(this, "python-packages", {
      code: lambda.Code.fromAsset(
        path.join(__dirname, "..", "python_packages")
      ),
      compatibleRuntimes: [lambda.Runtime.PYTHON_3_9],
      description: "Python Packages",
    });
    const dicebotlambdaFn = new lambda.Function(this, "discord-dicebot-lambda", {
      functionName: "discord-dicebot",
      runtime: lambda.Runtime.PYTHON_3_9,
      handler: "app.handler",
      code: lambda.Code.fromAsset(path.join(__dirname, "..", "..", "lambda")),
      timeout: cdk.Duration.seconds(5),
      retryAttempts: 1,
      environment,
      layers: [lambdaLayer],
    });

    httpApi.addRoutes({
      path: '/roll',
      methods: [HttpMethod.POST],
      // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-call
      integration: new HttpLambdaIntegration(
        'dicebot-lambda-integration-roll',
        dicebotlambdaFn,
      ),
    });
  }
}