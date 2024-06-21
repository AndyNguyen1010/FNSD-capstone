

eksctl create cluster --name simple-jwt-api
kubectl get nodes
aws sts get-caller-identity --query Account --output text
aws iam create-role --role-name UdacityFlaskDeployCBKubectlRole --assume-role-policy-document file://trust.json --output text --query 'Role.Arn'

aws iam put-role-policy --role-name UdacityFlaskDeployCBKubectlRole --policy-name eks-describe --policy-document file://iam-role-policy.json

kubectl get -n kube-system configmap/aws-auth -o yaml > /tmp/aws-auth-patch.yml

kubectl patch configmap/aws-auth -n kube-system --patch "$(cat /tmp/aws-auth-patch.yml)"
kubectl get nodes
aws ssm put-parameter --name JWT_SECRET --overwrite --value "myjwtsecret" --type SecureString
## Verify
aws ssm get-parameter --name JWT_SECRET