from localstack.utils.aws import aws_models
nkPrK=super
nkPrW=None
nkPrq=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  nkPrK(LambdaLayer,self).__init__(arn)
  self.cwd=nkPrW
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,nkPrq,env=nkPrW):
  nkPrK(RDSDatabase,self).__init__(nkPrq,env=env)
 def name(self):
  return self.nkPrq.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,nkPrq,env=nkPrW):
  nkPrK(RDSCluster,self).__init__(nkPrq,env=env)
 def name(self):
  return self.nkPrq.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
