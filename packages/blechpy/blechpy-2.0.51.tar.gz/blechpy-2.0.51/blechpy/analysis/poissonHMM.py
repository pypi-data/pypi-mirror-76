import os
import math
import numpy as np
import itertools as it
import pandas as pd
import tables
import time as sys_time
from numba import njit
from scipy.ndimage.filters import gaussian_filter1d
from blechpy.utils.particles import HMMInfoParticle
from blechpy import load_dataset
from blechpy.dio import h5io, hmmIO
from blechpy.plotting import hmm_plot as hmmplt
from blechpy.utils import math_tools as mt
from joblib import Parallel, delayed, Memory, cpu_count
from appdirs import user_cache_dir
cachedir = user_cache_dir('blechpy')
memory = Memory(cachedir, verbose=0)



TEST_PARAMS = {'n_cells': 10, 'n_states': 4, 'state_seq_length': 5,
               'trial_time': 3.5, 'dt': 0.001, 'max_rate': 50, 'n_trials': 15,
               'min_state_dur': 0.05, 'noise': 0.01, 'baseline_dur': 1}


HMM_PARAMS = {'hmm_id': None, 'taste': None, 'channel': None,  'unit_type':
              'single', 'dt': 0.001, 'threshold': 1e-4, 'max_iter': 1000,
              'n_cells': None, 'n_trials': None, 'time_start': 0, 'time_end':
              2000, 'n_repeats': 25, 'n_states': 3, 'fitted': False, 'area': None}


FACTORIAL_LOOKUP = np.array([math.factorial(x) for x in range(20)])


@njit
def fast_factorial(x):
    if x < len(FACTORIAL_LOOKUP):
        return FACTORIAL_LOOKUP[x]
    else:
        y = 1
        for i in range(1,x+1):
            y = y*i

        return y


@njit
def poisson(rate, n, dt):
    '''Gives probability of each neurons spike count assuming poisson spiking
    '''
    tmp = np.power(rate*dt, n) / np.array([fast_factorial(x) for x in n])
    tmp = tmp * np.exp(-rate*dt)
    return tmp


@njit
def forward(spikes, dt, PI, A, B):
    '''Run forward algorithm to compute alpha = P(Xt = i| o1...ot, pi)
    Gives the probabilities of being in a specific state at each time point
    given the past observations and initial probabilities

    Parameters
    ----------
    spikes : np.array
        N x T matrix of spike counts with each entry ((i,j)) holding the # of
        spikes from neuron i in timebine j
    nStates : int, # of hidden states predicted to have generate the spikes
    dt : float, timebin in seconds (i.e. 0.001)
    PI : np.array
        nStates x 1 vector of initial state probabilities
    A : np.array
        nStates x nStates state transmission matrix with each entry ((i,j))
        giving the probability of transitioning from state i to state j
    B : np.array
        N x nSates rate matrix. Each entry ((i,j)) gives this predicited rate
        of neuron i in state j

    Returns
    -------
    alpha : np.array
        nStates x T matrix of forward probabilites. Each entry (i,j) gives
        P(Xt = i | o1,...,oj, pi)
    norms : np.array
        1 x T vector of norm used to normalize alpha to be a probability
        distribution and also to scale the outputs of the backward algorithm.
        norms(t) = sum(alpha(:,t))
    '''
    nTimeSteps = spikes.shape[1]
    nStates = A.shape[0]

    # For each state, use the the initial state distribution and spike counts
    # to initialize alpha(:,1)
    row = np.array([PI[i] * np.prod(poisson(B[:,i], spikes[:,0], dt))
                    for i in range(nStates)])
    alpha = np.zeros((nStates, nTimeSteps))
    norms = [np.sum(row)]
    alpha[:, 0] = row/norms[0]
    for t in range(1, nTimeSteps):
        tmp = np.array([np.prod(poisson(B[:, s], spikes[:, t], dt)) *
                        np.sum(alpha[:, t-1] * A[:,s])
                        for s in range(nStates)])
        tmp_norm = np.sum(tmp)
        norms.append(tmp_norm)
        tmp = tmp / tmp_norm
        alpha[:, t] = tmp

    return alpha, norms


@njit
def backward(spikes, dt, A, B, norms):
    ''' Runs the backward algorithm to compute beta = P(ot+1...oT | Xt=s)
    Computes the probability of observing all future observations given the
    current state at each time point

    Paramters
    ---------
    spike : np.array, N x T matrix of spike counts
    nStates : int, # of hidden states predicted
    dt : float, timebin size in seconds
    A : np.array, nStates x nStates matrix of transition probabilities
    B : np.array, N x nStates matrix of estimated spike rates for each neuron

    Returns
    -------
    beta : np.array, nStates x T matrix of backward probabilities
    '''
    nTimeSteps = spikes.shape[1]
    nStates = A.shape[0]
    beta = np.zeros((nStates, nTimeSteps))
    beta[:, -1] = 1  # Initialize final beta to 1 for all states
    tStep = list(range(nTimeSteps-1))
    tStep.reverse()
    for t in tStep:
        for s in range(nStates):
            beta[s,t] = np.sum((beta[:, t+1] * A[s,:]) *
                               np.prod(poisson(B[:, s], spikes[:, t+1], dt)))

        beta[:, t] = beta[:, t] / norms[t+1]

    return beta


