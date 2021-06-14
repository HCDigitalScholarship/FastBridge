"""How to use:
Every function defined here must begin with test_
then type pytest in the shell
tests should end with an assert statment
"""
import importlib
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_text_integrity_dcc():
    response = client.get("oracle/Latin/result/dcc_latin_core_list/start/end/10/cicero_in_catilinam_1-4/1.1.1-1.1.1")
    assert response.status_code == 200


def test_text_integrity_in_cat():
    response = client.get("oracle/Latin/result/cicero_in_catilinam_1-4/start/end/10/cicero_in_catilinam_1-4/1.1.1-1.1.1")
    assert response.status_code == 200


def test_text_integrity_testamentum_porcelli():
    response = client.get("oracle/Latin/result/testamentum_porcelli/start/end/1/cicero_in_catilinam_1-4/1.1.1-1.1.1")
    #note: this is a very, very small text with only 4 sections
    assert response.status_code == 200

def test_text_integrity_BG():
    response = client.get("oracle/Latin/result/caesar_bellum_gallicum/start/end/10/cicero_in_catilinam_1-4/1.1.1-1.1.1")
    assert response.status_code == 200


def test_text_integrity_38grot():
    response = client.get("oracle/Latin/result/38_latin_stories_groton/start/end/10/38_latin_stories_groton/start-end")
    assert response.status_code == 200

