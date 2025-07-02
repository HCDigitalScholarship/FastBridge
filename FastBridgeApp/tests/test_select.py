"""Auto-generated test file with absolute imports"""
import os, sys
from fastapi.testclient import TestClient

# Add project root to sys.path in order to import main
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from main import app

client = TestClient(app)


def test_select_simple_claudian_in_eutropium_preface_to_book_2():
    response = client.get("/select/Latin/result/claudian_in_eutropium_preface_to_book_2/2.70-2.72/non_running/")
    assert response.status_code == 200

def test_select_full_pliny_the_younger_panegyricu():
    response = client.get("/select/Latin/result/pliny_the_younger_panegyricu/95.4-95.5/include/augustus_res_gestae_1/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_oxford_latin_course_for_college():
    response = client.get("/select/Latin/result/oxford_latin_course_for_college/24-25/non_running/")
    assert response.status_code == 200

def test_select_full_owen_epigrams():
    response = client.get("/select/Latin/result/owen_epigrams/4.187.3-9.30.2/include/vergil_aeneid_new_ap_selections/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_horace_carmen_saeculare():
    response = client.get("/select/Latin/result/horace_carmen_saeculare/54-75/non_running/")
    assert response.status_code == 200

def test_select_full_lhomond_de_viris_illustribus_1_18_exordium_to_coriolanus():
    response = client.get("/select/Latin/result/lhomond_de_viris_illustribus_1-18_exordium_to_coriolanus/1.1-2.2/include/seneca_ad_helviam_matrem_de_consolatione/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_cicero_de_lege_agraria():
    response = client.get("/select/Latin/result/cicero_de_lege_agraria/57.11-99.14/include/seneca_apocolocyntosis/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_gsce_rvl():
    response = client.get("/select/Latin/result/gsce_rvl/47-107/non_running/")
    assert response.status_code == 200

def test_select_simple_elizabeth_jane_weston_addenda_ad_parthenica():
    response = client.get("/select/Latin/result/elizabeth_jane_weston_addenda_ad_parthenica/1.1.17-1.1.23/non_running/")
    assert response.status_code == 200

def test_select_full_eutropius_breviarium_book_3_beyer():
    response = client.get("/select/Latin/result/eutropius_breviarium_book_3_beyer/3.20-3.21/include/stabat_mater/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_groton_from_alpha_to_omega():
    response = client.get("/select/Greek/result/groton_from_alpha_to_omega/start-end/include/aesop_fables/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_elizabeth_jane_weston_ad_schosserum():
    response = client.get("/select/Latin/result/elizabeth_jane_weston_ad_schosserum/7.7-7.9/include/caesar_bellum_gallicum/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_claudian_in_eutropium_preface_to_book_2():
    response = client.get("/select/Latin/result/claudian_in_eutropium_preface_to_book_2/2.70-2.72/include/florus_epitome_11_romulus_and_roman_kings/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_hildegard_of_bingen_scivias_72():
    response = client.get("/select/Latin/result/hildegard_of_bingen_scivias_72/7.3-7.4/non_running/")
    assert response.status_code == 200

def test_select_full_concat_aesop_fables_demonsthenes_against_neaira():
    response = client.get("/select/Greek/result/aesop_fables+demonsthenes_against_neaira/start+start-end+end/include/dcc_greek_core_list/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_eutropius_breviarium_book_1_beyer():
    response = client.get("/select/Latin/result/eutropius_breviarium_book_1_beyer/7-19/include/ovid_halieutica/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_apuleius_asclepius():
    response = client.get("/select/Latin/result/apuleius_asclepius/6.16-41.2/include/claudian_de_raptu_prosperinae_prefaces/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_claudian_panegyricus_de_iii_consulatu_honorii_augusti():
    response = client.get("/select/Latin/result/claudian_panegyricus_de_iii_consulatu_honorii_augusti/453-521/non_running/")
    assert response.status_code == 200

def test_select_full_catullus_carmina_garrison():
    response = client.get("/select/Latin/result/catullus_carmina_garrison/61.44-66.4/include/physiologus_latina_1-6_9_16_17_23/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_epitaph_of_allia_potestas_cil_637966():
    response = client.get("/select/Latin/result/epitaph_of_allia_potestas_cil_637966/12-34/non_running/")
    assert response.status_code == 200

def test_select_full_concat_ovid_in_ibin_seneca_phaedra():
    response = client.get("/select/Latin/result/ovid_in_ibin+seneca_phaedra/187+169-451+534/include/cicero_de_lege_agraria/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_diederich_frequency_list_general():
    response = client.get("/select/Latin/result/diederich_frequency_list_general/1342-1502/include/eduqas/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_cicero_pro_murena():
    response = client.get("/select/Latin/result/cicero_pro_murena/20.8-61.10/non_running/")
    assert response.status_code == 200

def test_select_full_horace_carmen_saeculare():
    response = client.get("/select/Latin/result/horace_carmen_saeculare/54-75/include/cambridge_latin_course/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_anthologia_latina_507_518_epitaphs_of_vergil():
    response = client.get("/select/Latin/result/anthologia_latina_507-518_epitaphs_of_vergil/509-510/include/vergil_aeneid_ap_selections/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_tacitus_historiae():
    response = client.get("/select/Latin/result/tacitus_historiae/3.18.6-4.22.8/include/elizabeth_jane_weston_de_ebrietate/start-end/non_running/")
    assert response.status_code == 200

def test_select_concat_cicero_in_verrem_actio_prima_claudian_de_raptu_prosperinae():
    response = client.get("/select/Latin/result/cicero_in_verrem_actio_prima+claudian_de_raptu_prosperinae/16.7+1.5-41.6+2.228/non_running/")
    assert response.status_code == 200

def test_select_full_seneca_de_otio():
    response = client.get("/select/Latin/result/seneca_de_otio/3.1-5.4/include/plautus_amphitruo/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_latin_for_the_new_millennium_vols_1_and_2_tunberg_minkova():
    response = client.get("/select/Latin/result/latin_for_the_new_millennium_vols_1_and_2_tunberg-minkova/2.13-2.15/non_running/")
    assert response.status_code == 200

def test_select_concat_homer_core_list_frequency_categories_1_4_herodotus_book_1_high_frequency_vocabulary_list():
    response = client.get("/select/Greek/result/homer_core_list_frequency_categories_1-4+herodotus_book_1_high_frequency_vocabulary_list/start+start-end+end/non_running/")
    assert response.status_code == 200

def test_select_full_florus_epitome_11_romulus_and_roman_kings():
    response = client.get("/select/Latin/result/florus_epitome_11_romulus_and_roman_kings/1.1.6-1.1.7/include/seneca_hercules_oetaeus/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_seneca_phoenissae():
    response = client.get("/select/Latin/result/seneca_phoenissae/602-650/non_running/")
    assert response.status_code == 200

def test_select_full_claudian_de_consulatu_stilichonis_preface_to_book_3():
    response = client.get("/select/Latin/result/claudian_de_consulatu_stilichonis_preface_to_book_3/172-186/include/jenney_first_year_combined/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_ovid_heroidum_epistulae():
    response = client.get("/select/Latin/result/ovid_heroidum_epistulae/4.121-6.84/include/diederich_frequency_list_medieval/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_martial_epigrams():
    response = client.get("/select/Latin/result/martial_epigrams/3.91.12-7.10.7/include/latin_stopwords_list_cltk/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_seneca_agamemnon():
    response = client.get("/select/Latin/result/seneca_agamemnon/701-942/non_running/")
    assert response.status_code == 200

def test_select_full_new_latin_primer_english_irby():
    response = client.get("/select/Latin/result/new_latin_primer_english-irby/30-32/include/cicero_pro_marco_tullio/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_cicero_pro_marcello():
    response = client.get("/select/Latin/result/cicero_pro_marcello/28.5-29.6/non_running/")
    assert response.status_code == 200

def test_select_full_concat_cicero_pro_marco_tullio_eutropius_breviarium_book_3_beyer():
    response = client.get("/select/Latin/result/cicero_pro_marco_tullio+eutropius_breviarium_book_3_beyer/15.6+3.16-39.5+3.17/include/cicero_de_lege_agraria/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_aesop_fables():
    response = client.get("/select/Greek/result/aesop_fables/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_apuleius_peri_hermeneias():
    response = client.get("/select/Latin/result/apuleius_peri_hermeneias/6.36-14.35/non_running/")
    assert response.status_code == 200

def test_select_simple_claudian_panegyricus_de_iv_consulatu_honorii_augusti():
    response = client.get("/select/Latin/result/claudian_panegyricus_de_iv_consulatu_honorii_augusti/38-465/non_running/")
    assert response.status_code == 200

def test_select_full_prudentius_psychomachia_preface():
    response = client.get("/select/Latin/result/prudentius_psychomachia_preface/60-63/include/pseudo-caesar_bellum_alexandrinum/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_apollonius_king_of_tyre():
    response = client.get("/select/Latin/result/apollonius_king_of_tyre/19-50/include/owen_epigrams/start-end/non_running/")
    assert response.status_code == 200

def test_select_concat_aesop_fables_groton_from_alpha_to_omega():
    response = client.get("/select/Greek/result/aesop_fables+groton_from_alpha_to_omega/start+start-end+end/non_running/")
    assert response.status_code == 200

def test_select_full_plautus_curculio():
    response = client.get("/select/Latin/result/plautus_curculio/405-697/include/aesop_romulus_anglicus_1-10/start-end/non_running/")
    assert response.status_code == 200

def test_select_concat_egeria_itinerarium_book_1_ovid_halieutica():
    response = client.get("/select/Latin/result/egeria_itinerarium_book_1+ovid_halieutica/6.1+134-13.4+135/non_running/")
    assert response.status_code == 200

def test_select_full_ovid_in_ibin():
    response = client.get("/select/Latin/result/ovid_in_ibin/59-120/include/bede_historia_ecclesiastica_gentis_anglorum_prologue_11_125-26_21-2_12-14_16_20_31-3_5-6/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_seneca_de_brevitate_vitae():
    response = client.get("/select/Latin/result/seneca_de_brevitate_vitae/1.1-8.5/non_running/")
    assert response.status_code == 200

def test_select_simple_seneca_de_beneficiis():
    response = client.get("/select/Latin/result/seneca_de_beneficiis/6.31.7-6.41.1/non_running/")
    assert response.status_code == 200

def test_select_concat_a_primer_of_ecclesiastical_latin_collins_eduqas():
    response = client.get("/select/Latin/result/a_primer_of_ecclesiastical_latin_collins+eduqas/25+427-32+439/non_running/")
    assert response.status_code == 200

def test_select_concat_plautus_amphitruo_passio_santarum_perpetuae_et_felicitatis():
    response = client.get("/select/Latin/result/plautus_amphitruo+passio_santarum_perpetuae_et_felicitatis/487+4.3-1003+10.4/non_running/")
    assert response.status_code == 200

def test_select_full_homer_core_list_frequency_categories_1_4():
    response = client.get("/select/Greek/result/homer_core_list_frequency_categories_1-4/start-end/include/hansen_quinn_greek_an_intensive_course/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_seneca_de_constantia():
    response = client.get("/select/Latin/result/seneca_de_constantia/16.1-16.4/non_running/")
    assert response.status_code == 200

def test_select_full_dares_de_excidio_troiae():
    response = client.get("/select/Latin/result/dares_de_excidio_troiae/31-40/include/cicero_pro_murena/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_concat_a_primer_of_ecclesiastical_latin_collins_eduqas():
    response = client.get("/select/Latin/result/a_primer_of_ecclesiastical_latin_collins+eduqas/25+427-32+439/include/marie_de_france_fables_1-22/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_wiley_real_latin_maltby_belcher():
    response = client.get("/select/Latin/result/wiley_real_latin_maltby-belcher/18-21/include/elizabeth_jane_weston_elegia_consolatoria_ad_havlik/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_claudian_panegyricus_dictus_manlio_theodoro_consuli():
    response = client.get("/select/Latin/result/claudian_panegyricus_dictus_manlio_theodoro_consuli/316-322/include/elizabeth_jane_weston_ad_michaelem_pecka/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_vergil_eclogues():
    response = client.get("/select/Latin/result/vergil_eclogues/2.44-9.33/include/jerome_life_of_malchus_dcc/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_jenney_first_year_latin_red():
    response = client.get("/select/Latin/result/jenney_first_year_latin_red/15-24/non_running/")
    assert response.status_code == 200

def test_select_full_gsce_rvl():
    response = client.get("/select/Latin/result/gsce_rvl/47-107/include/egeria_itinerarium_book_1/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_cicero_in_vatinium():
    response = client.get("/select/Latin/result/cicero_in_vatinium/34.7-38.1/non_running/")
    assert response.status_code == 200

def test_select_simple_cicero_pro_caelio():
    response = client.get("/select/Latin/result/cicero_pro_caelio/38.18-55.17/non_running/")
    assert response.status_code == 200

def test_select_full_concat_plautus_amphitruo_passio_santarum_perpetuae_et_felicitatis():
    response = client.get("/select/Latin/result/plautus_amphitruo+passio_santarum_perpetuae_et_felicitatis/487+4.3-1003+10.4/include/livy_ab_urbe_condita_ib_list_2_selections/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_ocr_gsce_defined_vocabulary_list():
    response = client.get("/select/Latin/result/ocr_gsce_defined_vocabulary_list/161-269/non_running/")
    assert response.status_code == 200

def test_select_full_florus_epitome_221_cleopatra():
    response = client.get("/select/Latin/result/florus_epitome_221_cleopatra/2.21.5-2.21.6/include/carmina_burana_orff_latin_lyrics_1-5_11-15_17-25/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_horace_odes_garrison_edition():
    response = client.get("/select/Latin/result/horace_odes_garrison_edition/4.9.35-4.15.11/include/elizabeth_jane_weston_addenda_ad_parthenica/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_aesop_romulus_anglicus_1_10():
    response = client.get("/select/Latin/result/aesop_romulus_anglicus_1-10/7-10/non_running/")
    assert response.status_code == 200

def test_select_concat_piantaggini_livia_mater_eloquen_jenney_first_year_latin_red():
    response = client.get("/select/Latin/result/piantaggini_livia_mater_eloquen+jenney_first_year_latin_red/2.4+26-2.11+27/non_running/")
    assert response.status_code == 200

def test_select_full_plautus_poenulus():
    response = client.get("/select/Latin/result/plautus_poenulus/1317-1353/include/eutropius_breviarium_all/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_plautus_amphitruo():
    response = client.get("/select/Latin/result/plautus_amphitruo/899-1103/include/claudian_panegyricus_de_iii_consulatu_honorii_augusti/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_physiologus_latina_1_6_9_16_17_23():
    response = client.get("/select/Latin/result/physiologus_latina_1-6_9_16_17_23/23.23-23.35/include/claudian_in_eutropium_preface_to_book_2/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_cicero_pro_rabirio_postumo():
    response = client.get("/select/Latin/result/cicero_pro_rabirio_postumo/2.13-7.4/non_running/")
    assert response.status_code == 200

def test_select_simple_apuleius_de_deo_socratis_prologue():
    response = client.get("/select/Latin/result/apuleius_de_deo_socratis_prologue/4.5-4.11/non_running/")
    assert response.status_code == 200

def test_select_simple_hansen_quinn_greek_an_intensive_course():
    response = client.get("/select/Greek/result/hansen_quinn_greek_an_intensive_course/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_vergil_aeneid_ap_selections():
    response = client.get("/select/Latin/result/vergil_aeneid_ap_selections/2.209-4.702/non_running/")
    assert response.status_code == 200

def test_select_simple_nepos_life_of_hamilcar():
    response = client.get("/select/Latin/result/nepos_life_of_hamilcar/3-4/non_running/")
    assert response.status_code == 200

def test_select_full_colby_latin_list_years_1_3_4():
    response = client.get("/select/Latin/result/colby_latin_list_years_1_3_4/1-3/include/augustine_confessions_book_1/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_apuleius_de_deo_socratis():
    response = client.get("/select/Latin/result/apuleius_de_deo_socratis/16.12-21.8/include/vergil_eclogues_1_dcc/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_international_baccalaureate_vocabulary_sl_hl_selections():
    response = client.get("/select/Latin/result/international_baccalaureate_vocabulary_sl_hl_selections/4770-6072/non_running/")
    assert response.status_code == 200

def test_select_simple_cicero_in_toga_candida():
    response = client.get("/select/Latin/result/cicero_in_toga_candida/6.11-10.3/non_running/")
    assert response.status_code == 200

def test_select_full_cicero_pro_marcello():
    response = client.get("/select/Latin/result/cicero_pro_marcello/28.5-29.6/include/corderius_colloquia_book_2/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_requiem_mass():
    response = client.get("/select/Latin/result/requiem_mass/5-8/non_running/")
    assert response.status_code == 200

def test_select_full_prudentius_psychomachia():
    response = client.get("/select/Latin/result/prudentius_psychomachia/141-540/include/marie_de_france_fables_1-22/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_concat_physiologus_latina_1_6_9_16_17_23_seneca_ad_polybium_de_consolatione():
    response = client.get("/select/Latin/result/physiologus_latina_1-6_9_16_17_23+seneca_ad_polybium_de_consolatione/6.11+4.3-23.46+11.6/include/wheelock_latin_exercitationes/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_lingua_latina_per_se_illustrata_pars_i_oerberg():
    response = client.get("/select/Latin/result/lingua_latina_per_se_illustrata_pars_i_oerberg/28-31/include/martial_book_10/start-end/non_running/")
    assert response.status_code == 200

def test_select_concat_herodotus_book_1_aeschylus_prometheus_bound():
    response = client.get("/select/Greek/result/herodotus_book_1+aeschylus_prometheus_bound/start+start-end+end/non_running/")
    assert response.status_code == 200

def test_select_full_herodotus_book_1():
    response = client.get("/select/Greek/result/herodotus_book_1/start-end/include/athenaze_an_introduction_to_ancient_greek/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_concat_apollonius_argonautica_book_4_athenaze_an_introduction_to_ancient_greek():
    response = client.get("/select/Greek/result/apollonius_argonautica_book_4+athenaze_an_introduction_to_ancient_greek/start+start-end+end/include/hansen_quinn_greek_an_intensive_course/start-end/non_running/")
    assert response.status_code == 200

def test_select_concat_herodotus_book_1_homer_core_list_frequency_categories_1_4():
    response = client.get("/select/Greek/result/herodotus_book_1+homer_core_list_frequency_categories_1-4/start+start-end+end/non_running/")
    assert response.status_code == 200

def test_select_full_williams_ursus_et_porcus():
    response = client.get("/select/Latin/result/williams_ursus_et_porcus/10-13/include/catullus_carmina_garrison/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_claudian_in_rufinum():
    response = client.get("/select/Latin/result/claudian_in_rufinum/1.297-2.316/non_running/")
    assert response.status_code == 200

def test_select_full_elizabeth_jane_weston_ad_michaelem_pecka():
    response = client.get("/select/Latin/result/elizabeth_jane_weston_ad_michaelem_pecka/2.86-2.90/include/horace_ars_poetica/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_herodotus_book_1():
    response = client.get("/select/Greek/result/herodotus_book_1/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_hansen_quinn_greek_an_intensive_course():
    response = client.get("/select/Greek/result/hansen_quinn_greek_an_intensive_course/start-end/include/athenaze_an_introduction_to_ancient_greek/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_seneca_agamemnon():
    response = client.get("/select/Latin/result/seneca_agamemnon/701-942/include/cicero_pro_marcello/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_seneca_de_brevitate_vitae():
    response = client.get("/select/Latin/result/seneca_de_brevitate_vitae/1.1-8.5/include/eutropius_breviarium_all/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_aesop_fables():
    response = client.get("/select/Greek/result/aesop_fables/start-end/include/hansen_quinn_greek_an_intensive_course/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_prudentius_psychomachia():
    response = client.get("/select/Latin/result/prudentius_psychomachia/141-540/non_running/")
    assert response.status_code == 200

def test_select_simple_stabat_mater():
    response = client.get("/select/Latin/result/stabat_mater/49-54/non_running/")
    assert response.status_code == 200

def test_select_full_fabulae_faciles_ritchie():
    response = client.get("/select/Latin/result/fabulae_faciles_ritchie/3.59-3.71/include/seneca_ad_lucilium_epistulae_morales/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_cato_distichs():
    response = client.get("/select/Latin/result/cato_distichs/3.20.2-4.35.1/non_running/")
    assert response.status_code == 200

def test_select_simple_dcc_latin_core():
    response = client.get("/select/Latin/result/dcc_latin_core/678-755/non_running/")
    assert response.status_code == 200

def test_select_full_cicero_pro_milone():
    response = client.get("/select/Latin/result/cicero_pro_milone/78.9-100.9/include/petrionius_satyricon/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_ovid_halieutica():
    response = client.get("/select/Latin/result/ovid_halieutica/77-99/non_running/")
    assert response.status_code == 200

def test_select_simple_claudian_de_consulatu_stilichonis_preface_to_book_3():
    response = client.get("/select/Latin/result/claudian_de_consulatu_stilichonis_preface_to_book_3/172-186/non_running/")
    assert response.status_code == 200

def test_select_full_concat_herodotus_book_1_high_frequency_vocabulary_list_groton_from_alpha_to_omega():
    response = client.get("/select/Greek/result/herodotus_book_1_high_frequency_vocabulary_list+groton_from_alpha_to_omega/start+start-end+end/include/apollonius_argonautica_book_4/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_elizabeth_jane_weston_addenda_ad_parthenica():
    response = client.get("/select/Latin/result/elizabeth_jane_weston_addenda_ad_parthenica/1.1.17-1.1.23/include/elizabeth_jane_weston_in_obitum_ioannae/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_cicero_somnium_scipionis_9_29():
    response = client.get("/select/Latin/result/cicero_somnium_scipionis_9-29/10-12/include/elizabeth_jane_weston_ad_matthiam_secundum/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_classical_latin_mckeown():
    response = client.get("/select/Latin/result/classical_latin_mckeown/21-24/include/latin_an_intensive_course_moreland-fleischer/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_tibullus_elegies():
    response = client.get("/select/Latin/result/tibullus_elegies/2.5.68-3.7.98/non_running/")
    assert response.status_code == 200

def test_select_simple_dcc_greek_core_list():
    response = client.get("/select/Greek/result/dcc_greek_core_list/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_hildegard_of_bingen_ordo_virtutum():
    response = client.get("/select/Latin/result/hildegard_of_bingen_ordo_virtutum/123-204/include/horace_epodes/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_cato_distichs():
    response = client.get("/select/Latin/result/cato_distichs/3.20.2-4.35.1/include/ovid_ars_amatoria/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_seneca_medea():
    response = client.get("/select/Latin/result/seneca_medea/333-753/non_running/")
    assert response.status_code == 200

def test_select_full_concat_cicero_pro_flacco_elizabeth_jane_weston_epistula_josepho_scaligero():
    response = client.get("/select/Latin/result/cicero_pro_flacco+elizabeth_jane_weston_epistula_josepho_scaligero/6.4+0-88.5+1/include/nepos_life_of_hamilcar/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_dcc_greek_core_list():
    response = client.get("/select/Greek/result/dcc_greek_core_list/start-end/include/groton_from_alpha_to_omega/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_elizabeth_jane_weston_vota_pro_felicibus_et_secundis_nuptis():
    response = client.get("/select/Latin/result/elizabeth_jane_weston_vota_pro_felicibus_et_secundis_nuptis/2.14-2.38/include/jerome_life_of_malchus_dcc/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_gsce_dvl():
    response = client.get("/select/Latin/result/gsce_dvl/343-382/include/ovid_fasti/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_plautus_poenulus():
    response = client.get("/select/Latin/result/plautus_poenulus/1317-1353/non_running/")
    assert response.status_code == 200

def test_select_concat_dcc_greek_core_list_apollonius_argonautica_book_4():
    response = client.get("/select/Greek/result/dcc_greek_core_list+apollonius_argonautica_book_4/start+start-end+end/non_running/")
    assert response.status_code == 200

def test_select_simple_ocr_as():
    response = client.get("/select/Latin/result/ocr_as/536-627/non_running/")
    assert response.status_code == 200

def test_select_full_elizabeth_jane_weston_parthenica():
    response = client.get("/select/Latin/result/elizabeth_jane_weston_parthenica/2.102.34-3.1b.26/include/cicero_pro_marco_tullio/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_latin_stopwords_list_cltk():
    response = client.get("/select/Latin/result/latin_stopwords_list_cltk/13-42/include/colby_latin_list_years_1_3_4/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_elizabeth_jane_weston_poemata():
    response = client.get("/select/Latin/result/elizabeth_jane_weston_poemata/2.90.45-2.94.59/include/claudian_panegyricus_de_iii_consulatu_honorii_augusti/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_cicero_somnium_scipionis_9_29():
    response = client.get("/select/Latin/result/cicero_somnium_scipionis_9-29/10-12/non_running/")
    assert response.status_code == 200

def test_select_full_apuleius_de_deo_socratis_prologue():
    response = client.get("/select/Latin/result/apuleius_de_deo_socratis_prologue/4.5-4.11/include/suburani_fabulae/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_ovid_fasti():
    response = client.get("/select/Latin/result/ovid_fasti/6.225-6.227/include/diederich_frequency_list_general/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_seneca_apocolocyntosis():
    response = client.get("/select/Latin/result/seneca_apocolocyntosis/4.1.27-7.2.8/non_running/")
    assert response.status_code == 200

def test_select_full_seneca_de_tranquillitate_animi():
    response = client.get("/select/Latin/result/seneca_de_tranquillitate_animi/3.1-13.2/include/bernardo_de_riofrio_centonicum_virgilianum_monimentum/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_seneca_ad_marciam_de_consolatione():
    response = client.get("/select/Latin/result/seneca_ad_marciam_de_consolatione/18.3-18.5/include/passio_santarum_perpetuae_et_felicitatis/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_claudian_panegyricus_de_vi_consulatu_honorii_augusti_preface():
    response = client.get("/select/Latin/result/claudian_panegyricus_de_vi_consulatu_honorii_augusti_preface/18-24/include/bernardo_de_riofrio_centonicum_virgilianum_monimentum/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_ovid_medicamina_faciei_femineae():
    response = client.get("/select/Latin/result/ovid_medicamina_faciei_femineae/41-94/non_running/")
    assert response.status_code == 200

def test_select_full_athenaze_an_introduction_to_ancient_greek():
    response = client.get("/select/Greek/result/athenaze_an_introduction_to_ancient_greek/start-end/include/demonsthenes_against_neaira/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_piantaggini_livia_mater_eloquen():
    response = client.get("/select/Latin/result/piantaggini_livia_mater_eloquen/3.10-3.12/non_running/")
    assert response.status_code == 200

def test_select_concat_aeschylus_prometheus_bound_hansen_quinn_greek_an_intensive_course():
    response = client.get("/select/Greek/result/aeschylus_prometheus_bound+hansen_quinn_greek_an_intensive_course/start+start-end+end/non_running/")
    assert response.status_code == 200

def test_select_full_tacitus_dialogus_de_oratoribus():
    response = client.get("/select/Latin/result/tacitus_dialogus_de_oratoribus/18.3-28.5/include/apuleius_apology/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_ovid_heroidum_epistulae():
    response = client.get("/select/Latin/result/ovid_heroidum_epistulae/4.121-6.84/non_running/")
    assert response.status_code == 200

def test_select_full_ovid_metamorphoses_1_6_11_15():
    response = client.get("/select/Latin/result/ovid_metamorphoses_1-6_11_15/15.801-15.868/include/claudian_de_raptu_prosperinae/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_gsce_dvl():
    response = client.get("/select/Latin/result/gsce_dvl/343-382/non_running/")
    assert response.status_code == 200

def test_select_simple_cicero_in_verrem_actio_secunda():
    response = client.get("/select/Latin/result/cicero_in_verrem_actio_secunda/1.29.3-3.83.17/non_running/")
    assert response.status_code == 200

def test_select_full_petrionius_satyricon():
    response = client.get("/select/Latin/result/petrionius_satyricon/22-55/include/lhomond_de_viris_illustribus_1-18_exordium_to_coriolanus/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_cicero_pro_fonteio_excluding_fragments():
    response = client.get("/select/Latin/result/cicero_pro_fonteio_excluding_fragments/16.3-16.7/include/cato_monostichs/start-end/non_running/")
    assert response.status_code == 200

def test_select_concat_claudian_panegyricus_de_vi_consulatu_honorii_augusti_preface_claudian_panegyricus_dictus_manlio_theodoro_consuli():
    response = client.get("/select/Latin/result/claudian_panegyricus_de_vi_consulatu_honorii_augusti_preface+claudian_panegyricus_dictus_manlio_theodoro_consuli/3+83-16+232/non_running/")
    assert response.status_code == 200

def test_select_simple_apollonius_argonautica_book_4():
    response = client.get("/select/Greek/result/apollonius_argonautica_book_4/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_concat_aesop_fables_apollonius_argonautica_book_4():
    response = client.get("/select/Greek/result/aesop_fables+apollonius_argonautica_book_4/start+start-end+end/include/athenaze_an_introduction_to_ancient_greek/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_propertius_elegies():
    response = client.get("/select/Latin/result/propertius_elegies/3.18.5-4.3.9/include/corderius_colloquia_book_2/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_colby_latin_list_years_1_3_4():
    response = client.get("/select/Latin/result/colby_latin_list_years_1_3_4/1-3/non_running/")
    assert response.status_code == 200

def test_select_full_cicero_pro_rabirio_perduellionis_reo():
    response = client.get("/select/Latin/result/cicero_pro_rabirio_perduellionis_reo/18.11-27.11/include/claudian_de_raptu_prosperinae/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_ovid_fasti():
    response = client.get("/select/Latin/result/ovid_fasti/6.225-6.227/non_running/")
    assert response.status_code == 200

def test_select_full_cicero_in_calpurnium_pisonem():
    response = client.get("/select/Latin/result/cicero_in_calpurnium_pisonem/32.5-48.7/include/apollonius_king_of_tyre/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_latin_for_the_new_millennium_vols_1_and_2_tunberg_minkova():
    response = client.get("/select/Latin/result/latin_for_the_new_millennium_vols_1_and_2_tunberg-minkova/2.13-2.15/include/ovid_metamorphoses_1-6_11_15/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_cicero_de_imperio_cn_pompei():
    response = client.get("/select/Latin/result/cicero_de_imperio_cn_pompei/58.10-71.4/include/claudian_carmina_minora_25_preface/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_carmina_burana_orff_latin_lyrics_1_5_11_15_17_25():
    response = client.get("/select/Latin/result/carmina_burana_orff_latin_lyrics_1-5_11-15_17-25/12.14-24.6/non_running/")
    assert response.status_code == 200

def test_select_full_pseudo_caesar_bellum_africanum():
    response = client.get("/select/Latin/result/pseudo-caesar_bellum_africanum/58.1-70.7/include/seneca_troades/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_jenney_first_year_latin_purple_jenney_scudder_baade():
    response = client.get("/select/Latin/result/jenney_first_year_latin_purple_jenney-scudder-baade/6-30/include/hildegard_of_bingen_ordo_virtutum/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_elizabeth_jane_weston_ad_michaelem_pecka():
    response = client.get("/select/Latin/result/elizabeth_jane_weston_ad_michaelem_pecka/2.86-2.90/non_running/")
    assert response.status_code == 200

def test_select_full_cicero_in_verrem_actio_secunda():
    response = client.get("/select/Latin/result/cicero_in_verrem_actio_secunda/1.29.3-3.83.17/include/williams_rena_rhinoceros/start-end/non_running/")
    assert response.status_code == 200

def test_select_concat_cicero_pro_marco_tullio_eutropius_breviarium_book_3_beyer():
    response = client.get("/select/Latin/result/cicero_pro_marco_tullio+eutropius_breviarium_book_3_beyer/15.6+3.16-39.5+3.17/non_running/")
    assert response.status_code == 200

def test_select_simple_ap_latin_core_list_2025():
    response = client.get("/select/Latin/result/ap_latin_core_list_2025/88-602/non_running/")
    assert response.status_code == 200

def test_select_full_seneca_naturales_quaestiones___dcc():
    response = client.get("/select/Latin/result/seneca_naturales_quaestiones_-_dcc/3.0.1-2.38.1/include/horace_carmen_saeculare/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_concat_apollonius_argonautica_book_4_aesop_fables():
    response = client.get("/select/Greek/result/apollonius_argonautica_book_4+aesop_fables/start+start-end+end/include/hansen_quinn_greek_an_intensive_course/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_wiley_real_latin_maltby_belcher():
    response = client.get("/select/Latin/result/wiley_real_latin_maltby-belcher/18-21/non_running/")
    assert response.status_code == 200

def test_select_simple_carmina_priapea_1_80():
    response = client.get("/select/Latin/result/carmina_priapea_1-80/77.9-80.7/non_running/")
    assert response.status_code == 200

def test_select_full_introduction_to_latin_shelmerdine():
    response = client.get("/select/Latin/result/introduction_to_latin_shelmerdine/31-32/include/ovid_fasti/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_eduqas():
    response = client.get("/select/Latin/result/eduqas/370-430/include/cicero_in_verrem_actio_prima/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_seneca_ad_polybium_de_consolatione():
    response = client.get("/select/Latin/result/seneca_ad_polybium_de_consolatione/12.4-15.3/include/disce_kitchell-sienkewicz/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_cicero_de_imperio_pompei():
    response = client.get("/select/Latin/result/cicero_de_imperio_pompei/9.4-13.6/include/seneca_troades/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_vergil_aeneid_new_ap_selections():
    response = client.get("/select/Latin/result/vergil_aeneid_new_ap_selections/4.361-11.588/include/seneca_phoenissae/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_groton_from_alpha_to_omega():
    response = client.get("/select/Greek/result/groton_from_alpha_to_omega/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_seneca_phaedra():
    response = client.get("/select/Latin/result/seneca_phaedra/176-989b/non_running/")
    assert response.status_code == 200

def test_select_full_ovid_remedia_amoris():
    response = client.get("/select/Latin/result/ovid_remedia_amoris/770-792/include/pervigilium_veneris/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_seneca_ad_helviam_matrem_de_consolatione():
    response = client.get("/select/Latin/result/seneca_ad_helviam_matrem_de_consolatione/10.8-13.3/non_running/")
    assert response.status_code == 200

def test_select_simple_florus_epitome_221_cleopatra():
    response = client.get("/select/Latin/result/florus_epitome_221_cleopatra/2.21.5-2.21.6/non_running/")
    assert response.status_code == 200

def test_select_full_requiem_mass():
    response = client.get("/select/Latin/result/requiem_mass/5-8/include/ilias_latina/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_oxford_latin_course_for_college_fabulae_all():
    response = client.get("/select/Latin/result/oxford_latin_course_for_college_fabulae_all/15.2-18.3/non_running/")
    assert response.status_code == 200

def test_select_full_tibullus_elegies():
    response = client.get("/select/Latin/result/tibullus_elegies/2.5.68-3.7.98/include/latin_stopwords_list_cltk/start-end/non_running/")
    assert response.status_code == 200

def test_select_concat_pseudo_caesar_bellum_alexandrinum_claudian_panegyricus_dictus_manlio_theodoro_consuli():
    response = client.get("/select/Latin/result/pseudo-caesar_bellum_alexandrinum+claudian_panegyricus_dictus_manlio_theodoro_consuli/instructa+130-nomine+174/non_running/")
    assert response.status_code == 200

def test_select_simple_seneca_troades():
    response = client.get("/select/Latin/result/seneca_troades/505-530/non_running/")
    assert response.status_code == 200

def test_select_full_jenney_first_year_combined():
    response = client.get("/select/Latin/result/jenney_first_year_combined/6-61/include/eutropius_breviarium_book_1_beyer/start-end/non_running/")
    assert response.status_code == 200

def test_select_concat_aesop_fables_dcc_greek_core_list():
    response = client.get("/select/Greek/result/aesop_fables+dcc_greek_core_list/start+start-end+end/non_running/")
    assert response.status_code == 200

def test_select_full_international_baccalaureate_vocabulary_sl_hl_selections():
    response = client.get("/select/Latin/result/international_baccalaureate_vocabulary_sl_hl_selections/4770-6072/include/claudian_in_eutropium_preface_to_book_2/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_egeria_itinerarium_book_1():
    response = client.get("/select/Latin/result/egeria_itinerarium_book_1/4.6-17.3/non_running/")
    assert response.status_code == 200

def test_select_simple_seneca_de_tranquillitate_animi():
    response = client.get("/select/Latin/result/seneca_de_tranquillitate_animi/3.1-13.2/non_running/")
    assert response.status_code == 200

def test_select_simple_cicero_de_imperio_cn_pompei():
    response = client.get("/select/Latin/result/cicero_de_imperio_cn_pompei/58.10-71.4/non_running/")
    assert response.status_code == 200

def test_select_full_a_primer_of_ecclesiastical_latin_collins():
    response = client.get("/select/Latin/result/a_primer_of_ecclesiastical_latin_collins/11-21/include/pseudo-caesar_bellum_africanum/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_seneca_ad_lucilium_epistulae_morales():
    response = client.get("/select/Latin/result/seneca_ad_lucilium_epistulae_morales/98.15-101.9/include/seneca_ad_lucilium_epistulae_morales/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_herodotus_book_1_high_frequency_vocabulary_list():
    response = client.get("/select/Greek/result/herodotus_book_1_high_frequency_vocabulary_list/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_bernardo_de_riofrio_centonicum_virgilianum_monimentum():
    response = client.get("/select/Latin/result/bernardo_de_riofrio_centonicum_virgilianum_monimentum/52-122/non_running/")
    assert response.status_code == 200

def test_select_concat_new_latin_primer_english_irby_martial_book_10():
    response = client.get("/select/Latin/result/new_latin_primer_english-irby+martial_book_10/17+10.36.8-27+10.61.4/non_running/")
    assert response.status_code == 200

def test_select_simple_newton_axiomata_motus():
    response = client.get("/select/Latin/result/newton_axiomata_motus/2-3/non_running/")
    assert response.status_code == 200

def test_select_simple_seneca_hercules_furens_dcc():
    response = client.get("/select/Latin/result/seneca_hercules_furens_dcc/598-1308/non_running/")
    assert response.status_code == 200

def test_select_full_oxford_latin_course_for_college_fabulae_all():
    response = client.get("/select/Latin/result/oxford_latin_course_for_college_fabulae_all/15.2-18.3/include/livy_ab_urbe_condita_ib_list_2_selections/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_ecce_romani_chs_1_54():
    response = client.get("/select/Latin/result/ecce_romani_chs_1-54/23-34/non_running/")
    assert response.status_code == 200

def test_select_simple_catullus_carmina_garrison():
    response = client.get("/select/Latin/result/catullus_carmina_garrison/61.44-66.4/non_running/")
    assert response.status_code == 200

def test_select_full_ovid_ars_amatoria():
    response = client.get("/select/Latin/result/ovid_ars_amatoria/3.509-3.754/include/prudentius_psychomachia/start-end/non_running/")
    assert response.status_code == 200

def test_select_concat_ovid_in_ibin_seneca_phaedra():
    response = client.get("/select/Latin/result/ovid_in_ibin+seneca_phaedra/187+169-451+534/non_running/")
    assert response.status_code == 200

def test_select_simple_jerome_life_of_malchus_dcc():
    response = client.get("/select/Latin/result/jerome_life_of_malchus_dcc/9.10-10.2/non_running/")
    assert response.status_code == 200

def test_select_concat_apollonius_argonautica_book_4_aesop_fables():
    response = client.get("/select/Greek/result/apollonius_argonautica_book_4+aesop_fables/start+start-end+end/non_running/")
    assert response.status_code == 200

def test_select_concat_dcc_latin_core_suetonius_life_of_caligula():
    response = client.get("/select/Latin/result/dcc_latin_core+suetonius_life_of_caligula/884+52-949+53/non_running/")
    assert response.status_code == 200

def test_select_full_diederich_frequency_list_prose():
    response = client.get("/select/Latin/result/diederich_frequency_list_prose/2292-2336/include/cicero_in_toga_candida/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_williams_rena_rhinoceros():
    response = client.get("/select/Latin/result/williams_rena_rhinoceros/14-15/include/horace_ars_poetica/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_seneca_ad_helviam_matrem_de_consolatione():
    response = client.get("/select/Latin/result/seneca_ad_helviam_matrem_de_consolatione/10.8-13.3/include/owen_epigrams/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_cambridge_latin_course():
    response = client.get("/select/Latin/result/cambridge_latin_course/7-28/non_running/")
    assert response.status_code == 200

def test_select_simple_hildegard_of_bingen_ordo_virtutum():
    response = client.get("/select/Latin/result/hildegard_of_bingen_ordo_virtutum/123-204/non_running/")
    assert response.status_code == 200

def test_select_full_dcc_latin_core():
    response = client.get("/select/Latin/result/dcc_latin_core/678-755/include/pseudo-caesar_bellum_africanum/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_horace_epodes():
    response = client.get("/select/Latin/result/horace_epodes/8.7-16.46/include/ap_latin_core_list_2025/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_apuleius_apology():
    response = client.get("/select/Latin/result/apuleius_apology/38.6-83.11/include/apuleius_de_deo_socratis_prologue/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_horace_satires():
    response = client.get("/select/Latin/result/horace_satires/2.6.13-2.7.3/include/williams_ursus_et_porcus/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_williams_ursus_et_porcus():
    response = client.get("/select/Latin/result/williams_ursus_et_porcus/10-13/non_running/")
    assert response.status_code == 200

def test_select_full_seneca_de_beneficiis():
    response = client.get("/select/Latin/result/seneca_de_beneficiis/6.31.7-6.41.1/include/hildegard_of_bingen_ordo_virtutum/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_claudian_panegyricus_dictus_olybrio_et_probino_consulibus():
    response = client.get("/select/Latin/result/claudian_panegyricus_dictus_olybrio_et_probino_consulibus/128-213/non_running/")
    assert response.status_code == 200

def test_select_full_apuleius_florida():
    response = client.get("/select/Latin/result/apuleius_florida/3.28-19.26/include/horace_odes_garrison_edition/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_concat_cicero_pro_marcello_horace_epistulae():
    response = client.get("/select/Latin/result/cicero_pro_marcello+horace_epistulae/31.7+2.1.176-31.9+2.1.235/include/tibullus_elegies/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_claudian_panegyricus_dictus_olybrio_et_probino_consulibus():
    response = client.get("/select/Latin/result/claudian_panegyricus_dictus_olybrio_et_probino_consulibus/128-213/include/latin_for_the_new_millennium_readings_volume_1_tunberg-minkova/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_fabulae_ab_urbe_condita_sandford_scott():
    response = client.get("/select/Latin/result/fabulae_ab_urbe_condita_sandford-scott/18-19/non_running/")
    assert response.status_code == 200

def test_select_simple_claudian_panegyricus_de_vi_consulatu_honorii_augusti():
    response = client.get("/select/Latin/result/claudian_panegyricus_de_vi_consulatu_honorii_augusti/101-416/non_running/")
    assert response.status_code == 200

def test_select_simple_plautus_curculio():
    response = client.get("/select/Latin/result/plautus_curculio/405-697/non_running/")
    assert response.status_code == 200

def test_select_concat_vergil_eclogues_1_dcc_petrionius_satyricon():
    response = client.get("/select/Latin/result/vergil_eclogues_1_dcc+petrionius_satyricon/1.60+60-1.66+86/non_running/")
    assert response.status_code == 200

def test_select_simple_latin_for_the_new_millennium_readings_volume_1_tunberg_minkova():
    response = client.get("/select/Latin/result/latin_for_the_new_millennium_readings_volume_1_tunberg-minkova/1.17.1-1.18.1/non_running/")
    assert response.status_code == 200

def test_select_simple_horace_epodes():
    response = client.get("/select/Latin/result/horace_epodes/8.7-16.46/non_running/")
    assert response.status_code == 200

def test_select_full_cicero_in_toga_candida():
    response = client.get("/select/Latin/result/cicero_in_toga_candida/6.11-10.3/include/cicero_pro_murena/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_concat_aesop_fables_herodotus_book_1():
    response = client.get("/select/Greek/result/aesop_fables+herodotus_book_1/start+start-end+end/include/dcc_greek_core_list/start-end/non_running/")
    assert response.status_code == 200

def test_select_concat_aesop_fables_demonsthenes_against_neaira():
    response = client.get("/select/Greek/result/aesop_fables+demonsthenes_against_neaira/start+start-end+end/non_running/")
    assert response.status_code == 200

def test_select_simple_cicero_in_catilinam_1_4():
    response = client.get("/select/Latin/result/cicero_in_catilinam_1-4/3.12.10-4.17.6/non_running/")
    assert response.status_code == 200

def test_select_simple_claudian_epithalamium_de_nuptii_honorii_augusti():
    response = client.get("/select/Latin/result/claudian_epithalamium_de_nuptii_honorii_augusti/318-325/non_running/")
    assert response.status_code == 200

def test_select_full_herodotus_book_1_high_frequency_vocabulary_list():
    response = client.get("/select/Greek/result/herodotus_book_1_high_frequency_vocabulary_list/start-end/include/hansen_quinn_greek_an_intensive_course/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_claudian_carmina_minora_25_preface():
    response = client.get("/select/Latin/result/claudian_carmina_minora_25_preface/177-244/non_running/")
    assert response.status_code == 200

def test_select_full_latin_an_intensive_course_moreland_fleischer():
    response = client.get("/select/Latin/result/latin_an_intensive_course_moreland-fleischer/5-13/include/piantaggini_livia_mater_eloquen/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_horace_ars_poetica():
    response = client.get("/select/Latin/result/horace_ars_poetica/262-468/include/seneca_naturales_quaestiones_-_dcc/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_ovid_amores_1_dcc():
    response = client.get("/select/Latin/result/ovid_amores_1_dcc/7.60-9.42/non_running/")
    assert response.status_code == 200

def test_select_simple_seneca_hercules_oetaeus():
    response = client.get("/select/Latin/result/seneca_hercules_oetaeus/1752-1940/non_running/")
    assert response.status_code == 200

def test_select_full_seneca_de_ira():
    response = client.get("/select/Latin/result/seneca_de_ira/3.11.4-3.24.1/include/cambridge_latin_course/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_anthologia_latina_507_518_epitaphs_of_vergil():
    response = client.get("/select/Latin/result/anthologia_latina_507-518_epitaphs_of_vergil/509-510/non_running/")
    assert response.status_code == 200

def test_select_concat_cicero_pro_marcello_horace_epistulae():
    response = client.get("/select/Latin/result/cicero_pro_marcello+horace_epistulae/31.7+2.1.176-31.9+2.1.235/non_running/")
    assert response.status_code == 200

def test_select_simple_vergil_eclogues():
    response = client.get("/select/Latin/result/vergil_eclogues/2.44-9.33/non_running/")
    assert response.status_code == 200

def test_select_full_claudian_fescennia():
    response = client.get("/select/Latin/result/claudian_fescennia/2.15-3.4/include/gsce_rvl/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_cicero_in_vatinium():
    response = client.get("/select/Latin/result/cicero_in_vatinium/34.7-38.1/include/propertius_elegies/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_disce_kitchell_sienkewicz():
    response = client.get("/select/Latin/result/disce_kitchell-sienkewicz/17-24/include/apuleius_metamorphoses_finkelpearl/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_ocr_as_level_defined_vocabulary_list():
    response = client.get("/select/Latin/result/ocr_as_level_defined_vocabulary_list/312-627/non_running/")
    assert response.status_code == 200

def test_select_simple_apuleius_de_mundo():
    response = client.get("/select/Latin/result/apuleius_de_mundo/1.2-34.18/non_running/")
    assert response.status_code == 200

def test_select_simple_seneca_ad_lucilium_epistulae_morales():
    response = client.get("/select/Latin/result/seneca_ad_lucilium_epistulae_morales/98.15-101.9/non_running/")
    assert response.status_code == 200

def test_select_simple_florus_epitome_22_23_gracchi():
    response = client.get("/select/Latin/result/florus_epitome_22-23_gracchi/2.1.6-2.2.7/non_running/")
    assert response.status_code == 200

def test_select_full_hrotswitha_dulcitius():
    response = client.get("/select/Latin/result/hrotswitha_dulcitius/1.1-5.1/include/seneca_hercules_furens_dcc/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_cicero_pro_balbo():
    response = client.get("/select/Latin/result/cicero_pro_balbo/51.12-61.2/include/ovid_fasti/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_seneca_de_providentia():
    response = client.get("/select/Latin/result/seneca_de_providentia/4.15-5.8/include/cicero_de_domo_sua/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_piantaggini_livia_mater_eloquen():
    response = client.get("/select/Latin/result/piantaggini_livia_mater_eloquen/3.10-3.12/include/florus_epitome_221_cleopatra/start-end/non_running/")
    assert response.status_code == 200

def test_select_concat_trotula_de_curis_mulierum_74_78_86_87_167_168_174_178_181_182_cicero_somnium_scipionis_9_29():
    response = client.get("/select/Latin/result/trotula_de_curis_mulierum_74-78_86-87_167-168_174-178_181-182+cicero_somnium_scipionis_9-29/77+28-86+29/non_running/")
    assert response.status_code == 200

def test_select_simple_ovid_amores():
    response = client.get("/select/Latin/result/ovid_amores/2.16.41-3.6.87/non_running/")
    assert response.status_code == 200

def test_select_concat_apollonius_argonautica_book_4_athenaze_an_introduction_to_ancient_greek():
    response = client.get("/select/Greek/result/apollonius_argonautica_book_4+athenaze_an_introduction_to_ancient_greek/start+start-end+end/non_running/")
    assert response.status_code == 200

def test_select_simple_eduqas():
    response = client.get("/select/Latin/result/eduqas/370-430/non_running/")
    assert response.status_code == 200

def test_select_full_maffeius_historiae_indicae_13_5_7_10_27_31_35_39_22_7_53_5_6_all():
    response = client.get("/select/Latin/result/maffeius_historiae_indicae_13-5_7-10_27-31_35-39_22-7_53-5_6_all/1.38-5.3/include/caesar_bellum_civile/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_eutropius_breviarium_all():
    response = client.get("/select/Latin/result/eutropius_breviarium_all/9.12-9.2/include/cicero_somnium_scipionis_9-29/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_cicero_pro_rabirio_postumo():
    response = client.get("/select/Latin/result/cicero_pro_rabirio_postumo/2.13-7.4/include/cicero_in_verrem_actio_prima/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_cambridge_latin_course():
    response = client.get("/select/Latin/result/cambridge_latin_course/7-28/include/owen_epigrams/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_elizabeth_jane_weston_carmen_ad_rudolphum_ii():
    response = client.get("/select/Latin/result/elizabeth_jane_weston_carmen_ad_rudolphum_ii/3.25-5z.0/non_running/")
    assert response.status_code == 200

def test_select_simple_apuleius_florida():
    response = client.get("/select/Latin/result/apuleius_florida/3.28-19.26/non_running/")
    assert response.status_code == 200

def test_select_simple_claudian_panegyricus_de_vi_consulatu_honorii_augusti_preface():
    response = client.get("/select/Latin/result/claudian_panegyricus_de_vi_consulatu_honorii_augusti_preface/18-24/non_running/")
    assert response.status_code == 200

def test_select_concat_athenaze_an_introduction_to_ancient_greek_herodotus_book_1_high_frequency_vocabulary_list():
    response = client.get("/select/Greek/result/athenaze_an_introduction_to_ancient_greek+herodotus_book_1_high_frequency_vocabulary_list/start+start-end+end/non_running/")
    assert response.status_code == 200

def test_select_full_concat_new_latin_primer_english_irby_martial_book_10():
    response = client.get("/select/Latin/result/new_latin_primer_english-irby+martial_book_10/17+10.36.8-27+10.61.4/include/plautus_amphitruo/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_florus_epitome_22_23_gracchi():
    response = client.get("/select/Latin/result/florus_epitome_22-23_gracchi/2.1.6-2.2.7/include/requiem_mass/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_eutropius_breviarium_all():
    response = client.get("/select/Latin/result/eutropius_breviarium_all/9.12-9.2/non_running/")
    assert response.status_code == 200

def test_select_simple_horace_ars_poetica():
    response = client.get("/select/Latin/result/horace_ars_poetica/262-468/non_running/")
    assert response.status_code == 200

def test_select_simple_elizabeth_jane_weston_epistula_josepho_scaligero():
    response = client.get("/select/Latin/result/elizabeth_jane_weston_epistula_josepho_scaligero/0-1/non_running/")
    assert response.status_code == 200

def test_select_full_cicero_pro_caelio():
    response = client.get("/select/Latin/result/cicero_pro_caelio/38.18-55.17/include/cicero_in_calpurnium_pisonem/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_wheelock_latin_sententiae_antiquae():
    response = client.get("/select/Latin/result/wheelock_latin_sententiae_antiquae/9.8-28.4/include/claudian_de_raptu_prosperinae/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_suetonius_life_of_caligula():
    response = client.get("/select/Latin/result/suetonius_life_of_caligula/54-56/non_running/")
    assert response.status_code == 200

def test_select_full_vulgate_gospel_of_john():
    response = client.get("/select/Latin/result/vulgate_gospel_of_john/2.13-7.26/include/seneca_agamemnon/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_corderius_colloquia_book_2():
    response = client.get("/select/Latin/result/corderius_colloquia_book_2/2.10-2.67/include/elizabeth_jane_weston_in_obitum_ioannae/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_latin_for_the_new_millennium_readings_volume_1_tunberg_minkova():
    response = client.get("/select/Latin/result/latin_for_the_new_millennium_readings_volume_1_tunberg-minkova/1.17.1-1.18.1/include/ovid_amores_1_dcc/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_claudian_in_rufinum():
    response = client.get("/select/Latin/result/claudian_in_rufinum/1.297-2.316/include/cicero_post_reditum_ad_quirites/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_elizabeth_jane_weston_epistula_josepho_scaligero():
    response = client.get("/select/Latin/result/elizabeth_jane_weston_epistula_josepho_scaligero/0-1/include/claudian_in_rufinum_prefaces/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_martial_epigrams():
    response = client.get("/select/Latin/result/martial_epigrams/3.91.12-7.10.7/non_running/")
    assert response.status_code == 200

def test_select_full_nepos_life_of_hamilcar():
    response = client.get("/select/Latin/result/nepos_life_of_hamilcar/3-4/include/livy_ab_urbe_condita_ib_list_2_selections/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_cicero_de_domo_sua():
    response = client.get("/select/Latin/result/cicero_de_domo_sua/95.1-98.3/include/seneca_de_ira/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_seneca_phaedra():
    response = client.get("/select/Latin/result/seneca_phaedra/176-989b/include/apuleius_de_deo_socratis/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_concat_cicero_in_verrem_actio_prima_claudian_de_raptu_prosperinae():
    response = client.get("/select/Latin/result/cicero_in_verrem_actio_prima+claudian_de_raptu_prosperinae/16.7+1.5-41.6+2.228/include/elizabeth_jane_weston_addenda_ad_parthenica/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_lingua_latina_per_se_illustrata_pars_i_oerberg():
    response = client.get("/select/Latin/result/lingua_latina_per_se_illustrata_pars_i_oerberg/28-31/non_running/")
    assert response.status_code == 200

def test_select_simple_200_essential_latin_words_list_mahoney():
    response = client.get("/select/Latin/result/200_essential_latin_words_list_mahoney/156-197/non_running/")
    assert response.status_code == 200

def test_select_full_ocr_gsce_defined_vocabulary_list():
    response = client.get("/select/Latin/result/ocr_gsce_defined_vocabulary_list/161-269/include/elizabeth_jane_weston_vota_pro_felicibus_et_secundis_nuptis/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_concat_demonsthenes_against_neaira_apollonius_argonautica_book_4():
    response = client.get("/select/Greek/result/demonsthenes_against_neaira+apollonius_argonautica_book_4/start+start-end+end/include/homer_core_list_frequency_categories_1-4/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_owen_epigrams():
    response = client.get("/select/Latin/result/owen_epigrams/4.187.3-9.30.2/non_running/")
    assert response.status_code == 200

def test_select_concat_dcc_latin_core_gsce_rvl():
    response = client.get("/select/Latin/result/dcc_latin_core+gsce_rvl/192+45-515+85/non_running/")
    assert response.status_code == 200

def test_select_simple_livy_ab_urbe_condita_ib_list_2_selections():
    response = client.get("/select/Latin/result/livy_ab_urbe_condita_ib_list_2_selections/1.59.5-3.44.1/non_running/")
    assert response.status_code == 200

def test_select_simple_eutropius_breviarium_book_1_beyer():
    response = client.get("/select/Latin/result/eutropius_breviarium_book_1_beyer/7-19/non_running/")
    assert response.status_code == 200

def test_select_full_caesar_bellum_civile():
    response = client.get("/select/Latin/result/caesar_bellum_civile/3.84.3-3.112.4/include/cicero_pro_murena/start-end/non_running/")
    assert response.status_code == 200

def test_select_concat_cicero_pro_flacco_elizabeth_jane_weston_epistula_josepho_scaligero():
    response = client.get("/select/Latin/result/cicero_pro_flacco+elizabeth_jane_weston_epistula_josepho_scaligero/6.4+0-88.5+1/non_running/")
    assert response.status_code == 200

def test_select_full_200_essential_latin_words_list_mahoney():
    response = client.get("/select/Latin/result/200_essential_latin_words_list_mahoney/156-197/include/ovid_heroidum_epistulae/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_aeschylus_prometheus_bound():
    response = client.get("/select/Greek/result/aeschylus_prometheus_bound/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_vergil_eclogues_1_dcc():
    response = client.get("/select/Latin/result/vergil_eclogues_1_dcc/1.3-1.68/include/ovid_amores_1_dcc/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_lhomond_de_viris_illustribus_1_18_exordium_to_coriolanus():
    response = client.get("/select/Latin/result/lhomond_de_viris_illustribus_1-18_exordium_to_coriolanus/1.1-2.2/non_running/")
    assert response.status_code == 200

def test_select_full_wheelock_latin_exercitationes():
    response = client.get("/select/Latin/result/wheelock_latin_exercitationes/34.10-37.2/include/claudian_panegyricus_dictus_olybrio_et_probino_consulibus/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_concat_herodotus_book_1_homer_core_list_frequency_categories_1_4():
    response = client.get("/select/Greek/result/herodotus_book_1+homer_core_list_frequency_categories_1-4/start+start-end+end/include/hansen_quinn_greek_an_intensive_course/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_persius_satires():
    response = client.get("/select/Latin/result/persius_satires/0.8-5.107/non_running/")
    assert response.status_code == 200

def test_select_full_ovid_halieutica():
    response = client.get("/select/Latin/result/ovid_halieutica/77-99/include/wheelock_latin_exercitationes/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_horace_satires():
    response = client.get("/select/Latin/result/horace_satires/2.6.13-2.7.3/non_running/")
    assert response.status_code == 200

def test_select_full_concat_herodotus_book_1_demonsthenes_against_neaira():
    response = client.get("/select/Greek/result/herodotus_book_1+demonsthenes_against_neaira/start+start-end+end/include/demonsthenes_against_neaira/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_claudian_epithalamium_de_nuptii_honorii_augusti():
    response = client.get("/select/Latin/result/claudian_epithalamium_de_nuptii_honorii_augusti/318-325/include/ocr_as/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_stabat_mater():
    response = client.get("/select/Latin/result/stabat_mater/49-54/include/cicero_pro_caelio/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_wheelock_latin_sententiae_antiquae():
    response = client.get("/select/Latin/result/wheelock_latin_sententiae_antiquae/9.8-28.4/non_running/")
    assert response.status_code == 200

def test_select_full_ocr_gsce_restricted_vocabulary_list():
    response = client.get("/select/Latin/result/ocr_gsce_restricted_vocabulary_list/25-123/include/persius_satires/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_apuleius_peri_hermeneias():
    response = client.get("/select/Latin/result/apuleius_peri_hermeneias/6.36-14.35/include/apuleius_peri_hermeneias/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_ocr_as_level_defined_vocabulary_list():
    response = client.get("/select/Latin/result/ocr_as_level_defined_vocabulary_list/312-627/include/claudian_de_raptu_prosperinae_prefaces/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_dares_de_excidio_troiae():
    response = client.get("/select/Latin/result/dares_de_excidio_troiae/31-40/non_running/")
    assert response.status_code == 200

def test_select_full_claudian_in_rufinum_prefaces():
    response = client.get("/select/Latin/result/claudian_in_rufinum_prefaces/2.5-2.11/include/diederich_frequency_list_general/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_cicero_pro_marco_tullio():
    response = client.get("/select/Latin/result/cicero_pro_marco_tullio/36.1-Fr.1.7/include/seneca_de_providentia/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_apuleius_asclepius():
    response = client.get("/select/Latin/result/apuleius_asclepius/6.16-41.2/non_running/")
    assert response.status_code == 200

def test_select_simple_williams_rena_rhinoceros():
    response = client.get("/select/Latin/result/williams_rena_rhinoceros/14-15/non_running/")
    assert response.status_code == 200

def test_select_full_augustine_confessions_book_1():
    response = client.get("/select/Latin/result/augustine_confessions_book_1/1.18.29-1.20.31/include/cicero_in_calpurnium_pisonem/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_oxford_latin_course_for_college():
    response = client.get("/select/Latin/result/oxford_latin_course_for_college/24-25/include/seneca_de_otio/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_ilias_latina():
    response = client.get("/select/Latin/result/ilias_latina/817-1047/include/hildegard_of_bingen_symphoniae_2-5_10_11_12_17_19_21_23_64/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_jenney_first_year_combined():
    response = client.get("/select/Latin/result/jenney_first_year_combined/6-61/non_running/")
    assert response.status_code == 200

def test_select_concat_herodotus_book_1_high_frequency_vocabulary_list_groton_from_alpha_to_omega():
    response = client.get("/select/Greek/result/herodotus_book_1_high_frequency_vocabulary_list+groton_from_alpha_to_omega/start+start-end+end/non_running/")
    assert response.status_code == 200

def test_select_full_seneca_hercules_furens_dcc():
    response = client.get("/select/Latin/result/seneca_hercules_furens_dcc/598-1308/include/classical_latin_mckeown/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_seneca_de_providentia():
    response = client.get("/select/Latin/result/seneca_de_providentia/4.15-5.8/non_running/")
    assert response.status_code == 200

def test_select_simple_apuleius_de_deo_socratis():
    response = client.get("/select/Latin/result/apuleius_de_deo_socratis/16.12-21.8/non_running/")
    assert response.status_code == 200

def test_select_simple_diederich_frequency_list_general():
    response = client.get("/select/Latin/result/diederich_frequency_list_general/1342-1502/non_running/")
    assert response.status_code == 200

def test_select_full_passio_santarum_perpetuae_et_felicitatis():
    response = client.get("/select/Latin/result/passio_santarum_perpetuae_et_felicitatis/11.7-18.9/include/eduqas_gsce_defined_vocablary_list/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_elizabeth_jane_weston_de_ebrietate():
    response = client.get("/select/Latin/result/elizabeth_jane_weston_de_ebrietate/54.19-54.41/non_running/")
    assert response.status_code == 200

def test_select_simple_maffeius_historiae_indicae_13_5_7_10_27_31_35_39_22_7_53_5_6_all():
    response = client.get("/select/Latin/result/maffeius_historiae_indicae_13-5_7-10_27-31_35-39_22-7_53-5_6_all/1.38-5.3/non_running/")
    assert response.status_code == 200

def test_select_simple_introduction_to_latin_shelmerdine():
    response = client.get("/select/Latin/result/introduction_to_latin_shelmerdine/31-32/non_running/")
    assert response.status_code == 200

def test_select_simple_claudian_de_raptu_prosperinae_prefaces():
    response = client.get("/select/Latin/result/claudian_de_raptu_prosperinae_prefaces/2.5-2.7/non_running/")
    assert response.status_code == 200

def test_select_simple_claudian_de_raptu_prosperinae():
    response = client.get("/select/Latin/result/claudian_de_raptu_prosperinae/1.235-2.26/non_running/")
    assert response.status_code == 200

def test_select_full_concat_dcc_latin_core_suetonius_life_of_caligula():
    response = client.get("/select/Latin/result/dcc_latin_core+suetonius_life_of_caligula/884+52-949+53/include/seneca_medea/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_elizabeth_jane_weston_in_obitum_ioannae():
    response = client.get("/select/Latin/result/elizabeth_jane_weston_in_obitum_ioannae/1.14-1.85/include/cicero_de_officiis/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_abelard_historia_selections():
    response = client.get("/select/Latin/result/abelard_historia_selections/5-6/include/cicero_de_domo_sua/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_ovid_ars_amatoria():
    response = client.get("/select/Latin/result/ovid_ars_amatoria/3.509-3.754/non_running/")
    assert response.status_code == 200

def test_select_full_caesar_bellum_gallicum_ap_selections():
    response = client.get("/select/Latin/result/caesar_bellum_gallicum_ap_selections/5.26.1-5.41.2/include/augustus_res_gestae_1/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_seneca_oedipus():
    response = client.get("/select/Latin/result/seneca_oedipus/560-645/include/apuleius_de_deo_socratis_prologue/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_claudian_panegyricus_de_iv_consulatu_honorii_augusti():
    response = client.get("/select/Latin/result/claudian_panegyricus_de_iv_consulatu_honorii_augusti/38-465/include/carmina_priapea_1-80/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_landivar_rusticatio_mexicana_book_6():
    response = client.get("/select/Latin/result/landivar_rusticatio_mexicana_book_6/propinquum-seriem/non_running/")
    assert response.status_code == 200

def test_select_full_carmina_priapea_1_80():
    response = client.get("/select/Latin/result/carmina_priapea_1-80/77.9-80.7/include/elizabeth_jane_weston_carmen_ad_rudolphum_ii/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_elizabeth_jane_weston_vota_pro_felicibus_et_secundis_nuptis():
    response = client.get("/select/Latin/result/elizabeth_jane_weston_vota_pro_felicibus_et_secundis_nuptis/2.14-2.38/non_running/")
    assert response.status_code == 200

def test_select_simple_horace_odes_garrison_edition():
    response = client.get("/select/Latin/result/horace_odes_garrison_edition/4.9.35-4.15.11/non_running/")
    assert response.status_code == 200

def test_select_full_egeria_itinerarium_book_1():
    response = client.get("/select/Latin/result/egeria_itinerarium_book_1/4.6-17.3/include/seneca_medea/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_latin_stopwords_list_cltk():
    response = client.get("/select/Latin/result/latin_stopwords_list_cltk/13-42/non_running/")
    assert response.status_code == 200

def test_select_simple_cicero_post_reditum_in_senatu():
    response = client.get("/select/Latin/result/cicero_post_reditum_in_senatu/20.3-39.2/non_running/")
    assert response.status_code == 200

def test_select_simple_elizabeth_jane_weston_elegia_consolatoria_ad_havlik():
    response = client.get("/select/Latin/result/elizabeth_jane_weston_elegia_consolatoria_ad_havlik/1.3-1.4/non_running/")
    assert response.status_code == 200

def test_select_simple_caesar_bellum_gallicum_ap_selections():
    response = client.get("/select/Latin/result/caesar_bellum_gallicum_ap_selections/5.26.1-5.41.2/non_running/")
    assert response.status_code == 200

def test_select_simple_cicero_pro_fonteio_excluding_fragments():
    response = client.get("/select/Latin/result/cicero_pro_fonteio_excluding_fragments/16.3-16.7/non_running/")
    assert response.status_code == 200

def test_select_full_cicero_post_reditum_in_senatu():
    response = client.get("/select/Latin/result/cicero_post_reditum_in_senatu/20.3-39.2/include/carmina_burana_orff_latin_lyrics_1-5_11-15_17-25/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_ap_latin_core_list_2025():
    response = client.get("/select/Latin/result/ap_latin_core_list_2025/88-602/include/requiem_mass/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_claudian_fescennia():
    response = client.get("/select/Latin/result/claudian_fescennia/2.15-3.4/non_running/")
    assert response.status_code == 200

def test_select_full_concat_vergil_eclogues_1_dcc_petrionius_satyricon():
    response = client.get("/select/Latin/result/vergil_eclogues_1_dcc+petrionius_satyricon/1.60+60-1.66+86/include/new_latin_primer_english-irby/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_apollonius_king_of_tyre():
    response = client.get("/select/Latin/result/apollonius_king_of_tyre/19-50/non_running/")
    assert response.status_code == 200

def test_select_simple_augustus_res_gestae_1():
    response = client.get("/select/Latin/result/augustus_res_gestae_1/25-34/non_running/")
    assert response.status_code == 200

def test_select_simple_ovid_in_ibin():
    response = client.get("/select/Latin/result/ovid_in_ibin/59-120/non_running/")
    assert response.status_code == 200

def test_select_concat_aesop_fables_herodotus_book_1():
    response = client.get("/select/Greek/result/aesop_fables+herodotus_book_1/start+start-end+end/non_running/")
    assert response.status_code == 200

def test_select_simple_pseudo_caesar_bellum_alexandrinum():
    response = client.get("/select/Latin/result/pseudo-caesar_bellum_alexandrinum/integra-tradit/non_running/")
    assert response.status_code == 200

def test_select_full_concat_dcc_latin_core_gsce_rvl():
    response = client.get("/select/Latin/result/dcc_latin_core+gsce_rvl/192+45-515+85/include/elizabeth_jane_weston_ad_schosserum/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_bernardo_de_riofrio_centonicum_virgilianum_monimentum():
    response = client.get("/select/Latin/result/bernardo_de_riofrio_centonicum_virgilianum_monimentum/52-122/include/ovid_ars_amatoria/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_cicero_pro_cluentio():
    response = client.get("/select/Latin/result/cicero_pro_cluentio/186.5-192.7/include/plautus_curculio/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_seneca_de_vita_beata():
    response = client.get("/select/Latin/result/seneca_de_vita_beata/13.2-22.2/non_running/")
    assert response.status_code == 200

def test_select_full_epitaph_of_allia_potestas_cil_637966():
    response = client.get("/select/Latin/result/epitaph_of_allia_potestas_cil_637966/12-34/include/seneca_troades/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_cicero_post_reditum_ad_quirites():
    response = client.get("/select/Latin/result/cicero_post_reditum_ad_quirites/9.4-18.13/non_running/")
    assert response.status_code == 200

def test_select_full_hartnett_by_roman_hands():
    response = client.get("/select/Latin/result/hartnett_by_roman_hands/123-141/include/vulgate_gospel_of_john/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_caesar_bellum_gallicum():
    response = client.get("/select/Latin/result/caesar_bellum_gallicum/6.44.3-7.47.4/non_running/")
    assert response.status_code == 200

def test_select_simple_pseudo_caesar_bellum_hispanum():
    response = client.get("/select/Latin/result/pseudo-caesar_bellum_hispanum/27.5-19.2/non_running/")
    assert response.status_code == 200

def test_select_full_concat_seneca_medea_bede_historia_ecclesiastica_gentis_anglorum_prologue_11_125_26_21_2_12_14_16_20_31_3_5_6():
    response = client.get("/select/Latin/result/seneca_medea+bede_historia_ecclesiastica_gentis_anglorum_prologue_11_125-26_21-2_12-14_16_20_31-3_5-6/88+2.9-516+2.12/include/claudian_epithalamium_de_nuptii_honorii_augusti/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_classical_latin_mckeown():
    response = client.get("/select/Latin/result/classical_latin_mckeown/21-24/non_running/")
    assert response.status_code == 200

def test_select_full_jenney_first_year_latin_red():
    response = client.get("/select/Latin/result/jenney_first_year_latin_red/15-24/include/seneca_phaedra/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_carmina_burana_orff_latin_lyrics_1_5_11_15_17_25():
    response = client.get("/select/Latin/result/carmina_burana_orff_latin_lyrics_1-5_11-15_17-25/12.14-24.6/include/seneca_troades/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_apuleius_apology():
    response = client.get("/select/Latin/result/apuleius_apology/38.6-83.11/non_running/")
    assert response.status_code == 200

def test_select_full_cicero_pro_murena():
    response = client.get("/select/Latin/result/cicero_pro_murena/20.8-61.10/include/cicero_in_verrem_actio_secunda/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_claudian_panegyricus_dictus_manlio_theodoro_consuli_preface():
    response = client.get("/select/Latin/result/claudian_panegyricus_dictus_manlio_theodoro_consuli_preface/267-287/non_running/")
    assert response.status_code == 200

def test_select_simple_marie_de_france_fables_1_22():
    response = client.get("/select/Latin/result/marie_de_france_fables_1-22/21-22/non_running/")
    assert response.status_code == 200

def test_select_simple_seneca_de_ira():
    response = client.get("/select/Latin/result/seneca_de_ira/3.11.4-3.24.1/non_running/")
    assert response.status_code == 200

def test_select_concat_apollonius_argonautica_book_4_dcc_greek_core_list():
    response = client.get("/select/Greek/result/apollonius_argonautica_book_4+dcc_greek_core_list/start+start-end+end/non_running/")
    assert response.status_code == 200

def test_select_full_ovid_medicamina_faciei_femineae():
    response = client.get("/select/Latin/result/ovid_medicamina_faciei_femineae/41-94/include/livy_ab_urbe_condita_ib_list_2_selections/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_apuleius_de_mundo():
    response = client.get("/select/Latin/result/apuleius_de_mundo/1.2-34.18/include/oxford_latin_course_for_college/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_concat_piantaggini_livia_mater_eloquen_jenney_first_year_latin_red():
    response = client.get("/select/Latin/result/piantaggini_livia_mater_eloquen+jenney_first_year_latin_red/2.4+26-2.11+27/include/diederich_frequency_list_medieval/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_marie_de_france_fables_1_22():
    response = client.get("/select/Latin/result/marie_de_france_fables_1-22/21-22/include/tacitus_germania/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_cicero_de_lege_agraria():
    response = client.get("/select/Latin/result/cicero_de_lege_agraria/57.11-99.14/non_running/")
    assert response.status_code == 200

def test_select_concat_aesop_fables_apollonius_argonautica_book_4():
    response = client.get("/select/Greek/result/aesop_fables+apollonius_argonautica_book_4/start+start-end+end/non_running/")
    assert response.status_code == 200

def test_select_simple_cicero_de_imperio_pompei():
    response = client.get("/select/Latin/result/cicero_de_imperio_pompei/9.4-13.6/non_running/")
    assert response.status_code == 200

def test_select_simple_seneca_ad_marciam_de_consolatione():
    response = client.get("/select/Latin/result/seneca_ad_marciam_de_consolatione/18.3-18.5/non_running/")
    assert response.status_code == 200

def test_select_concat_gsce_dvl_tibullus_elegies():
    response = client.get("/select/Latin/result/gsce_dvl+tibullus_elegies/158+3.7.198-326+3.12.3/non_running/")
    assert response.status_code == 200

def test_select_full_elizabeth_jane_weston_ad_matthiam_secundum():
    response = client.get("/select/Latin/result/elizabeth_jane_weston_ad_matthiam_secundum/1.14-1.44/include/jerome_life_of_malchus_dcc/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_suburani_fabulae():
    response = client.get("/select/Latin/result/suburani_fabulae/20.1-32.2/non_running/")
    assert response.status_code == 200

def test_select_full_pervigilium_veneris():
    response = client.get("/select/Latin/result/pervigilium_veneris/76-83/include/claudian_de_raptu_prosperinae_prefaces/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_tacitus_historiae():
    response = client.get("/select/Latin/result/tacitus_historiae/3.18.6-4.22.8/non_running/")
    assert response.status_code == 200

def test_select_full_cicero_pro_quinctio():
    response = client.get("/select/Latin/result/cicero_pro_quinctio/1.5-16.12/include/latin_for_the_new_millennium_vols_1_and_2_tunberg-minkova/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_fabulae_faciles_ritchie():
    response = client.get("/select/Latin/result/fabulae_faciles_ritchie/3.59-3.71/non_running/")
    assert response.status_code == 200

def test_select_simple_martial_book_10():
    response = client.get("/select/Latin/result/martial_book_10/10.85.1-10.85.7/non_running/")
    assert response.status_code == 200

def test_select_full_seneca_apocolocyntosis():
    response = client.get("/select/Latin/result/seneca_apocolocyntosis/4.1.27-7.2.8/include/physiologus_latina_1-6_9_16_17_23/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_cicero_de_domo_sua():
    response = client.get("/select/Latin/result/cicero_de_domo_sua/95.1-98.3/non_running/")
    assert response.status_code == 200

def test_select_simple_cicero_pro_cluentio():
    response = client.get("/select/Latin/result/cicero_pro_cluentio/186.5-192.7/non_running/")
    assert response.status_code == 200

def test_select_full_persius_satires():
    response = client.get("/select/Latin/result/persius_satires/0.8-5.107/include/claudian_panegyricus_dictus_manlio_theodoro_consuli_preface/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_pliny_the_younger_panegyricu():
    response = client.get("/select/Latin/result/pliny_the_younger_panegyricu/95.4-95.5/non_running/")
    assert response.status_code == 200

def test_select_full_pseudo_caesar_bellum_hispanum():
    response = client.get("/select/Latin/result/pseudo-caesar_bellum_hispanum/27.5-19.2/include/ocr_as_level_defined_vocabulary_list/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_pervigilium_veneris():
    response = client.get("/select/Latin/result/pervigilium_veneris/76-83/non_running/")
    assert response.status_code == 200

def test_select_simple_hrotswitha_dulcitius():
    response = client.get("/select/Latin/result/hrotswitha_dulcitius/1.1-5.1/non_running/")
    assert response.status_code == 200

def test_select_full_tacitus_germania():
    response = client.get("/select/Latin/result/tacitus_germania/37.5-46.1/include/florus_epitome_11_romulus_and_roman_kings/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_seneca_naturales_quaestiones___dcc():
    response = client.get("/select/Latin/result/seneca_naturales_quaestiones_-_dcc/3.0.1-2.38.1/non_running/")
    assert response.status_code == 200

def test_select_simple_augustine_confessions_book_1():
    response = client.get("/select/Latin/result/augustine_confessions_book_1/1.18.29-1.20.31/non_running/")
    assert response.status_code == 200

def test_select_full_newton_axiomata_motus():
    response = client.get("/select/Latin/result/newton_axiomata_motus/2-3/include/newton_axiomata_motus/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_eutropius_breviarium_book_3_beyer():
    response = client.get("/select/Latin/result/eutropius_breviarium_book_3_beyer/3.20-3.21/non_running/")
    assert response.status_code == 200

def test_select_full_concat_athenaze_an_introduction_to_ancient_greek_herodotus_book_1_high_frequency_vocabulary_list():
    response = client.get("/select/Greek/result/athenaze_an_introduction_to_ancient_greek+herodotus_book_1_high_frequency_vocabulary_list/start+start-end+end/include/demonsthenes_against_neaira/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_cicero_pro_flacco():
    response = client.get("/select/Latin/result/cicero_pro_flacco/94.3-98.2/non_running/")
    assert response.status_code == 200

def test_select_simple_puer_romanus():
    response = client.get("/select/Latin/result/puer_romanus/18.1-23.2/non_running/")
    assert response.status_code == 200

def test_select_simple_wheelock_latin_exercitationes():
    response = client.get("/select/Latin/result/wheelock_latin_exercitationes/34.10-37.2/non_running/")
    assert response.status_code == 200

def test_select_full_ocr_as():
    response = client.get("/select/Latin/result/ocr_as/536-627/include/tacitus_dialogus_de_oratoribus/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_passio_santarum_perpetuae_et_felicitatis():
    response = client.get("/select/Latin/result/passio_santarum_perpetuae_et_felicitatis/11.7-18.9/non_running/")
    assert response.status_code == 200

def test_select_full_aesop_romulus_anglicus_1_10():
    response = client.get("/select/Latin/result/aesop_romulus_anglicus_1-10/7-10/include/latin_stopwords_list_cltk/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_claudian_de_raptu_prosperinae_prefaces():
    response = client.get("/select/Latin/result/claudian_de_raptu_prosperinae_prefaces/2.5-2.7/include/colby_latin_list_years_1_3_4/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_claudian_carmina_minora_25_preface():
    response = client.get("/select/Latin/result/claudian_carmina_minora_25_preface/177-244/include/ovid_amores/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_horace_epistulae():
    response = client.get("/select/Latin/result/horace_epistulae/1.17.42-1.17.43/non_running/")
    assert response.status_code == 200

def test_select_full_ecce_romani_chs_1_54():
    response = client.get("/select/Latin/result/ecce_romani_chs_1-54/23-34/include/cicero_de_lege_agraria/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_elizabeth_jane_weston_parthenica():
    response = client.get("/select/Latin/result/elizabeth_jane_weston_parthenica/2.102.34-3.1b.26/non_running/")
    assert response.status_code == 200

def test_select_full_seneca_pseudo_proverbia_or_de_moribu():
    response = client.get("/select/Latin/result/seneca_pseudo_proverbia_or_de_moribu/34-121/include/elizabeth_jane_weston_poemata/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_augustus_res_gestae_1():
    response = client.get("/select/Latin/result/augustus_res_gestae_1/25-34/include/seneca_pseudo_proverbia_or_de_moribu/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_cato_monostichs():
    response = client.get("/select/Latin/result/cato_monostichs/54-55/include/elizabeth_jane_weston_in_obitum_ioannae/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_livy_ab_urbe_condita_ib_list_2_selections():
    response = client.get("/select/Latin/result/livy_ab_urbe_condita_ib_list_2_selections/1.59.5-3.44.1/include/seneca_de_constantia/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_apollonius_argonautica_book_4():
    response = client.get("/select/Greek/result/apollonius_argonautica_book_4/start-end/include/hansen_quinn_greek_an_intensive_course/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_diederich_frequency_list_medieval():
    response = client.get("/select/Latin/result/diederich_frequency_list_medieval/596-1368/include/cicero_pro_fonteio_excluding_fragments/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_vulgate_gospel_of_john():
    response = client.get("/select/Latin/result/vulgate_gospel_of_john/2.13-7.26/non_running/")
    assert response.status_code == 200

def test_select_full_ovid_amores_1_dcc():
    response = client.get("/select/Latin/result/ovid_amores_1_dcc/7.60-9.42/include/eutropius_breviarium_book_3_beyer/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_diederich_frequency_list_prose():
    response = client.get("/select/Latin/result/diederich_frequency_list_prose/2292-2336/non_running/")
    assert response.status_code == 200

def test_select_full_puer_romanus():
    response = client.get("/select/Latin/result/puer_romanus/18.1-23.2/include/seneca_ad_lucilium_epistulae_morales/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_landivar_rusticatio_mexicana_book_6():
    response = client.get("/select/Latin/result/landivar_rusticatio_mexicana_book_6/propinquum-seriem/include/apuleius_de_deo_socratis/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_pseudo_caesar_bellum_alexandrinum():
    response = client.get("/select/Latin/result/pseudo-caesar_bellum_alexandrinum/integra-tradit/include/oxford_latin_course_for_college_fabulae_all/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_fabulae_ab_urbe_condita_sandford_scott():
    response = client.get("/select/Latin/result/fabulae_ab_urbe_condita_sandford-scott/18-19/include/cicero_pro_milone/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_a_primer_of_ecclesiastical_latin_collins():
    response = client.get("/select/Latin/result/a_primer_of_ecclesiastical_latin_collins/11-21/non_running/")
    assert response.status_code == 200

def test_select_full_concat_gsce_rvl_egeria_itinerarium_book_1():
    response = client.get("/select/Latin/result/gsce_rvl+egeria_itinerarium_book_1/100+16.4-121+20.9/include/cicero_pro_quinctio/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_bede_historia_ecclesiastica_gentis_anglorum_prologue_11_125_26_21_2_12_14_16_20_31_3_5_6():
    response = client.get("/select/Latin/result/bede_historia_ecclesiastica_gentis_anglorum_prologue_11_125-26_21-2_12-14_16_20_31-3_5-6/3.5-3.6/include/hildegard_of_bingen_scivias_72/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_elizabeth_jane_weston_ad_matthiam_secundum():
    response = client.get("/select/Latin/result/elizabeth_jane_weston_ad_matthiam_secundum/1.14-1.44/non_running/")
    assert response.status_code == 200

def test_select_full_ovid_amores():
    response = client.get("/select/Latin/result/ovid_amores/2.16.41-3.6.87/include/apuleius_de_deo_socratis/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_claudian_panegyricus_de_iii_consulatu_honorii_augusti():
    response = client.get("/select/Latin/result/claudian_panegyricus_de_iii_consulatu_honorii_augusti/453-521/include/cicero_pro_fonteio_excluding_fragments/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_ovid_remedia_amoris():
    response = client.get("/select/Latin/result/ovid_remedia_amoris/770-792/non_running/")
    assert response.status_code == 200

def test_select_simple_vergil_eclogues_1_dcc():
    response = client.get("/select/Latin/result/vergil_eclogues_1_dcc/1.3-1.68/non_running/")
    assert response.status_code == 200

def test_select_full_nepos_life_of_hannibal():
    response = client.get("/select/Latin/result/nepos_life_of_hannibal/2.5-13.2/include/ovid_remedia_amoris/start-end/non_running/")
    assert response.status_code == 200

def test_select_concat_physiologus_latina_1_6_9_16_17_23_seneca_ad_polybium_de_consolatione():
    response = client.get("/select/Latin/result/physiologus_latina_1-6_9_16_17_23+seneca_ad_polybium_de_consolatione/6.11+4.3-23.46+11.6/non_running/")
    assert response.status_code == 200

def test_select_full_concat_trotula_de_curis_mulierum_74_78_86_87_167_168_174_178_181_182_cicero_somnium_scipionis_9_29():
    response = client.get("/select/Latin/result/trotula_de_curis_mulierum_74-78_86-87_167-168_174-178_181-182+cicero_somnium_scipionis_9-29/77+28-86+29/include/seneca_ad_polybium_de_consolatione/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_newton_regulae_philosophandi():
    response = client.get("/select/Latin/result/newton_regulae_philosophandi/1.2-3.3/non_running/")
    assert response.status_code == 200

def test_select_full_concat_gsce_dvl_tibullus_elegies():
    response = client.get("/select/Latin/result/gsce_dvl+tibullus_elegies/158+3.7.198-326+3.12.3/include/propertius_elegies/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_suetonius_life_of_caligula():
    response = client.get("/select/Latin/result/suetonius_life_of_caligula/54-56/include/tacitus_dialogus_de_oratoribus/start-end/non_running/")
    assert response.status_code == 200

def test_select_concat_aeschylus_prometheus_bound_homer_core_list_frequency_categories_1_4():
    response = client.get("/select/Greek/result/aeschylus_prometheus_bound+homer_core_list_frequency_categories_1-4/start+start-end+end/non_running/")
    assert response.status_code == 200

def test_select_full_elizabeth_jane_weston_de_ebrietate():
    response = client.get("/select/Latin/result/elizabeth_jane_weston_de_ebrietate/54.19-54.41/include/claudian_carmina_minora_25_preface/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_claudian_in_rufinum_prefaces():
    response = client.get("/select/Latin/result/claudian_in_rufinum_prefaces/2.5-2.11/non_running/")
    assert response.status_code == 200

def test_select_simple_seneca_oedipus():
    response = client.get("/select/Latin/result/seneca_oedipus/560-645/non_running/")
    assert response.status_code == 200

def test_select_full_concat_homer_core_list_frequency_categories_1_4_herodotus_book_1_high_frequency_vocabulary_list():
    response = client.get("/select/Greek/result/homer_core_list_frequency_categories_1-4+herodotus_book_1_high_frequency_vocabulary_list/start+start-end+end/include/homer_core_list_frequency_categories_1-4/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_civis_romanus_a_reader_for_the_first_two_years_of_latin_cobban_and_colebourn():
    response = client.get("/select/Latin/result/civis_romanus_a_reader_for_the_first_two_years_of_latin_cobban_and_colebourn/50-57/non_running/")
    assert response.status_code == 200

def test_select_full_horace_epistulae():
    response = client.get("/select/Latin/result/horace_epistulae/1.17.42-1.17.43/include/nepos_life_of_hamilcar/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_cicero_pro_marco_tullio():
    response = client.get("/select/Latin/result/cicero_pro_marco_tullio/36.1-Fr.1.7/non_running/")
    assert response.status_code == 200

def test_select_simple_cicero_pro_balbo():
    response = client.get("/select/Latin/result/cicero_pro_balbo/51.12-61.2/non_running/")
    assert response.status_code == 200

def test_select_simple_abelard_historia_selections():
    response = client.get("/select/Latin/result/abelard_historia_selections/5-6/non_running/")
    assert response.status_code == 200

def test_select_full_claudian_panegyricus_de_vi_consulatu_honorii_augusti():
    response = client.get("/select/Latin/result/claudian_panegyricus_de_vi_consulatu_honorii_augusti/101-416/include/cicero_in_vatinium/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_aeschylus_prometheus_bound():
    response = client.get("/select/Greek/result/aeschylus_prometheus_bound/start-end/include/homer_core_list_frequency_categories_1-4/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_ilias_latina():
    response = client.get("/select/Latin/result/ilias_latina/817-1047/non_running/")
    assert response.status_code == 200

def test_select_simple_seneca_de_otio():
    response = client.get("/select/Latin/result/seneca_de_otio/3.1-5.4/non_running/")
    assert response.status_code == 200

def test_select_full_cicero_de_officiis():
    response = client.get("/select/Latin/result/cicero_de_officiis/1.100.3-2.80.3/include/apuleius_de_deo_socratis_prologue/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_concat_apollonius_argonautica_book_4_dcc_greek_core_list():
    response = client.get("/select/Greek/result/apollonius_argonautica_book_4+dcc_greek_core_list/start+start-end+end/include/herodotus_book_1_high_frequency_vocabulary_list/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_elizabeth_jane_weston_poemata():
    response = client.get("/select/Latin/result/elizabeth_jane_weston_poemata/2.90.45-2.94.59/non_running/")
    assert response.status_code == 200

def test_select_simple_cicero_de_officiis():
    response = client.get("/select/Latin/result/cicero_de_officiis/1.100.3-2.80.3/non_running/")
    assert response.status_code == 200

def test_select_full_concat_aeschylus_prometheus_bound_hansen_quinn_greek_an_intensive_course():
    response = client.get("/select/Greek/result/aeschylus_prometheus_bound+hansen_quinn_greek_an_intensive_course/start+start-end+end/include/herodotus_book_1_high_frequency_vocabulary_list/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_concat_pseudo_caesar_bellum_alexandrinum_claudian_panegyricus_dictus_manlio_theodoro_consuli():
    response = client.get("/select/Latin/result/pseudo-caesar_bellum_alexandrinum+claudian_panegyricus_dictus_manlio_theodoro_consuli/instructa+130-nomine+174/include/cicero_in_catilinam_1-4/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_seneca_hercules_oetaeus():
    response = client.get("/select/Latin/result/seneca_hercules_oetaeus/1752-1940/include/apuleius_florida/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_hildegard_of_bingen_scivias_72():
    response = client.get("/select/Latin/result/hildegard_of_bingen_scivias_72/7.3-7.4/include/elizabeth_jane_weston_carmen_ad_rudolphum_ii/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_eduqas_gsce_defined_vocablary_list():
    response = client.get("/select/Latin/result/eduqas_gsce_defined_vocablary_list/180-367/include/cicero_pro_rabirio_postumo/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_jenney_first_year_latin_purple_jenney_scudder_baade():
    response = client.get("/select/Latin/result/jenney_first_year_latin_purple_jenney-scudder-baade/6-30/non_running/")
    assert response.status_code == 200

def test_select_simple_plautus_amphitruo():
    response = client.get("/select/Latin/result/plautus_amphitruo/899-1103/non_running/")
    assert response.status_code == 200

def test_select_simple_athenaze_an_introduction_to_ancient_greek():
    response = client.get("/select/Greek/result/athenaze_an_introduction_to_ancient_greek/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_hartnett_by_roman_hands():
    response = client.get("/select/Latin/result/hartnett_by_roman_hands/123-141/non_running/")
    assert response.status_code == 200

def test_select_simple_disce_kitchell_sienkewicz():
    response = client.get("/select/Latin/result/disce_kitchell-sienkewicz/17-24/non_running/")
    assert response.status_code == 200

def test_select_simple_tacitus_germania():
    response = client.get("/select/Latin/result/tacitus_germania/37.5-46.1/non_running/")
    assert response.status_code == 200

def test_select_full_concat_herodotus_book_1_aeschylus_prometheus_bound():
    response = client.get("/select/Greek/result/herodotus_book_1+aeschylus_prometheus_bound/start+start-end+end/include/aesop_fables/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_cicero_pro_milone():
    response = client.get("/select/Latin/result/cicero_pro_milone/78.9-100.9/non_running/")
    assert response.status_code == 200

def test_select_concat_herodotus_book_1_demonsthenes_against_neaira():
    response = client.get("/select/Greek/result/herodotus_book_1+demonsthenes_against_neaira/start+start-end+end/non_running/")
    assert response.status_code == 200

def test_select_full_seneca_de_vita_beata():
    response = client.get("/select/Latin/result/seneca_de_vita_beata/13.2-22.2/include/apuleius_apology/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_claudian_de_raptu_prosperinae():
    response = client.get("/select/Latin/result/claudian_de_raptu_prosperinae/1.235-2.26/include/ovid_metamorphoses_1-6_11_15/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_hildegard_of_bingen_symphoniae_2_5_10_11_12_17_19_21_23_64():
    response = client.get("/select/Latin/result/hildegard_of_bingen_symphoniae_2-5_10_11_12_17_19_21_23_64/4.2-23.2/non_running/")
    assert response.status_code == 200

def test_select_full_vergil_aeneid_ap_selections():
    response = client.get("/select/Latin/result/vergil_aeneid_ap_selections/2.209-4.702/include/augustine_confessions_book_1/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_seneca_pseudo_proverbia_or_de_moribu():
    response = client.get("/select/Latin/result/seneca_pseudo_proverbia_or_de_moribu/34-121/non_running/")
    assert response.status_code == 200

def test_select_simple_cicero_in_verrem_actio_prima():
    response = client.get("/select/Latin/result/cicero_in_verrem_actio_prima/52.11-53.8/non_running/")
    assert response.status_code == 200

def test_select_simple_new_latin_primer_english_irby():
    response = client.get("/select/Latin/result/new_latin_primer_english-irby/30-32/non_running/")
    assert response.status_code == 200

def test_select_simple_claudian_panegyricus_dictus_manlio_theodoro_consuli():
    response = client.get("/select/Latin/result/claudian_panegyricus_dictus_manlio_theodoro_consuli/316-322/non_running/")
    assert response.status_code == 200

def test_select_concat_seneca_medea_bede_historia_ecclesiastica_gentis_anglorum_prologue_11_125_26_21_2_12_14_16_20_31_3_5_6():
    response = client.get("/select/Latin/result/seneca_medea+bede_historia_ecclesiastica_gentis_anglorum_prologue_11_125-26_21-2_12-14_16_20_31-3_5-6/88+2.9-516+2.12/non_running/")
    assert response.status_code == 200

def test_select_concat_gsce_rvl_egeria_itinerarium_book_1():
    response = client.get("/select/Latin/result/gsce_rvl+egeria_itinerarium_book_1/100+16.4-121+20.9/non_running/")
    assert response.status_code == 200

def test_select_full_civis_romanus_a_reader_for_the_first_two_years_of_latin_cobban_and_colebourn():
    response = client.get("/select/Latin/result/civis_romanus_a_reader_for_the_first_two_years_of_latin_cobban_and_colebourn/50-57/include/bernardo_de_riofrio_centonicum_virgilianum_monimentum/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_cicero_pro_rabirio_perduellionis_reo():
    response = client.get("/select/Latin/result/cicero_pro_rabirio_perduellionis_reo/18.11-27.11/non_running/")
    assert response.status_code == 200

def test_select_concat_herodotus_book_1_hansen_quinn_greek_an_intensive_course():
    response = client.get("/select/Greek/result/herodotus_book_1+hansen_quinn_greek_an_intensive_course/start+start-end+end/non_running/")
    assert response.status_code == 200

def test_select_simple_physiologus_latina_1_6_9_16_17_23():
    response = client.get("/select/Latin/result/physiologus_latina_1-6_9_16_17_23/23.23-23.35/non_running/")
    assert response.status_code == 200

def test_select_full_cicero_in_verrem_actio_prima():
    response = client.get("/select/Latin/result/cicero_in_verrem_actio_prima/52.11-53.8/include/cicero_in_catilinam_1-4/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_florus_epitome_11_romulus_and_roman_kings():
    response = client.get("/select/Latin/result/florus_epitome_11_romulus_and_roman_kings/1.1.6-1.1.7/non_running/")
    assert response.status_code == 200

def test_select_simple_prudentius_psychomachia_preface():
    response = client.get("/select/Latin/result/prudentius_psychomachia_preface/60-63/non_running/")
    assert response.status_code == 200

def test_select_full_trotula_de_curis_mulierum_74_78_86_87_167_168_174_178_181_182():
    response = client.get("/select/Latin/result/trotula_de_curis_mulierum_74-78_86-87_167-168_174-178_181-182/176-177/include/bede_historia_ecclesiastica_gentis_anglorum_prologue_11_125-26_21-2_12-14_16_20_31-3_5-6/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_eduqas_gsce_defined_vocablary_list():
    response = client.get("/select/Latin/result/eduqas_gsce_defined_vocablary_list/180-367/non_running/")
    assert response.status_code == 200

def test_select_full_concat_claudian_panegyricus_de_vi_consulatu_honorii_augusti_preface_claudian_panegyricus_dictus_manlio_theodoro_consuli():
    response = client.get("/select/Latin/result/claudian_panegyricus_de_vi_consulatu_honorii_augusti_preface+claudian_panegyricus_dictus_manlio_theodoro_consuli/3+83-16+232/include/vergil_aeneid_new_ap_selections/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_apuleius_metamorphoses_finkelpearl():
    response = client.get("/select/Latin/result/apuleius_metamorphoses_finkelpearl/10.17.6-11.5.1/non_running/")
    assert response.status_code == 200

def test_select_simple_caesar_bellum_civile():
    response = client.get("/select/Latin/result/caesar_bellum_civile/3.84.3-3.112.4/non_running/")
    assert response.status_code == 200

def test_select_simple_trotula_de_curis_mulierum_74_78_86_87_167_168_174_178_181_182():
    response = client.get("/select/Latin/result/trotula_de_curis_mulierum_74-78_86-87_167-168_174-178_181-182/176-177/non_running/")
    assert response.status_code == 200

def test_select_full_demonsthenes_against_neaira():
    response = client.get("/select/Greek/result/demonsthenes_against_neaira/start-end/include/demonsthenes_against_neaira/start-end/non_running/")
    assert response.status_code == 200

def test_select_concat_demonsthenes_against_neaira_apollonius_argonautica_book_4():
    response = client.get("/select/Greek/result/demonsthenes_against_neaira+apollonius_argonautica_book_4/start+start-end+end/non_running/")
    assert response.status_code == 200

def test_select_full_concat_egeria_itinerarium_book_1_ovid_halieutica():
    response = client.get("/select/Latin/result/egeria_itinerarium_book_1+ovid_halieutica/6.1+134-13.4+135/include/ocr_as_level_defined_vocabulary_list/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_hildegard_of_bingen_symphoniae_2_5_10_11_12_17_19_21_23_64():
    response = client.get("/select/Latin/result/hildegard_of_bingen_symphoniae_2-5_10_11_12_17_19_21_23_64/4.2-23.2/include/seneca_ad_marciam_de_consolatione/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_ocr_gsce_restricted_vocabulary_list():
    response = client.get("/select/Latin/result/ocr_gsce_restricted_vocabulary_list/25-123/non_running/")
    assert response.status_code == 200

def test_select_full_cicero_in_catilinam_1_4():
    response = client.get("/select/Latin/result/cicero_in_catilinam_1-4/3.12.10-4.17.6/include/jenney_first_year_latin_purple_jenney-scudder-baade/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_tacitus_dialogus_de_oratoribus():
    response = client.get("/select/Latin/result/tacitus_dialogus_de_oratoribus/18.3-28.5/non_running/")
    assert response.status_code == 200

def test_select_full_concat_aesop_fables_dcc_greek_core_list():
    response = client.get("/select/Greek/result/aesop_fables+dcc_greek_core_list/start+start-end+end/include/groton_from_alpha_to_omega/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_propertius_elegies():
    response = client.get("/select/Latin/result/propertius_elegies/3.18.5-4.3.9/non_running/")
    assert response.status_code == 200

def test_select_simple_nepos_life_of_hannibal():
    response = client.get("/select/Latin/result/nepos_life_of_hannibal/2.5-13.2/non_running/")
    assert response.status_code == 200

def test_select_full_claudian_panegyricus_dictus_manlio_theodoro_consuli_preface():
    response = client.get("/select/Latin/result/claudian_panegyricus_dictus_manlio_theodoro_consuli_preface/267-287/include/claudian_de_raptu_prosperinae_prefaces/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_pseudo_caesar_bellum_africanum():
    response = client.get("/select/Latin/result/pseudo-caesar_bellum_africanum/58.1-70.7/non_running/")
    assert response.status_code == 200

def test_select_full_caesar_bellum_gallicum():
    response = client.get("/select/Latin/result/caesar_bellum_gallicum/6.44.3-7.47.4/include/eduqas/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_diederich_frequency_list_medieval():
    response = client.get("/select/Latin/result/diederich_frequency_list_medieval/596-1368/non_running/")
    assert response.status_code == 200

def test_select_simple_cicero_in_calpurnium_pisonem():
    response = client.get("/select/Latin/result/cicero_in_calpurnium_pisonem/32.5-48.7/non_running/")
    assert response.status_code == 200

def test_select_full_elizabeth_jane_weston_carmen_ad_rudolphum_ii():
    response = client.get("/select/Latin/result/elizabeth_jane_weston_carmen_ad_rudolphum_ii/3.25-5z.0/include/hildegard_of_bingen_scivias_72/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_claudian_de_bello_gildonico():
    response = client.get("/select/Latin/result/claudian_de_bello_gildonico/281-391/non_running/")
    assert response.status_code == 200

def test_select_full_concat_dcc_greek_core_list_apollonius_argonautica_book_4():
    response = client.get("/select/Greek/result/dcc_greek_core_list+apollonius_argonautica_book_4/start+start-end+end/include/dcc_greek_core_list/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_seneca_ad_polybium_de_consolatione():
    response = client.get("/select/Latin/result/seneca_ad_polybium_de_consolatione/12.4-15.3/non_running/")
    assert response.status_code == 200

def test_select_full_concat_herodotus_book_1_hansen_quinn_greek_an_intensive_course():
    response = client.get("/select/Greek/result/herodotus_book_1+hansen_quinn_greek_an_intensive_course/start+start-end+end/include/athenaze_an_introduction_to_ancient_greek/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_latin_an_intensive_course_moreland_fleischer():
    response = client.get("/select/Latin/result/latin_an_intensive_course_moreland-fleischer/5-13/non_running/")
    assert response.status_code == 200

def test_select_simple_bede_historia_ecclesiastica_gentis_anglorum_prologue_11_125_26_21_2_12_14_16_20_31_3_5_6():
    response = client.get("/select/Latin/result/bede_historia_ecclesiastica_gentis_anglorum_prologue_11_125-26_21-2_12-14_16_20_31-3_5-6/3.5-3.6/non_running/")
    assert response.status_code == 200

def test_select_full_seneca_troades():
    response = client.get("/select/Latin/result/seneca_troades/505-530/include/jerome_life_of_malchus_dcc/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_suburani_fabulae():
    response = client.get("/select/Latin/result/suburani_fabulae/20.1-32.2/include/claudian_in_rufinum_prefaces/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_cato_monostichs():
    response = client.get("/select/Latin/result/cato_monostichs/54-55/non_running/")
    assert response.status_code == 200

def test_select_simple_cicero_pro_quinctio():
    response = client.get("/select/Latin/result/cicero_pro_quinctio/1.5-16.12/non_running/")
    assert response.status_code == 200

def test_select_simple_ovid_metamorphoses_1_6_11_15():
    response = client.get("/select/Latin/result/ovid_metamorphoses_1-6_11_15/15.801-15.868/non_running/")
    assert response.status_code == 200

def test_select_full_jerome_life_of_malchus_dcc():
    response = client.get("/select/Latin/result/jerome_life_of_malchus_dcc/9.10-10.2/include/dcc_latin_core/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_vergil_aeneid_new_ap_selections():
    response = client.get("/select/Latin/result/vergil_aeneid_new_ap_selections/4.361-11.588/non_running/")
    assert response.status_code == 200

def test_select_full_martial_book_10():
    response = client.get("/select/Latin/result/martial_book_10/10.85.1-10.85.7/include/ecce_romani_chs_1-54/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_claudian_de_bello_gildonico():
    response = client.get("/select/Latin/result/claudian_de_bello_gildonico/281-391/include/seneca_de_ira/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_seneca_medea():
    response = client.get("/select/Latin/result/seneca_medea/333-753/include/cambridge_latin_course/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_elizabeth_jane_weston_elegia_consolatoria_ad_havlik():
    response = client.get("/select/Latin/result/elizabeth_jane_weston_elegia_consolatoria_ad_havlik/1.3-1.4/include/carmina_priapea_1-80/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_seneca_de_constantia():
    response = client.get("/select/Latin/result/seneca_de_constantia/16.1-16.4/include/bede_historia_ecclesiastica_gentis_anglorum_prologue_11_125-26_21-2_12-14_16_20_31-3_5-6/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_seneca_phoenissae():
    response = client.get("/select/Latin/result/seneca_phoenissae/602-650/include/cicero_pro_marcello/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_cicero_pro_flacco():
    response = client.get("/select/Latin/result/cicero_pro_flacco/94.3-98.2/include/tacitus_germania/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_concat_aesop_fables_groton_from_alpha_to_omega():
    response = client.get("/select/Greek/result/aesop_fables+groton_from_alpha_to_omega/start+start-end+end/include/dcc_greek_core_list/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_homer_core_list_frequency_categories_1_4():
    response = client.get("/select/Greek/result/homer_core_list_frequency_categories_1-4/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_demonsthenes_against_neaira():
    response = client.get("/select/Greek/result/demonsthenes_against_neaira/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_elizabeth_jane_weston_ad_schosserum():
    response = client.get("/select/Latin/result/elizabeth_jane_weston_ad_schosserum/7.7-7.9/non_running/")
    assert response.status_code == 200

def test_select_simple_elizabeth_jane_weston_in_obitum_ioannae():
    response = client.get("/select/Latin/result/elizabeth_jane_weston_in_obitum_ioannae/1.14-1.85/non_running/")
    assert response.status_code == 200

def test_select_full_concat_aeschylus_prometheus_bound_homer_core_list_frequency_categories_1_4():
    response = client.get("/select/Greek/result/aeschylus_prometheus_bound+homer_core_list_frequency_categories_1-4/start+start-end+end/include/athenaze_an_introduction_to_ancient_greek/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_apuleius_metamorphoses_finkelpearl():
    response = client.get("/select/Latin/result/apuleius_metamorphoses_finkelpearl/10.17.6-11.5.1/include/newton_regulae_philosophandi/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_cicero_post_reditum_ad_quirites():
    response = client.get("/select/Latin/result/cicero_post_reditum_ad_quirites/9.4-18.13/include/horace_ars_poetica/start-end/non_running/")
    assert response.status_code == 200

def test_select_simple_petrionius_satyricon():
    response = client.get("/select/Latin/result/petrionius_satyricon/22-55/non_running/")
    assert response.status_code == 200

def test_select_simple_corderius_colloquia_book_2():
    response = client.get("/select/Latin/result/corderius_colloquia_book_2/2.10-2.67/non_running/")
    assert response.status_code == 200

def test_select_full_newton_regulae_philosophandi():
    response = client.get("/select/Latin/result/newton_regulae_philosophandi/1.2-3.3/include/seneca_de_brevitate_vitae/start-end/non_running/")
    assert response.status_code == 200

def test_select_full_concat_demonsthenes_against_neaira_apollonius_argonautica_book_4():
    response = client.get("/select/Greek/result/demonsthenes_against_neaira+apollonius_argonautica_book_4/start+start-end+end/include/dcc_greek_core_list/start-end/non_running/")
    assert response.status_code == 200