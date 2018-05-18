import matplotlib.pyplot as plt
import numpy as np

class NIPH_ILI_oslo_bergen:
    def __init__(self, filepath):
        print('hello')

    def get_data(self):
        print('get data')

    def draw_graph(self, x, y):
        print('draw graph')
    
    def get_graph(self): return self._FIGURE
    
def main():
    NIPH_ILI(r'./ILI_tall_2016_17.xlsx') # absolute path to protect sensitive data
    plt.show()

if __name__ == '__main__':
    main()
