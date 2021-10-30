from vector import *


def cartesian(vector: Polar2DInheritance or Polar2DAdapter):
    r = vector.abs()
    angle = vector.get_angle() * 180 / math.pi
    return f'[{r:.5}, {angle:.5}°]'


def main():
    v1_2D_src = Vector2D(1/2, math.sqrt(3)/2)
    v1_2D = Polar2DAdapter(v1_2D_src)
    v2_2D_src = Vector2D(math.sqrt(3), 1)
    v2_2D = Polar2DAdapter(v2_2D_src)
    v3_2D = Polar2DInheritance(2*math.sqrt(2), 2*math.sqrt(2))

    print(f'v1 = {v1_2D}, {cartesian(v1_2D)}')
    print(f'v2 = {v2_2D}, {cartesian(v2_2D)}')
    print(f'v3 = {v3_2D}, {cartesian(v3_2D)}')
    print('')
    print(f'v1 * v2 = {v1_2D.cdot(v2_2D):.7}')
    print(f'v2 * v1 = {v2_2D.cdot(v1_2D):.7}')
    print(f'v1 * v3 = {v1_2D.cdot(v3_2D):.7}')
    print(f'v3 * v1 = {v3_2D.cdot(v1_2D):.7}')
    print(f'v2 * v3 = {v2_2D.cdot(v3_2D):.7}')
    print(f'v3 * v2 = {v3_2D.cdot(v2_2D):.7}')
    print('\n')

    v4_3D = Vector3DDecorator(1, 2, 3)
    v5_3D = Vector3DInheritance(1, 1/2, 1/3)
    print(f'v4 = {v4_3D}')
    print(f'v5 = {v5_3D}')
    print('')
    print(f'v4 * v5 = {v4_3D.cdot(v5_3D):.7}')
    print(f'v4 x v5 = {v4_3D.cross(v5_3D)}')
    print(f'v5 * v1 = {v5_3D.cdot(v1_2D):.7}')
    print(f'v5 x v1 = {v5_3D.cross(v1_2D)}')


if __name__ == '__main__':
    main()