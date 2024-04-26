from dataclasses import dataclass, asdict
from typing import TYPE_CHECKING

from opendevin import config
from opendevin.schema import ActionType, ConfigType

if TYPE_CHECKING:
    from opendevin.controller import AgentController
    from opendevin.observation import Observation


@dataclass
class Action:
    async def run(self, controller: 'AgentController') -> 'Observation':
        raise NotImplementedError

    def to_memory(self):
        d = asdict(self)
        try:
            v = d.pop('action')
        except KeyError:
            raise NotImplementedError(f'{self=} does not have action attribute set')
        thoughts = ''
        if 'thoughts' in d:
            thoughts = d.pop('thoughts')
        if config.get(ConfigType.THOUGHTS_FIELD):
            return {'thoughts': thoughts, 'action': v, 'args': d}
        else:
            return {'action': v, 'args': d}

    def to_dict(self):
        d = self.to_memory()
        d['message'] = self.message
        return d

    @property
    def executable(self) -> bool:
        raise NotImplementedError

    @property
    def message(self) -> str:
        raise NotImplementedError


@dataclass
class ExecutableAction(Action):
    @property
    def executable(self) -> bool:
        return True


@dataclass
class NotExecutableAction(Action):
    @property
    def executable(self) -> bool:
        return False


@dataclass
class NullAction(NotExecutableAction):
    """An action that does nothing.
    """

    action: str = ActionType.NULL

    @property
    def message(self) -> str:
        return 'No action'
