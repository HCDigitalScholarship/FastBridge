"""Auto-generated test file with absolute imports"""
import os, sys
from fastapi.testclient import TestClient

# Add project root to sys.path in order to import main
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from main import app

client = TestClient(app)


def test_oracle_claudian_de_raptu_prosperinae():
    response = client.get("/oracle/Latin/result/claudian_de_raptu_prosperinae/1.235/2.26/1/9/seneca_de_constantia/start-end")
    assert response.status_code == 200

def test_oracle_ovid_in_ibin():
    response = client.get("/oracle/Latin/result/ovid_in_ibin/59/120/1/6/claudian_in_rufinum/start-end")
    assert response.status_code == 200

def test_oracle_concat_pseudo_caesar_bellum_alexandrinum_claudian_panegyricus_dictus_manlio_theodoro_consuli():
    response = client.get("/oracle/Latin/result/pseudo-caesar_bellum_alexandrinum+claudian_panegyricus_dictus_manlio_theodoro_consuli/instructa+130/nomine+174/1+1/7+5/aesop_romulus_anglicus_1-10/start-end")
    assert response.status_code == 200

def test_oracle_hrotswitha_dulcitius():
    response = client.get("/oracle/Latin/result/hrotswitha_dulcitius/1.1/5.1/1/7/disce_kitchell-sienkewicz/start-end")
    assert response.status_code == 200

def test_oracle_claudian_panegyricus_de_vi_consulatu_honorii_augusti():
    response = client.get("/oracle/Latin/result/claudian_panegyricus_de_vi_consulatu_honorii_augusti/101/416/1/3/williams_rena_rhinoceros/start-end")
    assert response.status_code == 200

def test_oracle_petrionius_satyricon():
    response = client.get("/oracle/Latin/result/petrionius_satyricon/22/55/1/5/claudian_in_rufinum_prefaces/start-end")
    assert response.status_code == 200

def test_oracle_concat_cicero_pro_marcello_horace_epistulae():
    response = client.get("/oracle/Latin/result/cicero_pro_marcello+horace_epistulae/31.7+2.1.176/31.9+2.1.235/1+1/8+8/seneca_oedipus/start-end")
    assert response.status_code == 200

def test_oracle_prudentius_psychomachia_preface():
    response = client.get("/oracle/Latin/result/prudentius_psychomachia_preface/60/63/1/8/ap_latin_core_list_2025/start-end")
    assert response.status_code == 200

def test_oracle_cicero_pro_murena():
    response = client.get("/oracle/Latin/result/cicero_pro_murena/20.8/61.10/1/9/ovid_ars_amatoria/start-end")
    assert response.status_code == 200

def test_oracle_ovid_amores():
    response = client.get("/oracle/Latin/result/ovid_amores/2.16.41/3.6.87/1/6/cicero_post_reditum_ad_quirites/start-end")
    assert response.status_code == 200

def test_oracle_horace_epistulae():
    response = client.get("/oracle/Latin/result/horace_epistulae/1.17.42/1.17.43/1/4/cicero_post_reditum_ad_quirites/start-end")
    assert response.status_code == 200

def test_oracle_oxford_latin_course_for_college_fabulae_all():
    response = client.get("/oracle/Latin/result/oxford_latin_course_for_college_fabulae_all/15.2/18.3/1/6/vulgate_gospel_of_john/start-end")
    assert response.status_code == 200

def test_oracle_concat_aesop_fables_herodotus_book_1():
    response = client.get("/oracle/Greek/result/aesop_fables+herodotus_book_1/start+start/end+end/1+1/3+9/aesop_fables/start-end")
    assert response.status_code == 200

def test_oracle_elizabeth_jane_weston_vota_pro_felicibus_et_secundis_nuptis():
    response = client.get("/oracle/Latin/result/elizabeth_jane_weston_vota_pro_felicibus_et_secundis_nuptis/2.14/2.38/1/9/diederich_frequency_list_medieval/start-end")
    assert response.status_code == 200

def test_oracle_ilias_latina():
    response = client.get("/oracle/Latin/result/ilias_latina/817/1047/1/7/200_essential_latin_words_list_mahoney/start-end")
    assert response.status_code == 200

def test_oracle_ovid_amores_1_dcc():
    response = client.get("/oracle/Latin/result/ovid_amores_1_dcc/7.60/9.42/1/7/hildegard_of_bingen_ordo_virtutum/start-end")
    assert response.status_code == 200

def test_oracle_concat_herodotus_book_1_homer_core_list_frequency_categories_1_4():
    response = client.get("/oracle/Greek/result/herodotus_book_1+homer_core_list_frequency_categories_1-4/start+start/end+end/1+1/4+8/homer_core_list_frequency_categories_1-4/start-end")
    assert response.status_code == 200

def test_oracle_elizabeth_jane_weston_ad_matthiam_secundum():
    response = client.get("/oracle/Latin/result/elizabeth_jane_weston_ad_matthiam_secundum/1.14/1.44/1/3/florus_epitome_221_cleopatra/start-end")
    assert response.status_code == 200

def test_oracle_cicero_in_verrem_actio_prima():
    response = client.get("/oracle/Latin/result/cicero_in_verrem_actio_prima/52.11/53.8/1/7/tacitus_historiae/start-end")
    assert response.status_code == 200

def test_oracle_ovid_ars_amatoria():
    response = client.get("/oracle/Latin/result/ovid_ars_amatoria/3.509/3.754/1/7/epitaph_of_allia_potestas_cil_637966/start-end")
    assert response.status_code == 200

def test_oracle_cicero_post_reditum_in_senatu():
    response = client.get("/oracle/Latin/result/cicero_post_reditum_in_senatu/20.3/39.2/1/9/eduqas_gsce_defined_vocablary_list/start-end")
    assert response.status_code == 200

def test_oracle_elizabeth_jane_weston_elegia_consolatoria_ad_havlik():
    response = client.get("/oracle/Latin/result/elizabeth_jane_weston_elegia_consolatoria_ad_havlik/1.3/1.4/1/9/tacitus_historiae/start-end")
    assert response.status_code == 200

def test_oracle_cicero_pro_rabirio_postumo():
    response = client.get("/oracle/Latin/result/cicero_pro_rabirio_postumo/2.13/7.4/1/7/fabulae_faciles_ritchie/start-end")
    assert response.status_code == 200

def test_oracle_augustine_confessions_book_1():
    response = client.get("/oracle/Latin/result/augustine_confessions_book_1/1.18.29/1.20.31/1/6/prudentius_psychomachia/start-end")
    assert response.status_code == 200

def test_oracle_concat_athenaze_an_introduction_to_ancient_greek_herodotus_book_1_high_frequency_vocabulary_list():
    response = client.get("/oracle/Greek/result/athenaze_an_introduction_to_ancient_greek+herodotus_book_1_high_frequency_vocabulary_list/start+start/end+end/1+1/9+4/dcc_greek_core_list/start-end")
    assert response.status_code == 200

def test_oracle_apuleius_de_deo_socratis():
    response = client.get("/oracle/Latin/result/apuleius_de_deo_socratis/16.12/21.8/1/8/pervigilium_veneris/start-end")
    assert response.status_code == 200

def test_oracle_claudian_fescennia():
    response = client.get("/oracle/Latin/result/claudian_fescennia/2.15/3.4/1/4/seneca_ad_lucilium_epistulae_morales/start-end")
    assert response.status_code == 200

def test_oracle_seneca_phaedra():
    response = client.get("/oracle/Latin/result/seneca_phaedra/176/989b/1/9/dares_de_excidio_troiae/start-end")
    assert response.status_code == 200

def test_oracle_cicero_pro_cluentio():
    response = client.get("/oracle/Latin/result/cicero_pro_cluentio/186.5/192.7/1/8/cicero_post_reditum_in_senatu/start-end")
    assert response.status_code == 200

def test_oracle_williams_ursus_et_porcus():
    response = client.get("/oracle/Latin/result/williams_ursus_et_porcus/10/13/1/6/jenney_first_year_latin_purple_jenney-scudder-baade/start-end")
    assert response.status_code == 200

def test_oracle_cicero_pro_caelio():
    response = client.get("/oracle/Latin/result/cicero_pro_caelio/38.18/55.17/1/5/caesar_bellum_civile/start-end")
    assert response.status_code == 200

def test_oracle_apollonius_argonautica_book_4():
    response = client.get("/oracle/Greek/result/apollonius_argonautica_book_4/start/end/1/7/aeschylus_prometheus_bound/start-end")
    assert response.status_code == 200

def test_oracle_aesop_romulus_anglicus_1_10():
    response = client.get("/oracle/Latin/result/aesop_romulus_anglicus_1-10/7/10/1/6/martial_epigrams/start-end")
    assert response.status_code == 200

def test_oracle_claudian_de_bello_gildonico():
    response = client.get("/oracle/Latin/result/claudian_de_bello_gildonico/281/391/1/9/a_primer_of_ecclesiastical_latin_collins/start-end")
    assert response.status_code == 200

