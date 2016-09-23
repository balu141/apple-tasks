import jenkins.model.*
import hudson.model.*
import hudson.slaves.*
Jenkins.instance.addNode(new DumbSlave("{{ slavename }}","test slave description","/tmp","1",Node.Mode.NORMAL,"test-slave-label",new JNLPLauncher(),new RetentionStrategy.Always(),new LinkedList())) 
