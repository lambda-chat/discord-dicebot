import * as path from 'path';
import * as cdk from 'aws-cdk-lib';
import * as lambda from "aws-cdk-lib/aws-lambda";
import { config } from "dotenv";

type Environment = {
  "PUBLIC_KEY": string;
}
const environment = config({ path: ".bridge.env" }).parsed as Environment;

export class BridgeLambdaStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // TODO: prepare lambda layer for Node.je runtime

    // const lambdaLayer = new lambda.LayerVersion(this, "python_packages", {
    //   code: lambda.Code.fromAsset(
    //     path.join(__dirname, "..", "python_packages")
    //   ),
    //   compatibleRuntimes: [lambda.Runtime.PYTHON_3_9],
    //   description: "Python Packages",
    // });

    const lambdaFn = new lambda.Function(this, "discord-dicebot-bridge", {
      functionName: "discord-dicebot-bridge",
      runtime: lambda.Runtime.NODEJS_14_X,
      handler: "index.js",  // FIXME
      code: lambda.Code.fromAsset(path.join(__dirname, "..", "..", "lambda")),  // FIXME
      timeout: cdk.Duration.seconds(10),
      retryAttempts: 1,
      environment,
      // layers: [lambdaLayer],
    });
  }
}
