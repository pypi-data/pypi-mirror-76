"""
    Matrix structural analysis.
    Each node has three degrees of freedom: ux, uy, rotation
    Stiffness matrix for each element is 6x6
    num_dof = number of degrees of freedom = 3*number of nodes
    Dimensions in inches
    Forces in kips, moments in kip-inches

    http://docs.ursavus.com/FrameAnalysis

    dof = local degree of freedom
    DoF = global degree of freedom
    F = global joint force matrix
    fef = local (member) fixed-end forces
    FeF = global fixed-end forces
    k = local (member) stiffness
    K = global stiffness matrix
    R = global reactions
    member = element
    node = joint
    t = member transformation matrix
    u = joint displacements in local coordinates
    U = joint displacements in global coordinates
"""

import copy
import geom
import math
import numpy

# Module constants
DOF_PER_JOINT = 3   # 0 = ux, 1 = uy, 2 = rotation
DOF_X = 0
DOF_Y = 1
DOF_ROTATION = 2

class Node(geom.Point):

    def __init__(self, frame, id, x, y):
        geom.Point.__init__(self, float(x), float(y))
        self.id = id
        self.frame = frame
        self.fixed_x = False
        self.fixed_y = False
        self.fixed_theta = False
        self.loads = []

    def is_support(self):
        return self.fixed_x or self.fixed_y or self.fixed_theta

    def is_free(self):
        "Returns true if no boundary conditions"
        return not self.is_support()

    def __lt__(self, other):
        "Compare for sorting"
        return (self.x, self.y) < (other.x, other.y)

    def pin(self):
        "Gives the ndoe a pinned support conditon."
        self.fixed_x = True
        self.fixed_y = True
        self.fixed_theta = False

    def fix(self):
        "Gives the ndoe a pinned support conditon."
        self.fixed_x = True
        self.fixed_y = True
        self.fixed_theta = True

    def free(self):
        "Clears any boundary conditions."
        self.fixed_x = False
        self.fixed_y = False
        self.fixed_theta = False

    def roller_x(self):
        "Sets x-roller boundary condition; reaction in y-direction"
        self.free()
        self.fixed_y = True

    def roller_y(self):
        "Sets y-roller boundary condition; reaction in x-direction"
        self.free()
        self.fixed_x = True

    def add_load(self, load):
        "Add a nodal load vector: (Fx, Fy, M) in kips, kip-in"
        self.loads.append(load)

    def dofs(self):
        "Returns list of local degrees of freedom"
        return list(range(0, DOF_PER_JOINT))

    def DoFs(self):
        "Returns global degrees of freedom corresponding to local ones."
        return [self.id*DOF_PER_JOINT + dof for dof in self.dofs()]

