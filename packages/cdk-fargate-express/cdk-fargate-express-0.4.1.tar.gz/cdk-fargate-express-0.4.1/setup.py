import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-fargate-express",
    "version": "0.4.1",
    "description": "A sample JSII construct lib for Express Apps in AWS Fargate",
    "license": "Apache-2.0",
    "url": "https://github.com/pahud/cdk-fargate-express.git",
    "long_description_content_type": "text/markdown",
    "author": "Pahud Hsieh<pahudnet@gmail.com>",
    "project_urls": {
        "Source": "https://github.com/pahud/cdk-fargate-express.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cd_fargate_express",
        "cd_fargate_express._jsii"
    ],
    "package_data": {
        "cd_fargate_express._jsii": [
            "cdk-fargate-express@0.4.1.jsii.tgz"
        ],
        "cd_fargate_express": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.10.0, <2.0.0",
        "publication>=0.0.3",
        "aws-cdk.aws-ec2==1.59.0",
        "aws-cdk.aws-ecs==1.59.0",
        "aws-cdk.aws-ecs-patterns==1.59.0",
        "aws-cdk.core==1.59.0",
        "constructs>=3.0.4, <4.0.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ]
}
"""
)

with open("README.md") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
