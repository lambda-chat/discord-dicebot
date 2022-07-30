import * as path from 'path';
import * as cdk from 'aws-cdk-lib';
import * as lambda from "aws-cdk-lib/aws-lambda";
import { config } from "dotenv";

type Environment = {
  "ENGINE_LAMBDA_API_KEY": string;
}
const environment = config({ path: ".engine.env" }).parsed as Environment;

export class EngineLambdaStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const lambdaLayer = new lambda.LayerVersion(this, "python_packages", {
      code: lambda.Code.fromAsset(
        path.join(__dirname, "..", "python_packages")
      ),
      compatibleRuntimes: [lambda.Runtime.PYTHON_3_9],
      description: "Python Packages",
    });

    const lambdaFn = new lambda.Function(this, "discord-dicebot-engine", {
      functionName: "discord-dicebot-engine",
      runtime: lambda.Runtime.PYTHON_3_9,
      handler: "app.handler",
      code: lambda.Code.fromAsset(path.join(__dirname, "..", "..", "lambda")),
      timeout: cdk.Duration.seconds(5),
      retryAttempts: 1,
      environment,
      layers: [lambdaLayer],
    });
  }
}
