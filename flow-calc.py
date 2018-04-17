import cv2
import numpy as np
from time import sleep

# def repopulate(p0, pl1, old_gray, gray, lk_params):
#     p1, st, err = cv2.calcOpticalFlowPyrLK(
#         old_gray, gray, pl1, None, **lk_params)
#     )
#     return p0

cap = cv2.VideoCapture('output.avi')

feature_params = dict(maxCorners = 100,
                        qualityLevel = .3,
                        minDistance = 7,
                        blockSize = 7)

lk_params = dict( winSize = (15,15),
                    maxLevel = 2,
                    criteria = (
                        cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
                        10, .03))
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
num_points = 10
h_seg = 640/num_points
w_seg = 480/num_points
p0 = np.float32([
    [[x*h_seg, y*w_seg]]
    for x in range(num_points+1)
    for y in range(num_points+1)])
# print(p0.shape)
# print(p0)

mask = np.zeros_like(old_frame)
tracks = []

while cap.isOpened():
    ret, frame = cap.read()
    img = frame
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if len(tracks) > 0:
        p0 = np.float32([tr[-1] for tr tracks]).reshape(-1, 1, 2)
        p1, st, err = cv2.calcOpticalFlowPyrLK(
                old_gray, gray,
                p0, None, **lk_params)
        p0r, st, err = cv2.calcOpticalFlowPyrLK(
            gray, old_gray,
            p1, None, **lk_params)
        d = abs(p0-p0r).reshape(-1, 2).max(-1)
        good = d < 1
        new_tracks = []
        for tr, (x,y), good_flag in zip(self.tracks, p1,reshape(-1, 2), good):
            if not good_flag:
                continue
            tr.append((x,y))
            new_tracks.append(tr)
            cv2.circle(frame, (x,y), 2, (0,255,0), -1)
        cv2.polylines(frame, [np.int32(tr), for tr in new_tracks], False, (0, 255,0))
        gesture = detect_direction(new_tracks)

    # good_new = p1[st==1]
    # good_old = p0[st==1]
    #
    # for i, (new,old) in enumerate(zip(good_new,good_old)):
    #     a,b = new.ravel()
    #     c,d = old.ravel()
    #     mask = cv2.line(mask, (a,b), (c,d), (255,0,0), 2)
    #     frame = cv2.circle(frame, (a,b),5,(255,0,0),-1)
    #     # frame = cv2.circle(frame, (c,d),5,(255,0,0),-1)
    # img = cv2.add(frame,mask)

    cv2.imshow('frame', img)
    sleep(.01)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    old_frame = frame
    old_gray = gray
    # p0 = cv2.goodFeaturesToTrack(
    #     old_gray, mask = None, **feature_params)


    p0 = np.array([
        [[x*w_seg, y*h_seg]]
        for x in range(num_points+1)
        for y in range(num_points+1)])
    # p0 = good_new.reshape(-1,1,2)
    # p0 = repopulate(p0, gray)

cap.release()
cv2.destroyAllWindows()