class FrameMember(geom.Segment):
    def __init__(self, frame, id, i_node, j_node, A = 1.0, E = 1.0, I = 1.0):
        geom.Segment.__init__(self, i_node, j_node)
        self.A = A
        self.E = E
        self.I = I
        self.frame = frame
        self.i = i_node
        self.id = id
        self.j = j_node
        self.uniform_loads = []
        self.point_loads = []

    def __unicode__(self):
        return "M%d %s (A = %.2f, E = %.0f, L = %.1f)" % \
                (self.id, geom.Segment.__unicode__(self), self.A, self.E, self.length())

    def add_uniform(self, kips_per_inch):
        self.uniform_loads.append(kips_per_inch)

    def add_point(self, kips, x):
        self.point_loads.append({"x" : x, "P" : kips})

    def t(self):
        "Returns transformation matrix for member."
        phi = self.bearing()    # radians
        c = math.cos(phi)
        s = math.sin(phi)
        return numpy.matrix([[c, s, 0.0, 0.0, 0.0, 0.0],
                          [-s, c, 0.0, 0.0, 0.0, 0.0],
                          [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                          [0.0, 0.0, 0.0, c, s, 0.0],
                          [0.0, 0.0, 0.0, -s, c, 0.0],
                          [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]])

    def k(self):
        "Returns element stiffness matrix in global coordinates."

        AE_L = self.A*self.E/self.length()
        EI = self.E*self.I
        L = self.length()
        k = numpy.matrix([[AE_L, 0.0, 0.0, -AE_L, 0.0, 0.0],
            [0.0, 12.0*EI/L**3, 6.0*EI/L**2, 0.0, -12.0*EI/L**3, 6.0*EI/L**2],
            [0.0, 6.0*EI/L**2, 4.0*EI/L, 0.0, -6.0*EI/L**2, 2.0*EI/L],
            [-AE_L, 0.0, 0.0, AE_L, 0.0, 0.0],
            [0.0, -12.0*EI/L**3, -6.0*EI/L**2, 0.0, 12.0*EI/L**3, -6.0*EI/L**2],
            [0.0, 6.0*EI/L**2, 2.0*EI/L, 0.0, -6.0*EI/L**2, 4.0*EI/L]])

        if self.bearing():
            # If member is not horizontal, transform stiffness to global coords
            t = self.t()
            k = (t.transpose())*k*t

        return k.round(5)

    def ue(self, u):
        "Recover member displacements given global displacements."
        return self.t()*u

    def Fe(self, u):
        "Recover member forces, Fe, given global displacements, u"
        dx1, dy1, theta1, dx2, dy2, theta2 = self.ue(u)
        EI = self.E*self.I
        L = self.length()

        dL = dx2 - dx1

        # Calculate axial force

        self.P = self.E*self.A*dL/self.length()
        k = self.k()

        # Calculate end forces
        # http://www.mae.ncsu.edu/courses/mae316/eischen/docs/FEBeamNotes.pdf
        M1 = (6.0*EI/L**2)*dy1 + 4.0*EI/L*theta1 - (6.0*EI/L**2)*dy2 + 2.0*EI/L*theta2
        M2 = (6.0*EI/L**2)*dy1 + 2.0*EI/L*theta1 - (6.0*EI/L**2)*dy2 + 4.0*EI/L*theta2
        V1 = (12.0*EI/L**3)*dy1 + (6.0*EI/L**2)*theta1 - (12.0*EI/L**3)*dy2 + (6.0*EI/L**2)*theta2
        V2 = (12.0*EI/L**3)*dy1 + (6.0*EI/L**2)*theta1 - (12.0*EI/L**3)*dy2 + (6.0*EI/L**2)*theta2

#        print "P = %.2f k, M1 = %.3f kip-ft, M2 = %.3f kip-ft, V1 = %.3f k, V2 = %.3f k" % (self.P,
#                M1/12.0, M2/12.0, V1, V2)

    def fef(self):
        """Returns fixed-end forces in local coordinates.
           (Pi, Vi, Mi, Pj, Vi, Mj"""
        # Initialize empty values
        P1 = 0.0    # k         dof 0
        V1 = 0.0    # k         dof 1
        M1 = 0.0    # k-in      dof 2
        P2 = 0.0    # k         dof 3
        V2 = 0.0    # k         dof 4
        M2 = 0.0    # k-in
        L = self.length()
#        print "L = %.2f" % (L)

        # Apply uniform loads
        for u in self.uniform_loads:
            V1 = V1 + u*L/2.0
            V2 = V2 + u*L/2.0
            M1 = u*L**2/12.0
            M2 = -u*L**2/12.0

        # Apply point loads
        for pl in self.point_loads:
            P = pl["P"]
            a = pl["x"]
            b = L - pl["x"]
#            print "Applying point load: %s kips at a = %s, b = %s" % (P, a, b)
            V2 = V2 + P*a/L
            V1 = V1 + P*b/L
            M1 = M1 + P*a*b*b/(L*L)
            M2 = M2 - P*a*a*b/(L*L)

#        print V1, V2, M1, M2

        return numpy.matrix([P1, V1, M1, P2, V2, M2]).transpose()

    def dofs(self):
        "Returns degrees of freedom for the member."
        return list(range(0, DOF_PER_JOINT*2))

    def DoFs(self):
        "Returns global degrees of freedom for the member."
        retval = list(self.i.DoFs()).extend(list(self.j.DoFs()))
        return retval


class Frame2D:
    "Class consisting of nodes, members and node forces."
    def __init__(self):
        self.nodes = []
        self.members = []

    def support_nodes(self):
        "Returns list of nodes which have a boundary condition"
        retval = []
        for n in self.nodes:
            if n.is_support():
                retval.append(n)
        return retval

    def renumber_nodes(self):
        "Renumbers nodes left to right, bottom to top"
        old_nodes = [n for n in self.nodes]
        old_nodes.sort()
        self.nodes = []
        for i in range(0, len(old_nodes)):
            n = old_nodes[i]
            n.id = i
            self.nodes.append(n)

    def node_ids(self):
        "Returns sorted node id's"
        retval = [n.id for n in self.nodes]
        retval.sort()
        return retval

    def add_node(self, x, y):
        for existing_node in self.nodes:
            if existing_node.dist((x, y)) <= 0.01:
                # Duplicate node - return it
                return existing_node
        n = Node(self, len(self.nodes), x, y)
        self.nodes.append(n)
        return n

    def add_member(self, i, j, A = 1.0, E = 1.0, I = 1.0):
        ni = self.nodes[i]
        nj = self.nodes[j]
        m = FrameMember(self, len(self.members), ni, nj, A, E, I)
        self.members.append(m)
        return m

    def __unicode__(self):
        retval = "\nTwo-dimensional truss with %d nodes:" % len(self.nodes)
        for i in range(0, len(self.nodes)):
            retval += "\nN%d\t%s" % (i, self.nodes[i])
        retval += "\n\n%d members:" % len(self.members)
        for i in range(0, len(self.members)):
            retval += "\nM%d\t%s" % (i, self.members[i])
        return retval

    def add_pin(self, i):
        if i in list(self.nodes.keys()):
            self.nodes[i].fixed_x = True
            self.nodes[i].fixed_y = True
            self.nodes[i].fixed_theta = False

    def add_roller_x(self, i):
        if i in list(self.nodes.keys()):
            self.nodes[i].fixed_x = False
            self.nodes[i].fixed_y = True
            self.nodes[i].fixed_theta = False

    def add_roller_y(self, i):
        if i in list(self.nodes.keys()):
            self.nodes[i].fixed_x = True
            self.nodes[i].fixed_y = False
            self.nodes[i].fixed_theta = False

    def fixed(self, i):
        if i in list(self.nodes.keys()):
            self.nodes[i].fixed_x = True
            self.nodes[i].fixed_y = True
            self.nodes[i].fixed_theta = True

    def build_K(self):
        # Create an empty global stiffness matrix
        n = len(self.nodes)*DOF_PER_JOINT
        self.K = numpy.zeros((n, n))

        # Make a map of global degress of freedom
        dof = 0
        DoF = {}
        for j in range(0, len(self.nodes)):
            DoF[j] = (dof, dof + 1, dof + 2)
            dof = dof + 3
        self.DoF = DoF

        # Cycle through members and add their stiffnesses to the global
        # stiffness matrix, self.K
        for m in range(0, len(self.members)):
            memb = self.members[m]
            k = memb.k()
            iDoF = []
            iDoF.extend(DoF[memb.i.id])
            iDoF.extend(DoF[memb.j.id])

            # Map each member DoF to a global DoF
            for r in range(0, DOF_PER_JOINT*2):
                for c in range(0, DOF_PER_JOINT*2):
                    self.K[iDoF[r]][iDoF[c]] = self.K[iDoF[r]][iDoF[c]] + k[r][c]

    def validate(self):
        "Check frame for various problems."
        # Check for orphaned joints
        connected_nodes = []
        retval = True
        for m in self.members:
            connected_nodes.extend([m.i, m.j])
        for node in self.nodes:
            if node not in connected_nodes:
#                print "Orphaned node %s" % node
                retval = False
        return retval

    def analyze(self):
        #TODO: fix duplicate nodes
        assert(self.validate())
        self.build_K()
#        print "\nGlobal Stiffness Matrix, K ="
        K = self.K
        Kmod = copy.copy(self.K)

        # Delete the rows and columns that are fixed
        num_dof = len(self.nodes)*DOF_PER_JOINT

        # Make a list of global DoFs that are supports
        supts = []
        for i in range(0, len(self.nodes)):
            if self.nodes[i].fixed_x:
                supts.append(self.DoF[i][0])
            if self.nodes[i].fixed_y:
                supts.append(self.DoF[i][1])
            if self.nodes[i].fixed_theta:
                supts.append(self.DoF[i][2])

        supts.sort()

        for i in supts:
            for j in range(0, num_dof):
                Kmod[i][j] = 0.0
                Kmod[j][i] = 0.0

            Kmod[i][i] = 1

        # F = Applied external forces
        F = numpy.matrix([0.0 for i in range(0, num_dof)]).transpose()

        for n in self.nodes:
            if len(n.loads):
                for dof in n.dofs():
                    DoF = n.DoFs()[dof]
                    for load in n.loads:
                        F[DoF] = F[DoF] + load[dof]

#        print "\nApplied Forces:"
#        print F

        # Directly applied joint loads

        # Add fixed-end forces
#        print self.DoF
        FeF = numpy.matrix([0.0 for i in range(0, num_dof)]).transpose()
        FeFmod = numpy.matrix([0.0 for i in range(0, num_dof)]).transpose()
        for m in range(0, len(self.members)):
            memb = self.members[m]
            mdof = [dof for dof in self.DoF[memb.i.id]]
            fef = memb.t()*memb.fef()
            mdof.extend([dof for dof in self.DoF[memb.j.id]])
            for dof in range(0, len(fef)):  # local degree of freedom
                DoF = mdof[dof]             # global degree of freedom
                FeF[DoF] = FeF[DoF] + fef[dof]
                if DoF not in supts:
                    # For the solution fixed-end force vector, we will not
                    # apply forces to degrees of freedom that are boundary
                    # conditions
                    FeFmod[DoF] = FeFmod[DoF] + fef[dof]


#        print "\nFixed End Forces:"
#        print FeF

       # Solve for u using the saved stiffness matrix Kmod
        U = numpy.linalg.solve(Kmod, (F - FeFmod))

        # Enforce zero displacements for each support DoF
        for i in supts:
            U[i] = 0.0

#        print "\nDisplacements:"
#        print U.round(3)

        # Recover the reactions using the unmodified stiffness matrix K,
        # subtracting out applied forces
        R = K*U - F + FeF
#        print "\nReactions:"
#        print R.round(3)



        for m in range(0, len(self.members)):
            memb = self.members[m]
#            print "\nMember Forces for %s:" % memb
            k = memb.k()
#            print memb.DoFs()
#            iDoF = []
#            iDoF.extend(self.DoF[memb.i.id])
#            iDoF.extend(self.DoF[memb.j.id])

#            ue = []
#            for dof in iDoF:
#                ue.append(numpy.array(u)[dof][0])

#            print memb.Fe(numpy.matrix(ue).transpose())

        # Convert the reaction matrix into a list of 3-tuples:
        # (P, V, M)
        R = [r[0] for r in R.tolist()]
        R = list(zip(*[R[i::3] for i in range(3)]))

        # Convert the deflection matrix into a list of 3-tuples:
        # (dx, dy, dtheta)
        U = [r[0] for r in U.tolist()]
        U = list(zip(*[U[i::3] for i in range(3)]))

        return {"reactions" : R, "deflections" : U}