@njit
def compute_baum_welch(spikes, dt, A, B, alpha, beta):
    nTimeSteps = spikes.shape[1]
    nStates = A.shape[0]
    gamma = np.zeros((nStates, nTimeSteps))
    epsilons = np.zeros((nStates, nStates, nTimeSteps-1))
    for t in range(nTimeSteps):
        if t < nTimeSteps-1:
            gamma[:, t] = (alpha[:, t] * beta[:, t]) / np.sum(alpha[:,t] * beta[:,t])
            epsilonNumerator = np.zeros((nStates, nStates))
            for si in range(nStates):
                for sj in range(nStates):
                    probs = np.prod(poisson(B[:,sj], spikes[:, t+1], dt))
                    epsilonNumerator[si, sj] = (alpha[si, t]*A[si, sj]*
                                                beta[sj, t+1]*probs)

            epsilons[:, :, t] = epsilonNumerator / np.sum(epsilonNumerator)

    return gamma, epsilons


@njit
def baum_welch(trial_dat, dt, PI, A, B):
    alpha, norms = forward(trial_dat, dt, PI, A, B)
    beta = backward(trial_dat, dt, A, B, norms)
    tmp_gamma, tmp_epsilons = compute_baum_welch(trial_dat, dt, A, B, alpha, beta)
    return tmp_gamma, tmp_epsilons


def compute_new_matrices(spikes, dt, gammas, epsilons):
    nTrials, nCells, nTimeSteps = spikes.shape
    minFR = 1/(nTimeSteps*dt)

    PI = np.sum(gammas, axis=0)[:,1] / nTrials
    Anumer = np.sum(np.sum(epsilons, axis=3), axis=0)
    Adenom = np.sum(np.sum(gammas[:,:,:-1], axis=2), axis=0)
    A = Anumer/Adenom
    A = A/np.sum(A, axis=1)
    Bnumer = np.sum(np.array([np.matmul(tmp_y, tmp_g.T)
                              for tmp_y, tmp_g in zip(spikes, gammas)]),
                    axis=0)
    Bdenom =  np.sum(np.sum(gammas, axis=2), axis=0)
    B = (Bnumer / Bdenom)/dt
    idx = np.where(B < minFR)[0]
    B[idx] = minFR

    return PI, A, B


def poisson_viterbi(spikes, dt, PI, A, B):
    '''
    Parameters
    ----------
    spikes : np.array, Neuron X Time matrix of spike counts
    PI : np.array, nStates x 1 vector of initial state probabilities
    A : np.array, nStates X nStates matric of state transition probabilities
    B : np.array, Neuron X States matrix of estimated firing rates
    dt : float, time step size in seconds

    Returns
    -------
    bestPath : np.array
        1 x Time vector of states representing the most likely hidden state
        sequence
    maxPathLogProb : float
        Log probability of the most likely state sequence
    T1 : np.array
        State X Time matrix where each entry (i,j) gives the log probability of
        the the most likely path so far ending in state i that generates
        observations o1,..., oj
    T2: np.array
        State X Time matrix of back pointers where each entry (i,j) gives the
        state x(j-1) on the most likely path so far ending in state i
    '''
    if A.shape[0] != A.shape[1]:
        raise ValueError('Transition matrix is not square')

    nStates = A.shape[0]
    nCells, nTimeSteps = spikes.shape
    T1 = np.zeros((nStates, nTimeSteps))
    T2 = np.zeros((nStates, nTimeSteps))
    T1[:,1] = np.array([np.log(PI[i]) +
                        np.log(np.prod(poisson(B[:,i], spikes[:, 1], dt)))
                        for i in range(nStates)])
    for t, s in it.product(range(1,nTimeSteps), range(nStates)):
        probs = np.log(np.prod(poisson(B[:, s], spikes[:, t], dt)))
        vec2 = T1[:, t-1] + np.log(A[:,s])
        vec1 = vec2 + probs
        T1[s, t] = np.max(vec1)
        idx = np.argmax(vec2)
        T2[s, t] = idx

    bestPathEndState = np.argmax(T1[:, -1])
    maxPathLogProb = T1[idx, -1]
    bestPath = np.zeros((nTimeSteps,))
    bestPath[-1] = bestPathEndState
    tStep = list(range(nTimeSteps-1))
    tStep.reverse()
    for t in tStep:
        bestPath[t] = T2[int(bestPath[t+1]), t+1]

    return bestPath, maxPathLogProb, T1, T2


def compute_BIC(PI, A, B, spikes=None, dt=None, maxLogProb=None, n_time_steps=None):
    if (maxLogProb is None or n_time_steps is None) and (spikes is None or dt is None):
        raise ValueError('Must provide max log prob and n_time_steps or spikes and dt')

    nParams = (A.shape[0]*(A.shape[1]-1) +
               (PI.shape[0]-1) +
               B.shape[0]*(B.shape[1]-1))
    if maxLogProb and n_time_steps:
        pass
    else:
        bestPaths, path_probs = compute_best_paths(spikes, dt, PI, A, B)
        maxLogProb = np.max(path_probs)
        n_time_steps = spikes.shape[-1]

    BIC = -2 * maxLogProb + nParams * np.log(n_time_steps)
    return BIC, bestPaths, maxLogProb


def compute_hmm_cost(spikes, dt, PI, A, B, win_size=0.25, true_rates=None):
    if true_rates is None:
        true_rates = convert_spikes_to_rates(spikes, dt, win_size,
                                             step_size=win_size)

    BIC, bestPaths, maxLogProb = compute_BIC(PI, A, B, spikes=spikes, dt=dt)
    hmm_rates = generate_rate_array_from_state_seq(bestPaths, B, dt, win_size,
                                                   step_size=win_size)
    RMSE = compute_rate_rmse(true_rates, hmm_rates)
    return RMSE, BIC, bestPaths, maxLogProb


def compute_best_paths(spikes, dt, PI, A, B):
    if len(spikes.shape) == 2:
        spikes = np.array([spikes])

    nTrials, nCells, nTimeSteps = spikes.shape
    bestPaths = np.zeros((nTrials, nTimeSteps))-1
    pathProbs = np.zeros((nTrials,))

    for i, trial in enumerate(spikes):
        bestPaths[i,:], pathProbs[i], _, _ = poisson_viterbi(trial, dt, PI,
                                                             A, B)
    return bestPaths, pathProbs


