import easyocr
import numpy as np
import pyautogui

class OCResult:

    def __init__(self, easyocresult):
        pts, self.text, self.conf = easyocresult[0:3]
        self.x, self.y = pts[0][0:2]
        self.w, self.h = pts[2][0] - self.x, pts[2][1] - self.y

    def to_string(self):
        return "%-4s | %-4s | %-4s | %-4s | %-12s | %s" % \
               (self.x, self.y, self.w, self.h, round(self.conf, ndigits=10), self.text)


class OCR:

    def __init__(self):
        self.reader = easyocr.Reader(["en"])

    def from_file(self, file) -> list[OCResult]:
        return [OCResult(result) for result in self.reader.readtext(file)]

    def from_img(self, img) -> list[OCResult]:
        return [OCResult(result) for result in self.reader.readtext(img)]


if __name__ == "__main__":
    ocr: OCR = OCR()
    img = pyautogui.screenshot()
    results = ocr.from_img(np.array(img))
    # results = ocr.from_file("game.png")
    with open("results.txt", "w") as f:
        for result in results:
            f.write(result.to_string() + "\n")
