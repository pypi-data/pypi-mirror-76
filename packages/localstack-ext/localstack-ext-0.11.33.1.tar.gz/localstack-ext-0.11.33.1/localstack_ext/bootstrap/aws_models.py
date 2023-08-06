from localstack.utils.aws import aws_models
xzjwI=super
xzjwV=None
xzjwl=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  xzjwI(LambdaLayer,self).__init__(arn)
  self.cwd=xzjwV
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,xzjwl,env=xzjwV):
  xzjwI(RDSDatabase,self).__init__(xzjwl,env=env)
 def name(self):
  return self.xzjwl.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,xzjwl,env=xzjwV):
  xzjwI(RDSCluster,self).__init__(xzjwl,env=env)
 def name(self):
  return self.xzjwl.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
