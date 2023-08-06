from matplotlib_venn import venn2, venn2_circles
from matplotlib import pyplot as plt

test = 'hi'


def single():
    v1 = venn2(subsets=(3, 3, 1), ax=ax1)
    c1 = venn2_circles(subsets=(3, 3, 1), ax=ax1)

    for area in ['01', '10', '11']:
        color = 'skyblue' if area != '01' else 'white'
        v1.get_patch_by_id(area).set_color(color)
        v1.get_patch_by_id(area).set_alpha(1)
        txt = v1.get_label_by_id(area)
        if txt:
            txt.set_text('')

    ax1.set_axis_on()
    ax1.set_facecolor('white')
    ax1.set_title('A', fontsize=20)
    ymin, ymax = ax1.get_ylim()
    ax1.set_ylim(ymin - 0.1, ymax)

    return plt