def test_oracle_dcc_latin_core():
    response = client.get("/oracle/Latin/result/dcc_latin_core/678/755/1/9/bernardo_de_riofrio_centonicum_virgilianum_monimentum/start-end")
    assert response.status_code == 200

def test_oracle_concat_cicero_pro_flacco_elizabeth_jane_weston_epistula_josepho_scaligero():
    response = client.get("/oracle/Latin/result/cicero_pro_flacco+elizabeth_jane_weston_epistula_josepho_scaligero/6.4+0/88.5+1/1+1/6+7/ovid_amores_1_dcc/start-end")
    assert response.status_code == 200

def test_oracle_florus_epitome_22_23_gracchi():
    response = client.get("/oracle/Latin/result/florus_epitome_22-23_gracchi/2.1.6/2.2.7/1/9/ovid_heroidum_epistulae/start-end")
    assert response.status_code == 200

def test_oracle_catullus_carmina_garrison():
    response = client.get("/oracle/Latin/result/catullus_carmina_garrison/61.44/66.4/1/3/ovid_fasti/start-end")
    assert response.status_code == 200

def test_oracle_pervigilium_veneris():
    response = client.get("/oracle/Latin/result/pervigilium_veneris/76/83/1/5/vergil_aeneid_ap_selections/start-end")
    assert response.status_code == 200

def test_oracle_cato_monostichs():
    response = client.get("/oracle/Latin/result/cato_monostichs/54/55/1/5/horace_ars_poetica/start-end")
    assert response.status_code == 200

def test_oracle_seneca_de_constantia():
    response = client.get("/oracle/Latin/result/seneca_de_constantia/16.1/16.4/1/5/ovid_heroidum_epistulae/start-end")
    assert response.status_code == 200

def test_oracle_newton_axiomata_motus():
    response = client.get("/oracle/Latin/result/newton_axiomata_motus/2/3/1/3/claudian_fescennia/start-end")
    assert response.status_code == 200

def test_oracle_horace_carmen_saeculare():
    response = client.get("/oracle/Latin/result/horace_carmen_saeculare/54/75/1/3/latin_stopwords_list_cltk/start-end")
    assert response.status_code == 200

def test_oracle_concat_claudian_panegyricus_de_vi_consulatu_honorii_augusti_preface_claudian_panegyricus_dictus_manlio_theodoro_consuli():
    response = client.get("/oracle/Latin/result/claudian_panegyricus_de_vi_consulatu_honorii_augusti_preface+claudian_panegyricus_dictus_manlio_theodoro_consuli/3+83/16+232/1+1/6+8/seneca_naturales_quaestiones_-_dcc/start-end")
    assert response.status_code == 200

def test_oracle_bernardo_de_riofrio_centonicum_virgilianum_monimentum():
    response = client.get("/oracle/Latin/result/bernardo_de_riofrio_centonicum_virgilianum_monimentum/52/122/1/9/ovid_ars_amatoria/start-end")
    assert response.status_code == 200

def test_oracle_cicero_pro_rabirio_perduellionis_reo():
    response = client.get("/oracle/Latin/result/cicero_pro_rabirio_perduellionis_reo/18.11/27.11/1/4/colby_latin_list_years_1_3_4/start-end")
    assert response.status_code == 200

def test_oracle_elizabeth_jane_weston_in_obitum_ioannae():
    response = client.get("/oracle/Latin/result/elizabeth_jane_weston_in_obitum_ioannae/1.14/1.85/1/8/prudentius_psychomachia/start-end")
    assert response.status_code == 200

def test_oracle_nepos_life_of_hannibal():
    response = client.get("/oracle/Latin/result/nepos_life_of_hannibal/2.5/13.2/1/5/apuleius_peri_hermeneias/start-end")
    assert response.status_code == 200

def test_oracle_ecce_romani_chs_1_54():
    response = client.get("/oracle/Latin/result/ecce_romani_chs_1-54/23/34/1/3/wheelock_latin_exercitationes/start-end")
    assert response.status_code == 200

def test_oracle_claudian_de_consulatu_stilichonis_preface_to_book_3():
    response = client.get("/oracle/Latin/result/claudian_de_consulatu_stilichonis_preface_to_book_3/172/186/1/3/apuleius_florida/start-end")
    assert response.status_code == 200

def test_oracle_concat_new_latin_primer_english_irby_martial_book_10():
    response = client.get("/oracle/Latin/result/new_latin_primer_english-irby+martial_book_10/17+10.36.8/27+10.61.4/1+1/5+9/bede_historia_ecclesiastica_gentis_anglorum_prologue_11_125-26_21-2_12-14_16_20_31-3_5-6/start-end")
    assert response.status_code == 200

def test_oracle_stabat_mater():
    response = client.get("/oracle/Latin/result/stabat_mater/49/54/1/7/dares_de_excidio_troiae/start-end")
    assert response.status_code == 200

def test_oracle_jenney_first_year_combined():
    response = client.get("/oracle/Latin/result/jenney_first_year_combined/6/61/1/3/cicero_de_imperio_pompei/start-end")
    assert response.status_code == 200

def test_oracle_persius_satires():
    response = client.get("/oracle/Latin/result/persius_satires/0.8/5.107/1/7/claudian_panegyricus_dictus_manlio_theodoro_consuli/start-end")
    assert response.status_code == 200

def test_oracle_apuleius_de_deo_socratis_prologue():
    response = client.get("/oracle/Latin/result/apuleius_de_deo_socratis_prologue/4.5/4.11/1/5/international_baccalaureate_vocabulary_sl_hl_selections/start-end")
    assert response.status_code == 200

def test_oracle_cicero_pro_milone():
    response = client.get("/oracle/Latin/result/cicero_pro_milone/78.9/100.9/1/4/hildegard_of_bingen_ordo_virtutum/start-end")
    assert response.status_code == 200

def test_oracle_epitaph_of_allia_potestas_cil_637966():
    response = client.get("/oracle/Latin/result/epitaph_of_allia_potestas_cil_637966/12/34/1/6/new_latin_primer_english-irby/start-end")
    assert response.status_code == 200

def test_oracle_concat_plautus_amphitruo_passio_santarum_perpetuae_et_felicitatis():
    response = client.get("/oracle/Latin/result/plautus_amphitruo+passio_santarum_perpetuae_et_felicitatis/487+4.3/1003+10.4/1+1/7+3/cicero_post_reditum_ad_quirites/start-end")
    assert response.status_code == 200

def test_oracle_concat_herodotus_book_1_hansen_quinn_greek_an_intensive_course():
    response = client.get("/oracle/Greek/result/herodotus_book_1+hansen_quinn_greek_an_intensive_course/start+start/end+end/1+1/5+4/herodotus_book_1/start-end")
    assert response.status_code == 200

def test_oracle_concat_herodotus_book_1_aeschylus_prometheus_bound():
    response = client.get("/oracle/Greek/result/herodotus_book_1+aeschylus_prometheus_bound/start+start/end+end/1+1/9+6/athenaze_an_introduction_to_ancient_greek/start-end")
    assert response.status_code == 200

def test_oracle_ovid_medicamina_faciei_femineae():
    response = client.get("/oracle/Latin/result/ovid_medicamina_faciei_femineae/41/94/1/4/catullus_carmina_garrison/start-end")
    assert response.status_code == 200

def test_oracle_bede_historia_ecclesiastica_gentis_anglorum_prologue_11_125_26_21_2_12_14_16_20_31_3_5_6():
    response = client.get("/oracle/Latin/result/bede_historia_ecclesiastica_gentis_anglorum_prologue_11_125-26_21-2_12-14_16_20_31-3_5-6/3.5/3.6/1/8/hrotswitha_dulcitius/start-end")
    assert response.status_code == 200

def test_oracle_dares_de_excidio_troiae():
    response = client.get("/oracle/Latin/result/dares_de_excidio_troiae/31/40/1/3/cicero_post_reditum_ad_quirites/start-end")
    assert response.status_code == 200

def test_oracle_tacitus_dialogus_de_oratoribus():
    response = client.get("/oracle/Latin/result/tacitus_dialogus_de_oratoribus/18.3/28.5/1/9/seneca_de_beneficiis/start-end")
    assert response.status_code == 200

def test_oracle_claudian_panegyricus_dictus_olybrio_et_probino_consulibus():
    response = client.get("/oracle/Latin/result/claudian_panegyricus_dictus_olybrio_et_probino_consulibus/128/213/1/3/latin_for_the_new_millennium_vols_1_and_2_tunberg-minkova/start-end")
    assert response.status_code == 200

def test_oracle_elizabeth_jane_weston_addenda_ad_parthenica():
    response = client.get("/oracle/Latin/result/elizabeth_jane_weston_addenda_ad_parthenica/1.1.17/1.1.23/1/5/seneca_de_constantia/start-end")
    assert response.status_code == 200