def test_text_integrity_50Verbs():
    response = client.get("oracle/Latin/result/50_most_important_latin_verbs/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200



def test_text_whole_BG():
    response = client.get("/select/Latin/result/caesar_bellum_gallicum/start-end/running/")
    assert response.status_code == 200

def test_abelard():
    response = client.get("oracle/Latin/result/abelard_historia_calamitatum_5-6/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_eutropius_breviarium_book_3():
    response = client.get("oracle/Latin/result/eutropius_breviarium_book_3/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_horace_ars_poetica():
    response = client.get("oracle/Latin/result/horace_ars_poetica/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_horace_carmen_saeculare():
    response = client.get("oracle/Latin/result/horace_carmen_saeculare/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_horace_epistles():
    response = client.get("oracle/Latin/result/horace_epistles/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_horace_epodes():
    response = client.get("oracle/Latin/result/horace_epodes/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_horace_odes_garrison_edition():
    response = client.get("oracle/Latin/result/horace_odes_garrison_edition/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_horace_satires():
    response = client.get("oracle/Latin/result/horace_satires/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_hyginus_fabulae():
    response = client.get("oracle/Latin/result/hyginus_fabulae/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_jerome_life_of_malchus_dcc():
    response = client.get("oracle/Latin/result/jerome_life_of_malchus_dcc/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_ilias_latina():
    response = client.get("oracle/Latin/result/ilias_latina/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_juvenal_624868_feminaeromanaeorg():
    response = client.get("oracle/Latin/result/juvenal_6.248-268_feminaeromanae.org/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_latin_for_the_new_millennium_readings_volume_1_tunbergminkova():
    response = client.get("oracle/Latin/result/latin_for_the_new_millennium_readings_volume_1_tunberg-minkova/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_latin_for_the_new_millennium_life_of_attitcus_readings_tunbergminkova():
    response = client.get("oracle/Latin/result/latin_for_the_new_millennium_life_of_attitcus_readings_tunberg-minkova/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_lucretius_de_rerum_natura():
    response = client.get("oracle/Latin/result/lucretius_de_rerum_natura/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_maffeius_historiae_indicae_all():
    response = client.get("oracle/Latin/result/maffeius_historiae_indicae_1.3-5_7-10_27-31_35-39;_2.2-7;_5.3-5;_6_all/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_marie_de_france_fables_122():
    response = client.get("oracle/Latin/result/marie_de_france_fables_1-22/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_nepos_life_of_hannibal_dcc():
    response = client.get("oracle/Latin/result/nepos_life_of_hannibal_dcc/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_newton_axiomata_motus():
    response = client.get("oracle/Latin/result/newton_axiomata_motus/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_newton_regulae_philosophandi():
    response = client.get("oracle/Latin/result/newton_regulae_philosophandi/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_olimpi_via_periculosa():
    response = client.get("oracle/Latin/result/olimpi_via_periculosa/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_oxford_latin_course_college_fabulae_all():
    response = client.get("oracle/Latin/result/oxford_latin_course_college_fabulae_all/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_ovid_amores_1_dcc():
    response = client.get("oracle/Latin/result/ovid_amores_1_dcc/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_ovid_amores():
    response = client.get("oracle/Latin/result/ovid_amores/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_ovid_ars_amatoria():
    response = client.get("oracle/Latin/result/ovid_ars_amatoria/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_ovid_fasti():
    response = client.get("oracle/Latin/result/ovid_fasti/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_ovid_fasti_6org():
    response = client.get("oracle/Latin/result/ovid_fasti_6.219-234_feminaeromane.org/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_ovid_halieutica():
    response = client.get("oracle/Latin/result/ovid_halieutica/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_ovid_heroides():
    response = client.get("oracle/Latin/result/ovid_heroides/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_ovid_ibis():
    response = client.get("oracle/Latin/result/ovid_ibis/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_ovid_medicamina_faciei_femineae():
    response = client.get("oracle/Latin/result/ovid_medicamina_faciei_femineae/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_ovid_medicamina_faciei_femineae():
    response = client.get("oracle/Latin/result/ovid_medicamina_faciei_femineae/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_ovid_remedia_amoris():
    response = client.get("oracle/Latin/result/ovid_remedia_amoris/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_owen_epigrams():
    response = client.get("oracle/Latin/result/owen_epigrams/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_persius_satires():
    response = client.get("oracle/Latin/result/persius_satires/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_pervigilium_veneris():
    response = client.get("oracle/Latin/result/pervigilium_veneris/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_petronius_satyricon():
    response = client.get("oracle/Latin/result/petronius_satyricon/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_physiologus_latina_16_9_16_17_23():
    response = client.get("oracle/Latin/result/physiologus_latina_1-6_9_16_17_23/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_piantaggini_livia_mater_eloquens():
    response = client.get("oracle/Latin/result/piantaggini_livia_mater_eloquens/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_ceinos_de_riofrio_centonicum_virgilianum_monimentum():
    response = client.get("oracle/Latin/result/ceinos_de_riofrio_centonicum_virgilianum_monimentum/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_plautus_amphitruo():
    response = client.get("oracle/Latin/result/plautus_amphitruo/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_plautus_asinaria():
    response = client.get("oracle/Latin/result/plautus_asinaria/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_plautus_bacchides():
    response = client.get("oracle/Latin/result/plautus_bacchides/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_plautus_curculio():
    response = client.get("oracle/Latin/result/plautus_curculio/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_pliny_the_younger_vesuvius_letters():
    response = client.get("oracle/Latin/result/pliny_the_younger_vesuvius_letters_6.16_&_6.20/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_pliny_the_younger_panegyricus():
    response = client.get("oracle/Latin/result/pliny_the_younger_panegyricus/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_propertius_elegies():
    response = client.get("oracle/Latin/result/propertius_elegies/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_pseudocaesar_bellum_africanum():
    response = client.get("oracle/Latin/result/pseudo-caesar_bellum_africanum/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_pseudocaesar_bellum_alexandrinum():
    response = client.get("oracle/Latin/result/pseudo-caesar_bellum_alexandrinum/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_pseudocaesar_bellum_hispanum():
    response = client.get("oracle/Latin/result/pseudo-caesar_bellum_hispanum/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_requiem_mass():
    response = client.get("oracle/Latin/result/requiem_mass/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_ritchies_fabulae_faciles():
    response = client.get("oracle/Latin/result/ritchie's_fabulae_faciles/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_ruaeus_aeneid_summaries():
    response = client.get("oracle/Latin/result/ruaeus_aeneid_summaries/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_sallust_bellum_catilinae():
    response = client.get("oracle/Latin/result/sallust_bellum_catilinae/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_sallust_bellum_iugurthinum():
    response = client.get("oracle/Latin/result/sallust_bellum_iugurthinum/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_seneca_pseudo_proverbia_or_de_moribus():
    response = client.get("oracle/Latin/result/seneca_pseudo_proverbia_or_de_moribus/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_seneca_ad_helviam_matrem_de_consolatione():
    response = client.get("oracle/Latin/result/seneca_ad_helviam_matrem_de_consolatione/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_seneca_ad_marciam_de_consolatione():
    response = client.get("oracle/Latin/result/seneca_ad_marciam_de_consolatione/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_seneca_ad_lucilium_epistulae_morales():
    response = client.get("oracle/Latin/result/seneca_ad_lucilium_epistulae_morales/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_seneca_agamemnon():
    response = client.get("oracle/Latin/result/seneca_agamemnon/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_seneca_apocolocyntosis():
    response = client.get("oracle/Latin/result/seneca_apocolocyntosis/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_seneca_de_beneficiis():
    response = client.get("oracle/Latin/result/seneca_de_beneficiis/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_seneca_de_brevitate_vitae():
    response = client.get("oracle/Latin/result/seneca_de_brevitate_vitae/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_seneca_de_clementia():
    response = client.get("oracle/Latin/result/seneca_de_clementia/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_seneca_de_constantia():
    response = client.get("oracle/Latin/result/seneca_de_constantia/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_seneca_de_ira():
    response = client.get("oracle/Latin/result/seneca_de_ira/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_seneca_de_otio():
    response = client.get("oracle/Latin/result/seneca_de_otio/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_seneca_de_providentia():
    response = client.get("oracle/Latin/result/seneca_de_providentia/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_seneca_de_tranquillitate_animi():
    response = client.get("oracle/Latin/result/seneca_de_tranquillitate_animi/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_seneca_hercules_furens_dcc():
    response = client.get("oracle/Latin/result/seneca_hercules_furens_dcc/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_seneca_hercules_furens_dcc():
    response = client.get("oracle/Latin/result/seneca_hercules_furens_dcc/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_seneca_de_vita_beata():
    response = client.get("oracle/Latin/result/seneca_de_vita_beata/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_seneca_hercules_oetaeus():
    response = client.get("oracle/Latin/result/seneca_hercules_oetaeus/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_seneca_medea():
    response = client.get("oracle/Latin/result/seneca_medea/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_seneca_oedipus():
    response = client.get("oracle/Latin/result/seneca_oedipus/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_seneca_phaedra():
    response = client.get("oracle/Latin/result/seneca_phaedra/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_seneca_phoenissae():
    response = client.get("oracle/Latin/result/seneca_phoenissae/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_seneca_thyestes():
    response = client.get("oracle/Latin/result/seneca_thyestes/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_seneca_troades():
    response = client.get("oracle/Latin/result/seneca_troades/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_stabat_mater():
    response = client.get("oracle/Latin/result/stabat_mater/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_tacitus_agricola():
    response = client.get("oracle/Latin/result/tacitus_agricola/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_tacitus_agricola_dcc():
    response = client.get("oracle/Latin/result/tacitus_agricola_dcc/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_tacitus_annales():
    response = client.get("oracle/Latin/result/tacitus_annales/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_tacitus_dialogus_de_oratoribus():
    response = client.get("oracle/Latin/result/tacitus_dialogus_de_oratoribus/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_tacitus_germania():
    response = client.get("oracle/Latin/result/tacitus_germania/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_terence_eunuchus():
    response = client.get("oracle/Latin/result/terence_eunuchus/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_testamentum_porcelli():
    response = client.get("oracle/Latin/result/testamentum_porcelli/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_tibullus_elegies():
    response = client.get("oracle/Latin/result/tibullus_elegies/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_trotula_de_curis_mulierum():
    response = client.get("oracle/Latin/result/trotula_de_curis_mulierum_74-78_86-87_167-168_174-178_181-182/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_vergil_aeneid():
    response = client.get("oracle/Latin/result/vergil_aeneid/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_vergil_eclogues():
    response = client.get("oracle/Latin/result/vergil_eclogues/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_vergil_georgics():
    response = client.get("oracle/Latin/result/vergil_georgics/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_vulgate_genesis_13():
    response = client.get("oracle/Latin/result/vulgate_genesis_1-3/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_vulgate_genesis_3743_story_of_joseph():
    response = client.get("oracle/Latin/result/vulgate_genesis_37-43_story_of_joseph/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_vulgate_gospel_of_john():
    response = client.get("oracle/Latin/result/vulgate_gospel_of_john/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_williams_rena_rhinoceros():
    response = client.get("oracle/Latin/result/williams_rena_rhinoceros/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_williams_ursus_et_porcus():
    response = client.get("oracle/Latin/result/williams_ursus_et_porcus/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_wheelocks_latin_sententiae_antiquae():
    response = client.get("oracle/Latin/result/wheelock’s_latin_sententiae_antiquae/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_wheelocks_latin_practice__review():
    response = client.get("oracle/Latin/result/wheelock’s_latin_practice_&_review/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_cambridge_latin_course_chs_1_34():
    response = client.get("oracle/Latin/result/cambridge_latin_course_chs._1-34/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_classical_latin_mckeown():
    response = client.get("oracle/Latin/result/classical_latin_mckeown/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_disce_kitchellienkewicz():
    response = client.get("oracle/Latin/result/disce!_kitchell-sienkewicz/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_ecce_romani_chs_1_54():
    response = client.get("oracle/Latin/result/ecce_romani_chs._1-54/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_introduction_to_latin_shelmerdine():
    response = client.get("oracle/Latin/result/introduction_to_latin_shelmerdine/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_jennes_first_year_latin_purple_jennescudderbaade():
    response = client.get("oracle/Latin/result/jenney's_first_year_latin_purple_jenney-scudder-baade/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_jenneys_first_year_latin_red():
    response = client.get("oracle/Latin/result/jenney's_first_year_latin_red/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_latin_for_americans_vol_1_and_2_ullmanhenderson():
    response = client.get("oracle/Latin/result/latin_for_americans_vol_1_and_2_ullman-henderson/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_latin_for_the_new_millennium_vols_1_and_2_tunbergminkova():
    response = client.get("oracle/Latin/result/latin_for_the_new_millennium_vols_1_and_2_tunberg-minkova/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_latin_an_intensive_course_morelandfleischer():
    response = client.get("oracle/Latin/result/latin_an_intensive_course_moreland-fleischer/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_learn_to_read_latin_kellerrussell():
    response = client.get("oracle/Latin/result/learn_to_read_latin_keller-russell/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_lingua_latina_per_se_illustrata_pars_i_oerberg():
    response = client.get("oracle/Latin/result/lingua_latina_per_se_illustrata_pars_i_oerberg/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_new_latin_primer_englishirby():
    response = client.get("oracle/Latin/result/new_latin_primer_english-irby/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_oxford_latin_course_balmemorwood():
    response = client.get("oracle/Latin/result/oxford_latin_course_balme-morwood/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_oxford_latin_course_college():
    response = client.get("oracle/Latin/result/oxford_latin_course_college/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_wheelocks_latin_lafleur():
    response = client.get("oracle/Latin/result/wheelock's_latin_lafleur/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_wileys_real_latin_maltbybelcher():
    response = client.get("oracle/Latin/result/wiley's_real_latin_maltby-belcher/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_anthologia_latina_507518_epitaphs_of_vergil():
    response = client.get("oracle/Latin/result/anthologia_latina_507-518_epitaphs_of_vergil/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_tacitus_historiae():
    response = client.get("oracle/Latin/result/tacitus_historiae/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_pliny_the_younger_epistulae():
    response = client.get("oracle/Latin/result/pliny_the_younger_epistulae/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_cato_monostichs():
    response = client.get("oracle/Latin/result/cato_monostichs/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_narcissus_anthologia_latina__9_r():
    response = client.get("oracle/Latin/result/narcissus_anthologia_latina__9_r/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_lhomond_de_viris_illustribus_118_exordium_to_coriolanus():
    response = client.get("oracle/Latin/result/lhomond_de_viris_illustribus_1-18_exordium_to_coriolanus/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_seneca_ad_polybium_de_consolatione():
    response = client.get("oracle/Latin/result/seneca_ad_polybium_de_consolatione/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_cicero_in_catilinam_14():
    response = client.get("oracle/Latin/result/cicero_in_catilinam_1-4/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_cicero_philippics():
    response = client.get("oracle/Latin/result/cicero_philippics/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_aeschylus_prometheus_bound():
    response = client.get("oracle/Latin/result/aeschylus_prometheus_bound/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_sophocles_antigone():
    response = client.get("oracle/Latin/result/sophocles_antigone/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_sophocles_ajax():
    response = client.get("oracle/Latin/result/sophocles_ajax/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_sophocles_oedipus_tyrannus():
    response = client.get("oracle/Latin/result/sophocles_oedipus_tyrannus/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_plato_euthyphro_all_2a16b():
    response = client.get("oracle/Latin/result/plato_euthyphro_all_2a-16b/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_abelard_historia_calamitatum_56():
        response = client.get("oracle/Latin/result/abelard_historia_calamitatum_5-6/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
def test_integrity_aesop_romulus_anglicus_110():
    response = client.get("oracle/Latin/result/aesop_romulus_anglicus_1-10/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_appendix_vergiliana_priapea():
    response = client.get("oracle/Latin/result/appendix_vergiliana_priapea/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_apuleius_apologia():
    response = client.get("oracle/Latin/result/apuleius_apologia/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_apuleius_asclepius():
    response = client.get("oracle/Latin/result/apuleius_asclepius/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_apuleius_de_deo_socratis():
    response = client.get("oracle/Latin/result/apuleius_de_deo_socratis/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_apuleius_de_deo_socratis_prologus():
    response = client.get("oracle/Latin/result/apuleius_de_deo_socratis_prologus/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_apuleius_de_mundo():
    response = client.get("oracle/Latin/result/apuleius_de_mundo/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_apuleius_de_platone():
    response = client.get("oracle/Latin/result/apuleius_de_platone/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_apuleius_florida():
    response = client.get("oracle/Latin/result/apuleius_florida/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_apuleius_peri_hermeneias():
    response = client.get("oracle/Latin/result/apuleius_peri_hermeneias/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_apuleius_de_mundo():
    response = client.get("oracle/Latin/result/apuleius_de_mundo/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_apuleius_de_deo_socratis_prologus():
        response = client.get("oracle/Latin/result/apuleius_de_deo_socratis_prologus/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
def test_integrity_augustus_res_gestae_i():
    response = client.get("oracle/Latin/result/augustus_res_gestae_i/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_carmina_priapea_180():
    response = client.get("oracle/Latin/result/carmina_priapea_1-80/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_cato_distichs():
    response = client.get("oracle/Latin/result/cato_distichs/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_catullus_carmina_garrison():
    response = client.get("oracle/Latin/result/catullus_carmina_garrison/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200
def test_integrity_cicero_de_haruspicum_responso():
    response = client.get("oracle/Latin/result/cicero_de_haruspicum_responso/start/end/10/50_most_important_latin_verbs/start-end")
    assert response.status_code == 200

def test_integrity_cicero_de_haruspicum_responso():
    response = client.get("oracle/Latin/result/cicero_de_haruspicum_responso/start/end/1/cicero_de_haruspicum_responso/start-end")
    assert response.status_code == 200

def test_integrity_cicero_de_imperio_cn_pompei():
    response = client.get("oracle/Latin/result/cicero_de_imperio_cn_pompei/start/end/1/cicero_de_imperio_cn_pompei/start-end")
    assert response.status_code == 200

def test_integrity_cicero_in_vatinium():
    response = client.get("oracle/Latin/result/cicero_in_vatinium/start/end/1/cicero_in_vatinium/start-end")
    assert response.status_code == 200

def test_integrity_cicero_in_verrem_actio_prima():
    response = client.get("oracle/Latin/result/cicero_in_verrem_actio_prima/start/end/1/cicero_in_verrem_actio_prima/start-end")
    assert response.status_code == 200

def test_integrity_cicero_in_verrem_actio_secunda():
    response = client.get("oracle/Latin/result/cicero_in_verrem_actio_secunda/start/end/1/cicero_in_verrem_actio_secunda/start-end")
    assert response.status_code == 200

def test_integrity_horace_odes_garrison_edition():
    response = client.get("oracle/Latin/result/horace_odes_garrison_edition/start/end/1/horace_odes_garrison_edition/start-end")
    assert response.status_code == 200

def test_integrity_juvenal_6248268_feminaeromanaeorg():
    response = client.get("oracle/Latin/result/juvenal_6248-268_feminaeromanaeorg/start/end/1/juvenal_6248-268_feminaeromanaeorg/start-end")
    assert response.status_code == 200

def test_integrity_maffeius_historiae_indicae_all():
    response = client.get("oracle/Latin/result/maffeius_historiae_indicae_13-5_7-10_27-31_35-39_22-7_53-5_6_all/start/end/1/maffeius_historiae_indicae_13-5_7-10_27-31_35-39_22-7_53-5_6_all/start-end")
    assert response.status_code == 200

def test_integrity_marie_de_france_fables_122():
    response = client.get("oracle/Latin/result/marie_de_france_fables_1-22/start/end/1/marie_de_france_fables_1-22/start-end")
    assert response.status_code == 200

def test_integrity_ruaeus_aeneid_summaries():
    response = client.get("oracle/Latin/result/ruaeus_aeneid_summaries/start/end/1/ruaeus_aeneid_summaries/start-end")
    assert response.status_code == 200

def test_integrity_cicero_post_reditum_in_senatu():
    response = client.get("oracle/Latin/result/cicero_post_reditum_in_senatu/start/end/1/cicero_post_reditum_in_senatu/start-end")
    assert response.status_code == 200

def test_integrity_cicero_pro_caelio():
    response = client.get("oracle/Latin/result/cicero_pro_caelio/start/end/1/cicero_pro_caelio/start-end")
    assert response.status_code == 200

def test_integrity_cicero_pro_cluentio():
    response = client.get("oracle/Latin/result/cicero_pro_cluentio/start/end/1/cicero_pro_cluentio/start-end")
    assert response.status_code == 200

def test_integrity_cicero_pro_flacco():
    response = client.get("oracle/Latin/result/cicero_pro_flacco/start/end/1/cicero_pro_flacco/start-end")
    assert response.status_code == 200

def test_integrity_cicero_pro_marco_tullio():
    response = client.get("oracle/Latin/result/cicero_pro_marco_tullio/start/end/1/cicero_pro_marco_tullio/start-end")
    assert response.status_code == 200

def test_integrity_cicero_pro_marco_tullio():
    response = client.get("oracle/Latin/result/cicero_pro_marco_tullio/start/end/1/cicero_pro_marco_tullio/start-end")
    assert response.status_code == 200

def test_integrity_cicero_pro_plancio():
    response = client.get("oracle/Latin/result/cicero_pro_plancio/start/end/1/cicero_pro_plancio/start-end")
    assert response.status_code == 200

def test_integrity_cicero_pro_quinctio():
    response = client.get("oracle/Latin/result/cicero_pro_quinctio/start/end/1/cicero_pro_quinctio/start-end")
    assert response.status_code == 200

def test_integrity_cicero_pro_rabirio_perduellionis_reo():
    response = client.get("oracle/Latin/result/cicero_pro_rabirio_perduellionis_reo/start/end/1/cicero_pro_rabirio_perduellionis_reo/start-end")
    assert response.status_code == 200

def test_integrity_cicero_pro_rege_deiotario():
    response = client.get("oracle/Latin/result/cicero_pro_rege_deiotario/start/end/1/cicero_pro_rege_deiotario/start-end")
    assert response.status_code == 200

def test_integrity_cicero_pro_roscio_comedo():
    response = client.get("oracle/Latin/result/cicero_pro_roscio_comedo/start/end/1/cicero_pro_roscio_comedo/start-end")
    assert response.status_code == 200

def test_integrity_cicero_pro_sestio():
    response = client.get("oracle/Latin/result/cicero_pro_sestio/start/end/1/cicero_pro_sestio/start-end")
    assert response.status_code == 200

def test_integrity_cicero_pro_sulla():
    response = client.get("oracle/Latin/result/cicero_pro_sulla/start/end/1/cicero_pro_sulla/start-end")
    assert response.status_code == 200

def test_integrity_cicero_somnium_scipionis_929():
    response = client.get("oracle/Latin/result/cicero_somnium_scipionis_9-29/start/end/1/cicero_somnium_scipionis_9-29/start-end")
    assert response.status_code == 200

def test_integrity_corderius_colloquia_book_2():
    response = client.get("oracle/Latin/result/corderius_colloquia_book_2/start/end/1/corderius_colloquia_book_2/start-end")
    assert response.status_code == 200

def test_integrity_epistulae_corneliae_fr_1_and_2():
    response = client.get("oracle/Latin/result/epistulae_corneliae_fr_1_and_2/start/end/1/epistulae_corneliae_fr_1_and_2/start-end")
    assert response.status_code == 200

def test_integrity_epistulae_corneliae_fr_1_and_2():
    response = client.get("oracle/Latin/result/epistulae_corneliae_fr_1_and_2/start/end/1/epistulae_corneliae_fr_1_and_2/start-end")
    assert response.status_code == 200

def test_integrity_civis_romanus_a_reader_for_the_first_two_years_of_latin_cobban_and_colebourn():
    response = client.get("oracle/Latin/result/civis_romanus_a_reader_for_the_first_two_years_of_latin_cobban_and_colebourn/start/end/1/civis_romanus_a_reader_for_the_first_two_years_of_latin_cobban_and_colebourn/start-end")
    assert response.status_code == 200

def test_integrity_epitaph_of_allia_potestas_cil_637966():
    response = client.get("oracle/Latin/result/epitaph_of_allia_potestas_cil_637966/start/end/1/epitaph_of_allia_potestas_cil_637966/start-end")
    assert response.status_code == 200

def test_integrity_eutropius_breviarium_book_1():
    response = client.get("oracle/Latin/result/eutropius_breviarium_book_1/start/end/1/eutropius_breviarium_book_1/start-end")
    assert response.status_code == 200

def test_integrity_florus_epitome_11_romulus_and_roman_kings():
    response = client.get("oracle/Latin/result/florus_epitome_11_romulus_and_roman_kings/start/end/1/florus_epitome_11_romulus_and_roman_kings/start-end")
    assert response.status_code == 200

def test_integrity_florus_epitome_212_catiline():
    response = client.get("oracle/Latin/result/florus_epitome_212_catiline/start/end/1/florus_epitome_212_catiline/start-end")
    assert response.status_code == 200

def test_integrity_florus_epitome_2223_gracchi():
    response = client.get("oracle/Latin/result/florus_epitome_22-23_gracchi/start/end/1/florus_epitome_22-23_gracchi/start-end")
    assert response.status_code == 200

def test_integrity_florus_epitome_221_cleopatra():
    response = client.get("oracle/Latin/result/florus_epitome_221_cleopatra/start/end/1/florus_epitome_221_cleopatra/start-end")
    assert response.status_code == 200

def test_integrity_hildegard_of_bingen_physica_85():
    response = client.get("oracle/Latin/result/hildegard_of_bingen_physica_85/start/end/1/hildegard_of_bingen_physica_85/start-end")
    assert response.status_code == 200

def test_integrity_gibbs_brevissima():
    response = client.get("oracle/Latin/result/gibbs_brevissima/start/end/1/gibbs_brevissima/start-end")
    assert response.status_code == 200

def test_integrity_brevissima_gibbs():
    response = client.get("oracle/Latin/result/brevissima_gibbs/start/end/1/brevissima_gibbs/start-end")
    assert response.status_code == 200

def test_integrity_hildegard_of_bingen_scivias_72():
    response = client.get("oracle/Latin/result/hildegard_of_bingen_scivias_72/start/end/1/hildegard_of_bingen_scivias_72/start-end")
    assert response.status_code == 200

def test_integrity_hildegard_of_bingen_symphoniae_25_10_11_12_17_19_21_23_64():
    response = client.get("oracle/Latin/result/hildegard_of_bingen_symphoniae_2-5_10_11_12_17_19_21_23_64/start/end/1/hildegard_of_bingen_symphoniae_2-5_10_11_12_17_19_21_23_64/start-end")
    assert response.status_code == 200

def test_integrity_horace_satires():
    response = client.get("oracle/Latin/result/horace_satires/start/end/1/horace_satires/start-end")
    assert response.status_code == 200

def test_integrity_horace_odes_garrison_edition():
    response = client.get("oracle/Latin/result/horace_odes_garrison_edition/start/end/1/horace_odes_garrison_edition/start-end")
    assert response.status_code == 200

def test_integrity_hyginus_fabulae():
    response = client.get("oracle/Latin/result/hyginus_fabulae/start/end/1/hyginus_fabulae/start-end")
    assert response.status_code == 200

def test_integrity_juvenal_satires():
    response = client.get("oracle/Latin/result/juvenal_satires/start/end/1/juvenal_satires/start-end")
    assert response.status_code == 200

def test_integrity_latin_for_the_new_millennium_readings_volume_1_tunbergminkova():
    response = client.get("oracle/Latin/result/latin_for_the_new_millennium_readings_volume_1_tunberg-minkova/start/end/1/latin_for_the_new_millennium_readings_volume_1_tunberg-minkova/start-end")
    assert response.status_code == 200

def test_integrity_maffeius_historiae_indicae_135_710_2731_3539_227_535_6_all():
    response = client.get("oracle/Latin/result/maffeius_historiae_indicae_13-5_7-10_27-31_35-39_22-7_53-5_6_all/start/end/1/maffeius_historiae_indicae_13-5_7-10_27-31_35-39_22-7_53-5_6_all/start-end")
    assert response.status_code == 200

def test_integrity_martial_epigrams():
    response = client.get("oracle/Latin/result/martial_epigrams/start/end/1/martial_epigrams/start-end")
    assert response.status_code == 200

def test_integrity_nepos_life_of_hamilcar():
    response = client.get("oracle/Latin/result/nepos_life_of_hamilcar/start/end/1/nepos_life_of_hamilcar/start-end")
    assert response.status_code == 200

def test_integrity_nepos_prologue_to_the_lives_of_foreign_generals():
    response = client.get("oracle/Latin/result/nepos_prologue_to_the_lives_of_foreign_generals/start/end/1/nepos_prologue_to_the_lives_of_foreign_generals/start-end")
    assert response.status_code == 200

def test_integrity_newton_regulae_philosophandi():
    response = client.get("oracle/Latin/result/newton_regulae_philosophandi/start/end/1/newton_regulae_philosophandi/start-end")
    assert response.status_code == 200

def test_integrity_persius_satires():
    response = client.get("oracle/Latin/result/persius_satires/start/end/1/persius_satires/start-end")
    assert response.status_code == 200

def test_integrity_olimpi_via_periculosa():
    response = client.get("oracle/Latin/result/olimpi_via_periculosa/start/end/1/olimpi_via_periculosa/start-end")
    assert response.status_code == 200

def test_integrity_ovid_amores():
    response = client.get("oracle/Latin/result/ovid_amores/start/end/1/ovid_amores/start-end")
    assert response.status_code == 200

def test_integrity_ovid_amores_1_dcc():
    response = client.get("oracle/Latin/result/ovid_amores_1_dcc/start/end/1/ovid_amores_1_dcc/start-end")
    assert response.status_code == 200

def test_integrity_ovid_ars_amatoria():
    response = client.get("oracle/Latin/result/ovid_ars_amatoria/start/end/1/ovid_ars_amatoria/start-end")
    assert response.status_code == 200

def test_integrity_ovid_fasti():
    response = client.get("oracle/Latin/result/ovid_fasti/start/end/1/ovid_fasti/start-end")
    assert response.status_code == 200

def test_integrity_ovid_fasti_6219234_feminaeromanaeorg():
    response = client.get("oracle/Latin/result/ovid_fasti_6219-234_feminaeromanaeorg/start/end/1/ovid_fasti_6219-234_feminaeromanaeorg/start-end")
    assert response.status_code == 200

def test_integrity_wheelocks_latin_lafleur():
    response = client.get("oracle/Latin/result/wheelocks_latin_lafleur/start/end/1/wheelocks_latin_lafleur/start-end")
    assert response.status_code == 200

def test_integrity_ovid_halieutica():
    response = client.get("oracle/Latin/result/ovid_halieutica/start/end/1/ovid_halieutica/start-end")
    assert response.status_code == 200

def test_integrity_ovid_heroides():
    response = client.get("oracle/Latin/result/ovid_heroides/start/end/1/ovid_heroides/start-end")
    assert response.status_code == 200

def test_integrity_ovid_ibis():
    response = client.get("oracle/Latin/result/ovid_ibis/start/end/1/ovid_ibis/start-end")
    assert response.status_code == 200

def test_integrity_ovid_remedia_amoris():
    response = client.get("oracle/Latin/result/ovid_remedia_amoris/start/end/1/ovid_remedia_amoris/start-end")
    assert response.status_code == 200

def test_integrity_wheelocks_latin_lafleur():
    response = client.get("oracle/Latin/result/wheelock’s_latin_lafleur/start/end/1/wheelock’s_latin_lafleur/start-end")
    assert response.status_code == 200

def test_integrity_plautus_amphitruo():
    response = client.get("oracle/Latin/result/plautus_amphitruo/start/end/1/plautus_amphitruo/start-end")
    assert response.status_code == 200

def test_integrity_plautus_bacchides():
    response = client.get("oracle/Latin/result/plautus_bacchides/start/end/1/plautus_bacchides/start-end")
    assert response.status_code == 200

def test_integrity_plautus_curculio():
    response = client.get("oracle/Latin/result/plautus_curculio/start/end/1/plautus_curculio/start-end")
    assert response.status_code == 200

def test_integrity_plautus_casina():
    response = client.get("oracle/Latin/result/plautus_casina/start/end/1/plautus_casina/start-end")
    assert response.status_code == 200

def test_integrity_pliny_the_younger_vesuvius_letters_616_and_620():
    response = client.get("oracle/Latin/result/pliny_the_younger_vesuvius_letters_616_and_620/start/end/1/pliny_the_younger_vesuvius_letters_616_and_620/start-end")
    assert response.status_code == 200

def test_integrity_propertius_elegies():
    response = client.get("oracle/Latin/result/propertius_elegies/start/end/1/propertius_elegies/start-end")
    assert response.status_code == 200

def test_integrity_pseudocaesar_bellum_alexandrinum():
    response = client.get("oracle/Latin/result/pseudo-caesar_bellum_alexandrinum/start/end/1/pseudo-caesar_bellum_alexandrinum/start-end")
    assert response.status_code == 200

def test_integrity_requiem_mass():
    response = client.get("oracle/Latin/result/requiem_mass/start/end/1/requiem_mass/start-end")
    assert response.status_code == 200

def test_integrity_fabulae_faciles_ritchie():
    response = client.get("oracle/Latin/result/fabulae_faciles_ritchie/start/end/1/fabulae_faciles_ritchie/start-end")
    assert response.status_code == 200

def test_integrity_sallust_bellum_iugurthinum():
    response = client.get("oracle/Latin/result/sallust_bellum_iugurthinum/start/end/1/sallust_bellum_iugurthinum/start-end")
    assert response.status_code == 200

def test_integrity_pseudocaesar_bellum_alexandrinum():
    response = client.get("oracle/Latin/result/pseudo-caesar_bellum_alexandrinum/start/end/1/pseudo-caesar_bellum_alexandrinum/start-end")
    assert response.status_code == 200

def test_integrity_fabulae_faciles_ritchie():
    response = client.get("oracle/Latin/result/fabulae_faciles_ritchie/start/end/1/fabulae_faciles_ritchie/start-end")
    assert response.status_code == 200

def test_integrity_sallust_bellum_catilinae():
    response = client.get("oracle/Latin/result/sallust_bellum_catilinae/start/end/1/sallust_bellum_catilinae/start-end")
    assert response.status_code == 200

def test_integrity_seneca_pseudo_proverbia_or_de_moribus():
    response = client.get("oracle/Latin/result/seneca_pseudo_proverbia_or_de_moribus/start/end/1/seneca_pseudo_proverbia_or_de_moribus/start-end")
    assert response.status_code == 200

def test_integrity_seneca_ad_helviam_matrem_de_consolatione():
    response = client.get("oracle/Latin/result/seneca_ad_helviam_matrem_de_consolatione/start/end/1/seneca_ad_helviam_matrem_de_consolatione/start-end")
    assert response.status_code == 200

def test_integrity_sallust_bellum_catilinae():
    response = client.get("oracle/Latin/result/sallust_bellum_catilinae/start/end/1/sallust_bellum_catilinae/start-end")
    assert response.status_code == 200

def test_integrity_seneca_ad_marciam_de_consolatione():
    response = client.get("oracle/Latin/result/seneca_ad_marciam_de_consolatione/start/end/1/seneca_ad_marciam_de_consolatione/start-end")
    assert response.status_code == 200

def test_integrity_seneca_pseudo_proverbia_or_de_moribus():
    response = client.get("oracle/Latin/result/seneca_pseudo_proverbia_or_de_moribus/start/end/1/seneca_pseudo_proverbia_or_de_moribus/start-end")
    assert response.status_code == 200

def test_integrity_seneca_de_beneficiis():
    response = client.get("oracle/Latin/result/seneca_de_beneficiis/start/end/1/seneca_de_beneficiis/start-end")
    assert response.status_code == 200

def test_integrity_seneca_de_brevitate_vitae():
    response = client.get("oracle/Latin/result/seneca_de_brevitate_vitae/start/end/1/seneca_de_brevitate_vitae/start-end")
    assert response.status_code == 200

def test_integrity_seneca_de_ira():
    response = client.get("oracle/Latin/result/seneca_de_ira/start/end/1/seneca_de_ira/start-end")
    assert response.status_code == 200

def test_integrity_seneca_de_brevitate_vitae():
    response = client.get("oracle/Latin/result/seneca_de_brevitate_vitae/start/end/1/seneca_de_brevitate_vitae/start-end")
    assert response.status_code == 200

def test_integrity_seneca_de_brevitate_vitae():
    response = client.get("oracle/Latin/result/seneca_de_brevitate_vitae/start/end/1/seneca_de_brevitate_vitae/start-end")
    assert response.status_code == 200

def test_integrity_seneca_de_tranquillitate_animi():
    response = client.get("oracle/Latin/result/seneca_de_tranquillitate_animi/start/end/1/seneca_de_tranquillitate_animi/start-end")
    assert response.status_code == 200

def test_integrity_seneca_hercules_oetaeus():
    response = client.get("oracle/Latin/result/seneca_hercules_oetaeus/start/end/1/seneca_hercules_oetaeus/start-end")
    assert response.status_code == 200

def test_integrity_seneca_hercules_oetaeus():
    response = client.get("oracle/Latin/result/seneca_hercules_oetaeus/start/end/1/seneca_hercules_oetaeus/start-end")
    assert response.status_code == 200

def test_integrity_seneca_phoenissae():
    response = client.get("oracle/Latin/result/seneca_phoenissae/start/end/1/seneca_phoenissae/start-end")
    assert response.status_code == 200

def test_integrity_seneca_thyestes():
    response = client.get("oracle/Latin/result/seneca_thyestes/start/end/1/seneca_thyestes/start-end")
    assert response.status_code == 200

def test_integrity_seneca_troades():
    response = client.get("oracle/Latin/result/seneca_troades/start/end/1/seneca_troades/start-end")
    assert response.status_code == 200

def test_integrity_suetonius_caligula():
    response = client.get("oracle/Latin/result/suetonius_caligula/start/end/1/suetonius_caligula/start-end")
    assert response.status_code == 200

def test_integrity_vergil_aeneid():
    response = client.get("oracle/Latin/result/vergil_aeneid/start/end/1/vergil_aeneid/start-end")
    assert response.status_code == 200

def test_integrity_vergil_eclogues():
    response = client.get("oracle/Latin/result/vergil_eclogues/start/end/1/vergil_eclogues/start-end")
    assert response.status_code == 200

def test_integrity_vulgate_genesis_13():
    response = client.get("oracle/Latin/result/vulgate_genesis_1-3/start/end/1/vulgate_genesis_1-3/start-end")
    assert response.status_code == 200

def test_integrity_vulgate_genesis_3743_story_of_joseph():
    response = client.get("oracle/Latin/result/vulgate_genesis_37-43_story_of_joseph/start/end/1/vulgate_genesis_37-43_story_of_joseph/start-end")
    assert response.status_code == 200

def test_integrity_vulgate_revelation():
    response = client.get("oracle/Latin/result/vulgate_revelation/start/end/1/vulgate_revelation/start-end")
    assert response.status_code == 200

def test_integrity_vulgate_revelation():
    response = client.get("oracle/Latin/result/vulgate_revelation/start/end/1/vulgate_revelation/start-end")
    assert response.status_code == 200

def test_integrity_williams_rena_rhinoceros():
    response = client.get("oracle/Latin/result/williams_rena_rhinoceros/start/end/1/williams_rena_rhinoceros/start-end")
    assert response.status_code == 200

def test_integrity_williams_ursus_et_porcus():
    response = client.get("oracle/Latin/result/williams_ursus_et_porcus/start/end/1/williams_ursus_et_porcus/start-end")
    assert response.status_code == 200

def test_integrity_williams_rena_rhinoceros():
    response = client.get("oracle/Latin/result/williams_rena_rhinoceros/start/end/1/williams_rena_rhinoceros/start-end")
    assert response.status_code == 200

def test_integrity_williams_rena_rhinoceros():
    response = client.get("oracle/Latin/result/williams_rena_rhinoceros/start/end/1/williams_rena_rhinoceros/start-end")
    assert response.status_code == 200

def test_integrity_cambridge_latin_course_chs_134():
    response = client.get("oracle/Latin/result/cambridge_latin_course_chs_1-34/start/end/1/cambridge_latin_course_chs_1-34/start-end")
    assert response.status_code == 200

def test_integrity_disce_kitchellsienkewicz():
    response = client.get("oracle/Latin/result/disce_kitchell-sienkewicz/start/end/1/disce_kitchell-sienkewicz/start-end")
    assert response.status_code == 200

def test_integrity_ecce_romani_chs_154():
    response = client.get("oracle/Latin/result/ecce_romani_chs_1-54/start/end/1/ecce_romani_chs_1-54/start-end")
    assert response.status_code == 200

def test_integrity_learn_to_read_latin_kellerrussell():
    response = client.get("oracle/Latin/result/learn_to_read_latin_keller-russell/start/end/1/learn_to_read_latin_keller-russell/start-end")
    assert response.status_code == 200

def test_integrity_apuleius_de_platone():
    response = client.get("oracle/Latin/result/apuleius_de_platone/start/end/1/apuleius_de_platone/start-end")
    assert response.status_code == 200

def test_integrity_apuleius_florida():
    response = client.get("oracle/Latin/result/apuleius_florida/start/end/1/apuleius_florida/start-end")
    assert response.status_code == 200

def test_integrity_apuleius_de_platone():
    response = client.get("oracle/Latin/result/apuleius_de_platone/start/end/1/apuleius_de_platone/start-end")
    assert response.status_code == 200

def test_integrity_apuleius_de_platone():
    response = client.get("oracle/Latin/result/apuleius_de_platone/start/end/1/apuleius_de_platone/start-end")
    assert response.status_code == 200

def test_integrity_cicero_in_verrem_actio_prima():
    response = client.get("oracle/Latin/result/cicero_in_verrem_actio_prima/start/end/1/cicero_in_verrem_actio_prima/start-end")
    assert response.status_code == 200

def test_integrity_cicero_in_verrem_actio_secunda():
    response = client.get("oracle/Latin/result/cicero_in_verrem_actio_secunda/start/end/1/cicero_in_verrem_actio_secunda/start-end")
    assert response.status_code == 200

def test_integrity_cicero_pro_rabirio_postumo():
    response = client.get("oracle/Latin/result/cicero_pro_rabirio_postumo/start/end/1/cicero_pro_rabirio_postumo/start-end")
    assert response.status_code == 200

def test_integrity_corderius_colloquia_book_2():
    response = client.get("oracle/Latin/result/corderius_colloquia_book_2/start/end/1/corderius_colloquia_book_2/start-end")
    assert response.status_code == 200

def test_integrity_florus_epitome_2223_gracchi():
    response = client.get("oracle/Latin/result/florus_epitome_22-23_gracchi/start/end/1/florus_epitome_22-23_gracchi/start-end")
    assert response.status_code == 200

def test_integrity_florus_epitome_11_romulus_and_roman_kings():
    response = client.get("oracle/Latin/result/florus_epitome_11_romulus_and_roman_kings/start/end/1/florus_epitome_11_romulus_and_roman_kings/start-end")
    assert response.status_code == 200

def test_integrity_ovid_amores():
    response = client.get("oracle/Latin/result/ovid_amores/start/end/1/ovid_amores/start-end")
    assert response.status_code == 200

def test_integrity_plautus_captivi():
    response = client.get("oracle/Latin/result/plautus_captivi/start/end/1/plautus_captivi/start-end")
    assert response.status_code == 200
    
def test_integrity_plautus_captivi():
    response = client.get("oracle/Latin/result/plautus_captivi/start/end/1/plautus_captivi/start-end")
    assert response.status_code == 200
    
def test_integrity_plautus_captivi():
    response = client.get("oracle/Latin/result/plautus_captivi/start/end/1/plautus_captivi/start-end")
    assert response.status_code == 200
    
def test_integrity_plautus_captivi():
    response = client.get("oracle/Latin/result/plautus_captivi/start/end/1/plautus_captivi/start-end")
    assert response.status_code == 200
    
def test_integrity_plautus_captivi():
    response = client.get("oracle/Latin/result/plautus_captivi/start/end/1/plautus_captivi/start-end")
    assert response.status_code == 200
    
def test_integrity_martial_epigrams():
    response = client.get("oracle/Latin/result/martial_epigrams/start/end/1/martial_epigrams/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_carmina_minora():
    response = client.get("oracle/Latin/result/claudian_carmina_minora/start/end/1/claudian_carmina_minora/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_carmina_minora_25_preface():
    response = client.get("oracle/Latin/result/claudian_carmina_minora_25_preface/start/end/1/claudian_carmina_minora_25_preface/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_carminum_minorum_appendix():
    response = client.get("oracle/Latin/result/claudian_carminum_minorum_appendix/start/end/1/claudian_carminum_minorum_appendix/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_de_bello_gildonico():
    response = client.get("oracle/Latin/result/claudian_de_bello_gildonico/start/end/1/claudian_de_bello_gildonico/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_de_bello_gothico_():
    response = client.get("oracle/Latin/result/claudian_de_bello_gothico_/start/end/1/claudian_de_bello_gothico_/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_de_bello_gothico_preface():
    response = client.get("oracle/Latin/result/claudian_de_bello_gothico_preface/start/end/1/claudian_de_bello_gothico_preface/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_de_consulatu_stilichonis_():
    response = client.get("oracle/Latin/result/claudian_de_consulatu_stilichonis_/start/end/1/claudian_de_consulatu_stilichonis_/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_de_consulatu_stilichonis_preface_to_book_3():
    response = client.get("oracle/Latin/result/claudian_de_consulatu_stilichonis_preface_to_book_3/start/end/1/claudian_de_consulatu_stilichonis_preface_to_book_3/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_de_raptu_prosperinae():
    response = client.get("oracle/Latin/result/claudian_de_raptu_prosperinae/start/end/1/claudian_de_raptu_prosperinae/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_de_raptu_prosperinae_prefaces():
    response = client.get("oracle/Latin/result/claudian_de_raptu_prosperinae_prefaces/start/end/1/claudian_de_raptu_prosperinae_prefaces/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_epithalamium_de_nuptii_honorii_augusti_preface():
    response = client.get("oracle/Latin/result/claudian_epithalamium_de_nuptii_honorii_augusti_preface/start/end/1/claudian_epithalamium_de_nuptii_honorii_augusti_preface/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_epithalamium_de_nuptiis_honorii_augusti():
    response = client.get("oracle/Latin/result/claudian_epithalamium_de_nuptiis_honorii_augusti/start/end/1/claudian_epithalamium_de_nuptiis_honorii_augusti/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_fescennia():
    response = client.get("oracle/Latin/result/claudian_fescennia/start/end/1/claudian_fescennia/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_in_eutropium():
    response = client.get("oracle/Latin/result/claudian_in_eutropium/start/end/1/claudian_in_eutropium/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_in_eutropium_preface_to_book_2():
    response = client.get("oracle/Latin/result/claudian_in_eutropium_preface_to_book_2/start/end/1/claudian_in_eutropium_preface_to_book_2/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_in_rufinum():
    response = client.get("oracle/Latin/result/claudian_in_rufinum/start/end/1/claudian_in_rufinum/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_in_rufinum_preface():
    response = client.get("oracle/Latin/result/claudian_in_rufinum_preface/start/end/1/claudian_in_rufinum_preface/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_panegyricus_de_iii_consulatu_honorii_augusti():
    response = client.get("oracle/Latin/result/claudian_panegyricus_de_iii_consulatu_honorii_augusti/start/end/1/claudian_panegyricus_de_iii_consulatu_honorii_augusti/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_panegyricus_de_iii_consulatu_honorii_augusti_preface():
    response = client.get("oracle/Latin/result/claudian_panegyricus_de_iii_consulatu_honorii_augusti_preface/start/end/1/claudian_panegyricus_de_iii_consulatu_honorii_augusti_preface/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_panegyricus_de_iv_consulatu_honorii_augusti():
    response = client.get("oracle/Latin/result/claudian_panegyricus_de_iv_consulatu_honorii_augusti/start/end/1/claudian_panegyricus_de_iv_consulatu_honorii_augusti/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_panegyricus_de_vi_consulatu_honorii_augusti():
    response = client.get("oracle/Latin/result/claudian_panegyricus_de_vi_consulatu_honorii_augusti/start/end/1/claudian_panegyricus_de_vi_consulatu_honorii_augusti/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_panegyricus_de_vi_consulatu_honorii_augusti_preface():
    response = client.get("oracle/Latin/result/claudian_panegyricus_de_vi_consulatu_honorii_augusti_preface/start/end/1/claudian_panegyricus_de_vi_consulatu_honorii_augusti_preface/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_panegyricus_dictus_manlio_theodoro_consuli():
    response = client.get("oracle/Latin/result/claudian_panegyricus_dictus_manlio_theodoro_consuli/start/end/1/claudian_panegyricus_dictus_manlio_theodoro_consuli/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_panegyricus_dictus_manlio_theodoro_consuli_preface():
    response = client.get("oracle/Latin/result/claudian_panegyricus_dictus_manlio_theodoro_consuli_preface/start/end/1/claudian_panegyricus_dictus_manlio_theodoro_consuli_preface/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_in_rufinum_preface():
    response = client.get("oracle/Latin/result/claudian_in_rufinum_preface/start/end/1/claudian_in_rufinum_preface/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_in_rufinum():
    response = client.get("oracle/Latin/result/claudian_in_rufinum/start/end/1/claudian_in_rufinum/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_in_eutropium():
    response = client.get("oracle/Latin/result/claudian_in_eutropium/start/end/1/claudian_in_eutropium/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_epithalamium_de_nuptiis_honorii_augusti():
    response = client.get("oracle/Latin/result/claudian_epithalamium_de_nuptiis_honorii_augusti/start/end/1/claudian_epithalamium_de_nuptiis_honorii_augusti/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_de_raptu_prosperinae_prefaces():
    response = client.get("oracle/Latin/result/claudian_de_raptu_prosperinae_prefaces/start/end/1/claudian_de_raptu_prosperinae_prefaces/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_de_consulatu_stilichonis():
    response = client.get("oracle/Latin/result/claudian_de_consulatu_stilichonis/start/end/1/claudian_de_consulatu_stilichonis/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_de_bello_gildonico():
    response = client.get("oracle/Latin/result/claudian_de_bello_gildonico/start/end/1/claudian_de_bello_gildonico/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_de_bello_gothico():
    response = client.get("oracle/Latin/result/claudian_de_bello_gothico/start/end/1/claudian_de_bello_gothico/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_de_bello_gothico_preface():
    response = client.get("oracle/Latin/result/claudian_de_bello_gothico_preface/start/end/1/claudian_de_bello_gothico_preface/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_de_bello_gildonico():
    response = client.get("oracle/Latin/result/claudian_de_bello_gildonico/start/end/1/claudian_de_bello_gildonico/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_in_rufinum():
    response = client.get("oracle/Latin/result/claudian_in_rufinum/start/end/1/claudian_in_rufinum/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_de_consulatu_stilichonis():
    response = client.get("oracle/Latin/result/claudian_de_consulatu_stilichonis/start/end/1/claudian_de_consulatu_stilichonis/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_de_raptu_prosperinae():
    response = client.get("oracle/Latin/result/claudian_de_raptu_prosperinae/start/end/1/claudian_de_raptu_prosperinae/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_fescennia():
    response = client.get("oracle/Latin/result/claudian_fescennia/start/end/1/claudian_fescennia/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_in_eutropium():
    response = client.get("oracle/Latin/result/claudian_in_eutropium/start/end/1/claudian_in_eutropium/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_de_raptu_prosperinae_prefaces():
    response = client.get("oracle/Latin/result/claudian_de_raptu_prosperinae_prefaces/start/end/1/claudian_de_raptu_prosperinae_prefaces/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_in_rufinum():
    response = client.get("oracle/Latin/result/claudian_in_rufinum/start/end/1/claudian_in_rufinum/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_in_rufinum_prefaces():
    response = client.get("oracle/Latin/result/claudian_in_rufinum_prefaces/start/end/1/claudian_in_rufinum_prefaces/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_in_eutropium_preface_to_book_2():
    response = client.get("oracle/Latin/result/claudian_in_eutropium_preface_to_book_2/start/end/1/claudian_in_eutropium_preface_to_book_2/start-end")
    assert response.status_code == 200
    
def test_integrity_martial_epigrams():
    response = client.get("oracle/Latin/result/martial_epigrams/start/end/1/martial_epigrams/start-end")
    assert response.status_code == 200
    
def test_integrity_apuleius_apologia():
    response = client.get("oracle/Latin/result/apuleius_apologia/start/end/1/apuleius_apologia/start-end")
    assert response.status_code == 200
    
def test_integrity_apuleius_asclepius():
    response = client.get("oracle/Latin/result/apuleius_asclepius/start/end/1/apuleius_asclepius/start-end")
    assert response.status_code == 200
    
def test_integrity_apuleius_de_deo_socratis():
    response = client.get("oracle/Latin/result/apuleius_de_deo_socratis/start/end/1/apuleius_de_deo_socratis/start-end")
    assert response.status_code == 200
    
def test_integrity_apuleius_de_deo_socratis_prologus():
    response = client.get("oracle/Latin/result/apuleius_de_deo_socratis_prologus/start/end/1/apuleius_de_deo_socratis_prologus/start-end")
    assert response.status_code == 200
    
def test_integrity_apuleius_de_mundo():
    response = client.get("oracle/Latin/result/apuleius_de_mundo/start/end/1/apuleius_de_mundo/start-end")
    assert response.status_code == 200
    
def test_integrity_apuleius_de_platone():
    response = client.get("oracle/Latin/result/apuleius_de_platone/start/end/1/apuleius_de_platone/start-end")
    assert response.status_code == 200
    
def test_integrity_apuleius_florida():
    response = client.get("oracle/Latin/result/apuleius_florida/start/end/1/apuleius_florida/start-end")
    assert response.status_code == 200
    
def test_integrity_apuleius_metamorphoses():
    response = client.get("oracle/Latin/result/apuleius_metamorphoses/start/end/1/apuleius_metamorphoses/start-end")
    assert response.status_code == 200
    
def test_integrity_apuleius_metamorphoses_finkelpearl_edition():
    response = client.get("oracle/Latin/result/apuleius_metamorphoses_finkelpearl_edition/start/end/1/apuleius_metamorphoses_finkelpearl_edition/start-end")
    assert response.status_code == 200
    
def test_integrity_apuleius_peri_hermeneias():
    response = client.get("oracle/Latin/result/apuleius_peri_hermeneias/start/end/1/apuleius_peri_hermeneias/start-end")
    assert response.status_code == 200
    
def test_integrity_vergil_aeneid():
    response = client.get("oracle/Latin/result/vergil_aeneid/start/end/1/vergil_aeneid/start-end")
    assert response.status_code == 200
    
def test_integrity_ovid_metamorphoses_1_3-6_11_15():
    response = client.get("oracle/Latin/result/ovid_metamorphoses_1_3-6_11_15/start/end/1/ovid_metamorphoses_1_3-6_11_15/start-end")
    assert response.status_code == 200
    
def test_integrity_ovid_metamorphoses_1_3-6_11_15():
    response = client.get("oracle/Latin/result/ovid_metamorphoses_1_3-6_11_15/start/end/1/ovid_metamorphoses_1_3-6_11_15/start-end")
    assert response.status_code == 200
    
def test_integrity_dares_de_excidio_troiae():
    response = client.get("oracle/Latin/result/dares_de_excidio_troiae/start/end/1/dares_de_excidio_troiae/start-end")
    assert response.status_code == 200
    
def test_integrity_bede_historia_ecclesiastica_gentis_anglorum_prologue_11_125-26_21-2_12-14_16_20_31-3_5-6():
    response = client.get("oracle/Latin/result/bede_historia_ecclesiastica_gentis_anglorum_prologue_11_125-26_21-2_12-14_16_20_31-3_5-6/start/end/1/bede_historia_ecclesiastica_gentis_anglorum_prologue_11_125-26_21-2_12-14_16_20_31-3_5-6/start-end")
    assert response.status_code == 200
    
def test_integrity_bico_elementary_core_fundamental_400():
    response = client.get("oracle/Greek/result/bico_elementary_core_fundamental_400/start/end/1/bico_elementary_core_fundamental_400/start-end")
    assert response.status_code == 200
    
def test_integrity_bico_fourth_semester_core_splendid_655():
    response = client.get("oracle/Greek/result/bico_fourth_semester_core_splendid_655/start/end/1/bico_fourth_semester_core_splendid_655/start-end")
    assert response.status_code == 200
    
def test_integrity_thucydides_history_of_the_peloponnesian_war_book_1_21_31_41():
    response = client.get("oracle/Greek/result/thucydides_history_of_the_peloponnesian_war_book_1_21_31_41/start/end/1/thucydides_history_of_the_peloponnesian_war_book_1_21_31_41/start-end")
    assert response.status_code == 200
    
def test_integrity_introduction_to_ancient_greek_luschnig():
    response = client.get("oracle/Greek/result/introduction_to_ancient_greek_luschnig/start/end/1/introduction_to_ancient_greek_luschnig/start-end")
    assert response.status_code == 200
    
def test_integrity_dcc_latin_core_list():
    response = client.get("oracle/Latin/result/dcc_latin_core_list/start/end/1/dcc_latin_core_list/start-end")
    assert response.status_code == 200
    
def test_integrity_pindar_olympian_1():
    response = client.get("oracle/Greek/result/pindar_olympian_1/start/end/1/pindar_olympian_1/start-end")
    assert response.status_code == 200
    
def test_integrity_pindar_pythian_4():
    response = client.get("oracle/Greek/result/pindar_pythian_4/start/end/1/pindar_pythian_4/start-end")
    assert response.status_code == 200
    
def test_integrity_lysias_against_simon():
    response = client.get("oracle/Greek/result/lysias_against_simon/start/end/1/lysias_against_simon/start-end")
    assert response.status_code == 200
    
def test_integrity_lysias_on_the_murder_of_eratosthenes():
    response = client.get("oracle/Greek/result/lysias_on_the_murder_of_eratosthenes/start/end/1/lysias_on_the_murder_of_eratosthenes/start-end")
    assert response.status_code == 200
    
def test_integrity_thucydides_history_of_the_peloponnesian_war_book_1_21_31_41():
    response = client.get("oracle/Greek/result/thucydides_history_of_the_peloponnesian_war_book_1_21_31_41/start/end/1/thucydides_history_of_the_peloponnesian_war_book_1_21_31_41/start-end")
    assert response.status_code == 200
    
def test_integrity_demosthenes_against_neaira():
    response = client.get("oracle/Greek/result/demosthenes_against_neaira/start/end/1/demosthenes_against_neaira/start-end")
    assert response.status_code == 200
    
def test_integrity_aesop_fables_1-53():
    response = client.get("oracle/Greek/result/aesop_fables_1-53/start/end/1/aesop_fables_1-53/start-end")
    assert response.status_code == 200
    
def test_integrity_homeric_hymn_to_demeter():
    response = client.get("oracle/Greek/result/homeric_hymn_to_demeter/start/end/1/homeric_hymn_to_demeter/start-end")
    assert response.status_code == 200
    
def test_integrity_homer_odyssey():
    response = client.get("oracle/Greek/result/homer_odyssey/start/end/1/homer_odyssey/start-end")
    assert response.status_code == 200
    
def test_integrity_campbell's_classical_greek_prose_a_basic_vocabulary():
    response = client.get("oracle/Greek/result/campbell's_classical_greek_prose_a_basic_vocabulary/start/end/1/campbell's_classical_greek_prose_a_basic_vocabulary/start-end")
    assert response.status_code == 200
    
def test_integrity_homer_iliad():
    response = client.get("oracle/Greek/result/homer_iliad/start/end/1/homer_iliad/start-end")
    assert response.status_code == 200
    
def test_integrity_herodotus_histories_book_1():
    response = client.get("oracle/Greek/result/herodotus_histories_book_1/start/end/1/herodotus_histories_book_1/start-end")
    assert response.status_code == 200
    
def test_integrity_campbell_classical_greek_prose_a_basic_vocabulary_core_list():
    response = client.get("oracle/Greek/result/campbell_classical_greek_prose_a_basic_vocabulary_core_list/start/end/1/campbell_classical_greek_prose_a_basic_vocabulary_core_list/start-end")
    assert response.status_code == 200
    
def test_integrity_homer_iliad():
    response = client.get("oracle/Greek/result/homer_iliad/start/end/1/homer_iliad/start-end")
    assert response.status_code == 200
    
def test_integrity_alpha_to_omega_groton():
    response = client.get("oracle/Greek/result/alpha_to_omega_groton/start/end/1/alpha_to_omega_groton/start-end")
    assert response.status_code == 200
    
def test_integrity_athenaze_balme-lawall():
    response = client.get("oracle/Greek/result/athenaze_balme-lawall/start/end/1/athenaze_balme-lawall/start-end")
    assert response.status_code == 200
    
def test_integrity_greek_stopwords_list_perseus():
    response = client.get("oracle/Greek/result/greek_stopwords_list_perseus/start/end/1/greek_stopwords_list_perseus/start-end")
    assert response.status_code == 200
    
def test_integrity_greek_an_intensive_course_hansen-quinn():
    response = client.get("oracle/Greek/result/greek_an_intensive_course_hansen-quinn/start/end/1/greek_an_intensive_course_hansen-quinn/start-end")
    assert response.status_code == 200
    
def test_integrity_herodotus_book_1_high_frequency_vocabulary():
    response = client.get("oracle/Greek/result/herodotus_book_1_high_frequency_vocabulary/start/end/1/herodotus_book_1_high_frequency_vocabulary/start-end")
    assert response.status_code == 200
    
def test_integrity_high_frequency_homer_1-4():
    response = client.get("oracle/Greek/result/high_frequency_homer_1-4/start/end/1/high_frequency_homer_1-4/start-end")
    assert response.status_code == 200
    
def test_integrity_aesop_fables_1-53():
    response = client.get("oracle/Greek/result/aesop_fables_1-53/start/end/1/aesop_fables_1-53/start-end")
    assert response.status_code == 200
    
def test_integrity_herodotus_book_1_high_frequency_vocabulary():
    response = client.get("oracle/Greek/result/herodotus_book_1_high_frequency_vocabulary/start/end/1/herodotus_book_1_high_frequency_vocabulary/start-end")
    assert response.status_code == 200
    
def test_integrity_alpha_to_omega_groton():
    response = client.get("oracle/Greek/result/alpha_to_omega_groton/start/end/1/alpha_to_omega_groton/start-end")
    assert response.status_code == 200
    
def test_integrity_athenaze_balme-lawall():
    response = client.get("oracle/Greek/result/athenaze_balme-lawall/start/end/1/athenaze_balme-lawall/start-end")
    assert response.status_code == 200
    
def test_integrity_greek_stopwords_list_perseus():
    response = client.get("oracle/Greek/result/greek_stopwords_list_perseus/start/end/1/greek_stopwords_list_perseus/start-end")
    assert response.status_code == 200
    
def test_integrity_high_frequency_homer_1-4():
    response = client.get("oracle/Greek/result/high_frequency_homer_1-4/start/end/1/high_frequency_homer_1-4/start-end")
    assert response.status_code == 200
    
def test_integrity_campbell_classical_greek_prose_a_basic_vocabulary_core_list():
    response = client.get("oracle/Greek/result/campbell_classical_greek_prose_a_basic_vocabulary_core_list/start/end/1/campbell_classical_greek_prose_a_basic_vocabulary_core_list/start-end")
    assert response.status_code == 200
    
def test_integrity_juvenal_satires():
    response = client.get("oracle/Latin/result/juvenal_satires/start/end/1/juvenal_satires/start-end")
    assert response.status_code == 200
    
def test_integrity_juvenal_6248-268_feminaeromanaeorg():
    response = client.get("oracle/Latin/result/juvenal_6248-268_feminaeromanaeorg/start/end/1/juvenal_6248-268_feminaeromanaeorg/start-end")
    assert response.status_code == 200
    
def test_integrity_caesar_bellum_gallicum_ap_selections():
    response = client.get("oracle/Latin/result/caesar_bellum_gallicum_ap_selections/start/end/1/caesar_bellum_gallicum_ap_selections/start-end")
    assert response.status_code == 200
    
def test_integrity_vergil_aeneid_ap_selections():
    response = client.get("oracle/Latin/result/vergil_aeneid_ap_selections/start/end/1/vergil_aeneid_ap_selections/start-end")
    assert response.status_code == 200
    
def test_integrity_vergil_aeneid_ap_selections():
    response = client.get("oracle/Latin/result/vergil_aeneid_ap_selections/start/end/1/vergil_aeneid_ap_selections/start-end")
    assert response.status_code == 200
    
def test_integrity_homer_iliad():
    response = client.get("oracle/Greek/result/homer_iliad/start/end/1/homer_iliad/start-end")
    assert response.status_code == 200
    
def test_integrity_cambridge_latin_course():
    response = client.get("oracle/Latin/result/cambridge_latin_course/start/end/1/cambridge_latin_course/start-end")
    assert response.status_code == 200
    
def test_integrity_cambridge_latin_course():
    response = client.get("oracle/Latin/result/cambridge_latin_course/start/end/1/cambridge_latin_course/start-end")
    assert response.status_code == 200
    
def test_integrity_wiley_real_latin_maltby-belcher():
    response = client.get("oracle/Latin/result/wiley_real_latin_maltby-belcher/start/end/1/wiley_real_latin_maltby-belcher/start-end")
    assert response.status_code == 200
    
def test_integrity_wheelock_latin_lafleur():
    response = client.get("oracle/Latin/result/wheelock_latin_lafleur/start/end/1/wheelock_latin_lafleur/start-end")
    assert response.status_code == 200
    
def test_integrity_oxford_latin_course_balme-morwood():
    response = client.get("oracle/Latin/result/oxford_latin_course_balme-morwood/start/end/1/oxford_latin_course_balme-morwood/start-end")
    assert response.status_code == 200
    
def test_integrity_new_latin_primer_english-irby():
    response = client.get("oracle/Latin/result/new_latin_primer_english-irby/start/end/1/new_latin_primer_english-irby/start-end")
    assert response.status_code == 200
    
def test_integrity_wiley_real_latin_maltby-belcher():
    response = client.get("oracle/Latin/result/wiley_real_latin_maltby-belcher/start/end/1/wiley_real_latin_maltby-belcher/start-end")
    assert response.status_code == 200
    
def test_integrity_wheelock_latin_lafleur():
    response = client.get("oracle/Latin/result/wheelock_latin_lafleur/start/end/1/wheelock_latin_lafleur/start-end")
    assert response.status_code == 200
    
def test_integrity_oxford_latin_course_balme-morwood():
    response = client.get("oracle/Latin/result/oxford_latin_course_balme-morwood/start/end/1/oxford_latin_course_balme-morwood/start-end")
    assert response.status_code == 200
    
def test_integrity_new_latin_primer_english-irby():
    response = client.get("oracle/Latin/result/new_latin_primer_english-irby/start/end/1/new_latin_primer_english-irby/start-end")
    assert response.status_code == 200
    
def test_integrity_lingua_latina_per_se_illustrata_pars_i_oerberg():
    response = client.get("oracle/Latin/result/lingua_latina_per_se_illustrata_pars_i_oerberg/start/end/1/lingua_latina_per_se_illustrata_pars_i_oerberg/start-end")
    assert response.status_code == 200
    
def test_integrity_latin_for_the_new_millennium_vols_1_and_2_tunberg-minkova():
    response = client.get("oracle/Latin/result/latin_for_the_new_millennium_vols_1_and_2_tunberg-minkova/start/end/1/latin_for_the_new_millennium_vols_1_and_2_tunberg-minkova/start-end")
    assert response.status_code == 200
    
def test_integrity_latin_an_intensive_course_moreland-fleischer():
    response = client.get("oracle/Latin/result/latin_an_intensive_course_moreland-fleischer/start/end/1/latin_an_intensive_course_moreland-fleischer/start-end")
    assert response.status_code == 200
    
def test_integrity_learn_to_read_latin_keller-russell():
    response = client.get("oracle/Latin/result/learn_to_read_latin_keller-russell/start/end/1/learn_to_read_latin_keller-russell/start-end")
    assert response.status_code == 200
    
def test_integrity_latin_for_americans_vol_1_and_2_ullman-henderson():
    response = client.get("oracle/Latin/result/latin_for_americans_vol_1_and_2_ullman-henderson/start/end/1/latin_for_americans_vol_1_and_2_ullman-henderson/start-end")
    assert response.status_code == 200
    
def test_integrity_jenney_first_year_latin_red():
    response = client.get("oracle/Latin/result/jenney_first_year_latin_red/start/end/1/jenney_first_year_latin_red/start-end")
    assert response.status_code == 200
    
def test_integrity_jenney_first_year_latin_purple_jenney-scudder-baade():
    response = client.get("oracle/Latin/result/jenney_first_year_latin_purple_jenney-scudder-baade/start/end/1/jenney_first_year_latin_purple_jenney-scudder-baade/start-end")
    assert response.status_code == 200
    
def test_integrity_introduction_to_latin_shelmerdine():
    response = client.get("oracle/Latin/result/introduction_to_latin_shelmerdine/start/end/1/introduction_to_latin_shelmerdine/start-end")
    assert response.status_code == 200
    
def test_integrity_ecce_romani_chs_1-54():
    response = client.get("oracle/Latin/result/ecce_romani_chs_1-54/start/end/1/ecce_romani_chs_1-54/start-end")
    assert response.status_code == 200
    
def test_integrity_disce_kitchell-sienkewicz():
    response = client.get("oracle/Latin/result/disce_kitchell-sienkewicz/start/end/1/disce_kitchell-sienkewicz/start-end")
    assert response.status_code == 200
    
def test_integrity_classical_latin_mckeown():
    response = client.get("oracle/Latin/result/classical_latin_mckeown/start/end/1/classical_latin_mckeown/start-end")
    assert response.status_code == 200
    
def test_integrity_alpha_to_omega_groton():
    response = client.get("oracle/Greek/result/alpha_to_omega_groton/start/end/1/alpha_to_omega_groton/start-end")
    assert response.status_code == 200
    
def test_integrity_introduction_to_ancient_greek_luschnig():
    response = client.get("oracle/Greek/result/introduction_to_ancient_greek_luschnig/start/end/1/introduction_to_ancient_greek_luschnig/start-end")
    assert response.status_code == 200
    
def test_integrity_greek_an_intensive_course_hansen-quinn():
    response = client.get("oracle/Greek/result/greek_an_intensive_course_hansen-quinn/start/end/1/greek_an_intensive_course_hansen-quinn/start-end")
    assert response.status_code == 200
    
def test_integrity_athenaze_balme-lawall():
    response = client.get("oracle/Greek/result/athenaze_balme-lawall/start/end/1/athenaze_balme-lawall/start-end")
    assert response.status_code == 200
    
def test_integrity_introduction_to_attic_greek_mastronarde_2013():
    response = client.get("oracle/Greek/result/introduction_to_attic_greek_mastronarde_2013/start/end/1/introduction_to_attic_greek_mastronarde_2013/start-end")
    assert response.status_code == 200
    
def test_integrity_learn_to_read_greek_keller-russell():
    response = client.get("oracle/Greek/result/learn_to_read_greek_keller-russell/start/end/1/learn_to_read_greek_keller-russell/start-end")
    assert response.status_code == 200
    
def test_integrity_cato_de_agricultura():
    response = client.get("oracle/Latin/result/cato_de_agricultura/start/end/1/cato_de_agricultura/start-end")
    assert response.status_code == 200
    
def test_integrity_cato_de_agricultura():
    response = client.get("oracle/Latin/result/cato_de_agricultura/start/end/1/cato_de_agricultura/start-end")
    assert response.status_code == 200
    
def test_integrity_caesar_bellum_gallicum_frequency_list_for_ap_selections():
    response = client.get("oracle/Latin/result/caesar_bellum_gallicum_frequency_list_for_ap_selections/start/end/1/caesar_bellum_gallicum_frequency_list_for_ap_selections/start-end")
    assert response.status_code == 200
    
def test_integrity_vergil_aeneid_frequency_list_for_ap_selections():
    response = client.get("oracle/Latin/result/vergil_aeneid_frequency_list_for_ap_selections/start/end/1/vergil_aeneid_frequency_list_for_ap_selections/start-end")
    assert response.status_code == 200
    
def test_integrity_vergil_aeneid_frequency_list():
    response = client.get("oracle/Latin/result/vergil_aeneid_frequency_list/start/end/1/vergil_aeneid_frequency_list/start-end")
    assert response.status_code == 200
    
def test_integrity_vergil_aeneid_frequency_list_for_ap_selections():
    response = client.get("oracle/Latin/result/vergil_aeneid_frequency_list_for_ap_selections/start/end/1/vergil_aeneid_frequency_list_for_ap_selections/start-end")
    assert response.status_code == 200
    
def test_integrity_vulgate_gospel_of_john():
    response = client.get("oracle/Latin/result/vulgate_gospel_of_john/start/end/1/vulgate_gospel_of_john/start-end")
    assert response.status_code == 200
    
def test_integrity_homer_odyssey():
    response = client.get("oracle/Greek/result/homer_odyssey/start/end/1/homer_odyssey/start-end")
    assert response.status_code == 200
    
def test_integrity_sallust_bellum_catilinae():
    response = client.get("oracle/Latin/result/sallust_bellum_catilinae/start/end/1/sallust_bellum_catilinae/start-end")
    assert response.status_code == 200
    
def test_integrity_cicero_somnium_scipionis_9-29():
    response = client.get("oracle/Latin/result/cicero_somnium_scipionis_9-29/start/end/1/cicero_somnium_scipionis_9-29/start-end")
    assert response.status_code == 200
    
def test_integrity_seneca_quaestiones_naturales_dcc_selections():
    response = client.get("oracle/Latin/result/seneca_quaestiones_naturales_dcc_selections/start/end/1/seneca_quaestiones_naturales_dcc_selections/start-end")
    assert response.status_code == 200
    
def test_integrity_seneca_quaestiones_naturales_dcc_selections():
    response = client.get("oracle/Latin/result/seneca_quaestiones_naturales_dcc_selections/start/end/1/seneca_quaestiones_naturales_dcc_selections/start-end")
    assert response.status_code == 200
    
def test_integrity_apuleius_apologia():
    response = client.get("oracle/Latin/result/apuleius_apologia/start/end/1/apuleius_apologia/start-end")
    assert response.status_code == 200
    
def test_integrity_carmina_priapea_1-80():
    response = client.get("oracle/Latin/result/carmina_priapea_1-80/start/end/1/carmina_priapea_1-80/start-end")
    assert response.status_code == 200
    
def test_integrity_cicero_laelius_de_amicitia():
    response = client.get("oracle/Latin/result/cicero_laelius_de_amicitia/start/end/1/cicero_laelius_de_amicitia/start-end")
    assert response.status_code == 200
    
def test_integrity_cicero_de_domo_sua():
    response = client.get("oracle/Latin/result/cicero_de_domo_sua/start/end/1/cicero_de_domo_sua/start-end")
    assert response.status_code == 200
    
def test_integrity_cicero_in_verrem_actio_secunda():
    response = client.get("oracle/Latin/result/cicero_in_verrem_actio_secunda/start/end/1/cicero_in_verrem_actio_secunda/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_de_consulatu_stilichonis():
    response = client.get("oracle/Latin/result/claudian_de_consulatu_stilichonis/start/end/1/claudian_de_consulatu_stilichonis/start-end")
    assert response.status_code == 200
    
def test_integrity_curtius_history_of_alexander_books_3-10():
    response = client.get("oracle/Latin/result/curtius_history_of_alexander_books_3-10/start/end/1/curtius_history_of_alexander_books_3-10/start-end")
    assert response.status_code == 200
    
def test_integrity_ovid_ars_amatoria():
    response = client.get("oracle/Latin/result/ovid_ars_amatoria/start/end/1/ovid_ars_amatoria/start-end")
    assert response.status_code == 200
    
def test_integrity_ovid_heroides():
    response = client.get("oracle/Latin/result/ovid_heroides/start/end/1/ovid_heroides/start-end")
    assert response.status_code == 200
    
def test_integrity_plautus_amphitruo():
    response = client.get("oracle/Latin/result/plautus_amphitruo/start/end/1/plautus_amphitruo/start-end")
    assert response.status_code == 200
    
def test_integrity_plautus_captivi():
    response = client.get("oracle/Latin/result/plautus_captivi/start/end/1/plautus_captivi/start-end")
    assert response.status_code == 200
    
def test_integrity_pliny_the_younger_epistulae():
    response = client.get("oracle/Latin/result/pliny_the_younger_epistulae/start/end/1/pliny_the_younger_epistulae/start-end")
    assert response.status_code == 200
    
def test_integrity_pliny_the_younger_panegyricus():
    response = client.get("oracle/Latin/result/pliny_the_younger_panegyricus/start/end/1/pliny_the_younger_panegyricus/start-end")
    assert response.status_code == 200
    
def test_integrity_ruaeus_aeneid_summaries():
    response = client.get("oracle/Latin/result/ruaeus_aeneid_summaries/start/end/1/ruaeus_aeneid_summaries/start-end")
    assert response.status_code == 200
    
def test_integrity_ruaeus_aeneid_summaries():
    response = client.get("oracle/Latin/result/ruaeus_aeneid_summaries/start/end/1/ruaeus_aeneid_summaries/start-end")
    assert response.status_code == 200
    
def test_integrity_seneca_ad_helviam_matrem_de_consolatione():
    response = client.get("oracle/Latin/result/seneca_ad_helviam_matrem_de_consolatione/start/end/1/seneca_ad_helviam_matrem_de_consolatione/start-end")
    assert response.status_code == 200
    
def test_integrity_seneca_ad_lucilium_epistulae_morales():
    response = client.get("oracle/Latin/result/seneca_ad_lucilium_epistulae_morales/start/end/1/seneca_ad_lucilium_epistulae_morales/start-end")
    assert response.status_code == 200
    
def test_integrity_seneca_ad_marciam_de_consolatione():
    response = client.get("oracle/Latin/result/seneca_ad_marciam_de_consolatione/start/end/1/seneca_ad_marciam_de_consolatione/start-end")
    assert response.status_code == 200
    
def test_integrity_seneca_de_beneficiis():
    response = client.get("oracle/Latin/result/seneca_de_beneficiis/start/end/1/seneca_de_beneficiis/start-end")
    assert response.status_code == 200
    
def test_integrity_seneca_de_clementia():
    response = client.get("oracle/Latin/result/seneca_de_clementia/start/end/1/seneca_de_clementia/start-end")
    assert response.status_code == 200
    
def test_integrity_seneca_de_constantia():
    response = client.get("oracle/Latin/result/seneca_de_constantia/start/end/1/seneca_de_constantia/start-end")
    assert response.status_code == 200
    
def test_integrity_seneca_de_ira():
    response = client.get("oracle/Latin/result/seneca_de_ira/start/end/1/seneca_de_ira/start-end")
    assert response.status_code == 200
    
def test_integrity_seneca_de_tranquillitate_animi():
    response = client.get("oracle/Latin/result/seneca_de_tranquillitate_animi/start/end/1/seneca_de_tranquillitate_animi/start-end")
    assert response.status_code == 200
    
def test_integrity_tacitus_agricola_dcc():
    response = client.get("oracle/Latin/result/tacitus_agricola_dcc/start/end/1/tacitus_agricola_dcc/start-end")
    assert response.status_code == 200
    
def test_integrity_tacitus_agricola():
    response = client.get("oracle/Latin/result/tacitus_agricola/start/end/1/tacitus_agricola/start-end")
    assert response.status_code == 200
    
def test_integrity_tacitus_annales():
    response = client.get("oracle/Latin/result/tacitus_annales/start/end/1/tacitus_annales/start-end")
    assert response.status_code == 200
    
def test_integrity_tacitus_dialogus_de_oratoribus():
    response = client.get("oracle/Latin/result/tacitus_dialogus_de_oratoribus/start/end/1/tacitus_dialogus_de_oratoribus/start-end")
    assert response.status_code == 200
    
def test_integrity_tacitus_historiae():
    response = client.get("oracle/Latin/result/tacitus_historiae/start/end/1/tacitus_historiae/start-end")
    assert response.status_code == 200
    
def test_integrity_wiley_real_latin_maltby-belcher():
    response = client.get("oracle/Latin/result/wiley_real_latin_maltby-belcher/start/end/1/wiley_real_latin_maltby-belcher/start-end")
    assert response.status_code == 200
    
def test_integrity_seneca_quaestiones_naturales_dcc_selections():
    response = client.get("oracle/Latin/result/seneca_quaestiones_naturales_dcc_selections/start/end/1/seneca_quaestiones_naturales_dcc_selections/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_de_bello_gothico():
    response = client.get("oracle/Latin/result/claudian_de_bello_gothico/start/end/1/claudian_de_bello_gothico/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_in_eutropium():
    response = client.get("oracle/Latin/result/claudian_in_eutropium/start/end/1/claudian_in_eutropium/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_de_bello_gothico_preface():
    response = client.get("oracle/Latin/result/claudian_de_bello_gothico_preface/start/end/1/claudian_de_bello_gothico_preface/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_panegyricus_de_vi_consulatu_honorii_augusti_preface():
    response = client.get("oracle/Latin/result/claudian_panegyricus_de_vi_consulatu_honorii_augusti_preface/start/end/1/claudian_panegyricus_de_vi_consulatu_honorii_augusti_preface/start-end")
    assert response.status_code == 200
    
def test_integrity_abelard_historia_calamitatum_5-6():
    response = client.get("oracle/Latin/result/abelard_historia_calamitatum_5-6/start/end/1/abelard_historia_calamitatum_5-6/start-end")
    assert response.status_code == 200
    
def test_integrity_apuleius_de_mundo():
    response = client.get("oracle/Latin/result/apuleius_de_mundo/start/end/1/apuleius_de_mundo/start-end")
    assert response.status_code == 200
    
def test_integrity_apuleius_de_mundo_prologus():
    response = client.get("oracle/Latin/result/apuleius_de_mundo_prologus/start/end/1/apuleius_de_mundo_prologus/start-end")
    assert response.status_code == 200
    
def test_integrity_apuleius_de_platone():
    response = client.get("oracle/Latin/result/apuleius_de_platone/start/end/1/apuleius_de_platone/start-end")
    assert response.status_code == 200
    
def test_integrity_apuleius_metamorphoses_finkelpearl_edition():
    response = client.get("oracle/Latin/result/apuleius_metamorphoses_finkelpearl_edition/start/end/1/apuleius_metamorphoses_finkelpearl_edition/start-end")
    assert response.status_code == 200
    
def test_integrity_apuleius_de_deo_socratis():
    response = client.get("oracle/Latin/result/apuleius_de_deo_socratis/start/end/1/apuleius_de_deo_socratis/start-end")
    assert response.status_code == 200
    
def test_integrity_cato_de_agricultura():
    response = client.get("oracle/Latin/result/cato_de_agricultura/start/end/1/cato_de_agricultura/start-end")
    assert response.status_code == 200
    
def test_integrity_cato_distichs():
    response = client.get("oracle/Latin/result/cato_distichs/start/end/1/cato_distichs/start-end")
    assert response.status_code == 200
    
def test_integrity_hyginus_fabulae():
    response = client.get("oracle/Latin/result/hyginus_fabulae/start/end/1/hyginus_fabulae/start-end")
    assert response.status_code == 200
    
def test_integrity_marie_de_france_fables_1-22():
    response = client.get("oracle/Latin/result/marie_de_france_fables_1-22/start/end/1/marie_de_france_fables_1-22/start-end")
    assert response.status_code == 200
    
def test_integrity_ruaeus_aeneid_summaries():
    response = client.get("oracle/Latin/result/ruaeus_aeneid_summaries/start/end/1/ruaeus_aeneid_summaries/start-end")
    assert response.status_code == 200
    
def test_integrity_de_romanis_radice():
    response = client.get("oracle/Latin/result/de_romanis_radice/start/end/1/de_romanis_radice/start-end")
    assert response.status_code == 200
    
def test_integrity_cambridge_latin_course():
    response = client.get("oracle/Latin/result/cambridge_latin_course/start/end/1/cambridge_latin_course/start-end")
    assert response.status_code == 200
    
def test_integrity_classical_latin_mckeown():
    response = client.get("oracle/Latin/result/classical_latin_mckeown/start/end/1/classical_latin_mckeown/start-end")
    assert response.status_code == 200
    
def test_integrity_disce_kitchell-sienkewicz():
    response = client.get("oracle/Latin/result/disce_kitchell-sienkewicz/start/end/1/disce_kitchell-sienkewicz/start-end")
    assert response.status_code == 200
    
def test_integrity_ecce_romani_chs_1-54():
    response = client.get("oracle/Latin/result/ecce_romani_chs_1-54/start/end/1/ecce_romani_chs_1-54/start-end")
    assert response.status_code == 200
    
def test_integrity_introduction_to_latin_shelmerdine():
    response = client.get("oracle/Latin/result/introduction_to_latin_shelmerdine/start/end/1/introduction_to_latin_shelmerdine/start-end")
    assert response.status_code == 200
    
def test_integrity_jenney_first_year_latin_purple_jenney-scudder-baade():
    response = client.get("oracle/Latin/result/jenney_first_year_latin_purple_jenney-scudder-baade/start/end/1/jenney_first_year_latin_purple_jenney-scudder-baade/start-end")
    assert response.status_code == 200
    
def test_integrity_jenney_first_year_latin_red():
    response = client.get("oracle/Latin/result/jenney_first_year_latin_red/start/end/1/jenney_first_year_latin_red/start-end")
    assert response.status_code == 200
    
def test_integrity_latin_for_americans_vol_1_and_2_ullman-henderson():
    response = client.get("oracle/Latin/result/latin_for_americans_vol_1_and_2_ullman-henderson/start/end/1/latin_for_americans_vol_1_and_2_ullman-henderson/start-end")
    assert response.status_code == 200
    
def test_integrity_latin_an_intensive_course_moreland-fleischer():
    response = client.get("oracle/Latin/result/latin_an_intensive_course_moreland-fleischer/start/end/1/latin_an_intensive_course_moreland-fleischer/start-end")
    assert response.status_code == 200
    
def test_integrity_latin_for_the_new_millennium_vols_1_and_2_tunberg-minkova():
    response = client.get("oracle/Latin/result/latin_for_the_new_millennium_vols_1_and_2_tunberg-minkova/start/end/1/latin_for_the_new_millennium_vols_1_and_2_tunberg-minkova/start-end")
    assert response.status_code == 200
    
def test_integrity_learn_to_read_latin_keller-russell():
    response = client.get("oracle/Latin/result/learn_to_read_latin_keller-russell/start/end/1/learn_to_read_latin_keller-russell/start-end")
    assert response.status_code == 200
    
def test_integrity_lingua_latina_per_se_illustrata_pars_i_oerberg():
    response = client.get("oracle/Latin/result/lingua_latina_per_se_illustrata_pars_i_oerberg/start/end/1/lingua_latina_per_se_illustrata_pars_i_oerberg/start-end")
    assert response.status_code == 200
    
def test_integrity_new_latin_primer_english-irby():
    response = client.get("oracle/Latin/result/new_latin_primer_english-irby/start/end/1/new_latin_primer_english-irby/start-end")
    assert response.status_code == 200
    
def test_integrity_oxford_latin_course_balme-morwood():
    response = client.get("oracle/Latin/result/oxford_latin_course_balme-morwood/start/end/1/oxford_latin_course_balme-morwood/start-end")
    assert response.status_code == 200
    
def test_integrity_oxford_latin_course_college():
    response = client.get("oracle/Latin/result/oxford_latin_course_college/start/end/1/oxford_latin_course_college/start-end")
    assert response.status_code == 200
    
def test_integrity_wheelock_latin_lafleur():
    response = client.get("oracle/Latin/result/wheelock_latin_lafleur/start/end/1/wheelock_latin_lafleur/start-end")
    assert response.status_code == 200
    
def test_integrity_wiley_real_latin_maltby-belcher():
    response = client.get("oracle/Latin/result/wiley_real_latin_maltby-belcher/start/end/1/wiley_real_latin_maltby-belcher/start-end")
    assert response.status_code == 200
    
def test_integrity_hrotswitha_dulcitius():
    response = client.get("oracle/Latin/result/hrotswitha_dulcitius/start/end/1/hrotswitha_dulcitius/start-end")
    assert response.status_code == 200
    
def test_integrity_ceinos_de_riofrio_centonicum_virgilianum_monimentum():
    response = client.get("oracle/Latin/result/ceinos_de_riofrio_centonicum_virgilianum_monimentum/start/end/1/ceinos_de_riofrio_centonicum_virgilianum_monimentum/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_panegyricus_de_vi_consulatu_honorii_augusti():
    response = client.get("oracle/Latin/result/claudian_panegyricus_de_vi_consulatu_honorii_augusti/start/end/1/claudian_panegyricus_de_vi_consulatu_honorii_augusti/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_panegyricus_de_vi_consulatu_honorii_augusti_preface():
    response = client.get("oracle/Latin/result/claudian_panegyricus_de_vi_consulatu_honorii_augusti_preface/start/end/1/claudian_panegyricus_de_vi_consulatu_honorii_augusti_preface/start-end")
    assert response.status_code == 200
    
def test_integrity_petronius_satyricon():
    response = client.get("oracle/Latin/result/petronius_satyricon/start/end/1/petronius_satyricon/start-end")
    assert response.status_code == 200
    
def test_integrity_horace_epistles():
    response = client.get("oracle/Latin/result/horace_epistles/start/end/1/horace_epistles/start-end")
    assert response.status_code == 200
    
def test_integrity_lhomond_de_viris_illustribus_1-18_exordium_to_coriolanus():
    response = client.get("oracle/Latin/result/lhomond_de_viris_illustribus_1-18_exordium_to_coriolanus/start/end/1/lhomond_de_viris_illustribus_1-18_exordium_to_coriolanus/start-end")
    assert response.status_code == 200
    
def test_integrity_tacitus_annales():
    response = client.get("oracle/Latin/result/tacitus_annales/start/end/1/tacitus_annales/start-end")
    assert response.status_code == 200
    
def test_integrity_tacitus_historiae():
    response = client.get("oracle/Latin/result/tacitus_historiae/start/end/1/tacitus_historiae/start-end")
    assert response.status_code == 200
    
def test_integrity_vergil_aeneid():
    response = client.get("oracle/Latin/result/vergil_aeneid/start/end/1/vergil_aeneid/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_panegyricus_de_iii_consulatu_honorii_augusti_preface():
    response = client.get("oracle/Latin/result/claudian_panegyricus_de_iii_consulatu_honorii_augusti_preface/start/end/1/claudian_panegyricus_de_iii_consulatu_honorii_augusti_preface/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_panegyricus_de_iii_consulatu_honorii_augusti():
    response = client.get("oracle/Latin/result/claudian_panegyricus_de_iii_consulatu_honorii_augusti/start/end/1/claudian_panegyricus_de_iii_consulatu_honorii_augusti/start-end")
    assert response.status_code == 200
    
def test_integrity_alpha_to_omega_groton():
    response = client.get("oracle/Greek/result/alpha_to_omega_groton/start/end/1/alpha_to_omega_groton/start-end")
    assert response.status_code == 200
    
def test_integrity_collins_latin_text():
    response = client.get("oracle/Latin/result/collins_latin_text/start/end/1/collins_latin_text/start-end")
    assert response.status_code == 200
    
def test_integrity_collins_latin_textbook():
    response = client.get("oracle/Latin/result/collins_latin_textbook/start/end/1/collins_latin_textbook/start-end")
    assert response.status_code == 200
    
def test_integrity_claudian_de_consulatu_stilichonis():
    response = client.get("oracle/Latin/result/claudian_de_consulatu_stilichonis/start/end/1/claudian_de_consulatu_stilichonis/start-end")
    assert response.status_code == 200
    
def test_integrity_collins_latin_textbook():
    response = client.get("oracle/Latin/result/collins_latin_textbook/start/end/1/collins_latin_textbook/start-end")
    assert response.status_code == 200
    
def test_integrity_latin_for_the_new_millennium_vols_1_and_2_tunberg-minkova():
    response = client.get("oracle/Latin/result/latin_for_the_new_millennium_vols_1_and_2_tunberg-minkova/start/end/1/latin_for_the_new_millennium_vols_1_and_2_tunberg-minkova/start-end")
    assert response.status_code == 200
    
def test_integrity_ovid_heroides():
    response = client.get("oracle/Latin/result/ovid_heroides/start/end/1/ovid_heroides/start-end")
    assert response.status_code == 200
    
def test_integrity_hrotswitha_dulcitius():
    response = client.get("oracle/Latin/result/hrotswitha_dulcitius/start/end/1/hrotswitha_dulcitius/start-end")
    assert response.status_code == 200
    
def test_integrity_tacitus_agricola():
    response = client.get("oracle/Latin/result/tacitus_agricola/start/end/1/tacitus_agricola/start-end")
    assert response.status_code == 200
    
def test_integrity_tacitus_annales():
    response = client.get("oracle/Latin/result/tacitus_annales/start/end/1/tacitus_annales/start-end")
    assert response.status_code == 200
    
def test_integrity_tacitus_historiae():
    response = client.get("oracle/Latin/result/tacitus_historiae/start/end/1/tacitus_historiae/start-end")
    assert response.status_code == 200
    
def test_integrity_seneca_naturales_quaestiones_dcc_selections():
    response = client.get("oracle/Latin/result/seneca_naturales_quaestiones_dcc_selections/start/end/1/seneca_naturales_quaestiones_dcc_selections/start-end")
    assert response.status_code == 200
    
def test_integrity_ruaeus_aeneid_summaries():
    response = client.get("oracle/Latin/result/ruaeus_aeneid_summaries/start/end/1/ruaeus_aeneid_summaries/start-end")
    assert response.status_code == 200
    
def test_integrity_cambridge_latin_course():
    response = client.get("oracle/Latin/result/cambridge_latin_course/start/end/1/cambridge_latin_course/start-end")
    assert response.status_code == 200
    
def test_integrity_cambridge_latin_course():
    response = client.get("oracle/Latin/result/cambridge_latin_course/start/end/1/cambridge_latin_course/start-end")
    assert response.status_code == 200
    
def test_integrity_cambridge_latin_course():
    response = client.get("oracle/Latin/result/cambridge_latin_course/start/end/1/cambridge_latin_course/start-end")
    assert response.status_code == 200
    
def test_integrity_title_test():
    response = client.get("oracle/Latin/result/title_test/start/end/1/title_test/start-end")
    assert response.status_code == 200
    
def test_integrity_cambridge_latin_course():
    response = client.get("oracle/Latin/result/cambridge_latin_course/start/end/1/cambridge_latin_course/start-end")
    assert response.status_code == 200
    
def test_integrity_ovid_heroides():
    response = client.get("oracle/Latin/result/ovid_heroides/start/end/1/ovid_heroides/start-end")
    assert response.status_code == 200
    
def test_integrity_ovid_heroides():
    response = client.get("oracle/Latin/result/ovid_heroides/start/end/1/ovid_heroides/start-end")
    assert response.status_code == 200
    
def test_integrity_200_essential_latin_words_list_mahoney():
    response = client.get("oracle/Latin/result/200_essential_latin_words_list_mahoney/start/end/1/200_essential_latin_words_list_mahoney/start-end")
    assert response.status_code == 200
    
def test_integrity_suburani():
    response = client.get("oracle/Latin/result/suburani/start/end/1/suburani/start-end")
    assert response.status_code == 200
    
def test_integrity_suburani():
    response = client.get("oracle/Latin/result/suburani/start/end/1/suburani/start-end")
    assert response.status_code == 200
    
def test_integrity_suburani():
    response = client.get("oracle/Latin/result/suburani/start/end/1/suburani/start-end")
    assert response.status_code == 200
    
def test_integrity_keep_going_with_latin_linney():
    response = client.get("oracle/Latin/result/keep_going_with_latin_linney/start/end/1/keep_going_with_latin_linney/start-end")
    assert response.status_code == 200
    
def test_integrity_epictetus_enchiridion_heyne():
    response = client.get("oracle/Latin/result/epictetus_enchiridion_heyne/start/end/1/epictetus_enchiridion_heyne/start-end")
    assert response.status_code == 200
    
def test_integrity_getting_started_with_latin_linney():
    response = client.get("oracle/Latin/result/getting_started_with_latin_linney/start/end/1/getting_started_with_latin_linney/start-end")
    assert response.status_code == 200
    
def test_integrity_keep_going_with_latin_linney():
    response = client.get("oracle/Latin/result/keep_going_with_latin_linney/start/end/1/keep_going_with_latin_linney/start-end")
    assert response.status_code == 200
    
def test_integrity_pseudo-sallust_invective_against_cicero():
    response = client.get("oracle/Latin/result/pseudo-sallust_invective_against_cicero/start/end/1/pseudo-sallust_invective_against_cicero/start-end")
    assert response.status_code == 200
    
def test_integrity_seneca_apocolocyntosis():
    response = client.get("oracle/Latin/result/seneca_apocolocyntosis/start/end/1/seneca_apocolocyntosis/start-end")
    assert response.status_code == 200
    
def test_integrity_alpha_to_omega_groton():
    response = client.get("oracle/Greek/result/alpha_to_omega_groton/start/end/1/alpha_to_omega_groton/start-end")
    assert response.status_code == 200
    
def test_integrity_apollonius_king_of_tyre():
    response = client.get("oracle/Latin/result/apollonius_king_of_tyre/start/end/1/apollonius_king_of_tyre/start-end")
    assert response.status_code == 200
    
def test_integrity_eutropius_breviarium_book_6():
    response = client.get("oracle/Latin/result/eutropius_breviarium_book_6/start/end/1/eutropius_breviarium_book_6/start-end")
    assert response.status_code == 200
    
def test_integrity_ovid_heroides():
    response = client.get("oracle/Latin/result/ovid_heroides/start/end/1/ovid_heroides/start-end")
    assert response.status_code == 200
    
def test_integrity_livy_ab_urbe_condita_ib_list_2_selections():
    response = client.get("oracle/Latin/result/livy_ab_urbe_condita_ib_list_2_selections/start/end/1/livy_ab_urbe_condita_ib_list_2_selections/start-end")
    assert response.status_code == 200
    
def test_integrity_suburani():
    response = client.get("oracle/Latin/result/suburani/start/end/1/suburani/start-end")
    assert response.status_code == 200
    
def test_integrity_international_baccalaureate_vocabulary_ib_hl_selections():
    response = client.get("oracle/Latin/result/international_baccalaureate_vocabulary_ib_hl_selections/start/end/1/international_baccalaureate_vocabulary_ib_hl_selections/start-end")
    assert response.status_code == 200
    
def test_integrity_international_baccalaureate_vocabulary_ib_sl_and_hl_selections():
    response = client.get("oracle/Latin/result/international_baccalaureate_vocabulary_ib_sl_and_hl_selections/start/end/1/international_baccalaureate_vocabulary_ib_sl_and_hl_selections/start-end")
    assert response.status_code == 200
    
def test_integrity_international_baccalaureate_vocabulary_ib_hl_selections():
    response = client.get("oracle/Latin/result/international_baccalaureate_vocabulary_ib_hl_selections/start/end/1/international_baccalaureate_vocabulary_ib_hl_selections/start-end")
    assert response.status_code == 200
    
def test_integrity_international_baccalaureate_vocabulary_ib_sl_and_hl_selections():
    response = client.get("oracle/Latin/result/international_baccalaureate_vocabulary_ib_sl_and_hl_selections/start/end/1/international_baccalaureate_vocabulary_ib_sl_and_hl_selections/start-end")
    assert response.status_code == 200
    
def test_integrity_international_baccalaureate_vocabulary_ib_sl_and_hl_selections():
    response = client.get("oracle/Latin/result/international_baccalaureate_vocabulary_ib_sl_and_hl_selections/start/end/1/international_baccalaureate_vocabulary_ib_sl_and_hl_selections/start-end")
    assert response.status_code == 200
    
def test_integrity_international_baccalaureate_vocabulary_ib_sl_and_hl_selections():
    response = client.get("oracle/Latin/result/international_baccalaureate_vocabulary_ib_sl_and_hl_selections/start/end/1/international_baccalaureate_vocabulary_ib_sl_and_hl_selections/start-end")
    assert response.status_code == 200
    
def test_integrity_horace_odes_garrison_edition():
    response = client.get("oracle/Latin/result/horace_odes_garrison_edition/start/end/1/horace_odes_garrison_edition/start-end")
    assert response.status_code == 200
    
def test_integrity_lingua_latina_per_se_illustrata_pars_i_oerberg():
    response = client.get("oracle/Latin/result/lingua_latina_per_se_illustrata_pars_i_oerberg/start/end/1/lingua_latina_per_se_illustrata_pars_i_oerberg/start-end")
    assert response.status_code == 200
    
def test_integrity_lingua_latina_per_se_illustrata_pars_i_oerberg():
    response = client.get("oracle/Latin/result/lingua_latina_per_se_illustrata_pars_i_oerberg/start/end/1/lingua_latina_per_se_illustrata_pars_i_oerberg/start-end")
    assert response.status_code == 200
    