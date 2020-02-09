# Try to put all the assumptions in this file
def CreateParametersDictionary():
    params = {}
    params['logfilename'] = 'eventlog.txt'
    params['room_cluster_count'] = 3
    params['room_per_cluster_count'] = 30
    params['prob_new_room_for_married'] = 0.5
    params['prob_new_single_male'] = 0.3
    params['max_age_male_resident'] = 365 * 90
    params['max_age_female_resident'] = 365 * 95
    params['mean_age_new_resident'] = 365 * 72
    params['sd_age_new_resident'] = 365 * 7
    params['max_days_room_empty'] = 90
    
    # std param
    # fraction of the population defined as high risk
    params['HR'] = 0.1
    params['LR'] = 0.9
    params['std_probability'] = 0.5

    # casual partners
    params['std_65_79_HR'] = ['beta', 3, 60 ]
    params['std_80_95_HR'] = ['beta', 3, 4000]
    params['std_65_79_LR'] = ['beta', 1, 160]
    params['std_80_95_LR'] = ['beta', 1, 160]

    # among paired
    params['std_65_79_HR'] = ['beta', 10, 70]
    params['std_80_95_HR'] = ['beta', 10, 100]
    
    # testing of the symptomatic, all using Beta distribution
    # formula 1/(52 * (0.079 + 0.072 * Beta(4,4)))
    params['woman_test_symptomatic'] = [52, 0.079, 0.072, 'beta', 4, 4] 
    params['man_test_symptomatic'] = [52, 0.079, 0.072, 'beta', 4, 4]

    # natural recovery
    # formula 1/(52*(1.13 + 0.5* Beta(4,4.496)))
    params['woman_nr'] = [51, 1.13, 0.5, 'beta', 4, 4.969]
    params['man_nr'] = [51, 1.13, 0.5, 'beta', 4, 4.969]

    return params