@njit
def compute_rate_rmse(rates1, rates2):
    # Compute RMSE per trial
    # Mean over trials
    n_trials, n_cells, n_steps = rates1.shape
    RMSE = np.zeros((n_trials,))
    for i in range(n_trials):
        t1 = rates1[i, :, :]
        t2 = rates2[i, :, :]
        # Compute RMSE from euclidean distances at each time point
        distances = np.zeros((n_steps,))
        for j in range(n_steps):
            distances[j] =  mt.euclidean(t1[:,j], t2[:,j])

        RMSE[i] = np.sqrt(np.mean(np.power(distances,2)))

    return np.mean(RMSE)


def convert_path_state_numbers(paths, state_map):
    newPaths = np.zeros(paths.shape)
    for k,v in state_map.items():
        idx = np.where(paths == k)
        newPaths[idx] = v

    return newPaths


def match_states(emission1, emission2):
    '''Takes 2 Cell X State firing rate matrices and determines which states
    are most similar. Returns dict mapping emission2 states to emission1 states
    '''
    distances = np.zeros((emission1.shape[1], emission2.shape[1]))
    for x, y in it.product(range(emission1.shape[1]), range(emission2.shape[1])):
        tmp = mt.euclidean(emission1[:, x], emission2[:, y])
        distances[x, y] = tmp

    states = list(range(emission2.shape[1]))
    out = {}
    for i in range(emission2.shape[1]):
        s = np.argmin(distances[:,i])
        r = np.argmin(distances[s, :])
        if r == i and s in states:
            out[i] = s
            idx = np.where(states == s)[0]
            states.pop(int(idx))

    for i in range(emission2.shape[1]):
        if i not in out:
            s = np.argmin(distances[states, i])
            out[i] = states[s]

    return out


@memory.cache
@njit
def convert_spikes_to_rates(spikes, dt, win_size, step_size=None):
    if step_size is None:
        step_size = win_size

    n_trials, n_cells, n_steps = spikes.shape
    n_pts = int(win_size/dt)
    n_step_pts = int(step_size/dt)
    win_starts = np.arange(0, n_steps, n_step_pts)
    out = np.zeros((n_trials, n_cells, len(win_starts)))
    for i, w in enumerate(win_starts):
        out[:, :, i] = np.sum(spikes[:, :, w:w+n_pts], axis=2) / win_size

    return out


@memory.cache
@njit
def generate_rate_array_from_state_seq(bestPaths, B, dt, win_size,
                                       step_size=None):
    if not step_size:
        step_size = win_size

    n_trials, n_steps = bestPaths.shape
    n_cells, n_states = B.shape
    rates = np.zeros((n_trials, n_cells, n_steps))
    for j in range(n_trials):
        seq = bestPaths[j, :].astype(np.int64)
        rates[j, :, :] = B[:, seq]

    n_pts = int(win_size / dt)
    n_step_pts = int(step_size/dt)
    win_starts = np.arange(0, n_steps, n_step_pts)
    mean_rates = np.zeros((n_trials, n_cells, len(win_starts)))
    for i, w in enumerate(win_starts):
        mean_rates[:, :, i] = np.sum(rates[:, : , w:w+n_pts], axis=2) / n_pts

    return mean_rates


@memory.cache
@njit
def rebin_spike_array(spikes, dt, time, new_dt):
    if dt == new_dt:
        return spikes, time

    n_trials, n_cells, n_steps = spikes.shape
    n_bins = int(new_dt/dt)
    new_time = np.arange(time[0], time[-1], n_bins)
    new_spikes = np.zeros((n_trials, n_cells, len(new_time)))
    for i, w in enumerate(new_time):
        idx = np.where((time >= w) & (time < w+new_dt))[0]
        new_spikes[:,:,i] = np.sum(spikes[:,:,idx], axis=-1)

    return new_spikes.astype(np.int32), new_time


@memory.cache
def get_hmm_spike_data(rec_dir, unit_type, channel, time_start=None,
                       time_end=None, dt=None, trials=None, area=None):
    # unit type can be 'single', 'pyramidal', or 'interneuron', or a list of unit names
    if isinstance(unit_type, str):
        units = query_units(rec_dir, unit_type, area=area)
    elif isinstance(unit_type, list):
        units = unit_type

    time, spike_array = h5io.get_spike_data(rec_dir, units, channel, trials=trials)
    spike_array = spike_array.astype(np.int32)
    time = time.astype(np.float64)
    curr_dt = np.unique(np.diff(time))[0] / 1000
    if dt is not None and curr_dt < dt:
        print('%s: Rebinning Spike Array' % os.getpid())
        spike_array, time = rebin_spike_array(spike_array, curr_dt, time, dt)
    elif dt is not None and curr_dt > dt:
        raise ValueError('Cannot upsample spike array from %f ms '
                         'bins to %f ms bins' % (dt, curr_dt))
    else:
        dt = curr_dt

    if time_start is not None and time_end is not None:
        print('%s: Trimming spike array' % os.getpid())
        idx = np.where((time >= time_start) & (time < time_end))[0]
        time = time[idx]
        spike_array = spike_array[:, :, idx]

    return spike_array, dt, time


