from pathlib import Path
import subprocess
from compilation import hydrogit_target_tag

class HydrogenAdapter:
    def __init__(self, hydrogen_binary):
        self.hy=hydrogen_binary
        assert self.hy.exists()

    def run(self, versions):
        '''
        Run Hydrogen on these versions
        '''

        # Select version
        bcs = [bc for v in versions for bc in v.bc_paths]
        target_names_unique = set([bc.stem.replace(hydrogit_target_tag, '') for bc in bcs])
        target_names = sorted(list(target_names_unique))
        if len(target_names) > 1:
            print(f'{len(target_names)} targets found:')
            print(' '.join(f'''{i}) {name}''' for i, name in enumerate(target_names, start=1)))

            try:
                selection_no = int(input(f'''Select a target to build(1-{len(target_names)}):'''))
            except KeyboardInterrupt:
                print()
                return

            build_target = target_names[selection_no - 1]
        else:
            build_target = target_names[0]
        build_target_bc = f'{build_target}{hydrogit_target_tag}'

        # Run Hydrogen
        args=[]
        for version in versions:
            build_target = next(bc for bc in version.bc_paths if bc.stem == build_target_bc)
            args.append(build_target)
        for version in versions:
            args.append("::")
            for c_path in version.c_paths:
                args.append(c_path)

        cmd = [str(self.hy)] + [str(arg) for arg in args]
        print(f'running command {cmd}')

        subprocess.run(cmd)
