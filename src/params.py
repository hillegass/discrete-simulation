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
    params['std_probabability'] = 0.5
    params['mean_age_new_resident'] = 365 * 72
    params['sd_age_new_resident'] = 365 * 7
    params['max_days_room_empty'] = 90
    return params
