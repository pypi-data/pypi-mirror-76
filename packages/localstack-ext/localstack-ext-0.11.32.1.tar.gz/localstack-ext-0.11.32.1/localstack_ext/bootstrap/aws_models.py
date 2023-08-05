from localstack.utils.aws import aws_models
rgEmd=super
rgEmL=None
rgEmV=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  rgEmd(LambdaLayer,self).__init__(arn)
  self.cwd=rgEmL
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,rgEmV,env=rgEmL):
  rgEmd(RDSDatabase,self).__init__(rgEmV,env=env)
 def name(self):
  return self.rgEmV.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,rgEmV,env=rgEmL):
  rgEmd(RDSCluster,self).__init__(rgEmV,env=env)
 def name(self):
  return self.rgEmV.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
