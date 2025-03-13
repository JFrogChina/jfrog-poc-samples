def server
def rtMaven
def buildInfo

def RESOLVE_SNAPSHOT_REPO = 'slash-maven-virtual'
def RESOLVE_RELEASE_REPO = 'slash-maven-virtual'
def DEPLOY_SNAPSHOT_REPO = 'slash-maven-dev-local'
def DEPLOY_RELEASE_REPO = 'slash-maven-test-local'

node() {
    stage('Artifactory configuration') {
        server = Artifactory.server 'JFrogChina-Server'
        rtMaven = Artifactory.newMavenBuild()
        rtMaven.tool = 'maven'
        rtMaven.deployer releaseRepo:DEPLOY_RELEASE_REPO, snapshotRepo:DEPLOY_SNAPSHOT_REPO, server: server
        rtMaven.resolver releaseRepo:RESOLVE_RELEASE_REPO, snapshotRepo:RESOLVE_SNAPSHOT_REPO, server: server
        rtMaven.deployer.deployArtifacts = false
        rtMaven.deployer.addProperty("unit-test", "pass").addProperty("qa-team", "platform", "ui")
        buildInfo = Artifactory.newBuildInfo()
        buildInfo.env.capture = true
    }
    stage('Check out') {
        git url: 'https://gitee.com/mumu79/app-kubernetes.git', branch: 'main'
    }
    stage('Maven Build') {
        dir('app-boot') {
            warVersion = "1.0.${BUILD_NUMBER}"
            def descriptor = Artifactory.mavenDescriptor()
            descriptor.version = warVersion
            descriptor.failOnSnapshot = true
            descriptor.transform()

            rtMaven.tool = 'maven'
            rtMaven.run pom: 'pom.xml', goals: 'clean install', buildInfo: buildInfo
            server.publishBuildInfo buildInfo
        }
    }

    stage('Xray Scan') {
        def xrayConfig = [
            'buildName': env.JOB_NAME,
            'buildNumber': env.BUILD_NUMBER,
            'failBuild': false
        ]
        def xrayResults = server.xrayScan xrayConfig
//        echo xrayResults as String
        xrayurl = readJSON text:xrayResults.toString()
//        echo xrayurl as String
        rtMaven.deployer.addProperty("scan", "true")
        rtMaven.deployer.addProperty("xrayresult.summary.total_alerts", xrayurl.summary.total_alerts as String)
    }

    stage('Publish To Test Repo') {
        rtMaven.deployer.deployArtifacts buildInfo
    }
}









//    stage ('Promotion') {
//        promotionConfig = [
//                //Mandatory parameters
//                'buildName'          : buildInfo.name,
//                'buildNumber'        : buildInfo.number,
//                'targetRepo'         : 'slash-maven-release-local',
//
//                //Optional parameters
//                'comment'            : 'this is the promotion comment',
//                'sourceRepo'         : 'slash-maven-test-local',
//                'status'             : 'Released',
//                'includeDependencies': true,
//                'copy'               : true
//        ]
//
//        // Promote build
//        server.promote promotionConfig
//    }


