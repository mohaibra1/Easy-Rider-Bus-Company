from hstest.stage_test import *
from hstest.test_case import TestCase
import re


class EasyRiderStage5(StageTest):
    def generate(self) -> List[TestCase]:
        return [
            TestCase(
                stdin='[{"bus_id" : 128, "stop_id" : 1, "stop_name" : "Prospekt Avenue", "next_stop" : 3, "stop_type" : "S", "a_time" : "08:12"}, '
                      '{"bus_id" : 128, "stop_id" : 3, "stop_name" : "Elm Street", "next_stop" : 5, "stop_type" : "", "a_time" : "08:19"}, '
                      '{"bus_id" : 128, "stop_id" : 5, "stop_name" : "Fifth Avenue", "next_stop" : 7, "stop_type" : "O", "a_time" : "08:17"}, '
                      '{"bus_id" : 128, "stop_id" : 7, "stop_name" : "Sesame Street", "next_stop" : 0, "stop_type" : "F", "a_time" : "08:07"}, '
                      '{"bus_id" : 256, "stop_id" : 2, "stop_name" : "Pilotow Street", "next_stop" : 3, "stop_type" : "S", "a_time" : "09:20"}, '
                      '{"bus_id" : 256, "stop_id" : 3, "stop_name" : "Elm Street", "next_stop" : 6, "stop_type" : "", "a_time" : "09:45"}, '
                      '{"bus_id" : 256, "stop_id" : 6, "stop_name" : "Sunset Boulevard", "next_stop" : 7, "stop_type" : "", "a_time" : "09:44"}, '
                      '{"bus_id" : 256, "stop_id" : 7, "stop_name" : "Sesame Street", "next_stop" : "0", "stop_type" : "F", "a_time" : "10:12"}, '
                      '{"bus_id" : 512, "stop_id" : 4, "stop_name" : "Bourbon Street", "next_stop" : 6, "stop_type" : "S", "a_time" : "08:13"}, '
                      '{"bus_id" : 512, "stop_id" : 6, "stop_name" : "Sunset Boulevard", "next_stop" : 0, "stop_type" : "F", "a_time" : "08:16"}]',
                attach=((3, 0, 0, 0, 1, 0, 2), (128, 256, 512), (4, 4, 2), 3,
                       (('Bourbon Street', 'Pilotow Street', 'Prospekt Avenue'),
                       ('Elm Street', 'Sesame Street', 'Sunset Boulevard'), ('Sesame Street', 'Sunset Boulevard')))),
            TestCase(
                stdin='[{"bus_id" : 128, "stop_id" : 1, "stop_name" : "Fifth Avenue", "next_stop" : 4, "stop_type" : "S", "a_time" : "08:12"}, '
                      '{"bus_id" : 128, "stop_id" : 4, "stop_name" : "Abbey Road", "next_stop" : 5, "stop_type" : "", "a_time" : "08:19"},  '
                      '{"bus_id" : 128, "stop_id" : 5, "stop_name" : "Santa Monica Boulevard", "next_stop" : 8, "stop_type" : "O", "a_time" : "08:25"},  '
                      '{"bus_id" : 128, "stop_id" : 8, "stop_name" : "Elm Street", "next_stop" : "11", "stop_type" : "", "a_time" : "08:37"},  '
                      '{"bus_id" : 128, "stop_id" : 11, "stop_name" : "Beale Street", "next_stop" : 12, "stop_type" : "", "a_time" : "09:20"},  '
                      '{"bus_id" : 128, "stop_id" : 12, "stop_name" : "Sesame Street", "next_stop" : 14, "stop_type" : "", "a_time" : "09:45"},  '
                      '{"bus_id" : 128, "stop_id" : "five", "stop_name" : "Bourbon Street", "next_stop" : 19, "stop_type" : "O", "a_time" : "09:59"},  '
                      '{"bus_id" : 128, "stop_id" : 19, "stop_name" : "Prospekt Avenue", "next_stop" : 0, "stop_type" : "F", "a_time" : "10:12"},  '
                      '{"bus_id" : 256, "stop_id" : 2, "stop_name" : "Pilotow Street", "next_stop" : 3, "stop_type" : "S", "a_time" : "08:13"},  '
                      '{"bus_id" : 256, "stop_id" : "", "stop_name" : "Startowa Street", "next_stop" : 8, "stop_type" : "", "a_time" : "08:16"},  '
                      '{"bus_id" : 256, "stop_id" : 8, "stop_name" : "Elm Street", "next_stop" : 10, "stop_type" : "", "a_time" : "08:29"},  '
                      '{"bus_id" : 256, "stop_id" : 10, "stop_name" : "Lombard Street", "next_stop" : 12, "stop_type" : "", "a_time" : "08:44"},  '
                      '{"bus_id" : 256, "stop_id" : 12, "stop_name" : "Sesame Street", "next_stop" : "", "stop_type" : "O", "a_time" : "08:46"},  '
                      '{"bus_id" : 256, "stop_id" : 13, "stop_name" : "Orchard Road", "next_stop" : 16, "stop_type" : "", "a_time" : "09:13"},  '
                      '{"bus_id" : 256, "stop_id" : 16, "stop_name" : "Sunset Boulevard", "next_stop" : 17.4, "stop_type" : "O", "a_time" : "09:26"},  '
                      '{"bus_id" : 256, "stop_id" : 17, "stop_name" : "Khao San Road", "next_stop" : 20, "stop_type" : "O", "a_time" : "10:25"},  '
                      '{"bus_id" : 256, "stop_id" : 20, "stop_name" : "Michigan Avenue", "next_stop" : 0, "stop_type" : "F", "a_time" : "11:26"},  '
                      '{"bus_id" : 512, "stop_id" : 6, "stop_name" : "Arlington Road", "next_stop" : 7, "stop_type" : "S", "a_time" : "11:06"},  '
                      '{"bus_id" : 512, "stop_id" : 7, "stop_name" : "Parizska Street", "next_stop" : 8, "stop_type" : "", "a_time" : "11:15"},  '
                      '{"bus_id" : 512, "stop_id" : 8, "stop_name" : "Elm Street", "next_stop" : 9, "stop_type" : "", "a_time" : "11:56"},  '
                      '{"bus_id" : 512, "stop_id" : 9, "stop_name" : "Niebajka Avenue", "next_stop" : 15, "stop_type" : "", "a_time" : "12:20"},  '
                      '{"bus_id" : 512, "stop_id" : 15, "stop_name" : "Jakis Street", "next_stop" : 16, "stop_type" : "", "a_time" : "12:44"},  '
                      '{"bus_id" : 512, "stop_id" : 16, "stop_name" : "Sunset Boulevard", "next_stop" : 18, "stop_type" : "", "a_time" : "13:01"},  '
                      '{"bus_id" : 512, "stop_id" : 18, "stop_name" : "Jakas Avenue", "next_stop" : 19, "stop_type" : "", "a_time" : "14:00"},  '
                      '{"bus_id" : 512, "stop_id" : 19, "stop_name" : "Prospekt Avenue", "next_stop" : 0, "stop_type" : "F", "a_time" : "14:11"}]',
                attach=((5, 0, 2, 0, 3, 0, 0), (128, 256, 512), (8, 9, 8), 3,
                       (('Arlington Road', 'Fifth Avenue', 'Pilotow Street'), ('Elm Street', 'Prospekt Avenue', 'Sesame Street', 'Sunset Boulevard'),
                       ('Michigan Avenue', 'Prospekt Avenue')))),
            TestCase(
                stdin='[{"bus_id" : 128, "stop_id" : 1, "stop_name" : "Fifth Avenue", "next_stop" : 4, "stop_type" : "S", "a_time" : "08:12"}, '
                      '{"bus_id" : 128, "stop_id" : 4, "stop_name" : "Abbey Road", "next_stop" : 5, "stop_type" : "", "a_time" : "08:19"},  '
                      '{"bus_id" : 128, "stop_id" : 5, "stop_name" : "Santa Monica Boulevard", "next_stop" : 8, "stop_type" : "O", "a_time" : "08:25"},  '
                      '{"bus_id" : 128, "stop_id" : 8, "stop_name" : "Elm Street", "next_stop" : "11", "stop_type" : "", "a_time" : "08:37"},  '
                      '{"bus_id" : 128, "stop_id" : 11, "stop_name" : "Beale Street", "next_stop" : 12, "stop_type" : "", "a_time" : "09:20"},  '
                      '{"bus_id" : 128, "stop_id" : 12, "stop_name" : "Sesame Street", "next_stop" : 14, "stop_type" : "", "a_time" : "09:45"},  '
                      '{"bus_id" : 128, "stop_id" : "five", "stop_name" : "Bourbon Street", "next_stop" : 19, "stop_type" : "O", "a_time" : "09:59"},  '
                      '{"bus_id" : 128, "stop_id" : 19, "stop_name" : "Prospekt Avenue", "next_stop" : 0, "stop_type" : "F", "a_time" : "10:12"},  '
                      '{"bus_id" : 256, "stop_id" : 2, "stop_name" : "Pilotow Street", "next_stop" : 3, "stop_type" : "S", "a_time" : "08:13"},  '
                      '{"bus_id" : 256, "stop_id" : "", "stop_name" : "Startowa Street", "next_stop" : 8, "stop_type" : "", "a_time" : "08:16"},  '
                      '{"bus_id" : 256, "stop_id" : 8, "stop_name" : "Elm Street", "next_stop" : 10, "stop_type" : "", "a_time" : "08:29"},  '
                      '{"bus_id" : 256, "stop_id" : 10, "stop_name" : "Lombard Street", "next_stop" : 12, "stop_type" : "", "a_time" : "08:28"},  '
                      '{"bus_id" : 256, "stop_id" : 12, "stop_name" : "Sesame Street", "next_stop" : "", "stop_type" : "O", "a_time" : "08:27"},  '
                      '{"bus_id" : 256, "stop_id" : 13, "stop_name" : "Orchard Road", "next_stop" : 16, "stop_type" : "", "a_time" : "08:42"},  '
                      '{"bus_id" : 256, "stop_id" : 16, "stop_name" : "Sunset Boulevard", "next_stop" : 17.4, "stop_type" : "O", "a_time" : "09:26"},  '
                      '{"bus_id" : 256, "stop_id" : 17, "stop_name" : "Khao San Road", "next_stop" : 20, "stop_type" : "O", "a_time" : "10:25"},  '
                      '{"bus_id" : 256, "stop_id" : 20, "stop_name" : "Michigan Avenue", "next_stop" : 0, "stop_type" : "F", "a_time" : "11:26"},  '
                      '{"bus_id" : 512, "stop_id" : 6, "stop_name" : "Arlington Road", "next_stop" : 7, "stop_type" : "S", "a_time" : "11:06"},  '
                      '{"bus_id" : 512, "stop_id" : 7, "stop_name" : "Parizska Street", "next_stop" : 8, "stop_type" : "", "a_time" : "11:15"},  '
                      '{"bus_id" : 512, "stop_id" : 8, "stop_name" : "Elm Street", "next_stop" : 9, "stop_type" : "", "a_time" : "11:06"},  '
                      '{"bus_id" : 512, "stop_id" : 9, "stop_name" : "Niebajka Avenue", "next_stop" : 15, "stop_type" : "", "a_time" : "12:20"},  '
                      '{"bus_id" : 512, "stop_id" : 15, "stop_name" : "Jakis Street", "next_stop" : 16, "stop_type" : "", "a_time" : "12:44"},  '
                      '{"bus_id" : 512, "stop_id" : 16, "stop_name" : "Sunset Boulevard", "next_stop" : 18, "stop_type" : "", "a_time" : "13:01"},  '
                      '{"bus_id" : 512, "stop_id" : 18, "stop_name" : "Jakas Avenue", "next_stop" : 19, "stop_type" : "", "a_time" : "14:00"},  '
                      '{"bus_id" : 512, "stop_id" : 19, "stop_name" : "Prospekt Avenue", "next_stop" : 0, "stop_type" : "F", "a_time" : "14:11"}]',
                attach=((7, 0, 2, 0, 3, 0, 2), (128, 256, 512), (8, 9, 8), 3,
                       (('Arlington Road', 'Fifth Avenue', 'Pilotow Street'),
                       ('Elm Street', 'Prospekt Avenue', 'Sesame Street', 'Sunset Boulevard'),
                       ('Michigan Avenue', 'Prospekt Avenue')))),
        ]

    def check(self, reply: str, result) -> CheckResult:
        # Checking format and type errors
        query = "".join(["[\\D]*" + str(result[0][x]) for x in range(7)])
        if not re.search(rf'{query}', reply.strip()):
            return CheckResult.wrong("A wrong number of bugs was detected. Expected output:\n\n"
                                     f"Type and field validation: {result[0][0]} errors\n"
                                     f"bus_id: {result[0][1]}\n"
                                     f"stop_id: {result[0][2]}\n"
                                     f"stop_name: {result[0][3]}\n"
                                     f"next_stop: {result[0][4]}\n"
                                     f"stop_type: {result[0][5]}\n"
                                     f"a_time: {result[0][6]}")
        # Checking the number of stops
        for x in range(result[3]):
            query = str(result[1][x]) + "[\\D]*" + str(result[2][x])
            if not re.search(rf'{query}', reply.strip()):
                return CheckResult.wrong("Wrong number of stops detected.")
        # Checking start stops, transfer stops, and finish stops
        if isinstance(result[4], int):
            query = "".join("[\\D]*" + str(result[4]))
            if not re.search(rf'{query}', reply.strip()):
                return CheckResult.wrong(f"There is incorrectly marked stop. Take a closer look at the line {result[4]}.")
        else:
            query = "".join(["[\\D]*" + str(len(result[4][x])) + "".join(["[\\D]*" + str(result[4][x][y]) for y in range(len(result[4][x]))]) for x in range(len(result[4]))])
            if not re.search(rf'{query}', reply.strip()):
                return CheckResult.wrong("Invalid number of stops detected or the output format is wrong. "
                                         "Expected output:\n\n"
                                         f"Start stops: {len(result[4][0])} {list(result[4][0])}\n"
                                         f"Transfer stops: {len(result[4][1])} {list(result[4][1])}\n"
                                         f"Finish stops: {len(result[4][2])} {list(result[4][2])}")
        return CheckResult.correct()


if __name__ == '__main__':
    EasyRiderStage5('easyrider.easyrider').run_tests()