def test_oracle_martial_epigrams():
    response = client.get("/oracle/Latin/result/martial_epigrams/3.91.12/7.10.7/1/8/passio_santarum_perpetuae_et_felicitatis/start-end")
    assert response.status_code == 200

def test_oracle_martial_book_10():
    response = client.get("/oracle/Latin/result/martial_book_10/10.85.1/10.85.7/1/4/claudian_in_rufinum_prefaces/start-end")
    assert response.status_code == 200

def test_oracle_apuleius_asclepius():
    response = client.get("/oracle/Latin/result/apuleius_asclepius/6.16/41.2/1/6/seneca_de_tranquillitate_animi/start-end")
    assert response.status_code == 200

def test_oracle_herodotus_book_1_high_frequency_vocabulary_list():
    response = client.get("/oracle/Greek/result/herodotus_book_1_high_frequency_vocabulary_list/start/end/1/4/dcc_greek_core_list/start-end")
    assert response.status_code == 200

def test_oracle_concat_aeschylus_prometheus_bound_hansen_quinn_greek_an_intensive_course():
    response = client.get("/oracle/Greek/result/aeschylus_prometheus_bound+hansen_quinn_greek_an_intensive_course/start+start/end+end/1+1/3+9/athenaze_an_introduction_to_ancient_greek/start-end")
    assert response.status_code == 200

def test_oracle_maffeius_historiae_indicae_13_5_7_10_27_31_35_39_22_7_53_5_6_all():
    response = client.get("/oracle/Latin/result/maffeius_historiae_indicae_13-5_7-10_27-31_35-39_22-7_53-5_6_all/1.38/5.3/1/7/ovid_amores/start-end")
    assert response.status_code == 200

def test_oracle_newton_regulae_philosophandi():
    response = client.get("/oracle/Latin/result/newton_regulae_philosophandi/1.2/3.3/1/8/catullus_carmina_garrison/start-end")
    assert response.status_code == 200

def test_oracle_elizabeth_jane_weston_carmen_ad_rudolphum_ii():
    response = client.get("/oracle/Latin/result/elizabeth_jane_weston_carmen_ad_rudolphum_ii/3.25/5z.0/1/5/cicero_pro_caelio/start-end")
    assert response.status_code == 200

def test_oracle_200_essential_latin_words_list_mahoney():
    response = client.get("/oracle/Latin/result/200_essential_latin_words_list_mahoney/156/197/1/6/cicero_pro_rabirio_postumo/start-end")
    assert response.status_code == 200

def test_oracle_seneca_de_beneficiis():
    response = client.get("/oracle/Latin/result/seneca_de_beneficiis/6.31.7/6.41.1/1/4/wheelock_latin_sententiae_antiquae/start-end")
    assert response.status_code == 200

def test_oracle_ovid_halieutica():
    response = client.get("/oracle/Latin/result/ovid_halieutica/77/99/1/5/dares_de_excidio_troiae/start-end")
    assert response.status_code == 200

def test_oracle_cicero_somnium_scipionis_9_29():
    response = client.get("/oracle/Latin/result/cicero_somnium_scipionis_9-29/10/12/1/3/augustine_confessions_book_1/start-end")
    assert response.status_code == 200

def test_oracle_eutropius_breviarium_book_1_beyer():
    response = client.get("/oracle/Latin/result/eutropius_breviarium_book_1_beyer/7/19/1/6/seneca_naturales_quaestiones_-_dcc/start-end")
    assert response.status_code == 200

def test_oracle_cicero_in_vatinium():
    response = client.get("/oracle/Latin/result/cicero_in_vatinium/34.7/38.1/1/3/claudian_de_consulatu_stilichonis_preface_to_book_3/start-end")
    assert response.status_code == 200

def test_oracle_caesar_bellum_gallicum_ap_selections():
    response = client.get("/oracle/Latin/result/caesar_bellum_gallicum_ap_selections/5.26.1/5.41.2/1/5/cicero_in_calpurnium_pisonem/start-end")
    assert response.status_code == 200

def test_oracle_aesop_fables():
    response = client.get("/oracle/Greek/result/aesop_fables/start/end/1/8/dcc_greek_core_list/start-end")
    assert response.status_code == 200

def test_oracle_cambridge_latin_course():
    response = client.get("/oracle/Latin/result/cambridge_latin_course/7/28/1/9/ovid_amores/start-end")
    assert response.status_code == 200

def test_oracle_concat_demonsthenes_against_neaira_apollonius_argonautica_book_4():
    response = client.get("/oracle/Greek/result/demonsthenes_against_neaira+apollonius_argonautica_book_4/start+start/end+end/1+1/7+3/homer_core_list_frequency_categories_1-4/start-end")
    assert response.status_code == 200

def test_oracle_international_baccalaureate_vocabulary_sl_hl_selections():
    response = client.get("/oracle/Latin/result/international_baccalaureate_vocabulary_sl_hl_selections/4770/6072/1/7/apuleius_metamorphoses_finkelpearl/start-end")
    assert response.status_code == 200

def test_oracle_florus_epitome_221_cleopatra():
    response = client.get("/oracle/Latin/result/florus_epitome_221_cleopatra/2.21.5/2.21.6/1/3/cicero_pro_murena/start-end")
    assert response.status_code == 200

def test_oracle_vergil_eclogues():
    response = client.get("/oracle/Latin/result/vergil_eclogues/2.44/9.33/1/7/cicero_pro_rabirio_perduellionis_reo/start-end")
    assert response.status_code == 200

def test_oracle_cicero_pro_fonteio_excluding_fragments():
    response = client.get("/oracle/Latin/result/cicero_pro_fonteio_excluding_fragments/16.3/16.7/1/7/cicero_in_verrem_actio_prima/start-end")
    assert response.status_code == 200

def test_oracle_plautus_poenulus():
    response = client.get("/oracle/Latin/result/plautus_poenulus/1317/1353/1/9/pseudo-caesar_bellum_alexandrinum/start-end")
    assert response.status_code == 200

def test_oracle_latin_for_the_new_millennium_readings_volume_1_tunberg_minkova():
    response = client.get("/oracle/Latin/result/latin_for_the_new_millennium_readings_volume_1_tunberg-minkova/1.17.1/1.18.1/1/8/jerome_life_of_malchus_dcc/start-end")
    assert response.status_code == 200

def test_oracle_eutropius_breviarium_book_3_beyer():
    response = client.get("/oracle/Latin/result/eutropius_breviarium_book_3_beyer/3.20/3.21/1/7/200_essential_latin_words_list_mahoney/start-end")
    assert response.status_code == 200

def test_oracle_claudian_de_raptu_prosperinae_prefaces():
    response = client.get("/oracle/Latin/result/claudian_de_raptu_prosperinae_prefaces/2.5/2.7/1/7/aesop_romulus_anglicus_1-10/start-end")
    assert response.status_code == 200

def test_oracle_jenney_first_year_latin_red():
    response = client.get("/oracle/Latin/result/jenney_first_year_latin_red/15/24/1/3/elizabeth_jane_weston_addenda_ad_parthenica/start-end")
    assert response.status_code == 200

def test_oracle_seneca_de_brevitate_vitae():
    response = client.get("/oracle/Latin/result/seneca_de_brevitate_vitae/1.1/8.5/1/6/apollonius_king_of_tyre/start-end")
    assert response.status_code == 200

def test_oracle_seneca_naturales_quaestiones___dcc():
    response = client.get("/oracle/Latin/result/seneca_naturales_quaestiones_-_dcc/3.0.1/2.38.1/1/5/pseudo-caesar_bellum_hispanum/start-end")
    assert response.status_code == 200

def test_oracle_concat_demonsthenes_against_neaira_apollonius_argonautica_book_4():
    response = client.get("/oracle/Greek/result/demonsthenes_against_neaira+apollonius_argonautica_book_4/start+start/end+end/1+1/6+4/herodotus_book_1_high_frequency_vocabulary_list/start-end")
    assert response.status_code == 200

def test_oracle_concat_a_primer_of_ecclesiastical_latin_collins_eduqas():
    response = client.get("/oracle/Latin/result/a_primer_of_ecclesiastical_latin_collins+eduqas/25+427/32+439/1+1/4+8/cicero_pro_quinctio/start-end")
    assert response.status_code == 200

def test_oracle_owen_epigrams():
    response = client.get("/oracle/Latin/result/owen_epigrams/4.187.3/9.30.2/1/9/wheelock_latin_sententiae_antiquae/start-end")
    assert response.status_code == 200

def test_oracle_marie_de_france_fables_1_22():
    response = client.get("/oracle/Latin/result/marie_de_france_fables_1-22/21/22/1/7/cicero_de_domo_sua/start-end")
    assert response.status_code == 200

def test_oracle_seneca_oedipus():
    response = client.get("/oracle/Latin/result/seneca_oedipus/560/645/1/8/international_baccalaureate_vocabulary_sl_hl_selections/start-end")
    assert response.status_code == 200

