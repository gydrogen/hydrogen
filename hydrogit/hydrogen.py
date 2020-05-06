from pathlib import Path
import subprocess
from compilation import hydrogit_target_tag

class HydrogenAdapter:
    def __init__(self, hydrogen_binary):
        self.hy=hydrogen_binary
        assert self.hy.exists()

    def select_target(self, versions):
        '''
        Select target to build
        '''
        bcs = [bc for v in versions for bc in v.bc_paths]
        target_names_unique = set([bc.stem.replace(hydrogit_target_tag, '') for bc in bcs])
        target_names = sorted(list(target_names_unique))
        if len(target_names) > 1:
            print(f'{len(target_names)} targets found:')
            print(' '.join(f'''{i}) {name}''' for i, name in enumerate(target_names, start=1)))

            selection_no = int(input(f'''Select a target to build(1-{len(target_names)}):'''))

            build_target = target_names[selection_no - 1]
        else:
            build_target = target_names[0]
        return f'{build_target}{hydrogit_target_tag}'

    def run(self, versions):
        '''
        Run Hydrogen on these versions
        '''

        if not any(versions):
            print('Nothing to build :(')
            return

        build_target_bc = self.select_target(versions)

        # Run Hydrogen
        bcs=[]
        sources=[]
        for version in versions:
            try:
                bc = next(bc for bc in version.bc_paths if bc.stem == build_target_bc)
            except StopIteration:
                # Only build the versions that have the specified target
                continue

            bcs.append(bc)
            sources.append("::")
            for c_path in version.c_paths:
                sources.append(c_path)

        cmd = [str(self.hy)] + list(map(str, bcs)) + list(map(str, sources))
        print(f'running command {cmd}')

        subprocess.run(cmd)
