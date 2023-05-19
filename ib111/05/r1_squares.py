from typing import Tuple, Optional, List
# Do programu (který si možná pamatujete z druhého týdne) doplňte
# typové anotace tak, aby prošel kontrolou nástrojem ‹mypy› bez
# chyb.

# Pomocné funkce.

Point = Tuple[int, int]
Points = List[Point]

def find_slope(points: Points, avg_x: float, avg_y: float) -> Optional[float]:
    dividend: float = 0
    divisor: float = 0

    for i in range(len(points)):
        dividend += ((points[i][0] - avg_x) * (points[i][1] - avg_y))
        divisor += (points[i][0] - avg_x) ** 2

    if divisor == 0:
        return None

    return dividend / divisor


def find_intercept(avg_x: float, avg_y: float, beta: float) -> float:
    return avg_y - beta * avg_x


# První verze má jako vstup dva vektory (seznamy), jeden se
# souřadnicemi ⟦x⟧ a druhý se souřadnicemi ⟦y⟧. Výsledkem nechť je
# dvojice ⟦(α, β)⟧.

def regress_vectors(x: List[int], y: List[int]) -> Optional[Tuple[float, float]]:
    return regress_points([(x[i], y[i]) for i in range(len(x))])


# Druhá verze má jako parametr seznam dvojic, kde každá dvojice
# popisuje jeden bod.

def regress_points(points: Points) -> Optional[Tuple[float, float]]:
    avg_x = sum(x for x, _ in points) / len(points)
    avg_y = sum(y for _, y in points) / len(points)

    slope = find_slope(points, avg_x, avg_y)

    if slope is None:
        return None

    intercept = find_intercept(avg_x, avg_y, slope)
    return (intercept, slope)


# Výpočet residuí z dvojice seznamů.

def residuals_vectors(x: List[int], y: List[int], alpha: int, beta: int) -> List[int]:
    points = [(x[i], y[i]) for i in range(len(x))]
    return residuals_points(points, alpha, beta)


# Výpočet residuí ze seznamu dvojic.

def residuals_points(points: Points, alpha: int, beta: int) -> List[int]:
    res = []
    for i in range(len(points)):
        res.append(abs(points[i][1] - beta * points[i][0] - alpha))
    return res


def main() -> None:
    from math import isclose

    points = [(1, 3), (2, 4)]
    expect_alpha = 2
    expect_beta = 1
    expect_residuals = [0, 0]

    regress_vectors_res = regress_vectors(
        [x for x, _ in points], [y for _, y in points])
    regress_points_res = regress_points(points)

    assert regress_vectors_res is not None
    assert regress_points_res is not None

    assert isclose(expect_alpha, regress_vectors_res[0])
    assert isclose(expect_alpha, regress_points_res[0])
    assert isclose(expect_beta, regress_vectors_res[1])
    assert isclose(expect_beta, regress_points_res[1])

    residuals_vectors_res = residuals_vectors(
        [x for x, _ in points], [y for _, y in points],
        expect_alpha, expect_beta)
    residuals_points_res = residuals_points(
        points, expect_alpha, expect_beta)

    assert isclose(residuals_vectors_res[0], expect_residuals[0])
    assert isclose(residuals_vectors_res[1], expect_residuals[1])
    assert isclose(residuals_points_res[0], expect_residuals[0])
    assert isclose(residuals_points_res[1], expect_residuals[1])


if __name__ == "__main__":
    main()
