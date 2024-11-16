#lớp lưu trữ các thông số của mỗi level
class Level:
    def __init__(self, caption, stage_enemies, speed):
        self.caption = caption
        self.stage_enemies = stage_enemies
        self.speed = speed

# lớp lưu nhưng thông số được cài đặt trước
class Preset:
    # lưu trữ số lượng quá của mỗ vòng, mỗi phần tử là một level
    # số phần tử trong một phần tử là số lượng stage
    #trong các phần tử đó có 4 phần tử con nữa là số enemy của mỗi đường.
    stage_enemies = [
        [
            [10 , 10, 0, 0],
            [5, 10, 10, 5],
            [10, 5, 5, 10],
            [10, 10, 10, 10]
        ],
        [
            [10 , 0, 0, 10],
            [5, 20, 20, 5],
            [20, 0, 20, 10],
            [30, 10, 10, 10]
        ],
        [
            [10 , 10, 10, 0],
            [0, 20, 20, 0],
            [10, 10, 10, 10],
            [10, 20, 20, 10]
        ]
    ]

    # lưu trữ tốc độ của quái ở mỗi stage trong mỗi level
    speed = [
        [1, 1, 1, 1],
        [1, 1.5, 1.5, 2],
        [1.5, 2, 2, 2.5]
    ]
    
    number_random = [
        [272, 304, 336],
        [112, 144, 176],
        [336, 368, 400],
        [368, 400, 432]
    ]
    
    enemy_target = [
        [112, 240],
        [112, 240],
        [112, 272],
        [112, 272]
    ]
    
    # lưu phương thức tìm đường của quái
    diagonal_movement = [2, 1, 1, 2]

    hp_castle = 197

    level = [
        Level("Level 1", stage_enemies[0], speed[0]),
        Level("Level 2", stage_enemies[1], speed[1]),
        Level("Level 3", stage_enemies[2], speed[2])
    ]