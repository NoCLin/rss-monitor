from pathlib import Path

from settings import PROJECT_DIR, DEFAULT_CONFIG_FILE


def create_runner(mode: str, config: str, *args, **kwargs):
    c = Path(config)
    if not c.exists():
        raise FileNotFoundError(f"未找到配置为文件{config}")
    return getattr(__import__("monitor.runner", fromlist=["monitor"]), f"{mode.title()}Runner")(config, *args, **kwargs)


if __name__ == '__main__':
    mode = "direct"
    runner = create_runner(mode, PROJECT_DIR.joinpath(DEFAULT_CONFIG_FILE))
    print(runner)
