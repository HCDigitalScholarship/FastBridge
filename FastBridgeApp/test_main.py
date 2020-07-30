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
    def test_integrity_juvenal_6.248-268_feminaeromanae.org():
        response = client.get("oracle/Latin/result/juvenal_6.248-268_feminaeromanae.org/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_juvenal_satires():
        response = client.get("oracle/Latin/result/juvenal_satires/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_latin_for_the_new_millennium_readings_volume_1_tunberg-minkova():
        response = client.get("oracle/Latin/result/latin_for_the_new_millennium_readings_volume_1_tunberg-minkova/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_latin_for_the_new_millennium_life_of_attitcus_readings_tunberg-minkova():
        response = client.get("oracle/Latin/result/latin_for_the_new_millennium_life_of_attitcus_readings_tunberg-minkova/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_lucretius_de_rerum_natura():
        response = client.get("oracle/Latin/result/lucretius_de_rerum_natura/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_maffeius_historiae_indicae_1.3-5_7-10_27-31_35-39;_2.2-7;_5.3-5;_6_all():
        response = client.get("oracle/Latin/result/maffeius_historiae_indicae_1.3-5_7-10_27-31_35-39;_2.2-7;_5.3-5;_6_all/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_marie_de_france_fables_1-22():
        response = client.get("oracle/Latin/result/marie_de_france_fables_1-22/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_martial_epigrams_():
        response = client.get("oracle/Latin/result/martial_epigrams_/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_nepos_life_of_hamilcar_():
        response = client.get("oracle/Latin/result/nepos_life_of_hamilcar_/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_nepos_life_of_hannibal_dcc():
        response = client.get("oracle/Latin/result/nepos_life_of_hannibal_dcc/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_nepos_prologue_to_the_lives_of_foreign_generals_():
        response = client.get("oracle/Latin/result/nepos_prologue_to_the_lives_of_foreign_generals_/start/end/10/50_most_important_latin_verbs/start-end")
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
    def test_integrity_ovid_fasti_6.219-234_feminaeromane.org():
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
    def test_integrity_physiologus_latina_1-6_9_16_17_23():
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
    def test_integrity_pliny_the_younger_vesuvius_letters_6.16_&_6.20():
        response = client.get("oracle/Latin/result/pliny_the_younger_vesuvius_letters_6.16_&_6.20/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_pliny_the_younger_panegyricus():
        response = client.get("oracle/Latin/result/pliny_the_younger_panegyricus/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_propertius_elegies():
        response = client.get("oracle/Latin/result/propertius_elegies/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_pseudo-caesar_bellum_africanum():
        response = client.get("oracle/Latin/result/pseudo-caesar_bellum_africanum/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_pseudo-caesar_bellum_alexandrinum():
        response = client.get("oracle/Latin/result/pseudo-caesar_bellum_alexandrinum/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_pseudo-caesar_bellum_hispanum():
        response = client.get("oracle/Latin/result/pseudo-caesar_bellum_hispanum/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_requiem_mass():
        response = client.get("oracle/Latin/result/requiem_mass/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_ritchie's_fabulae_faciles():
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
    def test_integrity_suetonius_caligula_():
        response = client.get("oracle/Latin/result/suetonius_caligula_/start/end/10/50_most_important_latin_verbs/start-end")
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
    def test_integrity_trotula_de_curis_mulierum_74-78_86-87_167-168_174-178_181-182():
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
    def test_integrity_vulgate_genesis_1-3():
        response = client.get("oracle/Latin/result/vulgate_genesis_1-3/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_vulgate_genesis_37-43_story_of_joseph():
        response = client.get("oracle/Latin/result/vulgate_genesis_37-43_story_of_joseph/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_vulgate_gospel_of_john():
        response = client.get("oracle/Latin/result/vulgate_gospel_of_john/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_vulgate_revelation_():
        response = client.get("oracle/Latin/result/vulgate_revelation_/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_williams_rena_rhinoceros():
        response = client.get("oracle/Latin/result/williams_rena_rhinoceros/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_williams_ursus_et_porcus():
        response = client.get("oracle/Latin/result/williams_ursus_et_porcus/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_wheelock’s_latin_sententiae_antiquae():
        response = client.get("oracle/Latin/result/wheelock’s_latin_sententiae_antiquae/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_wheelock’s_latin_practice_&_review():
        response = client.get("oracle/Latin/result/wheelock’s_latin_practice_&_review/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_cambridge_latin_course_chs._1-34():
        response = client.get("oracle/Latin/result/cambridge_latin_course_chs._1-34/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_classical_latin_mckeown():
        response = client.get("oracle/Latin/result/classical_latin_mckeown/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_disce!_kitchell-sienkewicz():
        response = client.get("oracle/Latin/result/disce!_kitchell-sienkewicz/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_ecce_romani_chs._1-54():
        response = client.get("oracle/Latin/result/ecce_romani_chs._1-54/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_introduction_to_latin_shelmerdine():
        response = client.get("oracle/Latin/result/introduction_to_latin_shelmerdine/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_jenney's_first_year_latin_purple_jenney-scudder-baade():
        response = client.get("oracle/Latin/result/jenney's_first_year_latin_purple_jenney-scudder-baade/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_jenney's_first_year_latin_red():
        response = client.get("oracle/Latin/result/jenney's_first_year_latin_red/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_latin_for_americans_vol_1_and_2_ullman-henderson():
        response = client.get("oracle/Latin/result/latin_for_americans_vol_1_and_2_ullman-henderson/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_latin_for_the_new_millennium_vols_1_and_2_tunberg-minkova():
        response = client.get("oracle/Latin/result/latin_for_the_new_millennium_vols_1_and_2_tunberg-minkova/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_latin_an_intensive_course_moreland-fleischer():
        response = client.get("oracle/Latin/result/latin_an_intensive_course_moreland-fleischer/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_learn_to_read_latin_keller-russell():
        response = client.get("oracle/Latin/result/learn_to_read_latin_keller-russell/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_lingua_latina_per_se_illustrata_pars_i_oerberg():
        response = client.get("oracle/Latin/result/lingua_latina_per_se_illustrata_pars_i_oerberg/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_new_latin_primer_english-irby():
        response = client.get("oracle/Latin/result/new_latin_primer_english-irby/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_oxford_latin_course_balme-morwood():
        response = client.get("oracle/Latin/result/oxford_latin_course_balme-morwood/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_oxford_latin_course_college():
        response = client.get("oracle/Latin/result/oxford_latin_course_college/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_wheelock's_latin_lafleur():
        response = client.get("oracle/Latin/result/wheelock's_latin_lafleur/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_wiley's_real_latin_maltby-belcher():
        response = client.get("oracle/Latin/result/wiley's_real_latin_maltby-belcher/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_anthologia_latina_507-518_epitaphs_of_vergil():
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
    def test_integrity_lhomond_de_viris_illustribus_1-18_exordium_to_coriolanus():
        response = client.get("oracle/Latin/result/lhomond_de_viris_illustribus_1-18_exordium_to_coriolanus/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_seneca_ad_polybium_de_consolatione():
        response = client.get("oracle/Latin/result/seneca_ad_polybium_de_consolatione/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_cicero_in_catilinam_1-4():
        response = client.get("oracle/Latin/result/cicero_in_catilinam_1-4/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    def test_integrity_cicero_philippics():
        response = client.get("oracle/Latin/result/cicero_philippics/start/end/10/50_most_important_latin_verbs/start-end")
        assert response.status_code == 200
    