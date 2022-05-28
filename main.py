from argparse import ArgumentParser

from monitor.helper import create_runner
from settings import AVAILABLE_RUNNER_CHOICE, DEFAULT_CONFIG_FILE


def _init_argument():
    parser = ArgumentParser("通用的Rss-Monitor, This is Helper, V2")
    parser.add_argument("-m", "--mode",
                        choices=AVAILABLE_RUNNER_CHOICE,
                        default=AVAILABLE_RUNNER_CHOICE[0],
                        help="选择运行模式")
    parser.add_argument("-c", "--config_file",
                        default=DEFAULT_CONFIG_FILE,
                        help="配置文件")
    return parser.parse_args()


if __name__ == '__main__':
    args = _init_argument()
    runner = create_runner(args.mode, args.config_file)
    runner.run()
