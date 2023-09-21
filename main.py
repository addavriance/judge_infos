import pprint

from scr.utils.types import DataDict
from scr.utils.constants import SOLUTION_ID_SPLITTER, SOLUTION_DATE_SPLITTER, CASE_ID_SPLITTER, JUDGE_NAME_SPLITTER


class DataScrapper:
    def __init__(self, path: str) -> None:
        self.path: str = path
        self.raw_data: str
        self.data: list[DataDict] = []
        self._extract()

    @staticmethod
    def _get_solution_id(solution_data: str) -> str:
        return solution_data.split(SOLUTION_ID_SPLITTER)[0].strip()

    @staticmethod
    def _get_solution_date(solution_data: str) -> str:
        return " ".join(solution_data.split(SOLUTION_DATE_SPLITTER)[1].split(" ")[0:4]).strip()

    @staticmethod
    def _get_case_id(solution_data: str) -> str:
        return solution_data.split(CASE_ID_SPLITTER)[1].split(" ")[0]

    @staticmethod
    def _get_place(solution_data: str, solution_id: str, case_id: str) -> str | None:
        data = [i for i in solution_data.lstrip(solution_id).split(case_id) if len(i) > 3][1]
        if "(" in data and ")" in data:

            place = data[data.find("(")+1:data.find(")")]

            return place.replace(" (", ", ")
        else:
            return None

    @staticmethod
    def _get_judge_name(solution_data: str) -> str:
        return " ".join(solution_data.partition(JUDGE_NAME_SPLITTER)[0].rsplit(" ", 4)[-4:-1]).strip()

    def _get_all(self, solution_data: str) -> DataDict:
        local_data: DataDict = DataDict()

        solution_id: str = self._get_solution_id(solution_data)
        solution_date: str = self._get_solution_date(solution_data)
        case_id: str = self._get_case_id(solution_data)
        place: str | None = self._get_place(solution_data, solution_id, case_id)
        judge: str = self._get_judge_name(solution_data)

        local_data["solution_id"] = solution_id
        local_data["solution_date"] = solution_date
        local_data["case_id"] = case_id
        local_data["place"] = place
        local_data["judge"] = judge

        return local_data

    def _extract(self) -> None:
        with open(self.path) as f:
            raw_datatable_unfiltered: list[str] = ("\n" + f.read()).split("\n  Решение № ")
            raw_datatable: list[str] = [i for i in raw_datatable_unfiltered if len(i) > 100]

            self.raw_data = raw_datatable

    def run(self) -> None:
        for raw_data in self.raw_data:
            data: DataDict = self._get_all(raw_data)
            self.data.append(data)


# example usage
scrapper = DataScrapper(path="assets/data.txt")
scrapper.run()
pprint.pprint(scrapper.data)
