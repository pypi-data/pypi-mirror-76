"""parse yarn ressource manager log4j aggregated logs"""
from dataclasses import dataclass, field
from typing import List, Pattern
import re
import logging
import arrow
from itertools import groupby

FILEPATTERN = 'yarn-yarn-resourcemanager*.log*'

@dataclass
class Parser():
    pattern_line: Pattern = field(init=False)

    def __post_init__(self):
        self.pattern_line = re.compile(
            r'(?P<ts>(\d+-?){3}\s(\d+[:,]?){4})\s(?P<level>[A-Z]+)\s{2}(?P<javaclass>\w+\.\w+)\s\(.*\((?P<java_id>\d+)\)\)\s-\s(?P<payload>.*)')

    def parse(self, data: List[str]) -> List[dict]:
        return [self.parse_line(line) for line in data]

    def parse_line(self, logline: str) -> dict:
        """try to parse line, fail silently by returning an empty dict"""
        try:
            return self.pattern_line.match(logline).groupdict()
        except Exception as e:
            logging.debug(e)
            return {}


@dataclass
class StateProcessor:
    pattern_state: Pattern = field(init=False)

    def __post_init__(self):
        self.pattern_state = re.compile(
            r'(?P<id_application>application_\d+_\d+)(.*)from\s(?P<from_state>[A-Z_]+)\sto\s(?P<to_state>[A-Z_]+)'
        )

    def parse(self, data: List[dict]) -> List[dict]:
        "parse 'state' line(transition) and discard other"
        def merge(line):
            return {**{'ts': line['ts']},
                    **(self.parse_payload(line['payload']))}
        valid = [line for line in data if self.is_state(line)]
        return [merge(elt) for elt in valid]

    def parse_payload(self, payload: str) -> dict:
        """try to parse, fail silently by returning an empty dict"""
        try:
            return self.pattern_state.match(payload).groupdict()
        except Exception as e:
            logging.debug(e)
            return {}

    @staticmethod
    def is_state(parsed: dict) -> bool:
        # code 779
        try:
            return parsed['java_id'] == '779'
        except KeyError:
            return False

    @staticmethod
    def delta(states: List[dict], from_state: str, to_state: str) -> dict:
        """reduce as diff of time"""
        def diff(first, last):
            if (not first) or (not last):
                return None
            else:
                return abs((arrow.get(last)-arrow.get(first)).seconds)
        def get_state(state):
            try:
                return list(filter(lambda x: x['to_state'] == state, states))[0]['ts']
            except IndexError:
                return ''
        # 'to_state' is the last state known.
        # It is the current state of the app at time T
        t1 = get_state(from_state) 
        t2 = get_state(to_state)
        return {'id_application': states[0]['id_application'], 'delta': diff(t1, t2)}

    @staticmethod
    def process_diff(parsed: List[dict],
                     from_state: str,
                     to_state: str) -> List[dict]:
        result = []
        def keyfunc(x): return x['id_application']
        sort_data = sorted(parsed, key=keyfunc)
        for key, group in groupby(sort_data, keyfunc):
            result.append(StateProcessor.delta(
                list(group), from_state, to_state))
        return result

@dataclass
class QueueProcessor:
    pattern: Pattern = field(init=False)
    def __post_init__(self):
        self.pattern = re.compile(r'(.*)(appId:\s)(?P<id_application>application[0-9_]+)\s(user:\s(?P<user>[a-zA-Z0-9]+)).*(leaf-queue:\s(?P<queue>[a-zA-Z0-9_]+))([^#])(\#user-pending-applications+:\s?(?P<nb_user_pending>\d+))([^#])(#user-active-applications:\s?(?P<nb_user_active>\d+))([^#])(#queue-pending-applications:\s?(?P<nb_queue_pending>\d+))([^#])(#queue-active-applications:\s?(?P<nb_queue_active>\d+))')

    def parse_line(self,logline:str)->dict:
        try:
            found = self.pattern.match(logline).groupdict()
        except (AttributeError,TypeError):
            return {}
        for k in found.keys():
            if 'nb_' in k:
                found[k] = int(found[k])
        return found

    @staticmethod
    def is_queue(parsed:dict)->bool:
        try:
            return (parsed['java_id'] == '744') and (parsed['javaclass']=='capacity.LeafQueue')
        except KeyError:
            return False

def kpi_accept_to_run(lines: List[str]):
    parser = Parser()
    processor = StateProcessor()
    return processor.process_diff(processor.parse((parser.parse(lines))),
                                  from_state='ACCEPTED',
                                  to_state='RUNNING'
                                  )

def kpi_nb_queue(lines:List[str]):
    parser = Parser()
    processor = QueueProcessor()
    parsed = parser.parse(lines)
    onlyqueue = [line for line in parsed if QueueProcessor.is_queue(line)]
    return [processor.parse_line(line['payload']) for line in parsed  if QueueProcessor.is_queue(line)]