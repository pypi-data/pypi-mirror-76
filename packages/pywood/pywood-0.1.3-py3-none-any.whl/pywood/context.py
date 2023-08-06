from dataclasses import dataclass
from typing import Type, Any, Optional

from pywood.events import BaseEvent


@dataclass
class Context:
    event_cls: Optional[Type[BaseEvent]]
    state_data: Any