def test_oracle_athenaze_an_introduction_to_ancient_greek():
    response = client.get("/oracle/Greek/result/athenaze_an_introduction_to_ancient_greek/start/end/1/9/herodotus_book_1/start-end")
    assert response.status_code == 200

def test_oracle_claudian_panegyricus_dictus_manlio_theodoro_consuli_preface():
    response = client.get("/oracle/Latin/result/claudian_panegyricus_dictus_manlio_theodoro_consuli_preface/267/287/1/7/cicero_pro_fonteio_excluding_fragments/start-end")
    assert response.status_code == 200

def test_oracle_claudian_in_rufinum_prefaces():
    response = client.get("/oracle/Latin/result/claudian_in_rufinum_prefaces/2.5/2.11/1/9/claudian_de_raptu_prosperinae/start-end")
    assert response.status_code == 200

def test_oracle_seneca_troades():
    response = client.get("/oracle/Latin/result/seneca_troades/505/530/1/3/elizabeth_jane_weston_carmen_ad_rudolphum_ii/start-end")
    assert response.status_code == 200

def test_oracle_claudian_panegyricus_de_iv_consulatu_honorii_augusti():
    response = client.get("/oracle/Latin/result/claudian_panegyricus_de_iv_consulatu_honorii_augusti/38/465/1/6/elizabeth_jane_weston_in_obitum_ioannae/start-end")
    assert response.status_code == 200

def test_oracle_colby_latin_list_years_1_3_4():
    response = client.get("/oracle/Latin/result/colby_latin_list_years_1_3_4/1/3/1/3/petrionius_satyricon/start-end")
    assert response.status_code == 200

def test_oracle_cicero_pro_marco_tullio():
    response = client.get("/oracle/Latin/result/cicero_pro_marco_tullio/36.1/Fr.1.7/1/6/physiologus_latina_1-6_9_16_17_23/start-end")
    assert response.status_code == 200

def test_oracle_seneca_hercules_oetaeus():
    response = client.get("/oracle/Latin/result/seneca_hercules_oetaeus/1752/1940/1/6/bernardo_de_riofrio_centonicum_virgilianum_monimentum/start-end")
    assert response.status_code == 200

def test_oracle_gsce_dvl():
    response = client.get("/oracle/Latin/result/gsce_dvl/343/382/1/8/newton_regulae_philosophandi/start-end")
    assert response.status_code == 200

def test_oracle_ocr_as():
    response = client.get("/oracle/Latin/result/ocr_as/536/627/1/6/seneca_de_vita_beata/start-end")
    assert response.status_code == 200

def test_oracle_hildegard_of_bingen_scivias_72():
    response = client.get("/oracle/Latin/result/hildegard_of_bingen_scivias_72/7.3/7.4/1/9/puer_romanus/start-end")
    assert response.status_code == 200

def test_oracle_concat_dcc_greek_core_list_apollonius_argonautica_book_4():
    response = client.get("/oracle/Greek/result/dcc_greek_core_list+apollonius_argonautica_book_4/start+start/end+end/1+1/4+8/dcc_greek_core_list/start-end")
    assert response.status_code == 200

def test_oracle_propertius_elegies():
    response = client.get("/oracle/Latin/result/propertius_elegies/3.18.5/4.3.9/1/5/newton_axiomata_motus/start-end")
    assert response.status_code == 200

def test_oracle_pseudo_caesar_bellum_africanum():
    response = client.get("/oracle/Latin/result/pseudo-caesar_bellum_africanum/58.1/70.7/1/5/cicero_pro_marco_tullio/start-end")
    assert response.status_code == 200

def test_oracle_concat_aesop_fables_demonsthenes_against_neaira():
    response = client.get("/oracle/Greek/result/aesop_fables+demonsthenes_against_neaira/start+start/end+end/1+1/5+9/hansen_quinn_greek_an_intensive_course/start-end")
    assert response.status_code == 200

def test_oracle_concat_physiologus_latina_1_6_9_16_17_23_seneca_ad_polybium_de_consolatione():
    response = client.get("/oracle/Latin/result/physiologus_latina_1-6_9_16_17_23+seneca_ad_polybium_de_consolatione/6.11+4.3/23.46+11.6/1+1/3+9/elizabeth_jane_weston_ad_michaelem_pecka/start-end")
    assert response.status_code == 200

def test_oracle_concat_aesop_fables_apollonius_argonautica_book_4():
    response = client.get("/oracle/Greek/result/aesop_fables+apollonius_argonautica_book_4/start+start/end+end/1+1/9+4/aesop_fables/start-end")
    assert response.status_code == 200

def test_oracle_concat_apollonius_argonautica_book_4_athenaze_an_introduction_to_ancient_greek():
    response = client.get("/oracle/Greek/result/apollonius_argonautica_book_4+athenaze_an_introduction_to_ancient_greek/start+start/end+end/1+1/4+3/homer_core_list_frequency_categories_1-4/start-end")
    assert response.status_code == 200

def test_oracle_diederich_frequency_list_general():
    response = client.get("/oracle/Latin/result/diederich_frequency_list_general/1342/1502/1/4/seneca_hercules_oetaeus/start-end")
    assert response.status_code == 200

def test_oracle_a_primer_of_ecclesiastical_latin_collins():
    response = client.get("/oracle/Latin/result/a_primer_of_ecclesiastical_latin_collins/11/21/1/5/elizabeth_jane_weston_parthenica/start-end")
    assert response.status_code == 200

def test_oracle_caesar_bellum_civile():
    response = client.get("/oracle/Latin/result/caesar_bellum_civile/3.84.3/3.112.4/1/5/cicero_somnium_scipionis_9-29/start-end")
    assert response.status_code == 200

def test_oracle_seneca_phoenissae():
    response = client.get("/oracle/Latin/result/seneca_phoenissae/602/650/1/8/seneca_de_constantia/start-end")
    assert response.status_code == 200

def test_oracle_claudian_carmina_minora_25_preface():
    response = client.get("/oracle/Latin/result/claudian_carmina_minora_25_preface/177/244/1/9/tacitus_historiae/start-end")
    assert response.status_code == 200

def test_oracle_homer_core_list_frequency_categories_1_4():
    response = client.get("/oracle/Greek/result/homer_core_list_frequency_categories_1-4/start/end/1/6/aesop_fables/start-end")
    assert response.status_code == 200

def test_oracle_elizabeth_jane_weston_ad_schosserum():
    response = client.get("/oracle/Latin/result/elizabeth_jane_weston_ad_schosserum/7.7/7.9/1/4/cicero_in_catilinam_1-4/start-end")
    assert response.status_code == 200

def test_oracle_hansen_quinn_greek_an_intensive_course():
    response = client.get("/oracle/Greek/result/hansen_quinn_greek_an_intensive_course/start/end/1/9/aeschylus_prometheus_bound/start-end")
    assert response.status_code == 200

def test_oracle_wheelock_latin_sententiae_antiquae():
    response = client.get("/oracle/Latin/result/wheelock_latin_sententiae_antiquae/9.8/28.4/1/9/maffeius_historiae_indicae_13-5_7-10_27-31_35-39_22-7_53-5_6_all/start-end")
    assert response.status_code == 200

def test_oracle_horace_ars_poetica():
    response = client.get("/oracle/Latin/result/horace_ars_poetica/262/468/1/3/eduqas/start-end")
    assert response.status_code == 200

def test_oracle_seneca_apocolocyntosis():
    response = client.get("/oracle/Latin/result/seneca_apocolocyntosis/4.1.27/7.2.8/1/6/elizabeth_jane_weston_vota_pro_felicibus_et_secundis_nuptis/start-end")
    assert response.status_code == 200

def test_oracle_corderius_colloquia_book_2():
    response = client.get("/oracle/Latin/result/corderius_colloquia_book_2/2.10/2.67/1/6/seneca_apocolocyntosis/start-end")
    assert response.status_code == 200

def test_oracle_cicero_de_imperio_pompei():
    response = client.get("/oracle/Latin/result/cicero_de_imperio_pompei/9.4/13.6/1/7/cicero_post_reditum_in_senatu/start-end")
    assert response.status_code == 200

def test_oracle_lhomond_de_viris_illustribus_1_18_exordium_to_coriolanus():
    response = client.get("/oracle/Latin/result/lhomond_de_viris_illustribus_1-18_exordium_to_coriolanus/1.1/2.2/1/3/diederich_frequency_list_general/start-end")
    assert response.status_code == 200

def test_oracle_cicero_de_officiis():
    response = client.get("/oracle/Latin/result/cicero_de_officiis/1.100.3/2.80.3/1/4/anthologia_latina_507-518_epitaphs_of_vergil/start-end")
    assert response.status_code == 200

def test_oracle_cicero_pro_quinctio():
    response = client.get("/oracle/Latin/result/cicero_pro_quinctio/1.5/16.12/1/6/cicero_in_verrem_actio_secunda/start-end")
    assert response.status_code == 200

