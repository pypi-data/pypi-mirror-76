from localstack.utils.aws import aws_models
YvrbO=super
Yvrbx=None
Yvrbj=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  YvrbO(LambdaLayer,self).__init__(arn)
  self.cwd=Yvrbx
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,Yvrbj,env=Yvrbx):
  YvrbO(RDSDatabase,self).__init__(Yvrbj,env=env)
 def name(self):
  return self.Yvrbj.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,Yvrbj,env=Yvrbx):
  YvrbO(RDSCluster,self).__init__(Yvrbj,env=env)
 def name(self):
  return self.Yvrbj.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
