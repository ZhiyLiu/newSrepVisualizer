# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 10:42:25 2014

@author: jvicory & jphong
"""

import numpy
import datetime

class spoke:
    def __init__(self, ux, uy, uz, r):
        self.U = numpy.array([ux,uy,uz])
        self.r = r

class hub:
    def __init__(self, x, y, z):
        self.P = numpy.array([x,y,z])

class atom:
    def __init__(self, hub):
        self.hub = hub

    def addSpoke(self, spoke, side):
        if side == 0:
            self.topSpoke = spoke
        elif side == 1:
            self.botSpoke = spoke
        else:
            self.crestSpoke = spoke;

    def setLocation(self, row, col):
        self.row = row;
        self.col = col;

    def isCrest(self):
        return hasattr(self,'crestSpoke')

class srep:
    def __init__(self, numRows, numCols):
        self.numRows = numRows
        self.numCols = numCols
        self.atoms = numpy.ndarray([numRows,numCols],dtype=object)

    def addAtom(self, row, col, atom):
        self.atoms[row,col] = atom

    def addAtomFromDict(self, row, col, primdict):
        px = float(primdict['x'])
        py = float(primdict['y'])
        pz = float(primdict['z'])

        newhub = hub(px,py,pz)
        newatom = atom(newhub)

        ux0 = float(primdict['ux[0]'])
        uy0 = float(primdict['uy[0]'])
        uz0 = float(primdict['uz[0]'])
        r0 = float(primdict['r[0]'])
        spoke0 = spoke(ux0,uy0,uz0,r0)
        newatom.addSpoke(spoke0,0)

        ux1 = float(primdict['ux[1]'])
        uy1 = float(primdict['uy[1]'])
        uz1 = float(primdict['uz[1]'])
        r1 = float(primdict['r[1]'])
        spoke1 = spoke(ux1,uy1,uz1,r1)
        newatom.addSpoke(spoke1,1)

        primtype = primdict['type']

        if primtype == 'EndPrimitive':
            ux2 = float(primdict['ux[2]'])
            uy2 = float(primdict['uy[2]'])
            uz2 = float(primdict['uz[2]'])
            r2 = float(primdict['r[2]'])
            spoke2 = spoke(ux2,uy2,uz2,r2)
            newatom.addSpoke(spoke2,2)

        self.addAtom(row,col,newatom)
    def readSrepFromM3D(filename):
        f = open(filename,'r')

        lines = [line.strip() for line in f.readlines()]

        figidx = lines.index('figure[0] {')
        coloridx = lines.index('color {')
        endidx = lines.index('}',coloridx)

        figparams = getSectionDict(lines,figidx+1,coloridx)
        numrows = int(figparams['numRows'])
        numcols = int(figparams['numColumns'])

        fig = srep.figure(numrows,numcols)

        primidx = endidx + 1;

        for row in range(numrows):
            for col in range(numcols):
                endprimidx = lines.index('}',primidx)
                primsection = getSectionDict(lines,primidx+1,endprimidx)
                fig.addAtomFromDict(row,col,primsection)
                primidx = endprimidx + 1;

        return fig

    def writeSrepToM3D(filename, fig):
        f = open(filename,'w')

        f.write('pabloVersion = 9974 2009/07/24 19:36:23;\n'.expandtabs(4));
        f.write('coordSystem {\n'.expandtabs(4));
        f.write('\tyDirection = 1;\n'.expandtabs(4));
        f.write('}\n'.expandtabs(4));

        f.write('model {\n'.expandtabs(4));
        f.write('\tfigureCount = 1;\n'.expandtabs(4));
        f.write('\tname = test;\n'.expandtabs(4));
        f.write('\tfigureTrees {\n'.expandtabs(4));
        f.write('\t\tcount=1;\n'.expandtabs(4));
        f.write('\t\ttree[0] {\n'.expandtabs(4));
        f.write('\t\t\tattachmentMode = 0;\n'.expandtabs(4));
        f.write('\t\t\tblendAmount = 0;\n'.expandtabs(4));
        f.write('\t\t\tblendExtent = 0;\n'.expandtabs(4));
        f.write('\t\t\tchildCount = 0;\n'.expandtabs(4));
        f.write('\t\t\tfigureId = 0;\n'.expandtabs(4));
        f.write('\t\t\tlinkCount = 0;\n'.expandtabs(4));
        f.write('\t\t}\n'.expandtabs(4));
        f.write('\t}\n'.expandtabs(4));

        f.write('\tfigure[0] {\n'.expandtabs(4));
        f.write('\t\tname = test;\n'.expandtabs(4));

        f.write('\t\tnumColumns = %s;\n'.expandtabs(4) % fig.numCols);

        f.write('\t\tnumLandmarks = 0;\n'.expandtabs(4));

        f.write('\t\tnumRows = %s;\n'.expandtabs(4) % fig.numRows);

        f.write('\t\tpositivePolarity = 1;\n'.expandtabs(4));
        f.write('\t\tpositiveSpace = 1;\n'.expandtabs(4));
        f.write('\t\tsmoothness = 50;\n'.expandtabs(4));
        f.write('\t\ttype = QuadFigure;\n'.expandtabs(4));

        f.write('\t\tcolor {\n'.expandtabs(4));
        f.write('\t\t\tblue = 0;\n'.expandtabs(4));
        f.write('\t\t\tgreen = 1;\n'.expandtabs(4));
        f.write('\t\t\tred = 0;\n'.expandtabs(4));
        f.write('\t\t}\n'.expandtabs(4));

        for row in range(fig.numRows):
            for col in range(fig.numCols):

                isCrest = fig.atoms[row,col].isCrest();
                f.write('\t\tprimitive[{0}][{1}] {{\n'.format(row,col).expandtabs(4));

                f.write('\t\t\tr[0] = {0};\n'.format(fig.atoms[row,col].topSpoke.r).expandtabs(4));
                f.write('\t\t\tr[1] = {0};\n'.format(fig.atoms[row,col].botSpoke.r).expandtabs(4));
                if isCrest:
                    f.write('\t\t\tr[2] = {0};\n'.format(fig.atoms[row,col].crestSpoke.r).expandtabs(4));

                f.write('\t\t\tselected = 1;\n'.expandtabs(4));

                if isCrest:
                    f.write('\t\t\ttype = EndPrimitive;\n'.expandtabs(4));
                else:
                    f.write('\t\t\ttype = StandardPrimitive;\n'.expandtabs(4));

                f.write('\t\t\tux[0] = {0};\n'.format(fig.atoms[row,col].topSpoke.U[0]).expandtabs(4));
                f.write('\t\t\tux[1] = {0};\n'.format(fig.atoms[row,col].botSpoke.U[0]).expandtabs(4));

                if isCrest:
                    f.write('\t\t\tux[2] = {0};\n'.format(fig.atoms[row,col].crestSpoke.U[0]).expandtabs(4));
                else:
                    f.write('\t\t\tux[2] = 1;\n'.expandtabs(4));

                f.write('\t\t\tuy[0] = {0};\n'.format(fig.atoms[row,col].topSpoke.U[1]).expandtabs(4));
                f.write('\t\t\tuy[1] = {0};\n'.format(fig.atoms[row,col].botSpoke.U[1]).expandtabs(4));

                if isCrest:
                    f.write('\t\t\tuy[2] = {0};\n'.format(fig.atoms[row,col].crestSpoke.U[1]).expandtabs(4));
                else:
                    f.write('\t\t\tuy[2] = 0;\n'.expandtabs(4));

                f.write('\t\t\tuz[0] = {0};\n'.format(fig.atoms[row,col].topSpoke.U[2]).expandtabs(4));
                f.write('\t\t\tuz[1] = {0};\n'.format(fig.atoms[row,col].botSpoke.U[2]).expandtabs(4));

                if isCrest:
                    f.write('\t\t\tuz[2] = {0};\n'.format(fig.atoms[row,col].crestSpoke.U[2]).expandtabs(4));
                else:
                    f.write('\t\t\tuz[2] = 0;\n'.expandtabs(4));

                f.write('\t\t\tx = {0};\n'.format(fig.atoms[row,col].hub.P[0]).expandtabs(4));
                f.write('\t\t\ty = {0};\n'.format(fig.atoms[row,col].hub.P[1]).expandtabs(4));
                f.write('\t\t\tz = {0};\n'.format(fig.atoms[row,col].hub.P[2]).expandtabs(4));

                f.write('\t\t}\n'.expandtabs(4));

        f.write('\t}\n'.expandtabs(4));
        f.write('}');



        f.close()



    def getSectionDict(lines, start, stop):
        section = [line.strip(';') for line in lines[start:stop]]
        sectiondict = dict(line.split(' = ') for line in section)
        return sectiondict