def test_oracle_horace_epodes():
    response = client.get("/oracle/Latin/result/horace_epodes/8.7/16.46/1/9/williams_ursus_et_porcus/start-end")
    assert response.status_code == 200

def test_oracle_seneca_de_providentia():
    response = client.get("/oracle/Latin/result/seneca_de_providentia/4.15/5.8/1/3/ovid_in_ibin/start-end")
    assert response.status_code == 200

def test_oracle_concat_egeria_itinerarium_book_1_ovid_halieutica():
    response = client.get("/oracle/Latin/result/egeria_itinerarium_book_1+ovid_halieutica/6.1+134/13.4+135/1+1/5+3/epitaph_of_allia_potestas_cil_637966/start-end")
    assert response.status_code == 200

def test_oracle_seneca_ad_helviam_matrem_de_consolatione():
    response = client.get("/oracle/Latin/result/seneca_ad_helviam_matrem_de_consolatione/10.8/13.3/1/4/apuleius_asclepius/start-end")
    assert response.status_code == 200

def test_oracle_claudian_in_eutropium_preface_to_book_2():
    response = client.get("/oracle/Latin/result/claudian_in_eutropium_preface_to_book_2/2.70/2.72/1/7/eutropius_breviarium_book_1_beyer/start-end")
    assert response.status_code == 200

def test_oracle_latin_an_intensive_course_moreland_fleischer():
    response = client.get("/oracle/Latin/result/latin_an_intensive_course_moreland-fleischer/5/13/1/3/seneca_phaedra/start-end")
    assert response.status_code == 200

def test_oracle_lingua_latina_per_se_illustrata_pars_i_oerberg():
    response = client.get("/oracle/Latin/result/lingua_latina_per_se_illustrata_pars_i_oerberg/28/31/1/4/gsce_dvl/start-end")
    assert response.status_code == 200

def test_oracle_tacitus_germania():
    response = client.get("/oracle/Latin/result/tacitus_germania/37.5/46.1/1/3/classical_latin_mckeown/start-end")
    assert response.status_code == 200

def test_oracle_physiologus_latina_1_6_9_16_17_23():
    response = client.get("/oracle/Latin/result/physiologus_latina_1-6_9_16_17_23/23.23/23.35/1/5/colby_latin_list_years_1_3_4/start-end")
    assert response.status_code == 200

def test_oracle_cicero_in_verrem_actio_secunda():
    response = client.get("/oracle/Latin/result/cicero_in_verrem_actio_secunda/1.29.3/3.83.17/1/7/ap_latin_core_list_2025/start-end")
    assert response.status_code == 200

def test_oracle_passio_santarum_perpetuae_et_felicitatis():
    response = client.get("/oracle/Latin/result/passio_santarum_perpetuae_et_felicitatis/11.7/18.9/1/4/diederich_frequency_list_general/start-end")
    assert response.status_code == 200

def test_oracle_civis_romanus_a_reader_for_the_first_two_years_of_latin_cobban_and_colebourn():
    response = client.get("/oracle/Latin/result/civis_romanus_a_reader_for_the_first_two_years_of_latin_cobban_and_colebourn/50/57/1/6/martial_epigrams/start-end")
    assert response.status_code == 200

def test_oracle_latin_for_the_new_millennium_vols_1_and_2_tunberg_minkova():
    response = client.get("/oracle/Latin/result/latin_for_the_new_millennium_vols_1_and_2_tunberg-minkova/2.13/2.15/1/7/elizabeth_jane_weston_ad_schosserum/start-end")
    assert response.status_code == 200

def test_oracle_hildegard_of_bingen_ordo_virtutum():
    response = client.get("/oracle/Latin/result/hildegard_of_bingen_ordo_virtutum/123/204/1/8/cicero_in_verrem_actio_secunda/start-end")
    assert response.status_code == 200

def test_oracle_dcc_greek_core_list():
    response = client.get("/oracle/Greek/result/dcc_greek_core_list/start/end/1/3/athenaze_an_introduction_to_ancient_greek/start-end")
    assert response.status_code == 200

def test_oracle_seneca_agamemnon():
    response = client.get("/oracle/Latin/result/seneca_agamemnon/701/942/1/6/eduqas_gsce_defined_vocablary_list/start-end")
    assert response.status_code == 200

def test_oracle_anthologia_latina_507_518_epitaphs_of_vergil():
    response = client.get("/oracle/Latin/result/anthologia_latina_507-518_epitaphs_of_vergil/509/510/1/5/cicero_pro_caelio/start-end")
    assert response.status_code == 200

def test_oracle_concat_aesop_fables_groton_from_alpha_to_omega():
    response = client.get("/oracle/Greek/result/aesop_fables+groton_from_alpha_to_omega/start+start/end+end/1+1/6+3/groton_from_alpha_to_omega/start-end")
    assert response.status_code == 200

def test_oracle_elizabeth_jane_weston_poemata():
    response = client.get("/oracle/Latin/result/elizabeth_jane_weston_poemata/2.90.45/2.94.59/1/5/ap_latin_core_list_2025/start-end")
    assert response.status_code == 200

def test_oracle_hartnett_by_roman_hands():
    response = client.get("/oracle/Latin/result/hartnett_by_roman_hands/123/141/1/4/cicero_de_officiis/start-end")
    assert response.status_code == 200

def test_oracle_demonsthenes_against_neaira():
    response = client.get("/oracle/Greek/result/demonsthenes_against_neaira/start/end/1/5/demonsthenes_against_neaira/start-end")
    assert response.status_code == 200

def test_oracle_gsce_rvl():
    response = client.get("/oracle/Latin/result/gsce_rvl/47/107/1/6/livy_ab_urbe_condita_ib_list_2_selections/start-end")
    assert response.status_code == 200

def test_oracle_cato_distichs():
    response = client.get("/oracle/Latin/result/cato_distichs/3.20.2/4.35.1/1/3/latin_for_the_new_millennium_readings_volume_1_tunberg-minkova/start-end")
    assert response.status_code == 200

def test_oracle_wheelock_latin_exercitationes():
    response = client.get("/oracle/Latin/result/wheelock_latin_exercitationes/34.10/37.2/1/6/apuleius_peri_hermeneias/start-end")
    assert response.status_code == 200

def test_oracle_claudian_panegyricus_de_iii_consulatu_honorii_augusti():
    response = client.get("/oracle/Latin/result/claudian_panegyricus_de_iii_consulatu_honorii_augusti/453/521/1/8/martial_book_10/start-end")
    assert response.status_code == 200

def test_oracle_claudian_panegyricus_de_vi_consulatu_honorii_augusti_preface():
    response = client.get("/oracle/Latin/result/claudian_panegyricus_de_vi_consulatu_honorii_augusti_preface/18/24/1/5/requiem_mass/start-end")
    assert response.status_code == 200

def test_oracle_prudentius_psychomachia():
    response = client.get("/oracle/Latin/result/prudentius_psychomachia/141/540/1/5/requiem_mass/start-end")
    assert response.status_code == 200

def test_oracle_claudian_in_rufinum():
    response = client.get("/oracle/Latin/result/claudian_in_rufinum/1.297/2.316/1/3/cicero_in_verrem_actio_prima/start-end")
    assert response.status_code == 200

def test_oracle_apuleius_florida():
    response = client.get("/oracle/Latin/result/apuleius_florida/3.28/19.26/1/3/elizabeth_jane_weston_ad_schosserum/start-end")
    assert response.status_code == 200

def test_oracle_jerome_life_of_malchus_dcc():
    response = client.get("/oracle/Latin/result/jerome_life_of_malchus_dcc/9.10/10.2/1/7/augustine_confessions_book_1/start-end")
    assert response.status_code == 200

def test_oracle_caesar_bellum_gallicum():
    response = client.get("/oracle/Latin/result/caesar_bellum_gallicum/6.44.3/7.47.4/1/4/seneca_naturales_quaestiones_-_dcc/start-end")
    assert response.status_code == 200

def test_oracle_disce_kitchell_sienkewicz():
    response = client.get("/oracle/Latin/result/disce_kitchell-sienkewicz/17/24/1/7/ocr_as/start-end")
    assert response.status_code == 200

def test_oracle_claudian_epithalamium_de_nuptii_honorii_augusti():
    response = client.get("/oracle/Latin/result/claudian_epithalamium_de_nuptii_honorii_augusti/318/325/1/6/vergil_aeneid_ap_selections/start-end")
    assert response.status_code == 200

def test_oracle_cicero_pro_flacco():
    response = client.get("/oracle/Latin/result/cicero_pro_flacco/94.3/98.2/1/3/colby_latin_list_years_1_3_4/start-end")
    assert response.status_code == 200

def test_oracle_vergil_eclogues_1_dcc():
    response = client.get("/oracle/Latin/result/vergil_eclogues_1_dcc/1.3/1.68/1/6/cicero_in_verrem_actio_secunda/start-end")
    assert response.status_code == 200