@memory.cache
def query_units(dat, unit_type, area=None):
    '''Returns the units names of all units in the dataset that match unit_type

    Parameters
    ----------
    dat : blechpy.dataset or str
        Can either be a dataset object or the str path to the recording
        directory containing that data .h5 object
    unit_type : str, {'single', 'pyramidal', 'interneuron', 'all'}
        determines whether to return 'single' units, 'pyramidal' (regular
        spiking single) units, 'interneuron' (fast spiking single) units, or
        'all' units
    area : str
        brain area of cells to return, must match area in
        dataset.electrode_mapping

    Returns
    -------
        list of str : unit_names
    '''
    if isinstance(dat, str):
        units = h5io.get_unit_table(dat)
        el_map = h5io.get_electrode_mapping(dat)
    else:
        units = dat.get_unit_table()
        el_map = dat.electrode_mapping.copy()

    u_str = unit_type.lower()
    q_str = ''
    if u_str == 'single':
        q_str = 'single_unit == True'
    elif u_str == 'pyramidal':
        q_str = 'single_unit == True and regular_spiking == True'
    elif u_str == 'interneuron':
        q_str = 'single_unit == True and fast_spiking == True'
    elif u_str == 'all':
        return units['unit_name'].tolist()
    else:
        raise ValueError('Invalid unit_type %s. Must be '
                         'single, pyramidal, interneuron or all' % u_str)

    units = units.query(q_str)
    if area is None or area == '':
        return units['unit_name'].to_list()

    out = []
    el_map = el_map.set_index('Electrode')
    for i, row in units.iterrows():
        if el_map.loc[row['electrode'], 'area'] == area:
            out.append(row['unit_name'])

    return out




def pick_best_hmm(HMMs):
    '''For each HMM it searches the history for the HMM with lowest BIC Then it
    compares HMMs. Those with same # of free parameters are compared by BIC
    Those with different # of free parameters (namely # of states) are compared
    by cost Best HMM is returned

    Parameters
    ----------
    HMMs : list of PoissonHmm objects

    Returns
    -------
    PoissonHmm
    '''
    # First optimize each HMMs and sort into groups based on # of states
    groups = {}
    for hmm in HMMs:
        hmm.set_to_lowest_BIC()
        if hmm.n_states in groups:
            groups[hmm.n_states].append(hmm)
        else:
            groups[hmm.n_states] = [hmm]

    best_per_state = {}
    for k, v in groups:
        BICs = np.array([x.get_BIC()[0] for x in v])
        idx = np.argmin(BICs)
        best_per_state[k] = v[idx]

    hmm_list = best_per_state.values()
    costs = np.array([x.get_cost() for x in hmm_list])
    idx = np.argmin(costs)
    return hmm_list[idx]


def fit_hmm_mp(rec_dir, params, h5_file=None):
    hmm_id = params['hmm_id']
    n_states = params['n_states']
    dt = params['dt']
    time_start = params['time_start']
    time_end = params['time_end']
    max_iter = params['max_iter']
    threshold = params['threshold']
    unit_type = params['unit_type']
    channel = params['channel']
    n_trials = params['n_trials']
    if 'area' in params.keys():
        area = params['area']
    else:
        area = None

    spikes, dt, time = get_hmm_spike_data(rec_dir, unit_type, channel,
                                          time_start=time_start,
                                          time_end=time_end, dt=dt,
                                          trials=n_trials, area=area)
    hmm = PoissonHMM(n_states, hmm_id=hmm_id)
    success = hmm.fit(spikes, dt, max_iter=max_iter, convergence_thresh=threshold)
    if not success:
        print('%s: Fitting Aborted for hmm %s' % (os.getpid(), hmm_id))
        if h5_file:
            return hmm_id, False
        else:
            return hmm_id, hmm

    hmm = roll_back_hmm_to_best(hmm, spikes, dt, threshold)
    print('%s: Done Fitting for hmm %s' % (os.getpid(), hmm_id))
    written = False
    if h5_file:
        pid = os.getpid()
        lock_file = h5_file + '.lock'
        while os.path.exists(lock_file):
            print('%s: Waiting for file lock' % pid)
            sys_time.sleep(10)

        os.mknod(lock_file)
        try:
            old_hmm, _, old_params = load_hmm_from_hdf5(h5_file, hmm_id)

            if old_hmm is None:
                print('%s: No existing HMM %s. Writing ...' % (pid, hmm_id))
                hmmIO.write_hmm_to_hdf5(h5_file, hmm, time, params)
                written = True
            else:
                if np.isnan(old_hmm.max_log_prob):
                    old_hmm._update_cost(spikes, dt)

                if old_hmm.gamma_probs == []:
                    old_hmm.gamma_probs = old_hmm.get_gamma_probabilities(spikes, dt)

                print('%s: Existing HMM %s found. Comparing BIC ...' % (pid, hmm_id))
                if hmm.max_log_prob > old_hmm.max_log_prob:
                    print('%s: Replacing HMM %s due to higher max log likelihood' % (pid, hmm_id))
                    hmmIO.write_hmm_to_hdf5(h5_file, hmm, time, params)
                    written = True
        except Exception as e:
            os.remove(lock_file)
            raise Exception(e)

        os.remove(lock_file)
        del old_hmm, hmm, spikes, dt, time
        return hmm_id, written
    else:
        return hmm_id, hmm


def load_hmm_from_hdf5(h5_file, hmm_id):
    existing_hmm = hmmIO.read_hmm_from_hdf5(h5_file, hmm_id)
    if existing_hmm is None:
        return None, None, None

    PI, A, B, time, best_paths, params, cost_hist, ll_hist, gamma_probs = existing_hmm
    hmm = PoissonHMM(params['n_states'], PI=PI, A=A, B=B, hmm_id=hmm_id,
                     iteration=params.pop('n_iterations'))
    hmm.BIC = params.pop('BIC')
    hmm.converged = params.pop('converged')
    hmm.fitted = params.pop('fitted')
    hmm.cost = params.pop('cost')
    hmm.best_sequences = best_paths
    hmm.gamma_probs = gamma_probs
    if 'max_log_prob' in params:
        hmm.max_log_prob = params.pop('max_log_prob')
    else:
        hmm.max_log_prob = np.nan

    hmm.cost_hist = cost_hist
    hmm.ll_hist = ll_hist
    return hmm, time, params


