
from typing import List, Dict, Any

import numpy as np
from pydantic import BaseModel



class Board(BaseModel):
    hero: Player
    vills: Dict[str, Player]
    comm: Cards

