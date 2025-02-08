def suff_stats(h, m, epsilon):
    C = D = Th = Tm = Thm = 0
    n = len(h)
    for hi, mi in zip(h, m):
        if hi == 0 and abs(mi) <= epsilon:
            Thm += 1
        elif hi == 0:
            Th += 1
        elif abs(mi) <= epsilon:
            Tm += 1
        elif hi * mi > 0:
            C += 1
        else:
            D += 1
    return C, D, Th, Tm, Thm

def calc_tau(C, D, Th, Tm, Thm):
    # This function calculates the current tau value based on the statistics
    # You can define your own logic here based on how tau is calculated in your context
    return (C + Thm) / (C + D + Th + Tm + Thm)

def calc_accuracy_with_ties(h, m):
    """
    algorithm: https://arxiv.org/abs/2305.14324
    O(N^2logN)
    Input:
        h: list of N human labels, 1 for preferred, -1 for not preferred, 0 for ties
        m: list of N model scores(scores_A - scores_B)
    Output:
        tau_star: accuracy-with-ties
    """
    try:
        C, D, Th, Tm, Thm = suff_stats(h, m, -1)
        
        sorted_pairs = sorted(zip(h, m), key=lambda x: abs(x[1]))
        
        tau_star = float('-inf')
        epsilon_star = 0
        epsilon_curr = -1

        current_thresholds = {
            'C': C, 'D': D, 'Th': Th, 'Tm': Tm, 'Thm': Thm
        }
        # print(current_thresholds)
        for hi, mi in sorted_pairs:
            # update the statistics by removing the current pair
            if hi == 0 and abs(mi) < epsilon_curr:
                current_thresholds['Thm'] -= 1
            elif hi == 0:
                current_thresholds['Th'] -= 1
            elif abs(mi) < epsilon_curr:
                current_thresholds['Tm'] -= 1
            elif hi * mi > 0:
                current_thresholds['C'] -= 1
            else:
                current_thresholds['D'] -= 1

            # update the epsilon value
            epsilon_curr = abs(mi)

            # update the statistics by adding the current pair
            if hi == 0 and abs(mi) <= epsilon_curr:
                current_thresholds['Thm'] += 1
            elif hi == 0:
                current_thresholds['Th'] += 1
            elif abs(mi) <= epsilon_curr:
                current_thresholds['Tm'] += 1
            elif hi * mi > 0:
                current_thresholds['C'] += 1
            else:
                current_thresholds['D'] += 1

            # calculate the new tau value
            tau_curr = calc_tau(**current_thresholds)

            if tau_curr > tau_star:
                tau_star = tau_curr
                epsilon_star = epsilon_curr
            # print(current_thresholds)
        # print("epsilon_star:", epsilon_star)
        return tau_star
    except Exception as e:
        print("Error in tie_calibration:", e)
        return 0
    

def calc_accuracy_without_ties(h, m):
    C, D, Th, Tm, Thm = suff_stats(h, m, -1)
    return C / (C + D)