def test_oracle_apuleius_peri_hermeneias():
    response = client.get("/oracle/Latin/result/apuleius_peri_hermeneias/6.36/14.35/1/4/claudian_de_raptu_prosperinae_prefaces/start-end")
    assert response.status_code == 200

def test_oracle_ovid_remedia_amoris():
    response = client.get("/oracle/Latin/result/ovid_remedia_amoris/770/792/1/9/trotula_de_curis_mulierum_74-78_86-87_167-168_174-178_181-182/start-end")
    assert response.status_code == 200

def test_oracle_concat_herodotus_book_1_high_frequency_vocabulary_list_groton_from_alpha_to_omega():
    response = client.get("/oracle/Greek/result/herodotus_book_1_high_frequency_vocabulary_list+groton_from_alpha_to_omega/start+start/end+end/1+1/6+6/groton_from_alpha_to_omega/start-end")
    assert response.status_code == 200

def test_oracle_vergil_aeneid_new_ap_selections():
    response = client.get("/oracle/Latin/result/vergil_aeneid_new_ap_selections/4.361/11.588/1/5/landivar_rusticatio_mexicana_book_6/start-end")
    assert response.status_code == 200

def test_oracle_concat_cicero_pro_marco_tullio_eutropius_breviarium_book_3_beyer():
    response = client.get("/oracle/Latin/result/cicero_pro_marco_tullio+eutropius_breviarium_book_3_beyer/15.6+3.16/39.5+3.17/1+1/8+7/owen_epigrams/start-end")
    assert response.status_code == 200

def test_oracle_plautus_amphitruo():
    response = client.get("/oracle/Latin/result/plautus_amphitruo/899/1103/1/4/oxford_latin_course_for_college_fabulae_all/start-end")
    assert response.status_code == 200

def test_oracle_wiley_real_latin_maltby_belcher():
    response = client.get("/oracle/Latin/result/wiley_real_latin_maltby-belcher/18/21/1/7/eutropius_breviarium_book_1_beyer/start-end")
    assert response.status_code == 200

def test_oracle_apuleius_apology():
    response = client.get("/oracle/Latin/result/apuleius_apology/38.6/83.11/1/7/cicero_in_verrem_actio_secunda/start-end")
    assert response.status_code == 200

def test_oracle_carmina_burana_orff_latin_lyrics_1_5_11_15_17_25():
    response = client.get("/oracle/Latin/result/carmina_burana_orff_latin_lyrics_1-5_11-15_17-25/12.14/24.6/1/3/ovid_amores/start-end")
    assert response.status_code == 200

def test_oracle_oxford_latin_course_for_college():
    response = client.get("/oracle/Latin/result/oxford_latin_course_for_college/24/25/1/4/petrionius_satyricon/start-end")
    assert response.status_code == 200

def test_oracle_diederich_frequency_list_prose():
    response = client.get("/oracle/Latin/result/diederich_frequency_list_prose/2292/2336/1/5/seneca_ad_polybium_de_consolatione/start-end")
    assert response.status_code == 200

def test_oracle_pseudo_caesar_bellum_hispanum():
    response = client.get("/oracle/Latin/result/pseudo-caesar_bellum_hispanum/27.5/19.2/1/4/eutropius_breviarium_book_3_beyer/start-end")
    assert response.status_code == 200

def test_oracle_cicero_in_catilinam_1_4():
    response = client.get("/oracle/Latin/result/cicero_in_catilinam_1-4/3.12.10/4.17.6/1/4/cicero_de_imperio_cn_pompei/start-end")
    assert response.status_code == 200

def test_oracle_seneca_de_ira():
    response = client.get("/oracle/Latin/result/seneca_de_ira/3.11.4/3.24.1/1/3/wheelock_latin_sententiae_antiquae/start-end")
    assert response.status_code == 200

def test_oracle_cicero_de_lege_agraria():
    response = client.get("/oracle/Latin/result/cicero_de_lege_agraria/57.11/99.14/1/5/augustus_res_gestae_1/start-end")
    assert response.status_code == 200

def test_oracle_elizabeth_jane_weston_epistula_josepho_scaligero():
    response = client.get("/oracle/Latin/result/elizabeth_jane_weston_epistula_josepho_scaligero/0/1/1/7/maffeius_historiae_indicae_13-5_7-10_27-31_35-39_22-7_53-5_6_all/start-end")
    assert response.status_code == 200

def test_oracle_pseudo_caesar_bellum_alexandrinum():
    response = client.get("/oracle/Latin/result/pseudo-caesar_bellum_alexandrinum/integra/tradit/1/3/claudian_panegyricus_dictus_manlio_theodoro_consuli/start-end")
    assert response.status_code == 200

def test_oracle_apollonius_king_of_tyre():
    response = client.get("/oracle/Latin/result/apollonius_king_of_tyre/19/50/1/6/puer_romanus/start-end")
    assert response.status_code == 200

def test_oracle_carmina_priapea_1_80():
    response = client.get("/oracle/Latin/result/carmina_priapea_1-80/77.9/80.7/1/9/pliny_the_younger_panegyricu/start-end")
    assert response.status_code == 200

def test_oracle_ocr_as_level_defined_vocabulary_list():
    response = client.get("/oracle/Latin/result/ocr_as_level_defined_vocabulary_list/312/627/1/4/elizabeth_jane_weston_in_obitum_ioannae/start-end")
    assert response.status_code == 200

def test_oracle_williams_rena_rhinoceros():
    response = client.get("/oracle/Latin/result/williams_rena_rhinoceros/14/15/1/6/lingua_latina_per_se_illustrata_pars_i_oerberg/start-end")
    assert response.status_code == 200

def test_oracle_elizabeth_jane_weston_de_ebrietate():
    response = client.get("/oracle/Latin/result/elizabeth_jane_weston_de_ebrietate/54.19/54.41/1/8/prudentius_psychomachia_preface/start-end")
    assert response.status_code == 200

def test_oracle_cicero_pro_marcello():
    response = client.get("/oracle/Latin/result/cicero_pro_marcello/28.5/29.6/1/3/vergil_eclogues/start-end")
    assert response.status_code == 200

def test_oracle_concat_dcc_latin_core_gsce_rvl():
    response = client.get("/oracle/Latin/result/dcc_latin_core+gsce_rvl/192+45/515+85/1+1/5+8/cicero_pro_marco_tullio/start-end")
    assert response.status_code == 200

def test_oracle_introduction_to_latin_shelmerdine():
    response = client.get("/oracle/Latin/result/introduction_to_latin_shelmerdine/31/32/1/4/seneca_ad_polybium_de_consolatione/start-end")
    assert response.status_code == 200

def test_oracle_claudian_panegyricus_dictus_manlio_theodoro_consuli():
    response = client.get("/oracle/Latin/result/claudian_panegyricus_dictus_manlio_theodoro_consuli/316/322/1/7/ocr_as_level_defined_vocabulary_list/start-end")
    assert response.status_code == 200

def test_oracle_seneca_de_otio():
    response = client.get("/oracle/Latin/result/seneca_de_otio/3.1/5.4/1/6/cicero_in_verrem_actio_prima/start-end")
    assert response.status_code == 200

def test_oracle_fabulae_faciles_ritchie():
    response = client.get("/oracle/Latin/result/fabulae_faciles_ritchie/3.59/3.71/1/4/ovid_fasti/start-end")
    assert response.status_code == 200

def test_oracle_concat_herodotus_book_1_demonsthenes_against_neaira():
    response = client.get("/oracle/Greek/result/herodotus_book_1+demonsthenes_against_neaira/start+start/end+end/1+1/4+4/demonsthenes_against_neaira/start-end")
    assert response.status_code == 200

def test_oracle_seneca_ad_polybium_de_consolatione():
    response = client.get("/oracle/Latin/result/seneca_ad_polybium_de_consolatione/12.4/15.3/1/9/pliny_the_younger_panegyricu/start-end")
    assert response.status_code == 200

def test_oracle_latin_stopwords_list_cltk():
    response = client.get("/oracle/Latin/result/latin_stopwords_list_cltk/13/42/1/3/apuleius_de_mundo/start-end")
    assert response.status_code == 200

def test_oracle_eduqas_gsce_defined_vocablary_list():
    response = client.get("/oracle/Latin/result/eduqas_gsce_defined_vocablary_list/180/367/1/9/seneca_apocolocyntosis/start-end")
    assert response.status_code == 200

def test_oracle_concat_homer_core_list_frequency_categories_1_4_herodotus_book_1_high_frequency_vocabulary_list():
    response = client.get("/oracle/Greek/result/homer_core_list_frequency_categories_1-4+herodotus_book_1_high_frequency_vocabulary_list/start+start/end+end/1+1/8+7/dcc_greek_core_list/start-end")
    assert response.status_code == 200

def test_oracle_suetonius_life_of_caligula():
    response = client.get("/oracle/Latin/result/suetonius_life_of_caligula/54/56/1/8/hartnett_by_roman_hands/start-end")
    assert response.status_code == 200

