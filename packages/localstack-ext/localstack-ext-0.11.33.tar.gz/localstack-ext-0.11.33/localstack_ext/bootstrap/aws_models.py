from localstack.utils.aws import aws_models
KLtow=super
KLtoS=None
KLtoO=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  KLtow(LambdaLayer,self).__init__(arn)
  self.cwd=KLtoS
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,KLtoO,env=KLtoS):
  KLtow(RDSDatabase,self).__init__(KLtoO,env=env)
 def name(self):
  return self.KLtoO.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,KLtoO,env=KLtoS):
  KLtow(RDSCluster,self).__init__(KLtoO,env=env)
 def name(self):
  return self.KLtoO.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
