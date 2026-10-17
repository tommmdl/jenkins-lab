import jenkins.model.Jenkins
import hudson.security.HudsonPrivateSecurityRealm
import hudson.security.FullControlOnceLoggedInAuthorizationStrategy
import org.jenkinsci.plugins.workflow.job.WorkflowJob
import org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition
import hudson.plugins.git.GitSCM
import jenkins.install.InstallState

def j = Jenkins.get()
if (!(j.securityRealm instanceof HudsonPrivateSecurityRealm)) {
    def realm = new HudsonPrivateSecurityRealm(false)
    realm.createAccount('admin', new File('/run/secrets/admin_password').text.trim())
    j.setSecurityRealm(realm)
}
def authorization = new FullControlOnceLoggedInAuthorizationStrategy()
authorization.setAllowAnonymousRead(false)
j.setAuthorizationStrategy(authorization)
j.setNumExecutors(1)
j.setInstallState(InstallState.INITIAL_SETUP_COMPLETED)
if (j.getItem('jenkins-lab') == null) {
    def job = j.createProject(WorkflowJob, 'jenkins-lab')
    def scm = new GitSCM('https://github.com/tommmdl/jenkins-lab.git')
    scm.branches = [new hudson.plugins.git.BranchSpec('*/main')]
    job.definition = new CpsScmFlowDefinition(scm, 'Jenkinsfile')
    job.save()
}
j.save()
