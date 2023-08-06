import subprocess
import os
import re
import json
import yaml
import random
import logging
import datetime
from urlextract import URLExtract



from openselery.github_connector import GithubConnector
from openselery.librariesio_connector import LibrariesIOConnector
from openselery.coinbase_connector import CoinbaseConnector
from openselery import git_utils
from openselery import selery_utils
from openselery import os_utils
from openselery.visualization import visualizeTransactions



class OpenSelery(object):
    def __init__(self, config, silent=False):
        super(OpenSelery, self).__init__()
        print("=======================================================")
        # set our openselery project dir, which is '../../this_script'
        self.seleryDir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))
        self.silent = silent
        self.librariesIoConnector = None
        self.githubConnector = None
        self.config = config
        # start initialization of configs
        self.initialize()

    def __del__(self):
        self.logNotify("Feel free to visit us @ https://github.com/protontypes/openselery")
        print("=======================================================")

    def finish(self, receiptFilePath):
        success = True
        if receiptFilePath:
            self.logNotify("Done")
        else:
            self.logWarning("Receipt missing")
            self.logWarning("Failed!")
            success = False
        return success

    def initialize(self):
        self.logNotify("Initializing OpenSelery")

        self.seleryPackageInfo = os_utils.getPackageInfo("openselery")
        self.log("OpenSelery version [%s]" % self.seleryPackageInfo["version"])

        self.log("Preparing Configuration")
        ### find all configs in potentially given configdir
        foundConfigs = []
        if(self.config.config_dir):
            for root, dirs, files in os.walk(self.config.config_dir):
                for f in files:
                    ext = os.path.splitext(f)[1]
                    if ext == ".yml" or ext == ".yaml":
                        foundConfigs.append(os.path.join(root, f))
        ### group all found configs together with individually given configuration paths from user on top
        self.config.config_paths = foundConfigs + self.config.config_paths
        ### apply yaml config to our configuration if possible
        self.log("Loading configurations" % self.config.config_paths)
        [print(" -- %s" % path) for path in self.config.config_paths]
        [self.loadYaml(path) for path in self.config.config_paths]
        # load our readme file
        extractor = URLExtract()
        fundingPath = self._getFile("README.md")
        if fundingPath is not None:
            self.log("Loading funding file [%s] for bitcoin wallet" % fundingPath)
            mdfile = open('README.md', 'r')
            mdstring = mdfile.read()
            urls = extractor.find_urls(mdstring)
            badge_string = "https://en.cryptobadges.io/donate/"
            for url in urls:
                if badge_string in url:
                    self.config.bitcoin_address=url.split(badge_string, 1)[1]
                    self.log("Found bitcoin address [%s]" % self.config.bitcoin_address)
        else:
            self.log("Using bitcoin address from configuration file for validation check [%s]" % self.config.bitcoin_address)

        # load tooling url
        if self.config.include_tooling_and_runtime and self.config.tooling_path:
            with open(self.config.tooling_path) as f:
                self.config.toolrepos = yaml.safe_load(f)
            if self.config.toolrepos is not None:
                self.log("Tooling file loaded [%s]" % self.config.toolrepos)
            else:
                self.log("No tooling urls found")
        else:
            self.log("Tooling not included")

        # load our environment variables
        self.loadEnv()
        self.logNotify("Initialized")
        self.log(str(self.getConfig()))

    def loadEnv(self):
        self._execCritical(lambda: self.config.applyEnv(), [])

    def loadYaml(self, path):
        self._execCritical(lambda x: self.config.applyYaml(x), [path])

    def _execCritical(self, lambdaStatement, args=[], canFail=False):
        try:
            r = lambdaStatement(*args)
        except Exception as e:
            self.logError(str(e))
            raise e if not canFail else e
        return r

    def connect(self):
        # establish connection to restapi services
        self.log("Establishing LibrariesIO connection")
        self.librariesIoConnector = self._execCritical(
            lambda x: LibrariesIOConnector(x), [self.config.libraries_api_key])
        self.logNotify("LibrariesIO connection established")
        self.log("Establishing Github connection")
        self.githubConnector = self._execCritical(
            lambda x: GithubConnector(x), [self.config.github_token])
        self.logNotify("Github connection established")
        if not self.config.simulation:
            self.coinConnector = CoinbaseConnector(
                self.config.coinbase_token, self.config.coinbase_secret)

    def gather(self):
        generalContributors = []
        generalProjects = []
        generalDependencies = []
        self.log("Gathering project information")
        print("=======================================================")
        if self.config.include_self:
            self.logWarning("Including local project '%s'" %
                            self.config.directory)

            # find official repositories
            projectUrl = git_utils.grabLocalProject(
                self.config.directory)

            localProject = self.githubConnector.grabRemoteProjectByUrl(projectUrl)
            self.log(" -- %s" % localProject)
            self.log(" -- %s" % localProject.html_url)
            #print(" -- %s" % [c.author.email for c in localContributors])

            # safe dependency information
            generalProjects.append(localProject)

        if self.config.include_dependencies:
            self.log("Searching for dependencies of project '%s' " %
                     self.config.directory)
            # scan for dependencies repositories
            rubyScanScriptPath = os.path.join(self.seleryDir, "openselery", "ruby_extensions", "scan.rb")
            process = subprocess.run(["ruby", rubyScanScriptPath, "--project=%s" % self.config.directory],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            # exec and evaluate stdout
            if process.returncode == 0:
                dependencies_json = json.loads(process.stdout)
            else:
                self.logError("Could not find project manifesto")
                print(process.stderr)
                raise Exception("Aborting")

            # process dependency json
            unique_dependency_dict = selery_utils.getUniqueDependencies(
                dependencies_json)
            for platform, depList in unique_dependency_dict.items():
                for dep in depList:
                    d = dep["name"]
                    r = dep["requirement"]
                    print(" -- %s: %s [%s]" % (platform, d, r))
                    libIoProject = self.librariesIoConnector.findProject(
                        platform, d)
                    print("  > %s" % ("FOUND %s" %
                                      libIoProject if libIoProject else "NOT FOUND"))
                    # gather more information for project dependency
                    if libIoProject:
                        libIoRepository = self.librariesIoConnector.findRepository(
                            libIoProject)
                        libIoDependencies = self.librariesIoConnector.findProjectDependencies(
                            libIoProject)
                        print("  > %s" %
                              [dep.project_name for dep in libIoDependencies])

                        if libIoRepository:
                            gitproject = self.githubConnector.grabRemoteProject(
                                libIoRepository.github_id)

                            # safe project / dependency information
                            generalProjects.append(gitproject)
                            generalDependencies.extend(libIoDependencies)

        if self.config.include_tooling_and_runtime and self.config.tooling_path:
            for toolurl in self.config.toolrepos['github']:
                toolingProject = self.githubConnector.grabRemoteProjectByUrl(
                    toolurl)
                self.log(" -- %s" % toolingProject)
                self.log(" -- %s" % toolingProject.html_url)

                # safe dependency information
                generalProjects.append(toolingProject)

        self.log("Gathering contributor information")
        # scan for project contributors
        for p in generalProjects:
            # grab contributors
            depContributors = self.githubConnector.grabRemoteProjectContributors(
                p)
            # filter contributors
            depContributors = selery_utils.validateContributors(
                depContributors, self.config.min_contributions)
            # safe contributor information
            generalContributors.extend(depContributors)
        print("=======================================================")

        self.logNotify("Gathered valid directory: %s" %
                       self.config.directory)
        self.logNotify("Gathered '%s' valid repositories" %
                       len(generalProjects))
        self.logNotify("Gathered '%s' valid dependencies" %
                       len(generalDependencies))
        self.logNotify("Gathered '%s' valid contributors" %
                       len(generalContributors))
        return  self.config.directory, generalProjects, generalDependencies, generalContributors

    def weight(self, contributor, local_repo, projects, deps):
        release_weights=[0] * len(contributor) 
        github_contributors={}
        if self.config.consider_releases:
             # calc release weights
            self.log("Add additional weight to release contributors of last " +
                    str(self.config.releases_included)+" releases")
            # Create a unique list of all release contributor
            release_contributor = git_utils.find_release_contributor(
                local_repo, self.config.releases_included)
            release_contributor = set(i.lower() for i in release_contributor)
            self.log("Found release contributor: "+str(len(release_contributor)))
            for idx,user in enumerate(contributor):
                if user.stats.author.email.lower() in release_contributor:
                    release_weights[idx]=self.config.release_weight
                    self.log("Github email address matches git email from last release: " +user.stats.author.name )
            self.log("Release Weights:" +str(release_weights))
            # considers all release contributor equal
            release_contributor = set(release_contributor)

        # create uniform probability
        self.log("Start with unifrom probability weights for contributors")
        uniform_weights = selery_utils.calculateContributorWeights(
            contributor, self.config.uniform_weight)
        self.log("Uniform Weights:" +str(uniform_weights))

        # sum up the two list with the same size
        total_weights = [x + y for x, y in zip(uniform_weights, release_weights)]

        self.log("Total Weights:" +str(total_weights))
        # read @user from commit
        return total_weights

    def choose(self, contributors, repo_path, weights):
        recipients = []

        # chose contributors for payout
        self.log("Choosing recipients for payout")
        if len(contributors) < 1:
            self.logError("Could not find any contributors to payoff")
            raise Exception("Aborting")

        recipients = random.choices(
            contributors, weights, k=self.config.number_payout_contributors_per_run)
        for contributor in recipients:
            self.log(" -- '%s': '%s' [w: %s]" % (contributor.stats.author.html_url,
                                              contributor.stats.author.name, weights[contributors.index(contributor)]))
            self.log("  > via project '%s'" % contributor.fromProject)
        return recipients

    def visualize(self, receiptFilePath, transactionFilePath):
        if transactionFilePath:
            self.log("Creating visualizations for past transactions [%s]" % transactionFilePath)
            try:
                visualizeTransactions(self.config.result_dir, transactionFilePath)
            except Exception as e:
                self.logError("Error creating visualization: %s" % e)

    def payout(self, recipients):
        transactionFilePath = None
        receiptFilePath = None

        if not self.config.simulation:
            transactionFilePath = os.path.join(self.config.result_dir, "transactions.txt")
            receiptFilePath = os.path.join(self.config.result_dir, "receipt.txt")

            # check if the public address is in the privat wallet
            if self.config.check_equal_private_and_public_address:
                if self.coinConnector.iswalletAddress(self.config.bitcoin_address):
                    self.log("Public and privat address match")
                else:    
                    self.logError("Public address does not match wallet address")
                    raise Exception("Aborting")
                
            # Check what transactions are done on the account.
            self.log(
            "Checking transaction history of given account [%s]" % transactionFilePath)
            transactions = self.coinConnector.pastTransactions()
            with open(transactionFilePath, "w") as f:
                f.write(str(transactions))
            
            amount,currency = self.coinConnector.balancecheck()
            self.log("Chech account wallet balance [%s] : [%s]" % (amount, currency))

            # Create the balance badge to show on the README
            balance_badge = {
                "schemaVersion": 1,
                "label": currency,
                "message": amount,
                "color": "green"
                }

            balanceBadgePath = os.path.join(self.config.result_dir, "balance_badge.json")
            with open(balanceBadgePath, "w") as write_file:
                json.dump(balance_badge, write_file)

            native_amount, native_currency = self.coinConnector.native_balancecheck()
            self.log("Check native account wallet balance [%s] : [%s]" % (native_amount, native_currency)) 

            # Create the native balance badge to show on the README
            native_balance_badge = {
                "schemaVersion": 1,
                "label": native_currency+" @ "+datetime.datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')+" UTC" ,
                "message": native_amount,
                "color": "green"
                }

            nativeBalanceBadgePath = os.path.join(self.config.result_dir, "native_balance_badge.json")
            with open(nativeBalanceBadgePath, "w") as write_file:
                json.dump(native_balance_badge, write_file)

            self.log("Trying to pay out recipients")
            self.receiptStr = ""
            for contributor in recipients:
                if self.coinConnector.useremail() != contributor.stats.author.email:
                    receipt = self.coinConnector.payout(contributor.stats.author.email, self.config.btc_per_transaction,
                                                    self.config.skip_email, self._getEmailNote())
                    self.receiptStr = self.receiptStr + str(receipt)
                    self.log("Payout of [%s][%s] succeeded" % (receipt['amount']['amount'],receipt['amount']['currency']))
                else:
                    self.logWarning("Skip payout since coinbase email is equal to contributor email")
                
            with open(receiptFilePath, "a") as f:
                f.write(str(self.receiptStr))

        else:
            ### simulate a receipt
            receiptFilePath = os.path.join(
                    self.config.result_dir, "simulated_receipt.txt")

            self.logWarning(
                    "Configuration 'simulation' is active, so NO transaction will be executed")
            for contributor in recipients:
                self.log(" -- would have been a payout of '%.10f' bitcoin to '%s'" %
                         (self.config.btc_per_transaction, contributor.stats.author.name))

                with open(receiptFilePath, "a") as f:
                    f.write(str(recipients))
        return receiptFilePath, transactionFilePath


    def _getFile(self, file):
        file_path = os.path.join(self.seleryDir, file)
        if os.path.exists(file_path):
            self.log(file_path+" read")
            return file_path
        else:
            return None

    def _getEmailNote(self):
      repo_message = ""
      try:
         remote_url = git_utils.grabLocalProject(self.config.directory)
         owner_project_name = self.githubConnector.parseRemoteToOwnerProjectName(remote_url)
         repo_message = " to " + owner_project_name
      except Exception as e:
        print("Cannot detect remote url of git repo", e)

      prefix = "Thank you for your contribution" + repo_message
      postfix = "Find out more about OpenSelery at https://github.com/protontypes/openselery."
      inner = ": " + self.config.email_note if self.config.email_note else ""
      return prefix + inner + ". " + postfix

    def getConfig(self):
        return self.config

    def log(self, msg):
        self._log(".", msg)

    def logNotify(self, msg):
        self._log("*", msg)

    def logWarning(self, msg):
        self._log("!", msg)

    def logError(self, msg):
        self._log("#", msg)

    def _log(self, sym, msg):
        if not self.silent:
            match = re.search(r'([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', msg)
            if match is not None:
                print("Do not print privat email data")
            else:
                print("[%s] %s" % (sym, msg))

