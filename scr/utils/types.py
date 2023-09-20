class DataDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        keys = ["solution_id", "solution_date", "case_id", "place", "judge"]

        [self.setdefault(key) for key in keys]