def test_oracle_concat_apollonius_argonautica_book_4_aesop_fables():
    response = client.get("/oracle/Greek/result/apollonius_argonautica_book_4+aesop_fables/start+start/end+end/1+1/3+6/aeschylus_prometheus_bound/start-end")
    assert response.status_code == 200

def test_oracle_seneca_de_vita_beata():
    response = client.get("/oracle/Latin/result/seneca_de_vita_beata/13.2/22.2/1/3/cicero_in_verrem_actio_secunda/start-end")
    assert response.status_code == 200

def test_oracle_hildegard_of_bingen_symphoniae_2_5_10_11_12_17_19_21_23_64():
    response = client.get("/oracle/Latin/result/hildegard_of_bingen_symphoniae_2-5_10_11_12_17_19_21_23_64/4.2/23.2/1/9/plautus_amphitruo/start-end")
    assert response.status_code == 200

def test_oracle_concat_apollonius_argonautica_book_4_dcc_greek_core_list():
    response = client.get("/oracle/Greek/result/apollonius_argonautica_book_4+dcc_greek_core_list/start+start/end+end/1+1/8+4/herodotus_book_1/start-end")
    assert response.status_code == 200

def test_oracle_elizabeth_jane_weston_ad_michaelem_pecka():
    response = client.get("/oracle/Latin/result/elizabeth_jane_weston_ad_michaelem_pecka/2.86/2.90/1/6/seneca_de_otio/start-end")
    assert response.status_code == 200

def test_oracle_livy_ab_urbe_condita_ib_list_2_selections():
    response = client.get("/oracle/Latin/result/livy_ab_urbe_condita_ib_list_2_selections/1.59.5/3.44.1/1/9/cicero_in_toga_candida/start-end")
    assert response.status_code == 200

def test_oracle_elizabeth_jane_weston_parthenica():
    response = client.get("/oracle/Latin/result/elizabeth_jane_weston_parthenica/2.102.34/3.1b.26/1/7/claudian_panegyricus_de_iii_consulatu_honorii_augusti/start-end")
    assert response.status_code == 200

def test_oracle_plautus_curculio():
    response = client.get("/oracle/Latin/result/plautus_curculio/405/697/1/5/wheelock_latin_sententiae_antiquae/start-end")
    assert response.status_code == 200

def test_oracle_cicero_de_imperio_cn_pompei():
    response = client.get("/oracle/Latin/result/cicero_de_imperio_cn_pompei/58.10/71.4/1/4/seneca_hercules_oetaeus/start-end")
    assert response.status_code == 200

def test_oracle_pliny_the_younger_panegyricu():
    response = client.get("/oracle/Latin/result/pliny_the_younger_panegyricu/95.4/95.5/1/6/vulgate_gospel_of_john/start-end")
    assert response.status_code == 200

def test_oracle_tacitus_historiae():
    response = client.get("/oracle/Latin/result/tacitus_historiae/3.18.6/4.22.8/1/7/horace_odes_garrison_edition/start-end")
    assert response.status_code == 200

def test_oracle_nepos_life_of_hamilcar():
    response = client.get("/oracle/Latin/result/nepos_life_of_hamilcar/3/4/1/6/passio_santarum_perpetuae_et_felicitatis/start-end")
    assert response.status_code == 200

def test_oracle_groton_from_alpha_to_omega():
    response = client.get("/oracle/Greek/result/groton_from_alpha_to_omega/start/end/1/4/herodotus_book_1/start-end")
    assert response.status_code == 200

def test_oracle_abelard_historia_selections():
    response = client.get("/oracle/Latin/result/abelard_historia_selections/5/6/1/4/claudian_panegyricus_dictus_manlio_theodoro_consuli_preface/start-end")
    assert response.status_code == 200

def test_oracle_ovid_fasti():
    response = client.get("/oracle/Latin/result/ovid_fasti/6.225/6.227/1/5/new_latin_primer_english-irby/start-end")
    assert response.status_code == 200

def test_oracle_ap_latin_core_list_2025():
    response = client.get("/oracle/Latin/result/ap_latin_core_list_2025/88/602/1/4/claudian_fescennia/start-end")
    assert response.status_code == 200

def test_oracle_eduqas():
    response = client.get("/oracle/Latin/result/eduqas/370/430/1/5/plautus_amphitruo/start-end")
    assert response.status_code == 200

def test_oracle_concat_gsce_dvl_tibullus_elegies():
    response = client.get("/oracle/Latin/result/gsce_dvl+tibullus_elegies/158+3.7.198/326+3.12.3/1+1/9+4/seneca_de_brevitate_vitae/start-end")
    assert response.status_code == 200

def test_oracle_concat_ovid_in_ibin_seneca_phaedra():
    response = client.get("/oracle/Latin/result/ovid_in_ibin+seneca_phaedra/187+169/451+534/1+1/3+6/ovid_remedia_amoris/start-end")
    assert response.status_code == 200

def test_oracle_seneca_de_tranquillitate_animi():
    response = client.get("/oracle/Latin/result/seneca_de_tranquillitate_animi/3.1/13.2/1/6/new_latin_primer_english-irby/start-end")
    assert response.status_code == 200

def test_oracle_puer_romanus():
    response = client.get("/oracle/Latin/result/puer_romanus/18.1/23.2/1/3/ocr_gsce_defined_vocabulary_list/start-end")
    assert response.status_code == 200

def test_oracle_concat_cicero_in_verrem_actio_prima_claudian_de_raptu_prosperinae():
    response = client.get("/oracle/Latin/result/cicero_in_verrem_actio_prima+claudian_de_raptu_prosperinae/16.7+1.5/41.6+2.228/1+1/8+8/propertius_elegies/start-end")
    assert response.status_code == 200

def test_oracle_concat_aesop_fables_dcc_greek_core_list():
    response = client.get("/oracle/Greek/result/aesop_fables+dcc_greek_core_list/start+start/end+end/1+1/8+3/demonsthenes_against_neaira/start-end")
    assert response.status_code == 200

def test_oracle_seneca_hercules_furens_dcc():
    response = client.get("/oracle/Latin/result/seneca_hercules_furens_dcc/598/1308/1/4/ocr_gsce_defined_vocabulary_list/start-end")
    assert response.status_code == 200

def test_oracle_requiem_mass():
    response = client.get("/oracle/Latin/result/requiem_mass/5/8/1/8/vergil_eclogues_1_dcc/start-end")
    assert response.status_code == 200

def test_oracle_augustus_res_gestae_1():
    response = client.get("/oracle/Latin/result/augustus_res_gestae_1/25/34/1/8/nepos_life_of_hamilcar/start-end")
    assert response.status_code == 200

def test_oracle_vergil_aeneid_ap_selections():
    response = client.get("/oracle/Latin/result/vergil_aeneid_ap_selections/2.209/4.702/1/8/seneca_oedipus/start-end")
    assert response.status_code == 200

def test_oracle_cicero_in_toga_candida():
    response = client.get("/oracle/Latin/result/cicero_in_toga_candida/6.11/10.3/1/9/claudian_panegyricus_de_iv_consulatu_honorii_augusti/start-end")
    assert response.status_code == 200

def test_oracle_suburani_fabulae():
    response = client.get("/oracle/Latin/result/suburani_fabulae/20.1/32.2/1/3/latin_for_the_new_millennium_vols_1_and_2_tunberg-minkova/start-end")
    assert response.status_code == 200

def test_oracle_egeria_itinerarium_book_1():
    response = client.get("/oracle/Latin/result/egeria_itinerarium_book_1/4.6/17.3/1/4/vulgate_gospel_of_john/start-end")
    assert response.status_code == 200

def test_oracle_concat_gsce_rvl_egeria_itinerarium_book_1():
    response = client.get("/oracle/Latin/result/gsce_rvl+egeria_itinerarium_book_1/100+16.4/121+20.9/1+1/5+5/aesop_romulus_anglicus_1-10/start-end")
    assert response.status_code == 200

def test_oracle_cicero_post_reditum_ad_quirites():
    response = client.get("/oracle/Latin/result/cicero_post_reditum_ad_quirites/9.4/18.13/1/4/jenney_first_year_combined/start-end")
    assert response.status_code == 200

def test_oracle_herodotus_book_1():
    response = client.get("/oracle/Greek/result/herodotus_book_1/start/end/1/8/homer_core_list_frequency_categories_1-4/start-end")
    assert response.status_code == 200

def test_oracle_seneca_pseudo_proverbia_or_de_moribu():
    response = client.get("/oracle/Latin/result/seneca_pseudo_proverbia_or_de_moribu/34/121/1/9/hildegard_of_bingen_symphoniae_2-5_10_11_12_17_19_21_23_64/start-end")
    assert response.status_code == 200

def test_oracle_ocr_gsce_restricted_vocabulary_list():
    response = client.get("/oracle/Latin/result/ocr_gsce_restricted_vocabulary_list/25/123/1/8/cicero_in_catilinam_1-4/start-end")
    assert response.status_code == 200

