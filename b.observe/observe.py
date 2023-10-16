
from b_learn.a_config.config import Config
from b_learn.b_shapes.collect import collect
from b_learn.b_shapes.combine import combine
from b_learn.c_regions.coordinate import coordinate, consolidate


def learn():
    config = Config()
    # collect(config)
    # combine(config)
    # coordinate(config)
    consolidate(config)
    