class PoissonHMM(object):
    '''Poisson implementation of Hidden Markov Model for fitting spike data
    from a neuronal population
    Author: Roshan Nanu
    Adpated from code by Ben Ballintyn
    '''
    def __init__(self, n_predicted_states, PI=None, A=None, B=None,
                 cost_window=0.25, max_history=1000, hmm_id=None, spikes=None,
                 dt=None, iteration=0):
        self.n_states = n_predicted_states
        self.hmm_id = hmm_id
        self._cost_window = cost_window
        self._max_history = max_history
        self.set_params(PI, A, B, iteration, spikes, dt)
        self.converged = False
        self.fitted = False
        self.cost_hist = []
        self.ll_hist = []
        self.gamma_probs = []

    def set_params(self, PI=None, A=None, B=None, iteration=0, spikes=None, dt=None):
        self.initial_distribution = PI
        self.transition = A
        self.emission = B
        self.iteration = iteration
        self.history = None
        if spikes is None or dt is None:
            self.cost = None
            self.BIC = None
            self.max_log_prob = None
            self.best_sequences = None
        elif PI is not None and A is not None and B is not None:
            spikes = spikes.astype(np.int32)
            self._update_cost(spikes, dt)
        else:
            spikes = spikes.astype(np.int32)
            self.randomize(spikes, dt)
            self._update_cost(spikes, dt)

    def randomize(self, spikes, dt):
        nStates = self.n_states
        n_trials, n_cells, n_steps = spikes.shape
        total_time = n_steps * dt

        # Initialize transition matrix with high stay probability
        print('%s: Randomizing' % os.getpid())
        diag = np.abs(np.random.normal(.99, .01, nStates))
        A = np.abs(np.random.normal(0.01/(nStates-1), 0.01, (nStates, nStates)))
        for i in range(nStates):
            A[i, i] = diag[i]
            A[i,:] = A[i,:] / np.sum(A[i,:])

        # Initialize rate matrix ("Emission" matrix)
        spike_counts = np.sum(spikes, axis=2) / total_time
        mean_rates = np.mean(spike_counts, axis=0)
        std_rates = np.std(spike_counts, axis=0)
        B = np.vstack([np.abs(np.random.normal(x, y, nStates))
                       for x,y in zip(mean_rates, std_rates)])
        # B = np.random.rand(nCells, nStates)

        PI = np.ones((nStates,)) / nStates
        self.set_params(PI=PI, A=A, B=B)
        self.converged = False
        self.fitted = False
        self._update_cost(spikes, dt)

    def fit(self, spikes, dt, max_iter = 1000, convergence_thresh = 1e-5,
            parallel=False):
        '''using parallels for processing trials actually seems to slow down
        processing (with 15 trials). Might still be useful if there is a very
        large nubmer of trials
        '''
        spikes = spikes.astype('int32')
        if (self.initial_distribution is None or
            self.transition is None or
            self.emission is None):
            self.randomize(spikes, dt)

        converged = False
        while (not converged and (self.iteration < max_iter)):
            self.update_history()
            if self.iteration >= 100:
                trend = check_ll_trend(self, convergence_thresh)
                if trend == 'decreasing':
                    return False
                elif trend == 'plateau':
                    converged = True
                    self.fitted = True
                    self.converged = True
                    return True

            self._step(spikes, dt, parallel=parallel)
            # Convergence check is replaced by checking LL trend for plateau
            converged = self.isConverged(convergence_thresh)
            print('%s: %s: Iter #%i complete.' % (os.getpid(), self.hmm_id, self.iteration))

        self.update_history()
        self.fitted = True
        self.converged = converged
        return True

    def _step(self, spikes, dt, parallel=False):
        if len(spikes.shape) == 2:
            spikes = np.expand_dims(spikes, 0)

        nTrials, nCells, nTimeSteps = spikes.shape

        A = self.transition
        B = self.emission
        PI = self.initial_distribution
        nStates = self.n_states

        # For multiple trials need to cmpute gamma and epsilon for every trial
        # and then update
        if parallel:
            n_cores = cpu_count() - 1
        else:
            n_cores = 1

        results = Parallel(n_jobs=n_cores)(delayed(baum_welch)(trial, dt, PI, A, B)
                                           for trial in spikes)
        gammas, epsilons = zip(*results)
        gammas = np.array(gammas)
        epsilons = np.array(epsilons)

        PI, A, B = compute_new_matrices(spikes, dt, gammas, epsilons)
        self.transition = A
        self.emission = B
        self.initial_distribution = PI
        self.gamma_probs = gammas
        self.iteration = self.iteration + 1
        self._update_cost(spikes, dt)

    def update_history(self):
        A = self.transition
        B = self.emission
        PI = self.initial_distribution
        BIC = self.BIC
        cost = self.cost
        iteration = self.iteration
        max_log_prob = self.max_log_prob

        self.cost_hist.append(cost)
        self.ll_hist.append(max_log_prob)
        if self.history is None:
            self.history = {}
            self.history['A'] = [A]
            self.history['B'] = [B]
            self.history['PI'] = [PI]
            self.history['iterations'] = [iteration]
            self.history['cost'] = [cost]
            self.history['BIC'] = [BIC]
            self.history['max_log_prob'] = [max_log_prob]
        else:
            if iteration in self.history['iterations']:
                return self.history

            self.history['A'].append(A)
            self.history['B'].append(B)
            self.history['PI'].append(PI)
            self.history['iterations'].append(iteration)
            self.history['cost'].append(cost)
            self.history['BIC'].append(BIC)
            self.history['max_log_prob'].append(max_log_prob)

        if len(self.history['iterations']) > self._max_history:
            nmax = self._max_history
            for k, v in self.history.items():
                self.history[k] = v[-nmax:]

        return self.history

    def isConverged(self, thresh):
        if self.history is None:
            return False

        idx = np.where(self.history['iterations'] == self.iteration-1)[0]
        if len(idx) == 0:
            return False
        else:
            idx = idx[0]

        oldPI = self.history['PI'][idx]
        oldA = self.history['A'][idx]
        oldB = self.history['B'][idx]
        oldCost = self.history['cost'][idx]

        PI = self.initial_distribution
        A = self.transition
        B = self.emission
        cost = self.cost

        # Instead of Euclidean distance, check that the change of EVERY item is less than threshold

        ##################################################
        # Old Way
        ##################################################
        # dPI = np.sqrt(np.sum(np.power(oldPI - PI, 2)))
        # dA = np.sqrt(np.sum(np.power(oldA - A, 2)))
        # dB = np.sqrt(np.sum(np.power(oldB - B, 2)))
        # dCost = cost-oldCost
        # print('dPI = %f,  dA = %f,  dB = %f, dCost = %f, cost = %f'
        #       % (dPI, dA, dB, dCost, cost))

        # TODO: determine if this is reasonable
        # dB takes waaaaay longer to converge than the rest, i'm going to
        # double the thresh just for that
        # dB = dB/2

        #if not all([x < thresh for x in [dPI, dA, dB]]):
        #    return False
        #else:
        #    return True

        ##################################################
        # New Way
        ##################################################
        dPI = np.abs(oldPI - PI)
        dA = np.abs(oldA - A)
        dB = np.abs(oldB - B)
        delta = np.concatenate((dPI.ravel(), dA.ravel(), dB.ravel()))
        dPI = np.sqrt(np.sum(np.power(dPI,2)))
        dA = np.sqrt(np.sum(np.power(dA,2)))
        dB = np.sqrt(np.sum(np.power(dB,2)))
        dCost = cost-oldCost
        print('dPI = %f,  dA = %f,  dB = %f, dCost = %f, cost = %f'
              % (dPI, dA, dB, dCost, cost))

        if all(delta <= thresh):
            return True
        else:
            return False

    def _update_cost(self, spikes, dt):
        spikes = spikes.astype('int32')
        win_size = self._cost_window
        PI = self.initial_distribution
        A  = self.transition
        B  = self.emission
        cost, BIC, bestPaths, maxLogProb = compute_hmm_cost(spikes, dt, PI, A, B,
                                                            win_size=win_size)
        self.cost = cost
        self.BIC = BIC
        self.best_sequences = bestPaths
        self.max_log_prob = maxLogProb

    def get_best_paths(self, spikes, dt):
        if self.best_sequences is not None:
            return self.best_sequences, self.max_log_prob

        PI = self.initial_distribution
        A = self.transition
        B = self.emission

        bestPaths, pathProbs = compute_best_paths(spikes, dt, PI, A, B)
        self.best_sequences = bestPaths
        self.max_log_prob = np.max(pathProbs)
        return bestPaths, self.max_log_prob

    def get_forward_probabilities(self, spikes, dt, parallel=False):
        PI = self.initial_distribution
        A = self.transition
        B = self.emission
        if parallel:
            n_cpu = cpu_count() -1
            a_results = Parallel(n_jobs=n_cpu, verbose=20)(delayed(forward)
                                                           (trial, dt, PI, A, B)
                                                           for trial in spikes)
            alphas, norms = zip(*a_results)
        else:
            n_cpu = 1
            alphas = []
            norms = []
            for trial in spikes:
                tmp_alpha, tmp_norms = forward(trial, dt, PI, A, B)
                alphas.append(tmp_alpha)
                norms.append(tmp_norms)

        return np.array(alphas)

    def get_backward_probabilities(self, spikes, dt, parallel=False):
        PI = self.initial_distribution
        A = self.transition
        B = self.emission
        betas = []
        if parallel:
            n_cpu = cpu_count() -1
        else:
            n_cpu = 1

        a_results = Parallel(n_jobs=n_cpu)(delayed(forward)(trial, dt, PI, A, B)
                                         for trial in spikes)
        _, norms = zip(*a_results)
        b_results = Parallel(n_jobs=n_cpu)(delayed(backward)(trial, dt, A, B, n)
                                           for trial, n in zip(spikes, norms))
        betas = np.array(b_results)

        return betas

    def get_gamma_probabilities(self, spikes, dt, parallel=False):
        PI = self.initial_distribution
        A = self.transition
        B = self.emission
        if parallel:
            n_cpu = cpu_count()-1
        else:
            n_cpu = 1

        results = Parallel(n_jobs=n_cpu)(delayed(baum_welch)(trial, dt, PI, A, B)
                                         for trial in spikes)
        gammas, _ = zip(*results)
        return np.array(gammas)

    def set_to_lowest_cost(self):
        hist = self.history
        idx = np.argmin(hist['cost'])
        iteration = hist['iterations'][idx]
        self.roll_back(iteration)

    def set_to_lowest_BIC(self):
        hist = self.history
        idx = np.argmin(hist['BIC'])
        iteration = hist['iterations'][idx]
        self.roll_back(iteration)

    def set_to_highest_likelihood(self, exclude=50):
        '''Rolls back the HMM to the iteration with the highest log likelihood,
        excluding the first N trials
        '''
        hist = self.history
        idx = np.argmax(self.ll_hist)
        iteration = hist['iterations'][idx]
        self.roll_back(iteration)

    def find_best_in_history(self):
        hist = self.history
        PIs = hist['PI']
        As = hist['A']
        Bs = hist['B']
        iters = hist['iterations']
        BICs = hist['BIC']
        idx = np.argmin(BICs)
        out = {'PI': PIs[idx], 'A': As[idx], 'B': Bs[idx]}
        return out, iters[idx], BICs

    def roll_back(self, iteration):
        hist = self.history
        try:
            idx = hist['iterations'].index(iteration)
        except ValueError:
            raise ValueError('Iteration %i not found in history' % iteration)

        dat = {k:v[idx] for k,v in hist.items()}
        self.set_params(PI=dat['PI'], A=dat['A'], B=dat['B'],
                        iteration=iteration)
        self.BIC = dat['BIC']
        self.cost = dat['cost']
        self.max_log_prob = dat['max_log_prob']


