from src.utils import load_data
from collections import defaultdict
from src.utils import constants as c


def load_profiles(gold_standard_file, profiles_files, no_normalization):
    normalize = False if no_normalization else True

    gs_samples_list = load_data.open_profile(gold_standard_file, normalize)
    sample_ids_list = []
    for sample in gs_samples_list:
        sample_id, sample_metadata, profile = sample
        sample_ids_list.append(sample_id)

    profiles_list_to_samples_list = []
    for profile_file in profiles_files:
        profiles_list_to_samples_list.append(load_data.open_profile(profile_file, normalize))

    return sample_ids_list, gs_samples_list, profiles_list_to_samples_list


gold_standard_file = '/home/fmeyer/projects/tutorial/profiles/cami2_mouse_gut_gs.profile'
profiles_files = '/home/fmeyer/projects/tutorial/profiles/cami2_mouse_gut_metaphlan2.2.0.profile,' \
                 '/home/fmeyer/projects/tutorial/profiles/cami2_mouse_gut_metaphlan2.9.21.profile,' \
                 '/home/fmeyer/projects/tutorial/profiles/cami2_mouse_gut_motus1.1.profile,' \
                 '/home/fmeyer/projects/tutorial/profiles/cami2_mouse_gut_motus2.5.1.profile,' \
                 '/home/fmeyer/projects/tutorial/profiles/cami2_mouse_gut_bracken2.5.profile,' \
                 '/home/fmeyer/projects/tutorial/profiles/cami2_mouse_gut_metapalette1.0.0.profile,' \
                 '/home/fmeyer/projects/tutorial/profiles/cami2_mouse_gut_metaphyler1.25.profile,' \
                 '/home/fmeyer/projects/tutorial/profiles/cami2_mouse_gut_focus0.31.profile,' \
                 '/home/fmeyer/projects/tutorial/profiles/cami2_mouse_gut_tipp2.0.0.profile,' \
                 '/home/fmeyer/projects/tutorial/profiles/cami2_mouse_gut_camiarkquikr1.0.0.profile'.split(',')
labels = 'MetaPhlAn 2.2.0,MetaPhlAn 2.9.21,mOTUs 1.1,mOTUs 2.5.1,Bracken 2.5,MetaPalette 1.0.0,MetaPhyler 1.25,FOCUS 0.31,TIPP 2.0.0,CAMIARKQuikr 1.0.0'.split(',')

sample_ids_list, gs_samples_list, profiles_list_to_samples_list = load_profiles(gold_standard_file,
                                                                                profiles_files,
                                                                                True)
# print(len(sample_ids_list))
# exit()

for samples_list, label in zip(profiles_list_to_samples_list, labels):
    print(label, len(samples_list))
    rank_sumpercentage = defaultdict(int)
    for sample in samples_list:
        sample_id, sample_metadata, profile = sample
        for prediction in profile:
            rank_sumpercentage[prediction.rank] += prediction.percentage

    for rank in c.ALL_RANKS[:-1]:
        # print(rank, rank_sumpercentage[rank])
        print(rank, rank_sumpercentage[rank] / len(samples_list))
        # print()
    print()