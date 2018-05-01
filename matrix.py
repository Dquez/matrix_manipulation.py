import math
from math import sqrt
import numbers

def zeroes(height, width):
    """
    Creates a matrix of zeroes.
    """
    g = [[0.0 for _ in range(width)] for __ in range(height)]
    return Matrix(g)

def identity(n):
    """
    Creates a n x n identity matrix.
    """
    I = zeroes(n, n)
    for i in range(n):
        I.g[i][i] = 1.0
    return I

class Matrix(object):
    
    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])
    
    #
    # Primary matrix math methods
    #############################
    
    def determinant(self):
        """
            Calculates the determinant of a 1x1 or 2x2 matrix.
            """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
        if self.h == 1:
            return [self.g[0]]
        else:
            ad = self.g[0][0] *  self.g[1][1]
            bc = self.g[0][1] *  self.g[1][0]
            return ad - bc

    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
            if not self.is_square():
                raise(ValueError, "Cannot calculate the trace of a non-square matrix.")
                    trace = 0
                        for i in range(len(self.g)):
                            for j in range(len(self.g[0])):
                                if i == j:
                                    trace += self.g[i][j]
                                        return trace

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
            inverse = []
            if not self.is_square():
                raise(ValueError, "Non-square Matrix does not have an inverse.")
            if self.h > 2:
                raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")
            elif len(self.g) == 1:
                inverse.append([1/self.g[0][0]])
            else:
                ad = self.g[0][0] *  self.g[1][1]
                bc = self.g[0][1] *  self.g[1][0]
                if ad == bc:
                    raise ValueError('The denominator of a fraction cannot be zero')
                        trace =  self.trace()
                        inverse_after_trace = [[1 * trace, 0 * trace],
                                               [0 * trace, 1 * trace]]
                        right_matrix_constant = []
                for i in range(len(self.g)):
                    row = []
                    for j in range(len(self.g[0])):
                        row.append(inverse_after_trace[i][j] - self.g[i][j])
                        right_matrix_constant.append(row)
                for i in range(len(right_matrix_constant)):
                    row = []
                    for j in range(len(right_matrix_constant[0])):
                        val = right_matrix_constant[i][j]  * (1/(ad-bc))
                            row.append(val)
                            inverse.append(row)
                return Matrix(inverse)
                 

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
            matrix_transpose = []
            for i in range(len(self.g[0])):
                row = []
                for j in range(len(self.g)):
                    row.append(self.g[j][i])
            matrix_transpose.append(row)
                return Matrix(matrix_transpose)

    def is_square(self):
        return self.h == self.w
    
        #
        # Begin Operator Overloading
        ############################
    def __getitem__(self,idx):
        """
            Defines the behavior of using square brackets [] on instances
            of this class.
            
            Example:
            
            > my_matrix = Matrix([ [1, 2], [3, 4] ])
            > my_matrix[0]
            [1, 2]
            
            > my_matrix[0][0]
            1
            """
        return self.g[idx]
    
    def __repr__(self):
        """
            Defines the behavior of calling print on an instance of this class.
            """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s
    
    def __add__(self,other):
        """
            Defines the behavior of the + operator
            """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same")
        added_matrix = []
        for i in range(len(self.g)):
            row = []
            for j in range(len(self.g)):
                row.append(self.g[i][j] + other.g[i][j])
            added_matrix.append(row)
        return Matrix(added_matrix)
    
    def __neg__(self):
        """
            Defines the behavior of - operator (NOT subtraction)
            
            Example:
            
            > my_matrix = Matrix([ [1, 2], [3, 4] ])
            > negative  = -my_matrix
            > print(negative)
            -1.0  -2.0
            -3.0  -4.0
            """
        negative_matrix = []
        for i in range(len(self.g)):
            row = []
            for j in range(len(self.g[0])):
                row.append(self.g[i][j] * -1)
            negative_matrix.append(row)
        return Matrix(negative_matrix)
    
    
    
    def __sub__(self, other):
        """
            Defines the behavior of - operator (as subtraction)
            """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be subtracted if the dimensions are the same")
        sub_matrix = []
        for i in range(len(self.g)):
            row = []
            for j in range(len(self.g)):
                row.append(self.g[i][j] - other.g[i][j])
            sub_matrix.append(row)
        return Matrix(sub_matrix)
    
    def __mul__(self, other):
        """
            Defines the behavior of * operator (matrix multiplication)
            """
        self_rows = len(self.g)
        other_columns = len(other.g[0])
        
        def get_column(matrix, column_number):
            column = []
            for i in range(len(matrix)):
                column.append(matrix[i][column_number])
            return column
        def dot_product(vector_one, vector_two):
            total = 0
            for i in range(len(vector_one)):
                total += vector_one[i] *  vector_two[i]
            return total
        # empty list that will hold the product of Self x Other
        result = []
        
        for i in range(self.h):
            row_result = []
            for j in range(other.w):
                vector1 = self.g[i]
                vector2 = get_column(other.g, j)
                row_result.append(dot_product(vector1,vector2))
            result.append(row_result)
        return Matrix(result)
    
    def __rmul__(self, other):
        """
            Called when the thing on the left of the * is not a matrix.
            
            Example:
            
            > identity = Matrix([ [1,0], [0,1] ])
            > doubled  = 2 * identity
            > print(doubled)
            2.0  0.0
            0.0  2.0
            """
        if isinstance(other, numbers.Number):
            pass
            for i in range(len(self.g)):
                for j in range(len(self.g[0])):
                    self.g[i][j] *= other
        return Matrix(self.g)

