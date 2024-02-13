import hashlib
import time
from tkinter import Tk, Canvas
from colorama import Fore, Style
import random

colors = [Fore.MAGENTA, Fore.LIGHTBLUE_EX, Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX]

class Shape:
    def __init__(self, canvas, coords):
        self.canvas = canvas
        self.coords = coords
        self.polygon_id = None
        self.id = self._generate_id(coords)

    def _generate_id(self, coords):
        text = "_".join([f"{x}:{y}" for x, y in coords])
        unique_text = text + "_" + str(time.time())
        return hashlib.sha256(unique_text.encode('utf-8')).hexdigest()

    def draw(self, coords, outline, fill='', width=2, dash=None):
        self.polygon_id = self.canvas.create_polygon(coords, outline=outline, fill=fill, width=width, dash=dash)

    def move(self, dx, dy):
        self.canvas.move(self.polygon_id, dx, dy)
        self.coords = [(x + dx, y + dy) for x, y in self.coords]

    def remove(self):
        self.canvas.delete(self.polygon_id)

class Triangle(Shape):
    def __init__(self, canvas, coords):
        super().__init__(canvas, coords)
        self.draw(coords, outline="green", dash=(5, 10))

class Tetragon(Shape):
    def __init__(self, canvas, coords):
        super().__init__(canvas, coords)
        self.draw(coords, outline="red", dash=(5, 10))

def get_coords(shape_name):
    num_vertices = 3 if shape_name == "Треугольник" else 4
    print(f"{colors[1]} Введите пары координат вершин для фигуры {shape_name} \n")
    coords = []
    for _ in range(num_vertices):
        while True:
            input_string = input(f"{colors[0]}Введите пару чисел: {Style.RESET_ALL}")
            if not input_string:
                print(f"{colors[2]}Пустая строка введена, пропуск вершины.{Style.RESET_ALL}")
                continue
            numbers = input_string.split()
            if len(numbers) != 2:
                print(f"{colors[2]}Пожалуйста, введите ровно две цифры.{Style.RESET_ALL}")
                continue
            try:
                coords.append(tuple(int(x) for x in numbers))
                break
            except ValueError:
                print(f"{colors[2]}Введите целочисленные значения.{Style.RESET_ALL}")
    return coords

def setup_bindings(canvas, triangle, tetragon, root):
    def move_triangle(event, dx, dy):
        triangle.move(dx, dy)

    def move_tetragon(event, dx, dy):
        tetragon.move(dx, dy)

    def remove_triangle(event):
        triangle.remove()

    def remove_tetragon(event):
        tetragon.remove()

    root.bind("<Left>", lambda event: move_triangle(event, -10, 0))
    root.bind("<Right>", lambda event: move_triangle(event, 10, 0))
    root.bind("<Up>", lambda event: move_triangle(event, 0, -10))
    root.bind("<Down>", lambda event: move_triangle(event, 0, 10))
    root.bind("a", lambda event: move_tetragon(event, -10, 0))
    root.bind("d", lambda event: move_tetragon(event, 10, 0))
    root.bind("w", lambda event: move_tetragon(event, 0, -10))
    root.bind("s", lambda event: move_tetragon(event, 0, 10))
    root.bind("q", remove_triangle)
    root.bind("e", remove_tetragon)
    root.bind("<Control_L>", lambda event: check_intersection(triangle, tetragon))
    root.bind("<Control_R>", lambda event: check_intersection(triangle, tetragon))


def intersect(a, b, c, d):
    def area(p1, p2, p3):
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

    def intersect_1(a, b, c, d):
        if a > b:
            a, b = b, a
        if c > d:
            c, d = d, c
        return max(a, c) <= min(b, d)

    return intersect_1(a[0], b[0], c[0], d[0]) and \
        intersect_1(a[1], b[1], c[1], d[1]) and \
        area(a, b, c) * area(a, b, d) <= 0 and \
        area(c, d, a) * area(c, d, b) <= 0


def check_intersection(triangle, tetragon):
    triangle_segments = [(triangle.coords[i], triangle.coords[(i + 1) % len(triangle.coords)]) for i in
                         range(len(triangle.coords))]
    tetragon_segments = [(tetragon.coords[i], tetragon.coords[(i + 1) % len(tetragon.coords)]) for i in
                         range(len(tetragon.coords))]

    for seg1 in triangle_segments:
        for seg2 in tetragon_segments:
            if intersect(seg1[0], seg1[1], seg2[0], seg2[1]):
                print(f"{colors[3]}True: Фигуры пересекаются")
                return
    print(f"{colors[2]}False: Фигуры не пересекаются")


def main():
    root = Tk()
    canvas = Canvas(root, width=600, height=400, bg="white")
    canvas.pack(pady=20)

    triangle_coords = get_coords("Треугольник")
    tetragon_coords = get_coords("Четырехугольник")
    print(f"{colors[1]} Up,Down,Left,Right arrows - перемещение треугольника")
    print(f"{colors[1]} W,A,S,W - перемещение четырехугольника")
    print(f"{colors[1]} Q - удалить треугольник")
    print(f"{colors[1]} E - удалить четырехугольник")
    print(f"{colors[1]} Ctrl - проверка пересечения")


    triangle = Triangle(canvas, triangle_coords)
    tetragon = Tetragon(canvas, tetragon_coords)

    print(f"{colors[0]} ID треугольника = {triangle.id} {Style.RESET_ALL}")
    print(f"{colors[0]} ID четырехугольника = {tetragon.id} {Style.RESET_ALL}")

    setup_bindings(canvas, triangle, tetragon, root)
    root.mainloop()

if __name__ == "__main__":
    main()
