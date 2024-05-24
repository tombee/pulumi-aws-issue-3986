"""
Sample program to reproduce issue 3986

When a Route Table is imported, its optional attributes are set to ""
"""

import pulumi
import pulumi_aws as aws

import_issue_vpc = aws.ec2.Vpc(
    "pulumi-import-issue-3986-vpc",
    cidr_block="10.255.255.0/24",
    tags={"Name": "pulumi-import-issue-3986"},
)

internet_gateway = aws.ec2.InternetGateway(
    "pulumi-import-issue-3986-igw", vpc_id=import_issue_vpc.id
)

if pulumi.get_stack() == "dev":
    # This stack is for staging AWS resources for repro
    route_table = aws.ec2.RouteTable(
        "pulumi-import-issue-3986-rtb",
        vpc_id=import_issue_vpc.id,
        routes=[
            aws.ec2.RouteTableRouteArgs(
                cidr_block="0.0.0.0/0",
                gateway_id=internet_gateway.id,
            ),
        ],
    )
    pulumi.export("vpc", import_issue_vpc.id)
    pulumi.export("igw", internet_gateway.id)
    pulumi.export("rtb", route_table.id)
else:
    # This is the actual stack we're importing into
    repro_route_table = aws.ec2.RouteTable(
        "pulumi-import-issue-3986-rtb",
        vpc_id=import_issue_vpc.id,
        tags={"Name": "pulumi-import-issue-3986"},
        # NOTE: Adding this ignore_changes is actually what triggers the issue
        # from what I can see!
        opts=pulumi.ResourceOptions(ignore_changes=["routes"]),
    )
    pulumi.export("vpc", import_issue_vpc.id)
    pulumi.export("igw", internet_gateway.id)
    pulumi.export("rtb", repro_route_table.id)
    pulumi.export("repro", True)