def test_oracle_florus_epitome_11_romulus_and_roman_kings():
    response = client.get("/oracle/Latin/result/florus_epitome_11_romulus_and_roman_kings/1.1.6/1.1.7/1/3/ovid_amores_1_dcc/start-end")
    assert response.status_code == 200

def test_oracle_cicero_de_domo_sua():
    response = client.get("/oracle/Latin/result/cicero_de_domo_sua/95.1/98.3/1/3/disce_kitchell-sienkewicz/start-end")
    assert response.status_code == 200

def test_oracle_concat_trotula_de_curis_mulierum_74_78_86_87_167_168_174_178_181_182_cicero_somnium_scipionis_9_29():
    response = client.get("/oracle/Latin/result/trotula_de_curis_mulierum_74-78_86-87_167-168_174-178_181-182+cicero_somnium_scipionis_9-29/77+28/86+29/1+1/6+8/ocr_gsce_restricted_vocabulary_list/start-end")
    assert response.status_code == 200

def test_oracle_horace_odes_garrison_edition():
    response = client.get("/oracle/Latin/result/horace_odes_garrison_edition/4.9.35/4.15.11/1/7/ovid_amores/start-end")
    assert response.status_code == 200

def test_oracle_concat_piantaggini_livia_mater_eloquen_jenney_first_year_latin_red():
    response = client.get("/oracle/Latin/result/piantaggini_livia_mater_eloquen+jenney_first_year_latin_red/2.4+26/2.11+27/1+1/4+7/marie_de_france_fables_1-22/start-end")
    assert response.status_code == 200

def test_oracle_jenney_first_year_latin_purple_jenney_scudder_baade():
    response = client.get("/oracle/Latin/result/jenney_first_year_latin_purple_jenney-scudder-baade/6/30/1/9/vergil_eclogues/start-end")
    assert response.status_code == 200

def test_oracle_new_latin_primer_english_irby():
    response = client.get("/oracle/Latin/result/new_latin_primer_english-irby/30/32/1/6/fabulae_ab_urbe_condita_sandford-scott/start-end")
    assert response.status_code == 200

def test_oracle_tibullus_elegies():
    response = client.get("/oracle/Latin/result/tibullus_elegies/2.5.68/3.7.98/1/5/ilias_latina/start-end")
    assert response.status_code == 200

def test_oracle_ocr_gsce_defined_vocabulary_list():
    response = client.get("/oracle/Latin/result/ocr_gsce_defined_vocabulary_list/161/269/1/6/diederich_frequency_list_medieval/start-end")
    assert response.status_code == 200

def test_oracle_aeschylus_prometheus_bound():
    response = client.get("/oracle/Greek/result/aeschylus_prometheus_bound/start/end/1/5/homer_core_list_frequency_categories_1-4/start-end")
    assert response.status_code == 200

def test_oracle_seneca_medea():
    response = client.get("/oracle/Latin/result/seneca_medea/333/753/1/9/claudian_de_consulatu_stilichonis_preface_to_book_3/start-end")
    assert response.status_code == 200

def test_oracle_vulgate_gospel_of_john():
    response = client.get("/oracle/Latin/result/vulgate_gospel_of_john/2.13/7.26/1/5/colby_latin_list_years_1_3_4/start-end")
    assert response.status_code == 200

def test_oracle_classical_latin_mckeown():
    response = client.get("/oracle/Latin/result/classical_latin_mckeown/21/24/1/5/latin_for_the_new_millennium_readings_volume_1_tunberg-minkova/start-end")
    assert response.status_code == 200

def test_oracle_fabulae_ab_urbe_condita_sandford_scott():
    response = client.get("/oracle/Latin/result/fabulae_ab_urbe_condita_sandford-scott/18/19/1/6/pseudo-caesar_bellum_alexandrinum/start-end")
    assert response.status_code == 200

def test_oracle_diederich_frequency_list_medieval():
    response = client.get("/oracle/Latin/result/diederich_frequency_list_medieval/596/1368/1/7/claudian_in_rufinum/start-end")
    assert response.status_code == 200

def test_oracle_apuleius_de_mundo():
    response = client.get("/oracle/Latin/result/apuleius_de_mundo/1.2/34.18/1/9/eutropius_breviarium_book_3_beyer/start-end")
    assert response.status_code == 200

def test_oracle_concat_dcc_latin_core_suetonius_life_of_caligula():
    response = client.get("/oracle/Latin/result/dcc_latin_core+suetonius_life_of_caligula/884+52/949+53/1+1/7+5/owen_epigrams/start-end")
    assert response.status_code == 200

def test_oracle_trotula_de_curis_mulierum_74_78_86_87_167_168_174_178_181_182():
    response = client.get("/oracle/Latin/result/trotula_de_curis_mulierum_74-78_86-87_167-168_174-178_181-182/176/177/1/4/claudian_in_rufinum/start-end")
    assert response.status_code == 200

def test_oracle_ovid_heroidum_epistulae():
    response = client.get("/oracle/Latin/result/ovid_heroidum_epistulae/4.121/6.84/1/8/claudian_panegyricus_dictus_manlio_theodoro_consuli/start-end")
    assert response.status_code == 200

def test_oracle_concat_aeschylus_prometheus_bound_homer_core_list_frequency_categories_1_4():
    response = client.get("/oracle/Greek/result/aeschylus_prometheus_bound+homer_core_list_frequency_categories_1-4/start+start/end+end/1+1/3+3/aesop_fables/start-end")
    assert response.status_code == 200

def test_oracle_eutropius_breviarium_all():
    response = client.get("/oracle/Latin/result/eutropius_breviarium_all/9.12/9.2/1/7/claudian_carmina_minora_25_preface/start-end")
    assert response.status_code == 200

def test_oracle_piantaggini_livia_mater_eloquen():
    response = client.get("/oracle/Latin/result/piantaggini_livia_mater_eloquen/3.10/3.12/1/6/elizabeth_jane_weston_parthenica/start-end")
    assert response.status_code == 200

def test_oracle_seneca_ad_lucilium_epistulae_morales():
    response = client.get("/oracle/Latin/result/seneca_ad_lucilium_epistulae_morales/98.15/101.9/1/3/eutropius_breviarium_all/start-end")
    assert response.status_code == 200

def test_oracle_apuleius_metamorphoses_finkelpearl():
    response = client.get("/oracle/Latin/result/apuleius_metamorphoses_finkelpearl/10.17.6/11.5.1/1/3/elizabeth_jane_weston_de_ebrietate/start-end")
    assert response.status_code == 200

def test_oracle_landivar_rusticatio_mexicana_book_6():
    response = client.get("/oracle/Latin/result/landivar_rusticatio_mexicana_book_6/propinquum/seriem/1/3/cicero_de_officiis/start-end")
    assert response.status_code == 200

def test_oracle_horace_satires():
    response = client.get("/oracle/Latin/result/horace_satires/2.6.13/2.7.3/1/8/seneca_agamemnon/start-end")
    assert response.status_code == 200

def test_oracle_concat_vergil_eclogues_1_dcc_petrionius_satyricon():
    response = client.get("/oracle/Latin/result/vergil_eclogues_1_dcc+petrionius_satyricon/1.60+60/1.66+86/1+1/8+5/apollonius_king_of_tyre/start-end")
    assert response.status_code == 200

def test_oracle_seneca_ad_marciam_de_consolatione():
    response = client.get("/oracle/Latin/result/seneca_ad_marciam_de_consolatione/18.3/18.5/1/6/seneca_de_tranquillitate_animi/start-end")
    assert response.status_code == 200

def test_oracle_cicero_in_calpurnium_pisonem():
    response = client.get("/oracle/Latin/result/cicero_in_calpurnium_pisonem/32.5/48.7/1/3/pseudo-caesar_bellum_alexandrinum/start-end")
    assert response.status_code == 200

def test_oracle_ovid_metamorphoses_1_6_11_15():
    response = client.get("/oracle/Latin/result/ovid_metamorphoses_1-6_11_15/15.801/15.868/1/9/cicero_post_reditum_in_senatu/start-end")
    assert response.status_code == 200

def test_oracle_cicero_pro_balbo():
    response = client.get("/oracle/Latin/result/cicero_pro_balbo/51.12/61.2/1/4/epitaph_of_allia_potestas_cil_637966/start-end")
    assert response.status_code == 200

def test_oracle_concat_seneca_medea_bede_historia_ecclesiastica_gentis_anglorum_prologue_11_125_26_21_2_12_14_16_20_31_3_5_6():
    response = client.get("/oracle/Latin/result/seneca_medea+bede_historia_ecclesiastica_gentis_anglorum_prologue_11_125-26_21-2_12-14_16_20_31-3_5-6/88+2.9/516+2.12/1+1/8+7/vergil_eclogues/start-end")
    assert response.status_code == 200