# 导入必要的包
import numpy as np
import imutils
import cv2
import math


class Stitcher:
    def __init__(self):
        self.isv3 = imutils.is_cv3(or_better=True)

    def stitch(self, images, ratio=0.75, reprojThresh=4.0, showMatches=False):
        (imageA, imageB) = images
        (kpsA, featuresA) = self.detectAndDescribe(imageA)
        (kpsB, featuresB) = self.detectAndDescribe(imageB)

        M = self.matchKeypoints(kpsA, kpsB,
                                featuresA, featuresB, ratio, reprojThresh)

        if M is None:
            return None

        (matches, H, status) = M
        result = None

        the_max = max(int(imageA.shape[0]), int(imageB.shape[0]))
        # dist = imageB.shape[0] - int(H.max() * math.sin(math.pi / 4)) + imageA.shape[0] # imageA.share[0]
        height = int(kpsB.max() * math.sin(math.pi / 4))
        dist = height + the_max  # imageA.share[0]
        result = cv2.warpPerspective(imageA, H, (imageA.shape[1],  dist))
        result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB

        # 检测关键点匹配是否可视化
        if showMatches:
            vis = self.drawMatches(imageA, imageB, kpsA, kpsB, matches,
                                   status)

            # 返回tuple，包括叠合后的全景图及可视化结果
            return (result, vis)

        return result

    def detectAndDescribe(self, image):
        # 转换图像为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 兼容openCV版本
        if self.isv3:
            # 从图像提取关键点特征
            descriptor = cv2.xfeatures2d.SIFT_create()
            (kps, features) = descriptor.detectAndCompute(image, None)
        # 如果是opencv 2.4.X
        else:
            # 从图像检测关键点
            detector = cv2.FeatureDetector_create("SIFT")
            kps = detector.detect(gray)

            extractor = cv2.DescriptorExtractor_create("SIFT")
            (kps, features) = extractor.compute(gray, kps)

        # 将关键点对象转换为Numpy数组
        kps = np.float32([kp.pt for kp in kps])

        # 返回一个元组，包括关键点数组和特征
        return (kps, features)

    def matchKeypoints(self, kpsA, kpsB, featuresA, featuresB,
                       ratio, reprojThresh):

        matcher = cv2.DescriptorMatcher_create("BruteForce")
        rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
        matches = []

        for m in rawMatches:
            # 确保距离在一个特定的比率下
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))

        if len(matches) > 4:
            # 构建俩组点
            ptsA = np.float32([kpsA[i] for (_, i) in matches])
            ptsB = np.float32([kpsB[i] for (i, _) in matches])

            # 计算俩组点的单应性
            (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC,
                                             reprojThresh)

            # 返回单应矩阵的匹配及每个匹配的点
            return (matches, H, status)
        # 否则，不会生成任何单应矩阵
        return None

    def drawMatches(self, imageA, imageB, kpsA, kpsB, matches, status):
        # 初始化可视化输出图像
        (hA, wA) = imageA.shape[:2]
        (hB, wB) = imageB.shape[:2]
        vis = np.zeros((max(hA, hB), wA + wB, 3), dtype="uint8")
        vis[0:hA, 0:wA] = imageA
        vis[0:hB, wA:] = imageB

        # 遍历匹配关系
        for ((trainIdx, queryIdx), s) in zip(matches, status):
            # 仅处理关键点成功匹配的情况
            if s == 1:
                ptA = (int(kpsA[queryIdx][0]), int(kpsA[queryIdx][1]))
                ptB = (int(kpsB[trainIdx][0]) + wA, int(kpsB[trainIdx][1]))
                cv2.line(vis, ptA, ptB, (0, 255, 0), 1)

        # 返回可视化结果
        return vis

