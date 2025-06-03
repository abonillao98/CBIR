import numpy as np

def rgb2hmmd(rgb_image_in, mode='HDS'):
    """
    Convierte una imagen RGB al espacio de color HMMD.
    mode: 'HMM' (Hue, Max, Min) o 'HDS' (Hue, Diff, Sum)
    """

    if mode not in ['HMM', 'HDS']:
        mode = 'HDS'

    # Asegurar tipo float64 en rango [0,1]
    if rgb_image_in.dtype == np.uint8:
        rgb_image_in = rgb_image_in.astype(np.float64) / 255.0

    rows, cols, _ = rgb_image_in.shape
    hmmd_image_out = np.zeros((rows, cols, 3), dtype=np.float64)

    for i in range(rows):
        for j in range(cols):
            r, g, b = rgb_image_in[i, j]

            maxx = max(r, g, b)
            minn = min(r, g, b)

            # Cálculo del Hue
            if maxx == minn:
                hue = 0
            elif maxx == r and g >= b:
                hue = 60 * ((g - b) / (maxx - minn))
            elif maxx == r and g < b:
                hue = 360 + 60 * ((g - b) / (maxx - minn))
            elif maxx == g:
                hue = 60 * (2 + (b - r) / (maxx - minn))
            else:
                hue = 60 * (4 + (r - g) / (maxx - minn))

            hue = hue / 360.0  # Normalizar hue a [0,1]

            diff = maxx - minn
            summ = (maxx + minn) / 2

            if mode == 'HMM':
                hmmd_image_out[i, j] = [hue, maxx, minn]
            else:  # HDS
                hmmd_image_out[i, j] = [hue, diff, summ]

    return hmmd_image_out