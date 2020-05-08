# Proggyfresh - Trivial Autotools test program
python hydrogit.py -v https://github.com/gydrogen/proggyfresh.git \
    6312f9f0a1a342483fbf2e0cdc49a5b75067f6b7 \
    2113db3a5ffca3940443cef8359acbeb56f674ec \
    109a409b465a208178c6128a5d7a8eea0225e0b1

# GNU findutils🐃
python hydrogit.py -vL -r find ./findutils \
    abec46d20493d7b4f2e4be1fbc4175c60e1c7cb8 \
    7642d172e10a890975696d28278e5192d81afc5b

# Progolone - Trivial CMake test program
python hydrogit.py -vC https://github.com/gydrogen/progolone.git \
    5e8651df381079d0347ddfa254f554972611d1a0 \
    70d03532975252bd9982beba60a8720e11ec8f02 \
    9cde7197d0a3fe0caf7ee0ec7fd291e19ccc18ed

# Lua - Happy path
python hydrogit.py -vC https://github.com/LuaDist/lua.git \
    9b19c7d3efdc203c6a067f51efa5626f3e440e49 \
    0937bc974bbf0c062a222ffa49fa20c7cc6ab357

# GLEW - project with one target failing on our system(and the rest succeeding)
python hydrogit.py -vC \
    https://github.com/Perlmint/glew-cmake.git \
    68ac8e80a990b756de0b6e091c6f8db2e1828621 \
    5ab6ba3039b02290cc899a56ef6f50af2c649292