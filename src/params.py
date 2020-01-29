def CreateParametersDictionary():
    params = {}
    params['logfilename'] = 'eventlog.txt'
    params['room_cluster_count'] = 3
    params['room_per_cluster_count'] = 50
    params['prob_new_room_for_married'] = 0.5
    params['prob_new_single_male'] = 0.3
    params['max_age_male_resident'] = 365 * 90
    params['max_age_female_resident'] = 365 * 95
    return params
