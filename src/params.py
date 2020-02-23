# Try to put all the assumptions in this file
def CreateParametersDictionary():
    params = {}
    params['logfilename'] = 'simulationDetail.txt'
    params['csvfilename'] = 'output.csv'
    params['room_cluster_count'] = 3
    params['room_per_cluster_count'] = 30
    params['prob_new_room_for_married'] = 0.5
    params['prob_new_single_male'] = 0.3
    params['max_age_male_resident'] = 365 * 90
    params['max_age_female_resident'] = 365 * 95
    params['mean_age_new_resident'] = 365 * 72
    params['sd_age_new_resident'] = 365 * 7
    params['max_days_room_empty'] = 90
    params['simulation_repetition'] = 10

    # std param
    # fraction of the population defined as high risk, we could easily use only high risk (HR) probability, then low risk (LR) is just 1 - HR
    params['HR'] = 0.1
    params['LR'] = 0.9
    params['std_probability'] = [0.5]
    params['std_with_condom'] = ['beta', 5.5, 50, 1.6]
    params['std_without_condom'] = ['beta', 5.5, 50]

    # casual partners
    params['casual_std_65_79_HR'] = ['beta', 3, 60 ]
    params['casual_std_80_95_HR'] = ['beta', 3, 4000]
    params['casual_std_65_79_LR'] = ['beta', 1, 160]
    params['casual_std_80_95_LR'] = ['beta', 1, 160]

    # among paired
    params['paired_std_65_79_HR'] = ['beta', 10, 70]
    params['paired_std_80_95_LR'] = ['beta', 10, 100]
    
    # testing of the symptomatic, all using Beta distribution
    # formula 1/(52 * (0.079 + 0.072 * Beta(4,4)))
    params['woman_test_symptomatic'] = [52, 0.079, 0.072, 'beta', 4, 4] 
    params['man_test_symptomatic'] = [52, 0.079, 0.072, 'beta', 4, 4]

    # treatment choice
    # natural or antibiotics
    params['choice_of_treatment'] = 'natural recovery'
    
    # intervention:
    params['use_condom'] = 'no'
    params['notify_partner'] = 'no'
    
    # natural recovery
    # formula 1/(52*(1.13 + 0.5* Beta(4,4.496)))
    params['woman_nr'] = [52, 1.13, 0.5, 'beta', 4, 4.969]
    params['man_nr'] = [52, 1.13, 0.5, 'beta', 4, 4.969]

    # treatment success
    params['antibiotics'] = ['beta', 190, 8]

    # intervention 1 - partner notification, this happen when patients notify their partners
    params['notification'] = ['beta', 4, 3]

    # intervention 2 - condom usage how likely resident use condom
    params['condom_casual_partner'] = 0.131
    params['condom_paired_partner'] = 0.368

    return params
