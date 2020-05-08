from git_stuff import GitManager
from compilation import CompileManager
from hydrogen import HydrogenAdapter
from arguments import get_args
import os
from pathlib import Path

class HydroGit:
    def __init__(self, url, commit_ids, language):
        self.git_commits = commit_ids

        wd = (Path(__file__).parent.absolute())
        tmp = wd / "tmp"
        self.git_manager=GitManager(url, tmp)
        self.compiler=CompileManager(language, tmp)
        self.hydrogen_manager=HydrogenAdapter(wd / "../buildninja/Hydrogen.out")

    def clone(self, local_dir):
        # git
        self.git_manager.clone(local_dir)
        self.git_manager.checkout_copy_versions(self.git_commits)

    def compile(self, verbose, with_cmake, rule):
        # compilation
        self.compiler.build_all(verbose, with_cmake, rule)

    def hydrogen(self):
        self.hydrogen_manager.run(self.compiler.versions_built)

def run(args):
    commit_ids = [args.first_version, *args.latter_versions]

    # setup
    hg=HydroGit(args.url, commit_ids, args.language)

    # clone
    hg.clone(args.local_dir)

    # fake compilation
    hg.compile(args.verbose, args.with_cmake, args.rule_name)

    # hydrogen
    hg.hydrogen()

if __name__ == '__main__':
    args = get_args()

    # git_url="https://github.com/feddischson/include_gardener.git"
    # commit_ids = ["093ab9c1126c6f946e4183dcf02d8cdff837337b", "90539a60dd83a6f0a30ecbb2ddfa3eeac529e975"]
    # langauge='CXX'
    # git_url="https://github.com/gydrogen/progolone.git"
    # commit_ids = ["5e8651df381079d0347ddfa254f554972611d1a0", "70d03532975252bd9982beba60a8720e11ec8f02", "9cde7197d0a3fe0caf7ee0ec7fd291e19ccc18ed"]
    # language='C'

    run(args)