class HmmHandler(object):
    def __init__(self, dat, params=None, save_dir=None):
        '''Takes a blechpy dataset object and fits HMMs for each tastant

        Parameters
        ----------
        dat: blechpy.dataset
        params: dict or list of dicts
            each dict must have fields:
                time_window: list of int, time window to cut around stimuli in ms
                convergence_thresh: float
                max_iter: int
                n_repeats: int
                unit_type: str, {'single', 'pyramidal', 'interneuron', 'all'}
                bin_size: time bin for spike array when fitting in seconds
                n_states: predicted number of states to fit
        '''
        if isinstance(params, dict):
            params = [params]

        if isinstance(dat, str):
            fd = dat
            dat = load_dataset(dat)
            if os.path.realpath(fd) != os.path.realpath(dat.root_dir):
                print('Changing dataset root_dir to match local directory')
                dat._change_root(fd)

            if dat is None:
                raise FileNotFoundError('No dataset.p file found given directory')

        if save_dir is None:
            save_dir = os.path.join(dat.root_dir,
                                    '%s_analysis' % dat.data_name)

        self._dataset = dat
        self.root_dir = dat.root_dir
        self.save_dir = save_dir
        self.h5_file = os.path.join(save_dir, '%s_HMM_Analysis.hdf5' % dat.data_name)
        dim = dat.dig_in_mapping.query('exclude==False')
        tastes = dim['name'].tolist()
        self._orig_params = params
        self.load_params()
        if params is not None:
            self.add_params(params)

        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)

        self.plot_dir = os.path.join(save_dir, 'HMM_Plots')
        if not os.path.isdir(self.plot_dir):
            os.makedirs(self.plot_dir)

        hmmIO.setup_hmm_hdf5(self.h5_file)
        # this function can be edited to account for parameters added in the
        # future
        hmmIO.fix_hmm_overview(self.h5_file)

    def load_params(self):
        self._data_params = []
        self._fit_params = []
        h5_file = self.h5_file
        if not os.path.isfile(h5_file):
            return

        with tables.open_file(h5_file, 'r') as hf5:
            if 'data_overview' not in hf5.root:
                return

            table = hf5.root.data_overview
            col_names = table.colnames
            for row in table[:]:
                p = {}
                for k in col_names:
                    if table.coltypes[k] == 'string':
                        p[k] = row[k].decode('utf-8')
                    else:
                        p[k] = row[k]

                _ = p.pop('BIC')
                _ = p.pop('cost')
                _ = p.pop('n_iterations')
                _ = p.pop('converged')
                if 'max_log_prob' in p:
                    _ = p.pop('max_log_prob')

                self.add_params(p)

    def get_parameter_overview(self):
        df = pd.DataFrame(self._data_params)
        return df

    def get_data_overview(self):
        with tables.open_file(self.h5_file, 'r') as hf5:
            table = hf5.root.data_overview
            df = pd.DataFrame(table[:])
            df['unit_type'] = df['unit_type'].apply(lambda x: x.decode('utf-8'))
            df['taste'] = df['taste'].apply(lambda x: x.decode('utf-8'))
            df['area'] = df['area'].apply(lambda x: x.decode('utf-8'))

        return df

    def run(self, parallel=True, overwrite=False):
        h5_file = self.h5_file
        rec_dir = self._dataset.root_dir
        if overwrite:
            fit_params = self._fit_params
        else:
            fit_params = [x for x in self._fit_params if not x['fitted']]

        if len(fit_params) == 0:
            return

        print('Running fittings')
        if parallel:
            n_cpu = np.min((cpu_count()-1, len(fit_params)))
        else:
            n_cpu = 1

        results = Parallel(n_jobs=n_cpu, verbose=100)(delayed(fit_hmm_mp)
                                                     (rec_dir, p, h5_file)
                                                     for p in fit_params)


        memory.clear(warn=False)
        print('='*80)
        print('Fitting Complete')
        print('='*80)
        print('HMMs written to hdf5:')
        for hmm_id, written in results:
            print('%s : %s' % (hmm_id, written))

        self.plot_saved_models()
        self.load_params()

    def plot_saved_models(self):
        print('Plotting saved models')
        data = self.get_data_overview().set_index('hmm_id')
        rec_dir = self._dataset.root_dir
        for i, row in data.iterrows():
            hmm, _, params = load_hmm_from_hdf5(self.h5_file, i)
            spikes, dt, time = get_hmm_spike_data(rec_dir, params['unit_type'],
                                                  params['channel'],
                                                  time_start=params['time_start'],
                                                  time_end=params['time_end'],
                                                  dt=params['dt'],
                                                  trials=params['n_trials'],
                                                  area=params['area'])
            plot_dir = os.path.join(self.plot_dir, 'hmm_%s' % i)
            if not os.path.isdir(plot_dir):
                os.makedirs(plot_dir)

            print('Plotting HMM %s...' % i)
            hmmplt.plot_hmm_figures(hmm, spikes, dt, time, save_dir=plot_dir)

    def add_params(self, params):
        if isinstance(params, list):
            for p in params:
                self.add_params(p)

            return
        elif not isinstance(params, dict):
            raise ValueError('Input must  be a dict or list or dicts')

        # Fill in blanks with defaults
        for k, v in HMM_PARAMS.items():
            if k not in params:
                params[k] = v
                print('Parameter %s not provided. Using default value: %s'
                      % (k, repr(v)))

        # Grab existing parameters
        data_params = self._data_params
        fit_params = self._fit_params

        # Get taste and trial info from dataset
        dat = self._dataset
        dim = dat.dig_in_mapping.query('exclude == False and spike_array == True')
        if params['taste'] is None:
            tastes = dim['name'].tolist()
        else:
            tastes = [params['taste']]

        dim = dim.set_index('name')
        if not hasattr(dat, 'dig_in_trials'):
            dat.create_trial_list()

        trials = dat.dig_in_trials
        hmm_ids = [x['hmm_id'] for x in data_params]
        for t in tastes:
            p = params.copy()

            p['taste'] = t
            # Skip if parameter is already in parameter set
            if any([hmmIO.compare_hmm_params(p, dp) for dp in data_params]):
                print('Parameter set already in data_params, '
                      'to re-fit run with overwrite=True')
                continue

            if t not in dim.index:
                print('Taste %s not found in dig_in_mapping or marked to exclude. Skipping...' % t)
                continue

            if p['hmm_id'] is None:
                hid = get_new_id(hmm_ids)
                p['hmm_id'] = hid
                hmm_ids.append(hid)

            p['channel'] = dim.loc[t, 'channel']
            unit_names = query_units(dat, p['unit_type'], area=p['area'])
            p['n_cells'] = len(unit_names)
            if p['n_trials'] is None:
                p['n_trials'] = len(trials.query('name == @t'))

            data_params.append(p)
            for i in range(p['n_repeats']):
                fit_params.append(p.copy())

        self._data_params = data_params
        self._fit_params = fit_params

    def get_hmm(self, hmm_id):
        return load_hmm_from_hdf5(self.h5_file, hmm_id)

    def delete_hmm(self, **kwargs):
        '''Deletes any HMMs whose parameters match the kwargs. i.e. n_states=2,
        taste="Saccharin" would delete all 2-state HMMs for Saccharin trials
        also reload parameters from hdf5, so any added but un-fit params will
        be lost
        '''
        hmmIO.delete_hmm_from_hdf5(self.h5_file, **kwargs)
        self.load_params()


