from plotting import plot_time_series_graph, plot_graph
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import numpy as np

if __name__ == "__main__":

    val_matrix = np.ones((4, 4, 4))

    val_matrix[1, 2, 0] = 0.6
    val_matrix[2, 1, 0] = 0.6
    val_matrix[0, 2, 0] = 0.8
    val_matrix[2, 0, 0] = 0.8
    val_matrix[2, 3, 0] = -0.7
    val_matrix[3, 2, 0] = -0.7
    val_matrix[1, 3, 0] = 0.4
    val_matrix[3, 1, 0] = 0.4
    val_matrix[3, 1, 1] = -0.9

    # Complete test case
    link_matrix = np.zeros(val_matrix.shape, dtype='U3')

    link_matrix[0, 1, 0] = '<-x'
    link_matrix[1, 0, 0] = 'x->'

    link_matrix[1, 2, 0] = 'o-o'
    link_matrix[2, 1, 0] = 'o-o'
    link_matrix[0, 2, 0] = 'o--'
    link_matrix[2, 0, 0] = '--o'
    link_matrix[2, 3, 0] = '---'
    link_matrix[3, 2, 0] = '---'
    link_matrix[1, 3, 0] = '<->'
    link_matrix[3, 1, 0] = '<->'

    link_matrix[0, 2, 1] = 'x-x'
    link_matrix[0, 0, 1] = 'o->'
    link_matrix[0, 1, 1] = '-->'
    link_matrix[1, 0, 3] = 'o-x'

    link_width = np.ones(val_matrix.shape)
    link_attribute = np.zeros(val_matrix.shape, dtype='object')
    link_attribute[:] = ''
    link_attribute[0, 1, 0] = 'spurious'
    link_attribute[1, 0, 0] = 'spurious'
    link_attribute[0, 2, 1] = 'spurious'

    for figsize in [(30,30), (50, 50)]:
        for nodesize in [10, 20, 30]:
            for arrowsize in [8, 12]:
                plot_time_series_graph(
                    val_matrix=val_matrix,
                    figsize=figsize,
                    sig_thres=None,
                    link_matrix=link_matrix,
                    link_width=link_width,
                    link_attribute=link_attribute,
                    arrow_linewidth=arrowsize,
                    node_size=nodesize,
                    var_names=range(len(val_matrix)),
                    inner_edge_style='dashed',
                    save_name=f"test-output/figsize-{figsize}_arrowsize-{arrowsize}_nodesize-{nodesize}.pdf"
                )
                plt.close()


"""
STATUS  TASK
Done    alle linktypen
?       plot_graph und plot_TSG, bei plot_graph contemp und lagged links in beide Richtungen bei Variables i und j
#       fig height and width, grosse und kleine figures, verschiedene Seitenverhaeltnisse
Done    verschiedene Link widths, muss fuer alle arrow-ARten gleich dick sein fuer den gleichen link_width Wert
Done    circles haben gleiche colormap wie edges
Done    circles sind exakt so breit wie arrows, das wird durch radiums~linewidth geloest, denke ich
#       shrinkA, shrinkB so, dass fuer alle node_sizes der Arrow immer schoen andockt, auch fuer alle Arrow-types und plot_graph usw
Done    Variables nodes sollten Kreise sein, also scatter?
-       dashed sollte mit '-' und '<->' funktionieren
Done    headwidth und length sollte schoen mit figure size etc skalieren
"""
