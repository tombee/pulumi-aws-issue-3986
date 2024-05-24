#!/bin/bash

# Usage:
# 	bash repro.sh

declare -A resource_types=(["rtb"]="aws:ec2/routeTable:RouteTable" ["igw"]="aws:ec2/internetGateway:InternetGateway" ["vpc"]="aws:ec2/vpc:Vpc")

pulumi stack select dev
dev_stack_outputs=$(pulumi stack output --json)

pulumi stack rm repro --preserve-config --yes --force
pulumi stack init repro
pulumi stack select repro
pulumi
echo "${dev_stack_outputs}" | jq -r 'to_entries[] | "\(.key) \(.value)"' | while read -r name value; do
	pulumi import --yes "${resource_types[${name}]}" "pulumi-import-issue-3986-${name}" "${value}"
done

pulumi preview -v=9 --diff
