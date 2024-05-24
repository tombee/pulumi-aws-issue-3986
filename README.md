# Reproduction of pulumi-aws issue 3986

- [ISSUE-3986](https://github.com/pulumi/pulumi-aws/issues/3986)

The `dev` stack is used to stage resources for repro.
The `repro` stack is used for importing staged resources back into a new stack and reproducing the issue

## Usage

```
pulumi stack select dev
pulumi up

bash repro.sh

...
error: aws:ec2/routeTable:RouteTable resource 'pulumi-import-issue-3986-rtb' has a problem: "" is not a valid CIDR block: invalid CIDR address: . Examine values at 'pulumi-import-issue-3986-rtb.routes'.
```
