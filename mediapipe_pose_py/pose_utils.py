from im_geometry import getAngle, getSlope

def get_face(pl_list):
    
    face_dict = {
                    'l_eye': (int(pl_list[2]['x']),  int(pl_list[2]['y'])),
                    'r_eye': (int(pl_list[5]['x']),  int(pl_list[5]['y'])),
                    'nose': (int(pl_list[0]['x']),  int(pl_list[0]['y'])),
                    'l_ear': (int(pl_list[7]['x']),  int(pl_list[7]['y'])),
                    'r_ear': (int(pl_list[8]['x']),  int(pl_list[8]['y'])),
                    'l_mouth': (int(pl_list[9]['x']),  int(pl_list[9]['y'])),
                    'r_mouth': (int(pl_list[10]['x']),  int(pl_list[10]['y']))
                }
    
    return face_dict
    
def get_left_arm(pl_list):
    
    lsh_slope = getSlope(pl_list[11]['x'], pl_list[11]['y'], pl_list[23]['x'], pl_list[23]['y'])
    lse_slope = getSlope(pl_list[11]['x'], pl_list[11]['y'], pl_list[13]['x'], pl_list[13]['y'])
    lew_slope = getSlope(pl_list[13]['x'], pl_list[13]['y'], pl_list[15]['x'], pl_list[15]['y'])
    
    hs_se_angle = getAngle(lsh_slope, lse_slope)
    se_ew_angle = getAngle(lse_slope, lew_slope)
    
    hssea = int(hs_se_angle)
    seewa = 180 - int(se_ew_angle)
    
    l_arm_dict = {'shoulder': (int(pl_list[11]['x']),  int(pl_list[11]['y'])),
                    'elbow': (int(pl_list[13]['x']), int(pl_list[13]['y'])),
                    'wrist': (int(pl_list[15]['x']), int(pl_list[15]['y'])),
                    'index': (int(pl_list[19]['x']), int(pl_list[19]['y'])),
                    'arm_body_angle': hssea,
                    'elbow_angle': seewa}
    
    return l_arm_dict
    
def get_left_leg(pl_list):
    
    lhk_slope = getSlope(pl_list[23]['x'], pl_list[23]['y'], pl_list[25]['x'], pl_list[25]['y'])
    lka_slope = getSlope(pl_list[25]['x'], pl_list[25]['y'], pl_list[27]['x'], pl_list[27]['y'])
    
    hk_ka_angle = getAngle(lhk_slope, lka_slope)
    
    hkkaa = int(hk_ka_angle)
    
    l_leg_dict = {'hip': (int(pl_list[23]['x']),  int(pl_list[23]['y'])),
                    'knee': (int(pl_list[25]['x']), int(pl_list[25]['y'])),
                    'ankle': (int(pl_list[27]['x']), int(pl_list[27]['y'])),
                    'heel': (int(pl_list[29]['x']), int(pl_list[29]['y'])),
                    'toes': (int(pl_list[31]['x']), int(pl_list[31]['y'])),
                    'knee_angle': hkkaa}
    
    return l_leg_dict
    
def get_right_arm(pl_list):
    
    rsh_slope = getSlope(pl_list[12]['x'], pl_list[12]['y'], pl_list[24]['x'], pl_list[24]['y'])
    rse_slope = getSlope(pl_list[12]['x'], pl_list[12]['y'], pl_list[14]['x'], pl_list[14]['y'])
    rew_slope = getSlope(pl_list[14]['x'], pl_list[14]['y'], pl_list[16]['x'], pl_list[16]['y'])
    
    hs_se_angle = getAngle(rsh_slope, rse_slope)
    se_ew_angle = getAngle(rse_slope, rew_slope)
    
    hssea = 180 - int(hs_se_angle)
    seewa = int(se_ew_angle)
    
    r_arm_dict = {'shoulder': (int(pl_list[12]['x']),  int(pl_list[12]['y'])),
                    'elbow': (int(pl_list[14]['x']), int(pl_list[14]['y'])),
                    'wrist': (int(pl_list[16]['x']), int(pl_list[16]['y'])),
                    'index': (int(pl_list[20]['x']), int(pl_list[20]['y'])),
                    'arm_body_angle': hssea,
                    'elbow_angle': seewa}
    
    return r_arm_dict
    
def get_right_leg(pl_list):
    
    rhk_slope = getSlope(pl_list[24]['x'], pl_list[24]['y'], pl_list[26]['x'], pl_list[26]['y'])
    rka_slope = getSlope(pl_list[26]['x'], pl_list[26]['y'], pl_list[28]['x'], pl_list[28]['y'])
    
    hk_ka_angle = getAngle(rhk_slope, rka_slope)
    
    hkkaa = 180 - int(hk_ka_angle)
    
    r_leg_dict = {'hip': (int(pl_list[24]['x']),  int(pl_list[24]['y'])),
                    'knee': (int(pl_list[26]['x']), int(pl_list[26]['y'])),
                    'ankle': (int(pl_list[28]['x']), int(pl_list[28]['y'])),
                    'heel': (int(pl_list[30]['x']), int(pl_list[30]['y'])),
                    'toes': (int(pl_list[32]['x']), int(pl_list[32]['y'])),
                    'knee_angle': hkkaa}
    
    return r_leg_dict