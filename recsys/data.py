import logging
from pathlib import Path
import yaml
import pandas as pd

logger = logging.getLogger(__name__)
def load_config(path: str = "configs/base.yaml") -> dict:
    with open(path , 'r' , encoding="utf-8") as f:
        return yaml.safe_load(f)

def setup_logging(log_file: str, level: str = "INFO") -> None:
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
def load_ratings(raw_dir:str) -> pd.DataFrame:
    df = pd.read_csv(
        Path(raw_dir)/"ratings.dat",
        sep= "::",
        engine= "python",
        header= None,
        names= ["user_id" , "item_id" , "rating" , "timestamp"],
    )
    return df
def print_stats(df: pd.DataFrame) -> None:
    n_users = df["user_id"].nunique()
    n_items = df["item_id"].nunique()
    n_ratings = len(df)
    ts = pd.to_datetime(df["timestamp"],unit="s")
    sparsity = 1 - n_ratings / (n_users * n_items)
    logger.info("评分数:%d", n_ratings)
    logger.info("用户数:%d", n_users)
    logger.info("电影数:%d",n_items)
    logger.info("时间跨度:%s ~ %s",ts.min() , ts.max())
    logger.info("稀疏度: %.2f%%", sparsity * 100)


if __name__ == "__main__":
    cfg = load_config()
    setup_logging(cfg["log"]["file"], cfg["log"]["level"])
    logger.info("配置加载成功：%s", cfg["data"]["raw_dir"])
    logger.info("数据目录存在吗：%s", Path(cfg["data"]["raw_dir"]).exists())
    df = load_ratings(cfg["data"]["raw_dir"])
    print_stats(df)