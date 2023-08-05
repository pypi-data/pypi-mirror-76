from typing import Dict, Any, Union, Optional, Tuple


class Trace(object):
    def __init__(self, repo, metric, name: str, context: list):
        self.repo = repo
        self.metric = metric
        self.name = name
        self.num_records = None
        self.context: Dict[str, Union[str, Any]] = {
            k: v for (k, v) in context
        }

    def __repr__(self):
        return str(self.context)

    def __len__(self):
        if self.num_records is not None:
            return self.num_records
        self._get_storage().open(self.name, uncommitted_bucket_visible=True)
        self.num_records = self._get_storage().get_records_num(self.name,
                                                               self.context)
        self._get_storage().close(self.name)

    def read_records(self, indices: Optional[Union[int, Tuple[int, ...],
                                                   slice]] = None):
        self._get_storage().open(self.name, uncommitted_bucket_visible=True)
        self.num_records = self._get_storage().get_records_num(self.name,
                                                               indices,
                                                               self.context)
        self._get_storage().close(self.name)

    def _get_storage(self):
        return self.metric.storage
