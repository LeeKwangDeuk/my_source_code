import argparse
from pathlib import Path
import numpy as np


def check_xyz_range(npy_path: str) -> str:
    npy_file = Path(npy_path).resolve()

    if not npy_file.exists():
        raise FileNotFoundError(f'파일을 찾을 수 없습니다: {npy_file}')

    # .npy 파일 데이터 로드
    data = np.load(npy_file)

    # x, y, z 축 분리 (Shape 검사)
    if data.shape[-1] == 3:
        x = data[..., 0]
        y = data[..., 1]
        z = data[..., 2]
    elif data.shape[0] == 3:
        x = data[0, ...]
        y = data[1, ...]
        z = data[2, ...]
    else:
        raise ValueError(f'x, y, z 3차원 축을 식별할 수 없는 데이터 Shape입니다: {data.shape}')

    # X, Y, Z 각각의 최소값 및 최댓값 계산
    x_min, x_max = float(np.min(x)), float(np.max(x))
    y_min, y_max = float(np.min(y)), float(np.max(y))
    z_min, z_max = float(np.min(z)), float(np.max(z))

    x_range = x_max - x_min
    y_range = y_max - y_min
    z_range = z_max - z_min

    # 리포트 텍스트 작성
    report_lines = [
        '=' * 60,
        '               NPY 파일 XYZ 범위 검사 결과',
        '=' * 60,
        f'대상 파일 경로 : {npy_file}',
        f'데이터 Shape   : {data.shape}',
        f'데이터 타입    : {data.dtype}',
        f'총 포인트 개수 : {x.size} 개',
        '-' * 60,
        '[ X 값 범위 ]',
        f'  - 최소값 (Min) : {x_min:18.8f}',
        f'  - 최댓값 (Max) : {x_max:18.8f}',
        f'  - 변화폭 (Range): {x_range:18.8f}',
        '-' * 60,
        '[ Y 값 범위 ]',
        f'  - 최소값 (Min) : {y_min:18.8f}',
        f'  - 최댓값 (Max) : {y_max:18.8f}',
        f'  - 변화폭 (Range): {y_range:18.8f}',
        '-' * 60,
        '[ Z 값 범위 ]',
        f'  - 최소값 (Min) : {z_min:18.8f}',
        f'  - 최댓값 (Max) : {z_max:18.8f}',
        f'  - 변화폭 (Range): {z_range:18.8f}',
        '=' * 60,
    ]

    report_content = chr(10).join(report_lines) + chr(10)

    # .npy 파일과 동일한 위치에 동일한 파일명 + _xyz범위.txt 생성
    output_filename = f'{npy_file.stem}_xyz범위.txt'
    output_path = npy_file.parent / output_filename

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(report_content)
    print(f'[성공] 검사 결과 파일이 생성되었습니다: {output_path}')
    return str(output_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='NPY 파일 x, y, z 값 범위 검사 도구')

    # 기본 파일 경로: ./workspace/1_001d455d42ee03a6_full.npy
    default_path = Path(__file__).parent / '1_001d455d42ee03a6_full.npy'

    parser.add_argument(
        '--file',
        '-f',
        type=str,
        default=str(default_path),
        help='검사할 .npy 파일 경로',
    )

    args = parser.parse_args()
    check_xyz_range(args.file)
