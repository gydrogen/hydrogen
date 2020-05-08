# Vanilla comands
clang -c -O0 -Xclang -disable-O0-optnone -g -emit-llvm -S -o Prog.o Prog.c
llvm-dis tut_prog.0.5.precodegen.bc -o bc
clang -flto -fuse-ld=lld -Wl,-save-temps Prog.o -o tut_prog

# With make
make CC=clang V=1 CPPFLAGS='-c -O0 -Xclang -disable-O0-optnone -g -flto' LDFLAGS='-flto -fuse-ld=lld -Wl,-save-temps'
llvm-dis tut_prog.0.5.precodegen.bc -o bc