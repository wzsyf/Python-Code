# #!/usr/bin/env python
#
from backend import *
#
# class RandomVideoImage:
#
#     def randomVideoImage(self, imagePostId):
#         bk = Backend()
#         bk.randomVideoUpdateTime(imagePostId)
#         print("Updated!")
#
# if __name__ == "__main__":
#     rvi = RandomVideoImage()
#
#     #videoPostIds = [206498,207025,207207,207218,207263,207383,207836,208131]
#     imagePostIds = [215082,214719,214575,213808,212032,210841,210129,194353,192265,
#                     191584,190932,187160,180748,174551,184784,60855,58642,
#                     165502,186348,202724,186858,66731,217254,104174,214758,
#                     57216,213168,180247,175798,187910,195138]
#     random.shuffle(imagePostIds)
#     for imagePostId in imagePostIds:
#         print imagePostId
#         rvi.randomVideoImage(imagePostId)
#

if __name__ == "__main__":
    bk = Backend()
    postIds = [
        186858, 165502, 214575, 213808,
        206498,
        212032, 210841, 175798, 194353,
        207025,
        104174, 191584, 213168, 187160,
        207207,
        180748, 174551, 192265, 60855,
        207218,
        217254, 195138, 186348, 202724,
        207263,
        215082, 66731, 58642, 184784,
        207383,
        214758, 57216, 190932, 180247,
        207836, 208131,
        210129, 187910, 214719]

    for postId in postIds:
        bk.updateTime(postId)
        print postId
        time.sleep(2)