def get_hmm_overview_from_hdf5(h5_file):
    with tables.open_file(h5_file, 'r') as hf5:
        table = hf5.root.data_overview
        df = pd.DataFrame(table[:])
        df['unit_type'] = df['unit_type'].apply(lambda x: x.decode('utf-8'))
        df['taste'] = df['taste'].apply(lambda x: x.decode('utf-8'))

    return df


def isConverged(hmm, thresh):
    '''Check HMM convergence based on the log-likelihood
    '''
    pass

def check_ll_trend(hmm, thresh, n_iter=None):
    '''Check the trend of the log-likelihood to see if it has plateaued, is
    decreasing or is increasing
    '''
    if n_iter is None:
        n_iter = hmm.iteration

    ll_hist = hmm.ll_hist
    if n_iter == len(ll_hist):
        n_iter = n_iter-1

    filt_ll = gaussian_filter1d(ll_hist, 4)
    diff_ll = np.diff(filt_ll)

    # Linear fit, if overall trend is decreasing, it fails
    z = np.polyfit(range(len(ll_hist)), filt_ll, 1)
    if z[0] <= 0:
        return 'decreasing'

    # Check if it has plateaued
    if all(np.abs(diff_ll[n_iter-5:n_iter]) <= thresh):
        return 'plateau'

    # if its a maxima and hasn't plateaued it needs to continue fitting
    if np.max(filt_ll) == filt_ll[n_iter]:
        return 'increasing'

    return 'flux'

