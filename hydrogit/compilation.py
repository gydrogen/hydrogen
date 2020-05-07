from pathlib import Path
import subprocess
import os
import fileinput
import re
import shutil

cmake_utils_dir = (Path(__file__).parent / 'llvm-ir-cmake-utils' / 'cmake').resolve()
assert cmake_utils_dir.exists()
hydrogit_target_tag = '_hydrogit'

class CompileManager:
    def __init__(self, language, tmp):
        self.language=language
        self.tmp=tmp
        self.versions_built=[]

    def build_all(self, force, verbose, cmake_dir, build_dir):
        '''
        Run compilation step for all versions.
        '''

        for version_path in Path(self.tmp).iterdir():
            if version_path.is_dir() and version_path.name!="cloned":
                ver=Version(version_path, self.language, cmake_dir, build_dir)
                try:
                    ver.build(force, verbose)
                except AssertionError as msg:
                    print(f'{ver.version}: Failed - Skipping ({msg})')
                    continue

                print(f'{ver.version}: Built successfully')
                self.versions_built.append(ver)

class Version:
    def __init__(self, root, language, cmake_dir, build_dir):
        self.root=root
        self.version = self.root.stem
        self.build_path = self.root / build_dir
        self.cmake_path = self.root / cmake_dir
        self.llvm_ir_path = self.build_path / 'llvm-ir'
        self.c_paths=[]
        self.bc_paths=[]
        self.language = language
    
    def build(self, force, verbose):
        # Set up build path
        self.setup_build_path(force)

        # Transform CMakeLists.txt
        root_cmakelist = self.root / 'CMakeLists.txt'
        assert root_cmakelist.exists(), 'CMakeLists.txt not found in project root'
        self.transform_cmakelists(root_cmakelist)

        # Run CMake and collect the output
        print(f'{self.version}: Running CMake...')
        targets = self.cmake(verbose)
        print(f'{self.version}: Building...')
        self.make(targets, verbose)
        print(f'{self.version}: Gathering files...')
        self.glob_files()

    def setup_build_path(self, force):
        # Skip if built already unless we wanna HULK SMASH
        if self.build_path.exists():
            if force:
                shutil.rmtree(self.build_path)
            else:
                print(f'Version {self.root} is already built, skipping')
                return

        self.build_path.mkdir(exist_ok=True)
    
    def glob_files(self):
        '''
        Gather sources and compiled bytecode for this version
        '''
        # gather C sources
        if self.language == 'C':
            for p in (self.root).glob('*.c'):
                self.c_paths.append(p)
            for p in (self.root / 'src').glob('**/*.c'):
                self.c_paths.append(p)
        
        # gather C++ sources
        elif self.language == 'CXX':
            for p in (self.root).glob('*.cpp'):
                self.c_paths.append(p)
            for p in (self.root / 'src').glob('**/*.cpp'):
                self.c_paths.append(p)
                
        assert any(self.c_paths), \
            f'No {self.language} sources found'

        # gather compiled bytecode
        # todo: make it get all bc's
        self.bc_paths = list(self.llvm_ir_path.glob(f'**/*{hydrogit_target_tag}.bc'))
        assert any(self.bc_paths), \
            f'CMake output not found in path {str(self.llvm_ir_path)}'

    def transform_cmakelists(self, cmakelists):
        '''
        Transform given CMakeLists.txt and return the llvmlink target name
        '''

        assert cmakelists.exists(), \
            f'CMakeLists.txt not found at path {str(cmakelists)}'

        with cmakelists.open('a') as file:        
            ir_gen = f'''
#{'='*10}LLVM IR generation
list(APPEND CMAKE_MODULE_PATH "{cmake_utils_dir}")
include(LLVMIRUtil)
enable_language(C)
get_directory_property(_allTargets BUILDSYSTEM_TARGETS)
foreach(_target ${{_allTargets}})
    get_target_property(_type ${{_target}} TYPE)
    message(STATUS "Hydrogit saw target ${{_target}} type ${{_type}}")
    if((_type STREQUAL "EXECUTABLE") OR (_type STREQUAL "STATIC_LIBRARY"))
        message(STATUS "Hydrogit adding IR for target ${{_target}} type ${{_type}}")
        set_target_properties(${{_target}} PROPERTIES LINKER_LANGUAGE C)
        add_compile_options(-c -O0 -Xclang -disable-O0-optnone -g -emit-llvm -S)
        llvmir_attach_bc_target(${{_target}}_bc ${{_target}})
        add_dependencies(${{_target}}_bc ${{_target}})
        llvmir_attach_link_target(${{_target}}{hydrogit_target_tag} ${{_target}}_bc -S)
    endif()
endforeach(_target ${{_allTargets}})
# end LLVM IR generation
#{'='*10}'''

            file.write(ir_gen)

    def cmake(self, verbose):
        '''
        Run CMake with the given target
        '''

        compile_env = os.environ.copy()
        if self.language == 'C':
            compile_env['CC'] = 'clang'
        elif self.language == 'CXX':
            compile_env['CXX'] = 'clang++'
        
        cmake_proc = subprocess.run(args=[
            'cmake',
            '-B', str(self.build_path),
            str(self.root)
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=compile_env)
            
        if verbose:
            print(cmake_proc.stdout)
        
        assert cmake_proc.returncode == 0, \
            f'CMake step returned error code {cmake_proc.returncode}'
        assert self.llvm_ir_path.exists(), \
            f'LLVM IR output directory {str(self.llvm_ir_path)} does not exist'

        target_bcs = list(self.llvm_ir_path.glob(f'*{hydrogit_target_tag}'))
        assert any(target_bcs), \
            f'No CMake output found in path {str(self.llvm_ir_path)}'
        for bc in target_bcs:
            assert bc.exists(), \
                f'CMake output not found for LLVM IR target {bc}'

        targets = [bc.stem for bc in target_bcs]
        return targets

    def make(self, targets, verbose):
            for target in targets:
                try:
                    print(f'{self.version}: Building target {target}...', end='', flush=True)
                    
                    args = [
                        'cmake',
                        '--build',
                        str(self.build_path),
                        '--target', target,
                    ]
                    if verbose:
                        args.append('--verbose') # show make output
                        
                    build_proc = subprocess.run(
                        args=args,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True)
                    
                    if verbose:
                        print(build_proc.stdout)

                    assert build_proc.returncode == 0, \
                        f'Build step returned error code {build_proc.returncode}'
                    
                    print('done')
                except Exception as ex:
                    # Print the newline & bubble if there's an error while processing
                    print()
                    raise ex

def main():
    cm=CompileManager('C', Path("./tmp").absolute())
    cm.build_all(True, True)

if __name__ == '__main__':
    main()