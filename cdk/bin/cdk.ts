#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { BridgeLambdaStack } from '../lib/bridge-lambda-stack';
import { EngineLambdaStack } from '../lib/engine-lambda-stack';

const app = new cdk.App();
new BridgeLambdaStack(app, 'BridgeLambdaStack');
new EngineLambdaStack(app, 'EngineLambdaStack');