def roll_back_hmm_to_best(hmm, spikes, dt, thresh):
    '''Looks at the log likelihood over fitting and determines the best
    iteration to have stopped at by choosing a local maxima during a period
    where the smoothed LL trace has plateaued
    '''
    ll_hist = np.array(hmm.ll_hist)
    filt_ll = gaussian_filter1d(ll_hist, 4)
    diff_ll = np.diff(filt_ll)
    iterations = np.array(hmm.history['iterations'])
    below = np.where(np.abs(diff_ll) < thresh)[0] + 1 # since diff_ll is 1 smaller than ll_hist
    # Exclude maxima less than 50 iterations since its pretty spikey early on
    below = [x for x in below if (x in iterations and x > 50)]
    # If there are none that fit criteria, just pick best past 50
    if len(below) == 0:
        below = iterations[iterations > 50]

    tmp = [x for x in below if check_ll_trend(hmm, thresh, x) == 'plateau']
    if len(tmp) != 0:
        below = tmp

    maxima = np.argmax(ll_hist[below]) # this gives the index in below
    maxima = below[maxima] # this is the iteration at which the maxima occurred
    hmm.roll_back(maxima)
    hmm._update_cost(spikes, dt)
    hmm.gamma_probs = hmm.get_gamma_probabilities(spikes, dt)
    return hmm


def get_new_id(ids=None):
    if ids is None or len(ids) == 0:
        return 0

    nums = np.arange(0, np.max(ids) + 2)
    diff_nums = [x for x in nums if x not in ids]
    return np.min(diff_nums)
