from typing import Dict, Any, Union, Optional, Tuple


class Trace(object):
    def __init__(self, repo, metric, name: str, context: list):
        self.repo = repo
        self.metric = metric
        self.name = name
        self.context: Dict[str, Union[str, Any]] = {
            k: v for (k, v) in context
        }
        self._num_records = None

    def __repr__(self):
        return str(self.context)

    def __len__(self):
        return self.num_records

    @property
    def num_records(self):
        if self._num_records is not None:
            return self._num_records
        self._get_storage().open(self.name, uncommitted_bucket_visible=True)
        self._num_records = self._get_storage().get_records_num(self.name,
                                                                self.context)
        self._get_storage().close(self.name)
        return self._num_records

    def read_records(self, indices: Optional[Union[int, Tuple[int, ...],
                                                   slice]] = None):
        self._get_storage().open(self.name, uncommitted_bucket_visible=True)
        records_iter = self._get_storage().read_records(self.name,
                                                        indices,
                                                        self.context)
        self._get_storage().close(self.name)
        return records_iter

    def _get_storage(self):
        return self.metric.storage
