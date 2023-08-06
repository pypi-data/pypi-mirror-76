"""
Characterization of incomparable pairs
"""


class ACM(object):
    """ACM calculation

    i1,i2 = 1,...,r, r: number of vertices (i1  < i2)
    j1,j2 = 1,...,k, k: number of attributes (syn: indicators)(j1 < j2)
    ACM[(xi1,xi2),(qj1,qj2)] = 1 if objects xi1, xi2 are incomparable
    with respect to indicators qj1,qj2,
    ACM[(xi1,xi2),(qj1,qj2)] = 0 if objects xi1, xi2 are comparable
    with respect to indicators qj1,qj2
    ACM informs:

    a) How often for a given objectpair (xi1,xi2), incomparabilities
       within the attributepair (qj1,qj2) appear.
    b) How often for a given attributepair (qj1,qj2) incomparabilities
       within the objectpair (xi1,xi2) appear.

    """

    def __init__(self,  matrix, csv):
        """
        :param matrix: reduced data matrix #???
        :type matrix: object of class matrix ???

        :param csv: source data with all objects
        :type csv: object of class csv
        """

        self.matrix = matrix
        self.csv = csv
        self.dm = csv.data
        self.r = matrix.rows
        self.k = matrix.cols
        self.lpx = None
        self.lpq = None
        self.acm = []
        self.maxobjectpairs = []
        self.maxattributepairs = []
        self.objlist = []
        self.userlist = []

    def generate_setofpairs(self, user_list):
        """ pairs of objects and attributes

        Objects (xi1,xi2) and of attributes (qj1,qj2) are generated.

        For example set of objects: {a,b,c,d} then

        px = {(a,b),(a,c),(a,d),(b,c),(b,d),(c,d)}

        Note (1): x must have an access to the pointers of the full
        object set even if the set of representants is not identical
        with the full object set.
        Note (2): px is a tuple of pairs, formed form the user_list,
                  however represented
        by idx, see Note(1). Taking the example  px would look like
        [(0,1), (0,2), (0,3), (1,2),...]
        Note (3): if equivalence classes appear, px is not affected
                  whether the representant or
        other objects of the class are selected
        Note (4): the pasirs are formed subsequently i.e. [0,1,2,3]
                  as tuple of object-idx,
        then px = [(0,1),(0,2), (0,3), (1,2), (1,3), (2,3)]
        Note (5): the user_list may also contain comparable objects.


        For example set of attributes (q1,q2,q3} then

        pq = {(q1,q2),(q1,q3),(q2,q3)}

        :param user_list: actual interesting subset of matrix.obj
        :type user_list: list

        :var r: number of rows
        :type r: int

        :var k: number of attributes (syn.: indicators)
        :type k: int

        :var px: objectpairs
        :type px: list

        :var pq: attributepairs
        :type pq: list

        :returns: (px, pq)
        """

        obj = self.csv.obj
        self.objlist = []
        lu = len(user_list)
        self.dim_r = int(lu * (lu - 1.0) / 2.0)
        self.dim_k = int(1.0 * self.k * (self.k - 1.0) / 2.0)
        for i in range(0, self.dim_r):
            self.objlist.append(0)
        px = []
        z = 0
        for i1 in range(0, len(user_list)):
            iob1 = obj.index(user_list[i1])
            for i2 in range(i1 + 1, lu):
                iob2 = obj.index(user_list[i2])
                px.append((iob1, iob2))
                self.objlist[z] = (iob1, iob2)
                z += 1

        self.attlist = []
        for j in range(0, self.dim_k):
            self.attlist.append(0)
        zq = 0
        pq = []
        for j1 in range(0, self.k):
            for j2 in range(j1 + 1, self.k):
                pq.append((j1, j2))
                self.attlist[zq] = (j1, j2)
                zq += 1
        return (px, pq)

    def calc_acm(self, px=[], pq=[], precision=3):
        """The matrix ACM ("antichain matrix") will be calculated.

        ACM[(xi1,xi2),(qj1,qj2)] = 1 if objects xi1, xi2 are incomparable

        with respect to indicators qj1,qj2,

        ACM[(xi1,xi2),(qj1,qj2)] = 0 if objects xi1, xi2 are comparable

        with respect to indicators qj1,qj2

        :var dm: data matrix with r rows and k columns

        :var acm: ACM, i.e. matrix of pairwise incomparabilities

        :param px: List of pairs of objects, generated for user_list.
                   Note: Objects defined by their indices
        :type px: list

        :param pq: List of pairs of indicatros
        :type pq: list

        :return: self.acm
        :type self.acm: matrix
        """
        self.lpx = len(px)
        self.lpq = len(pq)
        self.acm = []

        for i in range(0, self.lpx):
            self.acm.append(0)
            self.acm[i] = []
        # in the following loop (i=1,...,length of px), j= 1,..., length of pq
        # four boolean variables are calculated

        for i in range(0, self.lpx):
            for j in range(0, self.lpq):
                iob1 = px[i][0]
                iatt1 = pq[j][0]
                iob2 = px[i][1]
                iatt2 = pq[j][1]

                x11 = round(float(self.dm[iob1][iatt1]), precision)
                x21 = round(float(self.dm[iob2][iatt1]), precision)
                x12 = round(float(self.dm[iob1][iatt2]), precision)
                x22 = round(float(self.dm[iob2][iatt2]), precision)

                bool1 = x11 > x21
                bool2 = x12 < x22
                bool3 = x11 < x21
                bool4 = x12 > x22
                if (bool1 and bool2):
                    self.acm[i].append(1)
                else:
                    if (bool3 and bool4):
                        self.acm[i].append(1)
                    else:
                        self.acm[i].append(0)
        return self.acm

    def calc_obj_attprofile(self):
        """columnsum and rowsum of ACM

        :var acm: incomparability matrix
        :type acm: lists

        :var rowsumacm: row sum of ACM
        :type rowsuacm: list

        :var colsumacm: column sum of ACM
        :type colsumacm: list

        :returns: self.rowsumacm, self.colsumacm
        :rtype: tuple
        """

        self.colsumacm = []
        for j in range(0, self.lpq):
            sumhilf = 0
            for i in range(0, self.lpx):
                sumhilf += self.acm[i][j]
            self.colsumacm.append(sumhilf)

        self.rowsumacm = []
        for i in range(0, self.lpx):
            sumhilf = 0
            for j in range(0, self.lpq):
                sumhilf += self.acm[i][j]
            self.rowsumacm.append(sumhilf)
        return self.rowsumacm, self.colsumacm

    def calc_optimum(self):
        """ optimum of row- and colsums of acm

        :returns: self.maxirowsum, self.maxicolsum
        """

        # rowsum
        self.maxirowsum = - 9999
        for i in range(0, self.lpx):
            if self.rowsumacm[i] >= self.maxirowsum:
                self.maxirowsum = self.rowsumacm[i]

        # columnsum
        self.maxicolsum = -9999
        for j in range(0, self.lpq):
            if self.colsumacm[j] >= self.maxicolsum:
                self.maxicolsum = self.colsumacm[j]
        return self.maxirowsum, self.maxicolsum

    def find_optimalpairs(self, px, pq):
        """For maxirowsum and maxicolsum, resp. find the corresponding

         object/indicatorpairs

        :userlist: The input by the user.
                   Should be but must not be an antichain
        :lpx: number of objectpairs
        :type lpx: int
        :param px: List of pairs of objects, generated for user_list.
                   Note: Objects defined by their indices
        :type px: list
        :param pq: List of pairs of indicatros
        :type pq: list

        :returns: self.maxobjectpairs, self.maxattributepairs
        :rtype: tuple

        """
        # objectpairs
        self.maxobjectpairs = []
        for i in range(0, self.lpx):
            if self.rowsumacm[i] == self.maxirowsum:
                self.maxobjectpairs.append(px[i])

        # attributepairs
        self.maxattributepairs = []
        for j in range(0, self.lpq):
            if self.colsumacm[j] == self.maxicolsum:
                self.maxattributepairs.append(pq[j])
        return self.maxobjectpairs, self.maxattributepairs

    def acm_graphics(self, user_list):
        """ Prepares names and data for bar diagrams

        one bar diagram: name_obj and obj_labels and rowsumacm
        the other bar diagram: name:att and att_labels and colsumacm
        external label: Labels given by the user, not the internally used ones

        :var matrix.obj: object labels of reduced list
        :type matrix.obj: list

        :var labelmaxobj: Pairs of objects for which rowsum is maximal,
                          external labels
        :var labelmaxatt: Pairs of attributes for which the colsum is maximal,
                          external labels
        :var name_obj: are names for the ordinates
        :var name_att: are names for the ordinates
        :returns: name_obj, name_att, label_objpairs, label_attpairs,
                 labelsmaxobj, labelsmaxatt
        :rtype: tuple
        """
        prop = self.matrix.prop
        self.px, self.pq = self.generate_setofpairs(user_list)
        self.lpx = len(self.px)
        self.lpq = len(self.pq)
        obj = self.csv.obj

        name_obj = "count(incomparabilities) object-pairs"
        name_att = "count(incomparabilities) att-pairs"
        label_objpairs = []

        for i in range(0, self.lpx):
            label_objpairs.append((obj[self.objlist[i][0]],
                                   obj[self.objlist[i][1]]))
        label_attpairs = []
        for j in range(0, self.lpq):
            label_attpairs.append((prop[self.attlist[j][0]],
                                   prop[self.attlist[j][1]]))
        labelmaxobj = []
        for i in range(0, len(self.maxobjectpairs)):
            labelmaxobj.append((obj[self.maxobjectpairs[i][0]],
                                obj[self.maxobjectpairs[i][1]]))
        labelmaxatt = []
        for j in range(0, len(self.maxattributepairs)):
            labelmaxatt.append((prop[self.maxattributepairs[j][0]],
                                prop[self.maxattributepairs[j][1]]))
        return name_obj,\
            name_att, \
            label_objpairs, \
            label_attpairs, \
            labelmaxobj, \
            labelmaxatt
