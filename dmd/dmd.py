import numpy as np

class DMD(object):

    """
    Class to compute dynamic mode decomposition of dynamical system.
    """

    def __init__(self, n_modes=None, es=None, tr=0.720):

        """
        Initialization method.

        Parameters:
        - - - - -
        n_modes: int
            number of DMD modes to keep
        es: float
            fraction of energy of system to keep
        tr: float
            sampling frequency (repetition time)
            default set to TR of HCP data
        """

        self.n_modes = n_modes
        self.es = es
        self.tr = tr

    def fit(self, X):

        """
        Fit the DMD model.

        Parameters:
        - - - - -
        X: float, array
            matrix of time series / samples
        """

        n = self.n_modes
        p = self.es
        rT = self.tr

        X -= np.mean(X, axis=1)[:, None]
        C = X[:, :-1]
        Cp = X[:, 1:]

        [U, S, V] = np.linalg.svd(C, full_matrices=False)

        # If power is defined, but number of modes is not
        # estimate the number of modes form data
        if not n and p:
            n = np.where((np.cumsum(S)/np.sum(S)) >= p)[0][0]+1
            print('Keeping {:} modes to capture {:} of energy.'.format(n, p))

        # Otherwise, number of modes = number of samples
        if n == None:
            n = X.shape[0]
        
        Ut = U[:, :n]
        Sinv = np.diag(1./S[:n])
        Vt = V[:n].T

        # compute reduced-dimensional representation of A-matrix
        Ap = (Ut.T).dot(Cp.dot(Vt.dot(Sinv)))

        # weight Ap by singular values so that modes reflect explained variance
        Ah = np.diag(S[:n]**-0.5).dot(Ap.dot(np.diag(S[:n]**0.5)))

        # compute eigendecomposition of weighted A matrix
        [w, v] = np.linalg.eig(Ah)
        v = np.diag(S[:n]**0.5).dot(v)

        # compute DMD modes from eigenvectors
        # using this approach, modes are not normalized -- norm gives power
        # of mode in data
        Phi = Cp.dot(Vt.dot(Sinv.dot(v)))
        power = np.real(np.sum(Phi*Phi.conj(), 0))

        # using h to convert complex eigenvalues into corresponding
        # oscillation frequencies
        freq = np.angle(w)/(2*np.pi*rT)

        self.phi_ = Phi
        self.power_ = power
        self.freq_ = freq
