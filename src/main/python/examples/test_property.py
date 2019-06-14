class Parent:
    @property
    def n_cells(self):
        raise NotImplementedError('Please implement this method.')

    @n_cells.setter
    def n_cells(self, n):
        raise NotImplementedError('Cannot set number of board cells.')


class Child(Parent):
    @property
    def n_cells(self):
        return 0


if __name__ == '__main__':
    child = Child()
    print(child.n_cells)
    try:
        child.n_cells = 10
    except:
        print('Caught setter exception')
