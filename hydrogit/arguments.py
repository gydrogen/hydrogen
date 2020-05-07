from argparse import ArgumentParser, RawDescriptionHelpFormatter

def get_args():
    example_usage = '''example:
    python hydrogit.py \\
        -l C \\
        https://github.com/gydrogen/progolone.git \\
        5e8651df381079d0347ddfa254f554972611d1a0 \\
        70d03532975252bd9982beba60a8720e11ec8f02 \\
        9cde7197d0a3fe0caf7ee0ec7fd291e19ccc18ed
'''

    parser = ArgumentParser(
        prog='python hydrogit.py',
        epilog=example_usage,
        formatter_class=RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '-L',
        '--local',
        dest='local_dir',
        action='store_true',
        help='clone from a local dir',
        default=False,
        )

    parser.add_argument(
        '-p',
        '--force-pull',
        dest='force_pull',
        action='store_true',
        help='remove existing versions and pull again',
        default=False,
        )

    parser.add_argument(
        '-v',
        '--verbose',
        dest='verbose',
        action='store_true',
        help='show CMake output',
        default=False,
        )
        
    parser.add_argument(
        '-l',
        '--language',
        dest='language',
        help='compile with this language - should be C or CXX',
        default='C',
        )
        
    parser.add_argument(
        '-C',
        '--cmake',
        dest='with_cmake',
        help='build with CMake',
        default=False,
        )
        
    parser.add_argument('url')
    parser.add_argument('first_version')
    parser.add_argument('latter_versions', nargs='+')

    return parser.parse_args()